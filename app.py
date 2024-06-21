from flask import Flask, request, jsonify, Response
import cv2
import numpy as np
from lane_detection import LaneDetection
import logging

app = Flask(__name__)
lane_detection = LaneDetection()

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return "Lane Detection API"

@app.route('/process_frame', methods=['POST'])
def process_frame():
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video_file = request.files['video']
    video_path = 'uploaded_video.mp4'
    video_file.save(video_path)
    logging.debug(f"Saved video to {video_path}")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return jsonify({"error": "Could not open video"}), 400

    frame_count = 0
    processed_frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        logging.debug(f"Processing frame {frame_count}")
        processed_frame = lane_detection.process_frame(frame)
        _, buffer = cv2.imencode('.jpg', processed_frame)
        processed_frames.append(buffer.tobytes())

    cap.release()
    logging.debug(f"Total frames processed: {frame_count}")

    return Response(generate_frames(processed_frames), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_frames(frames):
    for frame in frames:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

if __name__ == '__main__':
    app.run(debug=True)
