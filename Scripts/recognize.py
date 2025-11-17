import tkinter as tk
from tkinter import messagebox
import cv2
import os
import pandas as pd
import datetime
import time


class FaceAttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recogniser - Attendance Tracker")
        self.root.geometry('1024x720')
        self.root.configure(bg="#f0f0f0")

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Face Recognition Attendance System", font=('Arial', 25, 'bold'), bg="#282c34",
                 fg="white", pady=20).pack(fill=tk.X)

        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=100)


        tk.Button(btn_frame, text="Track Attendance", font=('Arial', 18, 'bold'), command=self.track_images,
                  bg="#000000", fg="white", padx=30, pady=15).pack(side=tk.LEFT, padx=50)


    def is_number(self, s):
        return True

    def take_images(self):
        messagebox.showinfo("Info", "Registration/Capture is handled in the 'register_train.py' file.")

    def train_images(self):
        messagebox.showinfo("Info", "Training is handled in the 'register_train.py' file.")

    def get_images_and_labels(self, path):
        messagebox.showinfo("Error", "This method should not be called in this file.")
        return [], []

    def track_images(self):
        try:

            if not os.path.exists("TrainingImageLabel/Trainer.yml"):
                messagebox.showerror("Error",
                                     "Trainer.yml not found. Please train images in 'register_train.py' first.")
                return
            if not os.path.exists("EmployeeDetails/EmployeeDetails.csv"):
                messagebox.showerror("Error",
                                     "EmployeeDetails.csv not found. Please capture images in 'register_train.py' first.")
                return

            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.read("TrainingImageLabel/Trainer.yml")
            faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            df = pd.read_csv("EmployeeDetails/EmployeeDetails.csv", header=None, names=["Id", "Name"])
            cam = cv2.VideoCapture(0)
            font = cv2.FONT_HERSHEY_SIMPLEX

            attendance = pd.DataFrame(columns=['Id', 'Name', 'Date', 'Time'])

            while True:
                ret, im = cam.read()
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(gray, 1.2, 5)

                for (x, y, w, h) in faces:
                    Id, conf = recognizer.predict(gray[y:y + h, x:x + w])

                    if conf < 50:
                        ts = time.time()
                        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

                        name_data = df[df['Id'] == Id]

                        if not name_data.empty:
                            name = name_data['Name'].values[0]
                            label = f"{Id} - {name} (Present)"
                            # Log attendance
                            attendance.loc[len(attendance)] = [Id, name, date, timeStamp]
                        else:
                            label = f"{Id} - Unknown (No Record)"
                    else:
                        label = "Unknown"

                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(im, label, (x, y - 10), font, 0.75, (0, 255, 0), 2)

                cv2.imshow('Tracking Attendance', im)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cam.release()
            cv2.destroyAllWindows()

            # Save attendance log
            attendance.drop_duplicates(subset=['Id'], inplace=True)
            os.makedirs("Attendance", exist_ok=True)
            filename = f"Attendance/Attendance_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
            attendance.to_csv(filename, index=False)
            messagebox.showinfo("Attendance Saved", f"Attendance saved to {filename}")

        except Exception as e:
            messagebox.showerror("Error",
                                 f"Attendance tracking failed. Ensure files exist and camera works. Error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FaceAttendanceApp(root)
    root.mainloop()