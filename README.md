# VigilSense Dashboard

**Smart Field Patrolling & Hazard Detection Bot - Live Monitoring Dashboard**

A real-time monitoring dashboard for IoT + AI project featuring Raspberry Pi 4, Arduino UNO R4 WiFi, and multiple sensors for field patrolling and hazard detection.

## 🚀 Features

- **Live Camera Feed**: Real-time MJPEG stream from Pi Camera v3
- **Real-time Sensor Monitoring**: Temperature, Humidity, Gas, Flame, Sound, Vibration
- **Interactive Charts**: Live sensor trend visualization with Chart.js
- **Detection Logs**: Comprehensive hazard detection history
- **Fullscreen Mode**: Immersive viewing experience
- **Responsive Design**: Works on desktop and mobile devices
- **Premium Dark Theme**: Minimalist black theme with clean UI

## 📋 System Requirements

- Raspberry Pi 4 (or any system with Python 3.7+)
- Pi Camera v3 (optional - uses mock feed if unavailable)
- Arduino UNO R4 WiFi (for sensor data)
- Python 3.7 or higher

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd vigil_sense_dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or with system packages:
   ```bash
   pip install --break-system-packages -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the dashboard**
   - Local: `http://localhost:8080`
   - Network: `http://<raspberry-pi-ip>:8080`

## 📁 Project Structure

```
vigil_sense_dashboard/
├── app.py                 # Flask backend with API endpoints
├── requirements.txt       # Python dependencies
├── templates/
│   ├── index.html        # Main dashboard page
│   └── logs.html         # Detection logs page
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── dashboard.js  # Real-time update logic
└── README.md             # This file
```

## 🔌 API Endpoints

- `GET /` - Main dashboard page
- `GET /logs` - Detection logs page
- `GET /stream.mjpg` - MJPEG camera stream
- `GET /api/sensors` - Current sensor data (JSON)
- `GET /api/logs` - Detection log entries (JSON)
- `GET /api/status` - System status (JSON)

## 🎛️ Sensor Thresholds

Hazard alerts are triggered when:
- **Temperature** > 50°C
- **Gas Level** > 600 ppm
- **Flame** = 1 (detected)
- **Sound** > 300 dB
- **Vibration** > 100

## 🔧 Configuration

### Camera Setup
- The app automatically detects available cameras
- If no camera is found, a mock feed is displayed
- Camera index can be changed in `app.py` (default: 0)

### Sensor Data
- Currently uses mock data for standalone operation
- Connect to Arduino via serial/USB to get real sensor readings
- Update `update_sensor_data()` function in `app.py` to integrate real sensors

### Port Configuration
- Default port: `8080`
- Change in `app.py`: `app.run(host='0.0.0.0', port=8080)`

## 📊 Dashboard Features

### Main Dashboard
- Live camera feed with responsive player
- 6 sensor cards with color-coded alerts
- Real-time trend charts (Temperature, Gas, Sound, Vibration)
- System status indicator
- Fullscreen mode toggle

### Detection Logs Page
- Complete history of hazard detections
- Timestamp, detection type, and sensor values
- Refresh button for manual updates
- Auto-refresh every 5 seconds

## 🎨 Theme

- **Background**: Pure black (#000000)
- **Text**: White with gray accents
- **Borders**: Light gray (#404040)
- **Alerts**: Red highlights for hazards
- **Charts**: Multi-color lines with dark theme

## 🔄 Real-time Updates

- **Sensor Data**: Updates every 2 seconds
- **Detection Logs**: Updates every 5 seconds
- **System Status**: Updates every 2 seconds
- **Charts**: Updates with sensor data (last 20 points)

## 📱 Browser Compatibility

- Chrome/Edge (recommended)
- Firefox
- Safari
- Fullscreen mode works in all modern browsers

## 🐛 Troubleshooting

### Camera not working
- Check camera permissions
- Verify camera index in `app.py`
- Mock feed will display if camera unavailable

### Port already in use
- Change port in `app.py`
- Or kill process using port 8080: `lsof -ti:8080 | xargs kill`

### Dependencies not installing
- Use `--break-system-packages` flag if needed
- Or create a virtual environment: `python -m venv venv && source venv/bin/activate`

## 📝 License

This project is part of the VigilSense IoT + AI field patrolling system.

## 👨‍💻 Author

Built for VigilSense - Smart Field Patrolling & Hazard Detection Bot

---

**Note**: This dashboard is designed for demonstration and monitoring purposes. For production use, ensure proper security measures and authentication.

