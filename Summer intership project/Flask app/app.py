from flask import Flask, render_template
import requests
import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

app = Flask(__name__)

CHANNEL_ID = "2735752"
READ_API_KEY = "4TXQIDDOE2HKT70Y"

# Initialize the database
def init_db():
    conn = sqlite3.connect('pulse_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS pulses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        pulse_value REAL,
                        timestamp TEXT
                    )''')
    conn.commit()
    conn.close()

# Fetch data from ThingSpeak
def fetch_pulse_data():
    url = f"https://api.thingspeak.com/channels/2735752/fields/1.json?api_key=F2FP8WCLIEDJ902U&results=200"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        pulse_values = [float(entry['field1']) for entry in data['feeds'] if entry['field1'] is not None]
        timestamps = [entry['created_at'] for entry in data['feeds']]
        return pulse_values, timestamps
    return [], []

# Store data in the database
def store_data_in_db(pulse_values, timestamps):
    conn = sqlite3.connect('pulse_data.db')
    cursor = conn.cursor()
    for pulse, timestamp in zip(pulse_values, timestamps):
        cursor.execute('SELECT COUNT(*) FROM pulses WHERE pulse_value = ? AND timestamp = ?', (pulse, timestamp))
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO pulses (pulse_value, timestamp) VALUES (?, ?)', (pulse, timestamp))
    conn.commit()
    conn.close()

# Prepare and process data for ML
def prepare_data(pulse_values):
    pulse_sum = sum(pulse_values)
    pulse_avg = pulse_sum / len(pulse_values)
    data = pd.DataFrame({'pulse_sum': [pulse_sum], 'pulse_avg': [pulse_avg]})
    HEALTHY_LOWER_BOUND = 60
    HEALTHY_UPPER_BOUND = 100
    data['health_status'] = data['pulse_avg'].apply(lambda x: "Healthy" if HEALTHY_LOWER_BOUND <= x <= HEALTHY_UPPER_BOUND else "Unhealthy")

    return data
# Train or load model
def load_or_train_model(pulse_values):
    if len(pulse_values) < 2:
        return None
    data = prepare_data(pulse_values)
    if os.path.exists("pulse_model.pkl"):
        model = joblib.load("pulse_model.pkl")
    else:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(data[['pulse_sum', 'pulse_avg']], data['health_status'])
        joblib.dump(model, "pulse_model.pkl")
    return model

@app.route("/")
def home():
    pulse_values, timestamps = fetch_pulse_data()
    if pulse_values:
        store_data_in_db(pulse_values, timestamps)
        
        # Calculate pulse_sum and pulse_avg directly
        pulse_sum = sum(pulse_values)
        pulse_avg = pulse_sum / len(pulse_values)
        
        # Direct health status check with a modified range (if needed)
        # You can adjust these thresholds as required.
        HEALTHY_LOWER_BOUND = 60
        HEALTHY_UPPER_BOUND = 100
        health_status = "Healthy" if HEALTHY_LOWER_BOUND <= pulse_avg <= HEALTHY_UPPER_BOUND else "Unhealthy"
    else:
        health_status, pulse_sum, pulse_avg = "No Data", 0, 0

    # Retrieve all data from the database in ascending order of timestamp
    conn = sqlite3.connect('pulse_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pulses ORDER BY timestamp ASC")
    stored_data = cursor.fetchall()
    conn.close()

    return render_template("index.html", stored_data=stored_data, health_status=health_status, pulse_sum=pulse_sum, pulse_avg=pulse_avg)



if __name__ == "__main__":
    init_db()
    app.run(debug=True)
