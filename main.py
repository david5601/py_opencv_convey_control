from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
import os
import cv2
import numpy as np

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Convey Control")
        self.geometry("600x400")
        self.resizable(False, False)

        self.widget_width = 600
        self.widget_height = 400

        self.horizontal_line_position = self.widget_height // 2
        self.fruit_count = 0

        self.captureLabel = ttk.Label(
            self,
            text="Connecting the camera.",
            font=("Roboto", 13, "bold"),
            anchor="w"  # Align text to the left within the label
        )
        self.captureLabel.pack(fill="both", expand=True)
        
        friutNumFram = tk.Frame(self, bg="blue")
        friutNumFram.place(x=500, y=30, width=70, height=30) 
        self.fruitsNumLabel = ttk.Label(friutNumFram, text="0", font=("Roboto", 13, "bold"))
        self.fruitsNumLabel.pack(fill="both", expand=True)

        self.cap = cv2.VideoCapture("./fruits1.mp4")
        self.update_frame()
    
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.resize(frame, (self.widget_width, self.widget_height))

            # Define the color range for detecting red apples
            lower_red = np.array([160.0, 153.0, 153.0])  # Lower bound of red in HSV
            upper_red = np.array([180.0, 255.0, 255.0])  # Upper bound of red in HSV
            lower_red2 = np.array([0.0, 150.0, 150.0])  # Lower bound for the second red hue range
            upper_red2 = np.array([15.0, 255.0, 255.0])  # Upper bound for the second red hue range

             # Convert the frame to HSV color space
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # Create masks for the red color
            mask1 = cv2.inRange(hsv, lower_red, upper_red)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask = cv2.bitwise_or(mask1, mask2)

            # Find contours of the red areas
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # blurred = cv2.GaussianBlur(gray, (15, 15), 0)

            # _, thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY_INV)
            # contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                if cv2.contourArea(contour) > 50:  # Adjust this area threshold as needed
                    x, y, w, h = cv2.boundingRect(contour)
                    (Cx,Cy), rad = cv2.minEnclosingCircle(contour)
                    if rad <= 40:
                        if y < self.horizontal_line_position < y + rad:
                            self.fruit_count += 1
                            cv2.circle(frame, (int(Cx), int(Cy)), int(rad), (111, 220, 111), 2)
            self.fruitsNumLabel.config(text=str(self.fruit_count))
                            # cv2.putText(frame, str(int(self.fruit_count)), (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.line(frame, (0, self.horizontal_line_position), (self.widget_width, self.horizontal_line_position), (255, 0, 128), 1)
            frame_image = Image.fromarray(frame)
            frame_photo = ImageTk.PhotoImage(image=frame_image)
            self.captureLabel.configure(image=frame_photo)
            self.captureLabel.image = frame_photo
            self.after(40, self.update_frame)

    def on_closing(self):
        self.cap.release()
        self.destroy()

app = App()
app.protocol("WM_DELETE_WINDOW", app.on_closing)
app.mainloop()