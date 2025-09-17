import cv2
import face_recognition
import numpy as np
from tkinter import messagebox
from datetime import datetime
from face_capture import FaceCapture
from attendance_manager import AttendanceManager

class FaceRecognitionSystem:
    def __init__(self):
        self.face_capture = FaceCapture()
        self.attendance_manager = AttendanceManager()
        self.tolerance = 0.5  # Face recognition tolerance
        
    def recognize_and_mark_attendance(self):
        """Main function to recognize faces and mark attendance"""
        # Load known encodings
        known_names, known_encodings = self.face_capture.get_stored_faces()
        
        if not known_names:
            messagebox.showerror("Error", "No faces stored. Please capture first.")
            return
            
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Could not open the camera.")
            return
            
        recognized_today = set()
        today = datetime.now().strftime('%Y-%m-%d')
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            
            for encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
                name = self._identify_face(encoding, known_names, known_encodings)
                
                if name != "Unknown" and name not in recognized_today:
                    if self.attendance_manager.mark_attendance(name, today):
                        recognized_today.add(name)
                        print(f"Attendance marked for {name}")
                
                # Draw rectangle and name
                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, name, (left, top - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                           
            cv2.imshow("Recognize & Mark Attendance (Press 'q' to quit)", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Done", "Recognition session ended.")
        
    def _identify_face(self, face_encoding, known_names, known_encodings):
        """Identify a face against known encodings"""
        if len(known_encodings) == 0:
            return "Unknown"
            
        # Compute distances and find best match
        distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_match_index = np.argmin(distances)
        
        if distances[best_match_index] < self.tolerance:
            return known_names[best_match_index]
        else:
            return "Unknown"
            
    def set_tolerance(self, tolerance):
        """Set face recognition tolerance"""
        self.tolerance = tolerance
        
    def get_tolerance(self):
        """Get current face recognition tolerance"""
        return self.tolerance