# Invoice Matching System

## Overview

This project is a web-based prototype system for matching incoming invoices to existing ones based on content and structure similarity. The system extracts text from PDF invoices, extracts relevant features, and calculates similarity to find the most similar invoice in the database.

## How to Run

### Backend (Flask)

1. Navigate to the `backend` directory:
   ```sh
   cd server
   ```
2. Install the required Python libraries:
   ```sh
   pip install Flask Flask-Cors PyPDF2 scikit-learn numpy
   ```
3. Start the Flask server:
   ```sh
   python app.py
   ```

### Frontend (React)

1. Navigate to the `frontend` directory:
   ```sh
   cd client
   ```
2. Install the required npm packages:
   ```sh
   npm install
   ```
3. Start the React development server:
   ```sh
   npm run dev
   ```

## Usage

1. Open the React app in your browser.
2. Upload a PDF invoice using the form.
3. The system will display the most similar invoice from the database along with the similarity score.
