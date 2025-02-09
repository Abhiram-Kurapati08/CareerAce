
# CareerAce

**CareerAce** is an AI-powered career assistant that helps users get personalized career advice and guidance. It offers features like automatic resume extraction, job profile suggestions, and roadmap generation for career development.

---

## Features

- **Automatic Resume Extraction**: Upload your resume, and CareerAce extracts valuable information to recommend job profiles.
- **Career Roadmap**: Get personalized career roadmaps based on user input or a predefined set of options.
- **Interactive Chatbot**: Engage in an interactive conversation with the bot for career-related questions.

---

## Setup Instructions

### Prerequisites

Make sure you have the following tools installed:

- **Node.js** (for React front-end)
- **npm** (Node Package Manager, for React dependencies)
- **Python 3.x** (for the backend server)
- **virtualenv** (for Python virtual environments)

---

### Backend Setup (Python)

1. **Create a Python Virtual Environment**:

   Navigate to the backend directory and create a virtual environment:

   ```bash
   python -m venv venv
   ```

2. **Activate the Virtual Environment**:

   On **Windows**:

   ```bash
   .\venv\Scripts\activate
   ```

   On **MacOS/Linux**:

   ```bash
   source venv/bin/activate
   ```

3. **Install Required Python Packages**:

   Run the following command to install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Python Server**:

   To start the Python server, run:

   ```bash
   python server.py
   ```

   This will launch the backend server on `http://127.0.0.1:5000`.

---

### Frontend Setup (React)

1. **Install Dependencies**:

   Navigate to the React frontend directory and run the following command to install all dependencies:

   ```bash
   npm install
   ```

2. **Start the React Development Server**:

   To start the React app, run:

   ```bash
   npm start
   ```

   This will launch the React application on `http://localhost:3000`.

---

---
---

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: React, JavaScript
- **GenAI**: Ollama - LLama 3.2
- **Audio**: MP3 files for user interaction
- **Styling**: CSS for UI

---

## Contributing

We welcome contributions to improve CareerAce. Feel free to fork this repository and submit pull requests for bug fixes, improvements, or new features.

---

## License

This project is open-source and available under the MIT License.

---

## Acknowledgements

- Special thanks to everyone who has contributed to the development of CareerAce!
