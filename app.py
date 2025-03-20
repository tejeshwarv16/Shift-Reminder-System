import os
import time
from datetime import datetime, timedelta
import cv2
import numpy as np
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from twilio.rest import Client
from PIL import Image
import io
import sqlite3

load_dotenv()

app = Flask(__name__)

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Configure Twilio
twilio_client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")

# Database setup
def get_db_connection():
    conn = sqlite3.connect('faculty.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS faculties (
            register_number TEXT PRIMARY KEY,
            name TEXT,
            ph_no TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()  # Initialize the database on startup

def extract_text_from_image(image_bytes):
    """Extracts text from an image using Gemini."""
    img = Image.open(io.BytesIO(image_bytes))
    response = model.generate_content(img)
    return response.text

def send_sms(phone_number, message):
    """Sends an SMS message."""
    try:
        message = twilio_client.messages.create(
            body=message,
            from_=twilio_phone_number,
            to=phone_number
        )
        print(f"SMS sent to {phone_number}: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        image_data = request.files["image"].read()

        extracted_text = extract_text_from_image(image_data)
        print("Extracted Text:", extracted_text)

        # Basic parsing (improve this with more robust regex or NLP)
        name = "Unknown"
        register_number = "Unknown"
        if "Name :" in extracted_text:
            name = extracted_text.split("Name :")[1].split("\n")[0].strip()
        if "Register No .:" in extracted_text:
            register_number = extracted_text.split("Register No .:")[1].split("\n")[0].strip()

        # Database interaction
        conn = get_db_connection()
        faculty = conn.execute('SELECT * FROM faculties WHERE register_number = ?', (register_number,)).fetchone()

        if faculty:
            phone_number = faculty['ph_no']
        else:
            phone_number = request.form.get("contactNumber")  # Get from user if not in DB
            if phone_number:
                conn.execute('INSERT INTO faculties (register_number, name, ph_no) VALUES (?, ?, ?)', (register_number, name, phone_number))
                conn.commit()
            else:
                conn.close()
                return jsonify({"error": "Phone number required for new faculty."}), 400

        conn.close()

        sign_in_time = datetime.now()
        sign_out_time = sign_in_time + timedelta(minutes=5)

        sign_in_message = f"You have signed in at {sign_in_time.strftime('%Y-%m-%d %H:%M:%S')}. You can leave at {sign_out_time.strftime('%Y-%m-%d %H:%M:%S')}."
        send_sms(phone_number, sign_in_message)

        # Schedule sign-out message (for testing, using time.sleep)
        while datetime.now() < sign_out_time:
            time.sleep(1)

        sign_out_message = f"Your shift ends now {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."
        send_sms(phone_number, sign_out_message)

        return jsonify({"name": name, "register_number": register_number, "sign_in_time": sign_in_time.strftime("%Y-%m-%d %H:%M:%S")})

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)