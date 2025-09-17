import cv2
import sqlite3
import face_recognition
import numpy as np
from tkinter import messagebox

class FaceCapture:
    def __init__(self):
        pass
    
    def capture_face(self, name):
        """Capture face encodings for a given name"""
        if not name.strip():
            messagebox.showerror("Error", "Please enter a name first.")
            return False
            
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Could not open the camera.")
            return False

        messagebox.showinfo("Instructions", "Position your face clearly. Capturing 3 frames.")
        
        face_encodings = []
        count = 0
        
        while count < 3:
            ret, frame = cap.read()
            if not ret:
                break
                
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = face_recognition.face_locations(rgb_frame)
            
            cv2.putText(frame, f"Press space to capture {count+1}/3", (50, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Capture Face", frame)
            
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
                
            if key == 32:  # Spacebar to capture
                if faces:
                    encodings = face_recognition.face_encodings(rgb_frame, faces)
                    if encodings:
                        face_encodings.append(encodings[0])
                        count += 1
                        messagebox.showinfo("Captured", f"Captured {count}/3 successfully.")
                    else:
                        messagebox.showwarning("Warning", "Face not clear. Try again.")
                else:
                    messagebox.showwarning("Warning", "No face detected. Try again.")
        
        cap.release()
        cv2.destroyAllWindows()
        
        if len(face_encodings) == 0:
            messagebox.showerror("Error", "No face detected.")
            return False
            
        # Store the average encoding
        avg_encoding = np.mean(face_encodings, axis=0)
        return self._store_face_encoding(name.strip(), avg_encoding)
    
    def _store_face_encoding(self, name, encoding):
        """Store face encoding in database"""
        try:
            conn = sqlite3.connect('faces.db')
            c = conn.cursor()
            c.execute("INSERT INTO faces (name, encoding) VALUES (?, ?)",
                     (name, encoding.tobytes()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Face data stored for {name}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to store face data: {str(e)}")
            return False
    
    def get_stored_faces(self):
        """Retrieve all stored face encodings"""
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
            print(f"Error retrieving stored faces: {str(e)}")
            return [], []