import sqlite3
from datetime import datetime
from tkinter import messagebox

class AttendanceManager:
    def __init__(self):
        pass
        
    def mark_attendance(self, name, date=None):
        """Mark attendance for a person"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
            
        try:
            conn = sqlite3.connect('attendance.db')
            c = conn.cursor()
            # Check if last attendance for this person was within the last 5 minutes
            c.execute("SELECT time FROM attendance WHERE name=? AND date=? ORDER BY time DESC LIMIT 1", (name, date))
            last_record = c.fetchone()

            if last_record:
                last_time = datetime.strptime(last_record[0], '%H:%M:%S')
                now_time = datetime.now()
                if (now_time - last_time).seconds < 300:  # 5 minutes
                    return False  # Don't mark again too soon

            
            current_time = datetime.now().strftime('%H:%M:%S')
            c.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)", (name, date, current_time))
            if c.fetchone() is None:
                current_time = datetime.now().strftime('%H:%M:%S')
                c.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)",
                         (name, date, current_time))
                conn.commit()
                conn.close()
                return True
            else:
                conn.close()
                return False
        except Exception as e:
            print(f"Error marking attendance: {str(e)}")
            return False
            
    def get_attendance_records(self, date=None):
        """Get attendance records for a specific date or all records"""
        try:
            conn = sqlite3.connect('attendance.db')
            c = conn.cursor()
            
            if date:
                c.execute("SELECT name, date, time FROM attendance WHERE date=?", (date,))
            else:
                c.execute("SELECT name, date, time FROM attendance ORDER BY date DESC, time DESC")
                
            records = c.fetchall()
            conn.close()
            return records
        except Exception as e:
            print(f"Error retrieving attendance records: {str(e)}")
            return []
            
    def get_attendance_by_name(self, name):
        """Get attendance records for a specific person"""
        try:
            conn = sqlite3.connect('attendance.db')
            c = conn.cursor()
            c.execute("SELECT name, date, time FROM attendance WHERE name=? ORDER BY date DESC", (name,))
            records = c.fetchall()
            conn.close()
            return records
        except Exception as e:
            print(f"Error retrieving attendance for {name}: {str(e)}")
            return []
            
    def delete_attendance_record(self, name, date, time):
        """Delete a specific attendance record"""
        try:
            conn = sqlite3.connect('attendance.db')
            c = conn.cursor()
            c.execute("DELETE FROM attendance WHERE name=? AND date=? AND time=?", (name, date, time))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting attendance record: {str(e)}")
            return False
            
    def get_attendance_summary(self):
        """Get attendance summary statistics"""
        try:
            conn = sqlite3.connect('attendance.db')
            c = conn.cursor()
            
            # Total attendance records
            c.execute("SELECT COUNT(*) FROM attendance")
            total_records = c.fetchone()[0]
            
            # Unique persons who attended
            c.execute("SELECT COUNT(DISTINCT name) FROM attendance")
            unique_persons = c.fetchone()[0]
            
            # Attendance by date
            c.execute("SELECT date, COUNT(*) FROM attendance GROUP BY date ORDER BY date DESC")
            daily_summary = c.fetchall()
            
            conn.close()
            return {
                'total_records': total_records,
                'unique_persons': unique_persons,
                'daily_summary': daily_summary
            }
        except Exception as e:
            print(f"Error getting attendance summary: {str(e)}")
            return None
