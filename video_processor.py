import cv2
import os
import sqlite3
import face_recognition
import numpy as np
from tkinter import messagebox, filedialog
from datetime import datetime
import threading


class VideoProcessor:
    def __init__(self):
        self.min_video_duration = 0 # seconds
        self.max_video_duration = 20  # seconds
        self.frames_per_second = 1    # Extract 1 frame per second
        self.min_faces_per_frame = 1
        self.max_faces_per_frame = 1
        self.undetected_faces_folder = "undetected_faces"
        
        # Create folder for undetected faces
        if not os.path.exists(self.undetected_faces_folder):
            os.makedirs(self.undetected_faces_folder)
        
    def select_and_process_video_for_attendance(self):
        """Select video file and process it for attendance marking"""
        # File dialog to select video
        video_path = filedialog.askopenfilename(
            title="Select Video File for Attendance",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv"),
                ("MP4 files", "*.mp4"),
                ("AVI files", "*.avi"),
                ("All files", "*.*")
            ]
        )
        
        if not video_path:
            return False
            
        # Validate video before processing
        if not self._validate_video(video_path):
            return False
            
        # Process video in a separate thread to prevent UI freezing
        threading.Thread(target=self._process_video_for_attendance_thread, 
                        args=(video_path,), daemon=True).start()
        return True
        
    def _validate_video(self, video_path):
        """Validate video duration and format"""
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                messagebox.showerror("Error", "Could not open video file. Please check the format.")
                return False
                
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps if fps > 0 else 0
            
            cap.release()
            
            # Validate duration
            if duration < self.min_video_duration:
                messagebox.showerror("Error", 
                    f"Video is too short. Minimum duration: {self.min_video_duration} seconds. "
                    f"Current duration: {duration:.1f} seconds")
                return False
                
            if duration > self.max_video_duration:
                messagebox.showerror("Error", 
                    f"Video is too long. Maximum duration: {self.max_video_duration} seconds. "
                    f"Current duration: {duration:.1f} seconds")
                return False
                
            messagebox.showinfo("Video Validation", 
                f"Video validated successfully!\nDuration: {duration:.1f} seconds\nFPS: {fps:.1f}")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Error validating video: {str(e)}")
            return False
            
    def _process_video_for_attendance_thread(self, video_path):
        """Process video for attendance marking in a separate thread"""
        try:
            messagebox.showinfo("Processing", "Processing video for attendance... This may take a few moments.")
            
            # Load known faces from database
            known_names, known_encodings = self._get_known_faces()
            
            if not known_names:
                messagebox.showerror("Error", "No registered faces found in database. Please register faces first.")
                return
                
            # Extract faces from video and mark attendance
            attendance_results = self._process_video_for_attendance(video_path, known_names, known_encodings)
            
            if attendance_results:
                self._display_attendance_results(attendance_results)
            else:
                messagebox.showerror("Error", "No faces detected in the video or processing failed.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error processing video: {str(e)}")
            
    def _get_known_faces(self):
        """Get known faces from database"""
        try:
            conn = sqlite3.connect('faces.db')
            c = conn.cursor()
            c.execute("SELECT name, encoding FROM faces")
            data = c.fetchall()
            conn.close()
            
            known_names = []
            known_encodings = []
            
            for row in data:
                known_names.append(row[0])
                arr = np.frombuffer(row[1], dtype=np.float64)
                arr = arr.reshape((128,))
                known_encodings.append(arr)
                
            return known_names, known_encodings
        except Exception as e:
            print(f"Error retrieving known faces: {str(e)}")
            return [], []
            
    def _process_video_for_attendance(self, video_path, known_names, known_encodings):
        """Process video and mark attendance for recognized faces"""
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        # Calculate frame interval (1 frame per second)
        frame_interval = int(fps)
        
        # Track recognized people and undetected faces
        recognized_people = set()
        attendance_marked = {}
        undetected_faces = []
        today = datetime.now().strftime('%Y-%m-%d')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        results = {
            'total_frames_processed': 0,
            'faces_detected': 0,
            'people_recognized': 0,
            'attendance_marked': [],
            'unrecognized_faces': 0,
            'undetected_faces_count': 0,
            'undetected_faces_saved': 0
        }
        
        frame_number = 0
        processed_frames = 0
        undetected_face_counter = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Process every nth frame (1 frame per second)
            if frame_number % frame_interval == 0:
                processed_frames += 1
                
                # Convert BGR to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Detect faces
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                
                results['faces_detected'] += len(face_encodings)
                
                # Process each detected face
                for i, (face_encoding, face_location) in enumerate(zip(face_encodings, face_locations)):
                    name = self._identify_face(face_encoding, known_names, known_encodings)
                    
                    if name != "Unknown":
                        if name not in recognized_people:
                            # Mark attendance for this person
                            if self._mark_attendance(name, today):
                                recognized_people.add(name)
                                attendance_marked[name] = datetime.now().strftime('%H:%M:%S')
                                results['attendance_marked'].append({
                                    'name': name,
                                    'time': attendance_marked[name],
                                    'frame': processed_frames
                                })
                    else:
                        # Save undetected face
                        results['unrecognized_faces'] += 1
                        undetected_face_counter += 1
                        
                        # Extract and save face image
                        face_image = self._extract_face_from_frame(frame, face_location)
                        if face_image is not None:
                            face_filename = f"undetected_face_{timestamp}_{undetected_face_counter:03d}.jpg"
                            face_path = os.path.join(self.undetected_faces_folder, face_filename)
                            
                            try:
                                cv2.imwrite(face_path, face_image)
                                results['undetected_faces_saved'] += 1
                                undetected_faces.append({
                                    'filename': face_filename,
                                    'frame': processed_frames,
                                    'timestamp': datetime.now().strftime('%H:%M:%S')
                                })
                            except Exception as e:
                                print(f"Error saving undetected face: {str(e)}")
                        
            frame_number += 1
            
        cap.release()
        results['total_frames_processed'] = processed_frames
        results['people_recognized'] = len(recognized_people)
        results['undetected_faces_count'] = len(undetected_faces)
        results['undetected_faces_list'] = undetected_faces
        
        return results
        
    def _extract_face_from_frame(self, frame, face_location):
        """Extract face region from frame"""
        try:
            top, right, bottom, left = face_location
            
            # Add padding around face
            padding = 20
            height, width = frame.shape[:2]
            
            # Ensure coordinates are within frame bounds
            top = max(0, top - padding)
            bottom = min(height, bottom + padding)
            left = max(0, left - padding)
            right = min(width, right + padding)
            
            # Extract face region
            face_image = frame[top:bottom, left:right]
            
            # Resize to standard size for consistency
            if face_image.size > 0:
                face_image = cv2.resize(face_image, (150, 150))
                return face_image
            else:
                return None
                
        except Exception as e:
            print(f"Error extracting face: {str(e)}")
            return None
            
    def _identify_face(self, face_encoding, known_names, known_encodings, tolerance=0.5):
        """Identify a face against known encodings"""
        if len(known_encodings) == 0:
            return "Unknown"
            
        # Compute distances and find best match
        distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_match_index = np.argmin(distances)
        
        if distances[best_match_index] < tolerance:
            return known_names[best_match_index]
        else:
            return "Unknown"
            
    def _mark_attendance(self, name, date):
        """Mark attendance for a person"""
        try:
            conn = sqlite3.connect('attendance.db')
            c = conn.cursor()
            
            # Check if attendance already marked for today
            c.execute("SELECT * FROM attendance WHERE name=? AND date=?", (name, date))
            if c.fetchone() is None:
                current_time = datetime.now().strftime('%H:%M:%S')
                c.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)",
                         (name, date, current_time))
                conn.commit()
                conn.close()
                return True
            else:
                conn.close()
                return False  # Already marked
        except Exception as e:
            print(f"Error marking attendance: {str(e)}")
            return False
            
    def _display_attendance_results(self, results):
        """Display attendance marking results to user"""
        summary = f"""Video Processing Complete - Attendance Marked!

📊 Processing Summary:
Total Frames Processed: {results['total_frames_processed']}
Total Faces Detected: {results['faces_detected']}
People Recognized: {results['people_recognized']}
Unrecognized Faces: {results['unrecognized_faces']}
Undetected Face Photos Saved: {results['undetected_faces_saved']}

✅ Attendance Marked For:"""
        
        if results['attendance_marked']:
            for record in results['attendance_marked']:
                summary += f"\n• {record['name']} at {record['time']} (Frame {record['frame']})"
        else:
            summary += "\nNo new attendance records (all people already marked for today)"
            
        if results['undetected_faces_count'] > 0:
            summary += f"\n\n❓ Undetected Faces Information:"
            summary += f"\n• {results['undetected_faces_count']} unrecognized faces found"
            summary += f"\n• {results['undetected_faces_saved']} face photos saved"
            summary += f"\n• Photos saved in '{self.undetected_faces_folder}' folder"
            summary += f"\n• You can review these photos to identify unknown people"
            
        messagebox.showinfo("Attendance Processing Results", summary)
        
        # Show undetected faces details if any
        if results['undetected_faces_count'] > 0:
            self._show_undetected_faces_details(results['undetected_faces_list'])
            
    def _show_undetected_faces_details(self, undetected_faces):
        """Show details of undetected faces"""
        details = "📷 Undetected Faces Details:\n\n"
        
        for i, face_info in enumerate(undetected_faces[:10], 1):  # Show first 10
            details += f"{i}. {face_info['filename']}\n"
            details += f"   Frame: {face_info['frame']}, Time: {face_info['timestamp']}\n\n"
            
        if len(undetected_faces) > 10:
            details += f"... and {len(undetected_faces) - 10} more faces\n\n"
            
        details += f"All undetected face photos are saved in:\n'{os.path.abspath(self.undetected_faces_folder)}'"
        
        messagebox.showinfo("Undetected Faces Details", details)
    
    def open_undetected_faces_folder(self):
        """Open the folder containing undetected faces"""
        try:
            import subprocess
            import platform
            
            folder_path = os.path.abspath(self.undetected_faces_folder)
            
            if platform.system() == "Windows":
                subprocess.Popen(f'explorer "{folder_path}"')
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", folder_path])
            else:  # Linux
                subprocess.Popen(["xdg-open", folder_path])
                
        except Exception as e:
            messagebox.showinfo("Folder Location", 
                f"Undetected faces are saved in:\n{os.path.abspath(self.undetected_faces_folder)}")
        
    def get_video_info(self, video_path):
        """Get detailed video information"""
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return None
                
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = frame_count / fps if fps > 0 else 0
            
            cap.release()
            
            return {
                'fps': fps,
                'frame_count': frame_count,
                'width': width,
                'height': height,
                'duration': duration,
                'expected_frames_to_process': int(duration)
            }
            
        except Exception as e:
            print(f"Error getting video info: {str(e)}")
            return None
            
    def set_processing_parameters(self, min_duration=10, max_duration=20, 
                                 min_faces=3, max_faces=4, fps=1):
        """Configure video processing parameters"""
        self.min_video_duration = min_duration
        self.max_video_duration = max_duration
        self.min_faces_per_frame = min_faces
        self.max_faces_per_frame = max_faces
        self.frames_per_second = fps
        
    def get_undetected_faces_count(self):
        """Get count of undetected face photos"""
        try:
            if os.path.exists(self.undetected_faces_folder):
                files = [f for f in os.listdir(self.undetected_faces_folder) 
                        if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                return len(files)
            return 0
        except Exception as e:
            print(f"Error counting undetected faces: {str(e)}")
            return 0
            
    def clear_undetected_faces(self):
        """Clear all undetected face photos"""
        try:
            if os.path.exists(self.undetected_faces_folder):
                files = os.listdir(self.undetected_faces_folder)
                for file in files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        os.remove(os.path.join(self.undetected_faces_folder, file))
                return True
        except Exception as e:
            print(f"Error clearing undetected faces: {str(e)}")
            return False