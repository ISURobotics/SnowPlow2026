import cv2
import numpy as np

def initialize_camera():
    return cv2.VideoCapture(0)

class RedLightDetector:
    def __init__(self, persistence_threshold=3):
        self.consecutive_frames = 0
        self.persistence_threshold = persistence_threshold
        
        # Strict Red HSV ranges + High Value (Brightness)
        self.lower_red1 = np.array([0, 150, 210])
        self.upper_red1 = np.array([10, 255, 255])
        self.lower_red2 = np.array([170, 150, 210])
        self.upper_red2 = np.array([179, 255, 255])
        self.kernel = np.ones((3, 3), np.uint8)

    def update(self, frame):
        # Resize for performance optimization on Jetson Nano
        frame = cv2.resize(frame, (640, 480))
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        mask1 = cv2.inRange(hsv, self.lower_red1, self.upper_red1)
        mask2 = cv2.inRange(hsv, self.lower_red2, self.upper_red2)
        mask = mask1 + mask2
        
        # Clean up noise
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Adjust these based on how far away the lights look from the camera
        MIN_AREA = 10
        MAX_AREA = 500 
        
        light_found_in_frame = False
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if MIN_AREA < area < MAX_AREA:
                x, y, w, h = cv2.boundingRect(cnt)
                aspect_ratio = float(w) / h if h > 0 else 0
                
                # Lights are roughly square/circular
                if 0.5 <= aspect_ratio <= 2.0:
                    hull = cv2.convexHull(cnt)
                    hull_area = cv2.contourArea(hull)
                    solidity = float(area) / hull_area if hull_area > 0 else 0
                    
                    if solidity > 0.75:
                        light_found_in_frame = True
                        break # Found at least one valid light source in this frame
                        
        # Temporal persistence logic (debouncing)
        if light_found_in_frame:
            self.consecutive_frames += 1
        else:
            # Decay counter if frame missed to prevent lingering accumulation
            self.consecutive_frames = max(0, self.consecutive_frames - 1)
            
        # Return True only if the light has been continuously present for N frames
        return self.consecutive_frames >= self.persistence_threshold

# Main loop integration example
if __name__ == "__main__":
    cap = initialize_camera()
    detector = RedLightDetector(persistence_threshold=3)
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break
                
            light_is_on = detector.update(frame)
            
            if light_is_on:
                print("Confirmed Red Light Detected! Stopping robot.")
                # TODO: Trigger robot stop function here
            else:
                # Continue normal navigation
                pass
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
