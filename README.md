# World Cup Prediction App

A Streamlit-based web application designed to manage, predict, and track results for the World Cup 2026. The project features a main dashboard for users and an administrative panel for real-time score updates and leaderboard calculations.

## Getting Started

Follow these steps to set up the project locally on your machine.

### 1. Environment Setup

It is highly recommended to use a virtual environment to manage dependencies cleanly.

#### Create a virtual environment named '.venv'
```bash
python -m venv .venv
```
#### For macOS / Linux:
#### Activate the virtual environment
```bash
source .venv/bin/activate
```
#### For Windows:
#### Activate the virtual environment
```bash
.venv\Scripts\activate
```
#### Install required dependencies
```bash
pip install -r requirements.txt
```
### 2. Main Application Setup
#### Configuring Google Sheets Backend

### 3. Running Main Application
```bash
streamlit run Overview.py
```

### 4. Running Admin Application
#### Navigate to the admin subdirectory
```bash
cd admin
```
#### Launch the admin control panel
```bash
streamlit run admin_app.py
```