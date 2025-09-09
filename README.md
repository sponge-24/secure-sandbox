# Secure Sandbox

Secure Sandbox is a web-based platform for safely running and testing code snippets in an isolated environment. It consists of a React frontend and a FastAPI backend, with code execution handled in Docker containers for security.

## Features

- **Online Code Editor**: Write and edit Python code in the browser using Monaco Editor.
- **Safe Execution**: Code runs in a Docker container with resource limits and no network access.
- **Real-time Output**: View execution results instantly in the output panel.
- **Job Queue**: Backend uses Redis to queue and manage code execution jobs.

## Project Structure

- `frontend/`: React app with Monaco Editor, Tailwind CSS, and Axios for API calls.
- `backend/`: FastAPI server with endpoints for submitting code, checking status, and fetching results. Includes a worker that executes code in Docker containers.

## Technologies Used

- **Frontend**: React, Vite, Monaco Editor, Tailwind CSS, Axios
- **Backend**: FastAPI, Redis, Docker (Python 3.11 image)

## Setup Instructions

### Prerequisites

- uv
- Docker
- Python 3.12+
- Redis server

### Backend Setup

1. Install dependencies:
	```bash
	cd backend
	uv sync
	```
2. Start Redis server (if not running):
	```bash
	redis-server
	```
3. Start the FastAPI server:
	```bash
	uv run main.py
	```
4. Start the worker:
	```bash
	uv run worker.py
	```

### Frontend Setup

1. Install dependencies:
	```bash
	cd frontend
	npm install
	```
2. Start the development server:
	```bash
	npm run dev
	```
3. Open [http://localhost:5173](http://localhost:5173) in your browser.

## Usage

1. Write Python code in the editor panel.
2. Click "Run Code" to execute. The backend queues the job and runs it in a Docker container.
3. View the output in the output panel.

## Security

- Code runs in a restricted Docker container (no network, limited memory/CPU).
- Only Python is supported for now.
