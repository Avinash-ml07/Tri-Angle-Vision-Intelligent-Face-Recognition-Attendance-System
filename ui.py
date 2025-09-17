import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import os
from database_setup import initialize_databases
from face_capture import FaceCapture
from face_recognition_system import FaceRecognitionSystem
from attendance_manager import AttendanceManager
from video_processor import VideoProcessor

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("850x750")
        
        # Initialize components
        self.face_capture = FaceCapture()
        self.recognition_system = FaceRecognitionSystem()
        self.attendance_manager = AttendanceManager()
        self.video_processor = VideoProcessor()
        
        # Initialize databases
        initialize_databases()
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = tk.Label(self.root, text="Face Recognition Attendance System", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Tab 1: Face Capture
        self.setup_capture_tab(notebook)
        
        # Tab 2: Recognition & Attendance
        self.setup_recognition_tab(notebook)
        
        # Tab 3: Video Attendance Processing
        self.setup_video_attendance_tab(notebook)
        
        # Tab 4: Attendance Records
        self.setup_attendance_tab(notebook)
        
    def setup_capture_tab(self, notebook):
        """Setup face capture tab"""
        capture_frame = ttk.Frame(notebook)
        notebook.add(capture_frame, text="📷 Face Registration")
        
        # Instructions
        instructions = tk.Label(capture_frame, 
            text="Register people in the system by capturing their faces",
            font=("Arial", 20), fg="yellowgreen")
        instructions.pack(pady=30)
        
        # Name entry
        name_frame = tk.Frame(capture_frame)
        name_frame.pack(pady=40)
        
        tk.Label(name_frame, text="Enter Name:", font=("Arial", 12)).pack(side=tk.LEFT, padx=20)
        self.name_entry = tk.Entry(name_frame, width=30, font=("Arial", 12))
        self.name_entry.pack(side=tk.LEFT, padx=5)


        # Capture button
        tk.Button(capture_frame, text="📸 Capture Face", 
                 command=self.capture_face_handler,
                 width=20, height=2, font=("Arial", 12), bg="lightgreen").pack(pady=20)
                 
        # Instructions text
        instructions_text = """
Instructions for Face Registration:
1. Enter the person's name in the text field above
2. Click 'Capture Face' button
3. Position face clearly in front of the camera
4. Press SPACEBAR to capture each frame (3 frames total)
5. Press 'Q' to quit if needed

Tips:
• Ensure good lighting
• Look directly at the camera
• Avoid shadows on face
• Keep face centered in frame
        """
        
        tk.Label(capture_frame, text=instructions_text, 
                justify=tk.LEFT, font=("Arial", 20)).pack(pady=20)
        
    def setup_recognition_tab(self, notebook):
        """Setup live recognition tab"""
        recognition_frame = ttk.Frame(notebook)
        notebook.add(recognition_frame, text="🎯 Live Recognition")
        
        # Instructions
        instructions = tk.Label(recognition_frame, 
            text="Start live camera recognition to mark attendance in real-time",
            font=("Arial", 20), fg="yellowgreen")
        instructions.pack(pady=20)
        
        # Recognition button
        tk.Button(recognition_frame, text="🚀 Start Live Recognition", 
                 command=self.start_recognition_handler,
                 width=25, height=2, font=("Arial", 20), bg="yellow").pack(pady=40)
        
        # Settings frame
        settings_frame = tk.LabelFrame(recognition_frame, text="Recognition Settings", 
                                      font=("Arial", 11, "bold"))
        settings_frame.pack(pady=20, padx=20, fill='x')
        
        '''tolerance_frame = tk.Frame(settings_frame)
        tolerance_frame.pack(pady=10)
        
        tk.Label(tolerance_frame, text="Recognition Tolerance:", 
                font=("Arial", 10)).pack(side=tk.LEFT)
        self.tolerance_var = tk.DoubleVar(value=0.5)
        tolerance_scale = tk.Scale(tolerance_frame, from_=0.3, to=0.8, resolution=0.1,
                                  orient=tk.HORIZONTAL, variable=self.tolerance_var,
                                  command=self.update_tolerance, length=200)
        tolerance_scale.pack(side=tk.LEFT, padx=10)
        
        tk.Label(tolerance_frame, text="(Lower = Stricter)", 
                font=("Arial", 9), fg="gray").pack(side=tk.LEFT, padx=5)'''
        
    def setup_video_attendance_tab(self, notebook):
        """Setup video attendance processing tab"""
        video_frame = ttk.Frame(notebook)
        notebook.add(video_frame, text="🎬 Video Attendance")
        
        # Instructions
        instructions = tk.Label(video_frame, 
            text="Upload a video to automatically mark attendance for recognized faces",
            font=("Arial", 12), fg="blue")
        instructions.pack(pady=15)
        
        # Video requirements info
        requirements_frame = tk.LabelFrame(video_frame, text="Video Requirements", 
                                          font=("Arial", 11, "bold"))
        requirements_frame.pack(pady=10, padx=20, fill='x')
        
        requirements_text = """
📋 Video Requirements for Attendance:
• Duration: 10-20 seconds
• Format: MP4, AVI, MOV, MKV, WMV, FLV
• Should contain faces of registered people
• Good lighting and clear face visibility
• People must be already registered in the system
        """
        
        tk.Label(requirements_frame, text=requirements_text, 
                justify=tk.LEFT, font=("Arial", 10)).pack(pady=10, padx=10)
        
        # Main process button
        tk.Button(video_frame, text="📹 Process Video for Attendance", 
                 command=self.process_video_attendance_handler,
                 width=35, height=2, font=("Arial", 12), bg="orange").pack(pady=20)
        
        # Undetected faces management frame
        undetected_frame = tk.LabelFrame(video_frame, text="Undetected Faces Management", 
                                        font=("Arial", 11, "bold"))
        undetected_frame.pack(pady=15, padx=20, fill='x')
        
        # Undetected faces info
        self.undetected_info_label = tk.Label(undetected_frame, 
            text="No undetected faces yet", font=("Arial", 10), fg="gray")
        self.undetected_info_label.pack(pady=5)
        
        # Buttons for undetected faces
        undetected_buttons_frame = tk.Frame(undetected_frame)
        undetected_buttons_frame.pack(pady=10)
        
        tk.Button(undetected_buttons_frame, text="📂 Open Faces Folder", 
                 command=self.open_undetected_faces_folder,
                 width=20, font=("Arial", 10), bg="lightcyan").pack(side=tk.LEFT, padx=5)
                 
        tk.Button(undetected_buttons_frame, text="🔄 Refresh Count", 
                 command=self.refresh_undetected_count,
                 width=15, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
                 
        tk.Button(undetected_buttons_frame, text="🗑️ Clear Photos", 
                 command=self.clear_undetected_faces,
                 width=15, font=("Arial", 10), bg="lightcoral").pack(side=tk.LEFT, padx=5)
        
        
        
        # Processing status
        self.video_status_label = tk.Label(video_frame, text="📁 No video processed yet", 
                                          font=("Arial", 11), fg="gray")
        self.video_status_label.pack(pady=15)
        
        # Settings for video processing
        settings_frame = tk.LabelFrame(video_frame, text="Processing Settings", 
                                      font=("Arial", 11, "bold"))
        settings_frame.pack(pady=15, padx=20, fill='x')
        
        # Expected faces per frame
        faces_frame = tk.Frame(settings_frame)
        faces_frame.pack(pady=10)
        
        tk.Label(faces_frame, text="Expected faces per frame:", 
                font=("Arial", 10)).pack(side=tk.LEFT)
        
        tk.Label(faces_frame, text="Min:", font=("Arial", 9)).pack(side=tk.LEFT, padx=(20,5))
        self.min_faces_var = tk.IntVar(value=3)
        min_faces_spinbox = tk.Spinbox(faces_frame, from_=1, to=10, width=5, 
                                      textvariable=self.min_faces_var,
                                      command=self.update_video_settings)
        min_faces_spinbox.pack(side=tk.LEFT, padx=5)
        
        tk.Label(faces_frame, text="Max:", font=("Arial", 9)).pack(side=tk.LEFT, padx=(20,5))
        self.max_faces_var = tk.IntVar(value=4)
        max_faces_spinbox = tk.Spinbox(faces_frame, from_=1, to=10, width=5, 
                                      textvariable=self.max_faces_var,
                                      command=self.update_video_settings)
        max_faces_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Initial update of undetected faces count
        self.refresh_undetected_count()
        
    def setup_attendance_tab(self, notebook):
        """Setup attendance records tab"""
        attendance_frame = ttk.Frame(notebook)
        notebook.add(attendance_frame, text="📊 Attendance Records")
        
        # Control buttons
        control_frame = tk.Frame(attendance_frame)
        control_frame.pack(pady=10)
        
        tk.Button(control_frame, text="🔄 Refresh", 
                 command=self.refresh_attendance_list,
                 width=12, font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
                 
        tk.Button(control_frame, text="📈 Summary", 
                 command=self.show_summary,
                 width=12, font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
                 
        tk.Button(control_frame, text="💾 Export CSV", 
                 command=self.export_attendance,
                 width=12, font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        
        # Treeview for attendance list
        columns = ("Name", "Date", "Time")
        self.tree = ttk.Treeview(attendance_frame, columns=columns, show="headings", height=18)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=220)
            
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(attendance_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill='y', pady=10)
        
        # Initial load of attendance list
        self.refresh_attendance_list()
        
    # Event Handlers
    def capture_face_handler(self):
        """Handle face capture button click"""
        name = self.name_entry.get().strip()
        if self.face_capture.capture_face(name):
            self.clear_name_entry()
            
    def start_recognition_handler(self):
        """Handle live recognition start button click"""
        self.recognition_system.recognize_and_mark_attendance()
        self.refresh_attendance_list()
        
    def process_video_attendance_handler(self):
        """Handle video attendance processing"""
        self.video_status_label.config(text="🔍 Selecting video...", fg="orange")
        self.root.update()
        
        if self.video_processor.select_and_process_video_for_attendance():
            self.video_status_label.config(text="✅ Video processed for attendance!", fg="green")
            self.refresh_attendance_list()  # Refresh attendance list
            self.refresh_undetected_count()  # Update undetected faces count
        else:
            self.video_status_label.config(text="❌ Video processing cancelled", fg="red")
            
    def open_undetected_faces_folder(self):
        """Open the folder containing undetected faces"""
        self.video_processor.open_undetected_faces_folder()
        
    def refresh_undetected_count(self):
        """Refresh the count of undetected faces"""
        count = self.video_processor.get_undetected_faces_count()
        if count > 0:
            self.undetected_info_label.config(
                text=f"📷 {count} undetected face photos available for review", 
                fg="blue")
        else:
            self.undetected_info_label.config(
                text="No undetected faces yet", 
                fg="gray")
                
    def clear_undetected_faces(self):
        """Clear all undetected face photos"""
        count = self.video_processor.get_undetected_faces_count()
        if count == 0:
            messagebox.showinfo("Info", "No undetected faces to clear.")
            return
            
        response = messagebox.askyesno("Confirm Clear", 
            f"Are you sure you want to delete all {count} undetected face photos?")
        
        if response:
            if self.video_processor.clear_undetected_faces():
                messagebox.showinfo("Success", "All undetected face photos cleared.")
                self.refresh_undetected_count()
            else:
                messagebox.showerror("Error", "Failed to clear undetected face photos.")
            
    def update_tolerance(self, value):
        """Update recognition tolerance"""
        self.recognition_system.set_tolerance(float(value))
        
    def update_video_settings(self):
        """Update video processing settings"""
        min_faces = self.min_faces_var.get()
        max_faces = self.max_faces_var.get()
        
        # Ensure min <= max
        if min_faces > max_faces:
            self.min_faces_var.set(max_faces)
            min_faces = max_faces
            
        self.video_processor.set_processing_parameters(
            min_faces=min_faces,
            max_faces=max_faces
        )
        
    def refresh_attendance_list(self):
        """Refresh the attendance list display"""
        # Clear existing items
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        # Load new data
        records = self.attendance_manager.get_attendance_records()
        for record in records:
            self.tree.insert('', tk.END, values=record)
            
    def show_summary(self):
        """Show attendance summary in a popup"""
        summary = self.attendance_manager.get_attendance_summary()
        if summary:
            summary_text = f"""📊 Attendance Summary:
            
Total Records: {summary['total_records']}
Unique Persons: {summary['unique_persons']}

📅 Daily Summary (Last 10 days):
"""
            for date, count in summary['daily_summary'][:10]:
                summary_text += f"{date}: {count} attendees\n"
                
            # Add undetected faces info
            undetected_count = self.video_processor.get_undetected_faces_count()
            if undetected_count > 0:
                summary_text += f"\n📷 Undetected Faces: {undetected_count} photos available for review"
                
            messagebox.showinfo("Attendance Summary", summary_text)
        else:
            messagebox.showerror("Error", "Could not retrieve attendance summary.")
            
    def export_attendance(self):
        """Export attendance records to CSV"""
        try:
            import csv
            
            # Get save location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save Attendance Records"
            )
            
            if file_path:
                records = self.attendance_manager.get_attendance_records()
                
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Name", "Date", "Time"])  # Header
                    writer.writerows(records)
                    
                messagebox.showinfo("Success", f"📁 Attendance records exported to {file_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export records: {str(e)}")
            
    def clear_name_entry(self):
        """Clear the name entry field"""
        self.name_entry.delete(0, tk.END)

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()


