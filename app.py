"""
VigilSense - Smart Field Patrolling & Hazard Detection Bot
Flask Backend for Live Monitoring Dashboard
"""

from flask import Flask, render_template, Response, jsonify
from flask_cors import CORS
import cv2
import random
import time
from datetime import datetime
import threading

app = Flask(__name__)
CORS(app)

# Mock sensor data storage
sensor_data = {
    "temperature": 28.5,
    "humidity": 46,
    "gas": 300,
    "flame": 0,
    "sound": 150,
    "vibration": 0
}

# Mock detection logs
detection_logs = []

# Camera instance (will be None if camera not available)
camera = None

def init_camera():
    """Initialize camera - tries to open default camera (0)"""
    global camera
    try:
        camera = cv2.VideoCapture(0)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        if not camera.isOpened():
            camera = None
            print("Warning: Camera not available. Using mock feed.")
    except Exception as e:
        print(f"Camera initialization error: {e}")
        camera = None

def generate_frames():
    """Generate camera frames for MJPEG stream"""
    while True:
        if camera and camera.isOpened():
            success, frame = camera.read()
            if not success:
                break
        else:
            # Generate mock frame if camera not available
            frame = generate_mock_frame()
        
        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        if not ret:
            continue
        
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        time.sleep(0.033)  # ~30 FPS

def generate_mock_frame():
    """Generate a mock frame when camera is not available"""
    import numpy as np
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    # Add some text to indicate mock feed
    cv2.putText(frame, "Mock Camera Feed", (150, 240), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, "Camera not available", (120, 280), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    return frame

def update_sensor_data():
    """Thread function to continuously update mock sensor data"""
    global sensor_data, detection_logs
    
    while True:
        # Simulate realistic sensor readings with occasional hazards
        sensor_data["temperature"] = round(random.uniform(25, 55), 1)
        sensor_data["humidity"] = round(random.uniform(40, 60), 1)
        sensor_data["gas"] = round(random.uniform(200, 800), 1)
        sensor_data["flame"] = random.choice([0, 0, 0, 0, 1])  # 20% chance
        sensor_data["sound"] = round(random.uniform(100, 400), 1)
        sensor_data["vibration"] = round(random.uniform(0, 150), 1)
        
        # Check for hazards and add to logs
        if (sensor_data["temperature"] > 50 or 
            sensor_data["gas"] > 600 or 
            sensor_data["flame"] == 1 or 
            sensor_data["sound"] > 300 or 
            sensor_data["vibration"] > 100):
            
            detection_type = []
            if sensor_data["temperature"] > 50:
                detection_type.append("High Temp")
            if sensor_data["gas"] > 600:
                detection_type.append("Gas Leak")
            if sensor_data["flame"] == 1:
                detection_type.append("Flame")
            if sensor_data["sound"] > 300:
                detection_type.append("Loud Sound")
            if sensor_data["vibration"] > 100:
                detection_type.append("Vibration")
            
            log_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "detection": ", ".join(detection_type),
                "temp": sensor_data["temperature"],
                "gas": sensor_data["gas"],
                "flame": sensor_data["flame"],
                "sound": sensor_data["sound"],
                "vibration": sensor_data["vibration"]
            }
            
            detection_logs.insert(0, log_entry)
            # Keep only last 10 entries
            if len(detection_logs) > 10:
                detection_logs.pop()
        
        time.sleep(2)  # Update every 2 seconds

@app.route('/')
def index():
    """Render the main dashboard page"""
    return render_template('index.html')

@app.route('/logs')
def logs():
    """Render the detection logs page"""
    return render_template('logs.html')

@app.route('/stream.mjpg')
def stream():
    """MJPEG camera stream endpoint"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/sensors')
def get_sensors():
    """API endpoint to get current sensor data"""
    return jsonify(sensor_data)

@app.route('/api/logs')
def get_logs():
    """API endpoint to get detection logs"""
    return jsonify(detection_logs)

@app.route('/api/status')
def get_status():
    """API endpoint to get system status"""
    # Check if any hazard is detected
    is_hazard = (
        sensor_data["temperature"] > 50 or
        sensor_data["gas"] > 600 or
        sensor_data["flame"] == 1 or
        sensor_data["sound"] > 300 or
        sensor_data["vibration"] > 100
    )
    
    return jsonify({
        "status": "hazard" if is_hazard else "normal",
        "message": "⚠️ Hazard Detected" if is_hazard else "✅ All Systems Normal"
    })

if __name__ == '__main__':
    # Initialize camera
    init_camera()
    
    # Start sensor data update thread
    sensor_thread = threading.Thread(target=update_sensor_data, daemon=True)
    sensor_thread.start()
    
    # Run Flask app
    print("Starting VigilSense Dashboard...")
    print("Access at: http://localhost:8080")
    print("Camera:", "Connected" if camera and camera.isOpened() else "Not Available (using mock)")
    
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)

