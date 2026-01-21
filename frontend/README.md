# AI Mental Health Chatbot

This project consists of a FastAPI backend and a React + Vite frontend.

## Prerequisites

- [Node.js](https://nodejs.org/) (v16 or higher)
- [Python](https://www.python.org/) (v3.8 or higher)

## Getting Started

### 1. Backend Setup

The backend is built with FastAPI and handles the chatbot logic, authentication, and analysis.

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```

2.  Create and activate a virtual environment (optional but recommended):
    ```bash
    # Windows
    python -m venv .venv
    .venv\Scripts\activate

    # macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Set up environment variables:
    - Create a `.env` file in the `backend` directory (copy from `.env.example` if available).
    - Add your API keys (e.g., Gemini API key, Secret keys).

5.  Run the backend server:
    ```bash
    uvicorn app.main:app --reload
    ```
    The server will start at `http://127.0.0.1:8000`. API docs are available at `http://127.0.0.1:8000/docs`.

### 2. Frontend Setup

The frontend is a React application powered by Vite.

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```

2.  Install dependencies:
    ```bash
    npm install
    ```

3.  Run the development server:
    ```bash
    npm run dev
    ```
    The application will be accessible at `http://localhost:5173`.

## Features

- **Chat Interface**: Interact with the AI mental health companion.
- **Emotion Analysis**: Real-time face emotion detection.
- **Analytics**: View mental health metrics and chat history.
