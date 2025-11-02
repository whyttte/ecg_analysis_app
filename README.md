# ECG Analysis Web Application

This is a Flask-based web application for analyzing ECG (electrocardiogram) data. The app allows users to upload ECG data in various formats (CSV, TXT, XLS, XLSX), visualize the signal, and get a basic analysis, including heart rate calculation.

## Features

-   Upload ECG data in CSV, TXT, or Excel formats.
-   Interactive visualization of the ECG signal with marked R-peaks.
-   Calculation of average heart rate.
-   Log and view activities with timestamps.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python3 run.py
    ```

    The application will be available at `http://127.0.0.1:5000`.

## Usage

1.  Navigate to the homepage and click "Upload ECG Data".
2.  Choose a file to upload and set the sampling rate.
3.  The app will display the ECG signal with detected R-peaks and the calculated heart rate.
4.  Use the "Activity Log" to record activities and their timestamps.
