Step 1

# Shangri-La Petition Platform (SLPP)

## Description

This project is a Flask-based web application for managing petitions in the Valley of Shangri-La. It includes features for petitioners to create, view, and sign petitions and for a committee to manage petitions and set thresholds for parliamentary discussions. Additionally, it provides a REST API for accessing petition data.

---

## Prerequisites
- Python (3.7 or higher)
- pip (Python package installer)

---

## Installation and Setup

### Step 1: Install Python and pip
1. Download and install Python from the [official website](https://www.python.org/downloads/).
2. Verify installation by running the following commands in your terminal or command prompt:
   ```bash
   python --version
   pip --version


Step 2: Install Dependencies
Open your terminal or command prompt and navigate to the project directory.
Install the required dependencies by running:
bash
Copy code
pip install -r requirements.txt

Step 3: Run the Application
1.python app.py

2.The server will start running, and you will see output indicating the app is running on http://127.0.0.1:5000.

Step 4: Access the Application
Open your web browser.
Navigate to:
http://127.0.0.1:5000

You can interact with the application through the web interface.


REST API Usage
Endpoints
1. Fetch All Petitions
Endpoint: /slpp/petitions
Method: GET
Example
curl http://127.0.0.1:5000/slpp/petitions


Testing the Application
You can use tools like Postman or curl to test the REST API.

Fetch All Petitions:

Open Postman.
Create a new GET request.
Enter the URL: http://127.0.0.1:5000/slpp/petitions.
Click Send and verify the JSON response.
Fetch Open Petitions:

Create another GET request.
Enter the URL: http://127.0.0.1:5000/slpp/petitions?status=open.
Click Send and verify the JSON response.
Notes
Ensure the database is initialized with valid BioIDs and petitions.
For any issues or questions, refer to the application logs in the terminal.
Authors
Apurva Kulkarni