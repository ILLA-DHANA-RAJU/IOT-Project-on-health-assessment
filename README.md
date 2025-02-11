## 📌 Overview  
This project is a **Pulse Sensing and Health Monitoring System** that reads real-time heart rate data using an **Arduino Uno/Nano** and a **Pulse Sensor**. The data is displayed on an **I2C LCD (16x2)** and sent to a **Flask web application**, which analyzes the pulse data and predicts health status using a **Random Forest Model**.  

## ⚡ Features  
- ✅ Real-time pulse monitoring using an Arduino and Pulse Sensor  
- ✅ Displays BPM on an I2C LCD screen  
- ✅ Data is sent to a Flask web application for analysis  
- ✅ Machine Learning model (Random Forest) predicts health status  
- ✅ SQLite database stores pulse data for further analysis  

## 🔧 Components Used  
- **Arduino Nano/Uno**  
- **Pulse Sensor**  
- **I2C LCD Display (16x2)**  
- **ESP8266 Wi-Fi Module** (for wireless data transmission)  
- **Flask (Python Backend for Data Analysis)**  
- **RandomForestClassifier (ML Model for Health Prediction)**  
- **SQLite Database (for storing pulse data)**  

## 📜 Installation & Setup  

### 1️⃣ Hardware Setup  
- Connect the **Pulse Sensor** to the Arduino (`A0` for signal, `VCC` for power, `GND` for ground`).  
- Connect the **I2C LCD** (`SDA to A4, SCL to A5`).  
- Use **ESP8266** to send data wirelessly if required.  

### 2️⃣ Software Requirements  
- Install Python 3.x and required dependencies:  
  ```bash
  pip install flask sklearn sqlite3
Clone the repository:
bash
Copy
Edit
git clone https://github.com/yourusername/pulse-sensing.git
cd pulse-sensing
### 3️⃣ Running the Flask Server
bash
Copy
Edit
python app.py
Open http://127.0.0.1:5000 to view real-time pulse data and predictions.

## 📊 Machine Learning Model
Uses Random Forest Classification to predict health status based on pulse patterns.
Trained using data from pulse_data.db.
Prediction output:
- **✅ Healthy (Normal heart rate range)**
- **⚠️ Unhealthy (Abnormal readings detected)**
- **📌 Future Enhancements**
- **🏥 Integration with a mobile app for remote monitoring**
- **📡 Cloud-based data storage using ThingSpeak/Firebase**
- **📈 Improve ML model accuracy with more training data**

## 📜 License
This project is open-source and available under the MIT License.

## 🙌 Connect with Me

📧 Email: dhana.raju.illa@gmail.com
📱 Number: 6300462192
