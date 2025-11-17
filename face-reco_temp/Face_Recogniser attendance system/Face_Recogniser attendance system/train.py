import tkinter as tk
from tkinter import messagebox
import cv2
import os
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recogniser Attendance System")
        self.root.geometry('1024x720')
        self.root.configure(bg="#f0f0f0")

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Face Recognition Attendance System", font=('Arial', 25, 'bold'), bg="#282c34", fg="white", pady=20).pack(fill=tk.X)

        form_frame = tk.Frame(self.root, bg="#f0f0f0")
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Employee ID", font=('Arial', 14)).grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
        self.emp_id_entry = tk.Entry(form_frame, font=('Arial', 14))
        self.emp_id_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Employee Name", font=('Arial', 14)).grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
        self.emp_name_entry = tk.Entry(form_frame, font=('Arial', 14))
        self.emp_name_entry.grid(row=1, column=1, padx=10, pady=10)

        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Capture Images", font=('Arial', 14), command=self.take_images).pack(side=tk.LEFT, padx=20)
        tk.Button(btn_frame, text="Train Images", font=('Arial', 14), command=self.train_images).pack(side=tk.LEFT, padx=20)
        tk.Button(btn_frame, text="Track Attendance", font=('Arial', 14), command=self.track_images).pack(side=tk.LEFT, padx=20)

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def take_images(self):
        Id = self.emp_id_entry.get()
        name = self.emp_name_entry.get()

        if not (self.is_number(Id) and name.isalpha()):
            messagebox.showerror("Error", "Invalid ID or Name")
            return

        cam = cv2.VideoCapture(0)
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        sampleNum = 0

        os.makedirs("TrainingImage", exist_ok=True)

        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                sampleNum += 1
                cv2.imwrite(f"TrainingImage/{name}.{Id}.{sampleNum}.jpg", gray[y:y+h, x:x+w])
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.imshow('Capturing Image', img)
            if cv2.waitKey(100) & 0xFF == ord('q') or sampleNum >= 30:
                break

        cam.release()
        cv2.destroyAllWindows()

        os.makedirs("EmployeeDetails", exist_ok=True)
        with open('EmployeeDetails/EmployeeDetails.csv', 'a+', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([Id, name])

        messagebox.showinfo("Success", f"Images Saved for ID: {Id}, Name: {name}")

    def train_images(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        faces, Ids = self.get_images_and_labels("TrainingImage")
        recognizer.train(faces, np.array(Ids))

        os.makedirs("TrainingImageLabel", exist_ok=True)
        recognizer.save("TrainingImageLabel/Trainer.yml")

        messagebox.showinfo("Training Complete", "Model trained successfully!")

    def get_images_and_labels(self, path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
        faces, Ids = [], []
        for imagePath in imagePaths:
            pilImage = Image.open(imagePath).convert('L')
            imageNp = np.array(pilImage, 'uint8')
            Id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces.append(imageNp)
            Ids.append(Id)
        return faces, Ids

    def track_images(self):
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
                Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
                if conf < 50:
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    name_data = df[df['Id'] == Id]
                    if not name_data.empty:
                        name = name_data['Name'].values[0]
                        label = f"{Id} - {name} (Present)"
                        attendance.loc[len(attendance)] = [Id, name, date, timeStamp]
                    else:
                        label = f"{Id} - Unknown (No Record)"
                else:
                    label = "Unknown"

                cv2.rectangle(im, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(im, label, (x, y-10), font, 0.75, (0, 255, 0), 2)

            cv2.imshow('Tracking Attendance', im)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()

        attendance.drop_duplicates(subset=['Id'], inplace=True)
        os.makedirs("Attendance", exist_ok=True)
        filename = f"Attendance/Attendance_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        attendance.to_csv(filename, index=False)
        messagebox.showinfo("Attendance Saved", f"Attendance saved to {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
