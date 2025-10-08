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
# Intelligent Face Recognition Attendance System 📸

This project is a desktop application that uses facial recognition to take and manage attendance automatically.

---

## ## Prerequisites ⚙️

Before you begin, ensure you have the following installed on your system:
* **Python 3.10 or newer** ([Download Python](https://www.python.org/downloads/))
* **pip** (which is typically included with your Python installation)

---

## ## Setup and Installation Instructions ✅

Follow these steps to get your project up and running.

### ### 1. Clone the Repository

First, clone this repository to your local machine (or simply download the code as a ZIP file).

```bash
git clone <your-repository-url>
cd <repository-name>
```

### ### 2. Create and Activate a Virtual Environment

It's highly recommended to use a virtual environment to keep project dependencies isolated.

**Create the environment:**
```bash
python -m venv venv
```

**Activate the environment:**
* On **macOS and Linux**:
    ```bash
    source venv/bin/activate
    ```
* On **Windows**:
    ```bash
    .\venv\Scripts\activate
    ```
Your terminal prompt should now show `(venv)` at the beginning.

### ### 3. Prepare the `requirements.txt` File

The `dlib` library requires a special setup. Open your `requirements.txt` file and make sure the line for `dlib` **only contains the package name**, like this:

```
# requirements.txt

numpy==2.2.6
opencv-python==4.12.0.88
face-recognition==1.3.0
dlib
face_recognition_models==0.3.0
Pillow==11.3.0
```

### ### 4. Install All Dependencies

Now, install all the necessary Python packages using the prepared `requirements.txt` file.

```bash
pip install -r requirements.txt
```
> **Note:** If you run into issues installing `dlib`, you may need to install `CMake` and a C++ compiler first. You can download CMake [here](https://cmake.org/download/).

---

## ## Running the Application 🚀

Once all the dependencies are installed, you can start the application by running the `main.py` script.

```bash
python main.py
```

The application window should now open, and you can begin using the face recognition attendance system.