``` python
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
        
    # ... Rest of the code remains the same ...
```
