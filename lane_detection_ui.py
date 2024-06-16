from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
import cv2
from lane_detection import LaneDetection
import sys

class LaneDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lane_detection = LaneDetection()
        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_frame)
        self.cap = None

    def initUI(self):
        self.setWindowTitle("Lane Detection App")
        self.setGeometry(100, 100, 800, 600)

        self.label = QLabel(self)
        self.label.setGeometry(10, 10, 780, 540)

        self.button = QPushButton("Open Video", self)
        self.button.setGeometry(10, 560, 780, 30)
        self.button.clicked.connect(self.open_video)

    def open_video(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        video_path, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4 *.avi)", options=options)
        if video_path:
            print(f"Selected video path: {video_path}")
            self.cap = cv2.VideoCapture(video_path)
            if not self.cap.isOpened():
                print("Error: Could not open video.")
                return
            self.timer.start(30)  # Process a frame every 30ms

    def process_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                print("Finished processing video or failed to read frame.")
                self.timer.stop()
                self.cap.release()
                return
            print("Processing frame")
            processed_frame = self.lane_detection.process_frame(frame)
            self.display_frame(processed_frame)

    def display_frame(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(convert_to_Qt_format))
        print("Displayed frame")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = LaneDetectionApp()
    main_window.show()
    sys.exit(app.exec_())
