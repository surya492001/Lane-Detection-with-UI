import cv2
import numpy as np

class LaneDetection:
    def __init__(self):
        pass
    def region_of_interest(self,img,vertices):
        mask=np.zeros_like(img)
        cv2.fillPoly(mask,vertices,255)
        masked_image=cv2.bitwise_and(img,mask)
        return masked_image
    def detect_edges(self,frame):
        gray=cv2.cvtColor(frame,cv2.COLOR_BAYER_BG2GRAY)
        blur=cv2.GaussianBlur(gray,(5,5),0)
        edges=cv2.Canny(blur,50,150)
        return edges
    def detect_lines(self, edges):
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, maxLineGap=50)
        return lines

    def draw_lines(self, frame, lines):
        line_image = np.zeros_like(frame)
        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 10)
        combined = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
        return combined
    def process_frame(Self,frame):
          height, width = frame.shape[:2]
          region_of_interest_vertices = [
            (0, height),
            (width // 2, height // 2),
            (width, height),
        ]
          edges=Self.detect_edges(frame)
          cropped_edges = Self.region_of_interest(edges, np.array([region_of_interest_vertices], np.int32))
          lines = Self.detect_lines(cropped_edges)
          frame_with_lines = Self.draw_lines(frame, lines)
          return frame_with_lines
