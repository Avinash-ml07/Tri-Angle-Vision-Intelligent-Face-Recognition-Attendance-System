# 🎯 Face Recognition Attendance System

A **Tkinter-based Desktop Application** that uses **face recognition** to register, identify, and manage attendance records. The system supports:
- Live camera recognition
- Face registration (with multiple captures)
- Video-based attendance processing
- Attendance record storage and export

---

## 📌 Features

### 1. **Face Registration**
- Register new people by capturing **3 clear face images**.
- Ensures good lighting and face positioning.
- Stores captured faces in the system for recognition.

### 2. **Live Recognition & Attendance**
- Start **real-time face recognition** using a webcam.
- Automatically marks attendance for recognized individuals.
- Updates records instantly.

### 3. **Video Attendance Processing**
- Upload and process a pre-recorded video to mark attendance.
- Supports multiple formats: `MP4, AVI, MOV, MKV, WMV, FLV`.
- Saves **undetected faces** for later review.
- Adjustable **min/max expected faces per frame** for accuracy.

### 4. **Attendance Records Management**
- View all attendance logs in a tabular format.
- Generate daily attendance summary.
- Export records as **CSV files** for external use.
- Review and clear undetected faces folder.

---

## 🛠️ Tech Stack

- **Python** (>=3.9 recommended)
- **Tkinter** (GUI)
- **OpenCV** (for face capture & video processing)
- **face_recognition** library (dlib-based recognition)
- **SQLite** (database for attendance & user management)

---

## 📂 Project Structure

project/
│── app.py (main script to run GUI)<br>
│── database_setup.py (DB initialization)<br>
│── face_capture.py (handles capturing faces)<br>
│── face_recognition_system.py (live recognition logic)<br>
│── attendance_manager.py (attendance storage & summary)<br>
│── video_processor.py (video upload & processing)<br>
│── faces.db/ (stored face encodings/images)<br>
│── attendance.db (SQLite DB)<br>
│── undetected_faces/ (faces not recognized in videos)<br>




---

## 🚀 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/face-recognition-attendance.git
   cd face-recognition-attendance


python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
