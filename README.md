# Shift Reminder System

This project is a minimalist web application designed to help my faculty members in the Computer Science department of SRM College of Engineering and Technology manage their work shifts. It provides a simple interface to scan faculty ID cards, record sign-in times, and send reminders when their shift is over.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [SMS Reminders](#sms-reminders)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **ID Card Scanning:** Uses the device's camera to capture an image of the faculty ID card.
- **Text Extraction:** Employs Google's Gemini (formerly Bard) API to extract text from the scanned ID card, specifically the faculty's name and register number.
- **Sign-In Time Recording:** Records the time when the ID card is scanned.
- **Database Storage:** Stores faculty information (name, register number, and phone number) in an SQLite database.
- **SMS Reminders:** Sends SMS reminders to faculty members when their shift is over, using Twilio API.
- **Phone Number Input:** If a faculty member is not found in the database, the system prompts for their phone number.
- **Time-Based Reminders:** For testing purposes, reminders are sent 5 minutes after sign-in. In a production environment, this would be extended to 8 hours.

## Installation

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/tejeshwarv16/Shift-Reminder-System
    cd faculty-shift-reminder
    ```

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows
    ```

3.  **Install Dependencies:**

    ```bash
    pip install Flask google-generativeai python-dotenv opencv-python Pillow twilio
    ```

## Usage

1.  **Configure Environment Variables:**

    * Create a `.env` file in the project root directory.
    * Add your API keys and Twilio credentials to the `.env` file:

        ```
        GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
        TWILIO_ACCOUNT_SID=YOUR_TWILIO_ACCOUNT_SID
        TWILIO_AUTH_TOKEN=YOUR_TWILIO_AUTH_TOKEN
        TWILIO_PHONE_NUMBER=YOUR_TWILIO_PHONE_NUMBER
        ```

2.  **Run the Flask Application:**

    ```bash
    python app.py
    ```

3.  **Open in Browser:**

    * Open your web browser and navigate to `http://127.0.0.1:5000/`.

4.  **Use the Application:**

    * Click the "Capture ID Card" button.
    * Allow the browser to access your camera.
    * Hold the faculty ID card in front of the camera.
    * If the faculty is new, enter their phone number.
    * The system will extract the name and register number, store the information, and send an SMS reminder.
    * After 5 minutes (for testing), another SMS will be sent.

## Configuration

* **API Keys:** Ensure your Google Gemini API key and Twilio API keys are correctly set in the `.env` file.
* **Reminder Time:** The reminder time is currently set to 5 minutes for testing. Modify the `sign_out_time` calculation in `app.py` for production use.

## Database Setup

* The application uses SQLite, which creates a file named `faculty.db` in the project directory.
* The database schema includes a table named `faculties` with columns:
    * `register_number` (PRIMARY KEY)
    * `name`
    * `ph_no`

## SMS Reminders

* SMS reminders are sent using the Twilio API.
* Ensure that your Twilio account is configured to send SMS messages.
* For WhatsApp integration, configure your Twilio account for WhatsApp and use the `whatsapp:` prefix in the phone numbers.

## Dependencies

* **Flask:** Web framework.
* **google-generativeai:** Google Gemini API client.
* **python-dotenv:** Loads environment variables from a `.env` file.
* **opencv-python:** Image processing.
* **Pillow:** Image processing.
* **Twilio:** SMS messaging.
* **SQLite3:** Database.

## Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them.
4.  Push your changes to your fork.
5.  Submit a pull request.

## Contact

For any questions or issues, please contact mailto:tejeshwarv16@gmail.com
