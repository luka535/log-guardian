# Project LogGuardian 🛡️

**LogGuardian is an asynchronous backend service designed to automate the analysis of security log files. It serves as a robust, scalable pipeline for ingesting log data, processing it for suspicious activity, and storing the results for review. This project was built to demonstrate a deep understanding of modern Python backend architecture and professional software development practices.**

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

### ✨ Core Features

*   **Asynchronous Processing:** Utilizes Celery and Redis to handle time-consuming file analysis in the background, ensuring the API remains fast and responsive.
*   **API-Driven:** A modern FastAPI interface provides a clean, documented, and validated entrypoint for submitting analysis jobs.
*   **Scalable Parsing:** The log file parser is designed for memory efficiency, reading files line-by-line to handle large inputs without crashing.
*   **Robust & Resilient:** The Celery task includes automatic retries with backoff for transient failures, ensuring jobs are processed reliably.
*   **Professionally Tested:** The core business logic is validated with a comprehensive suite of unit tests using `pytest`.
*   **Structured, Production-Ready Logging:** All diagnostic output is in JSON format for easy parsing by log aggregation systems.

### 🛠️ Tech Stack

| Component         | Technology                               |
| ----------------- | ---------------------------------------- |
| **Backend**       | Python, FastAPI                          |
| **Database**      | PostgreSQL, SQLAlchemy (ORM)             |
| **Task Queue**    | Celery, Redis                            |
| **Testing**       | Pytest                                   |
| **Configuration** | Pydantic Settings                        |
| **Logging**       | `python-json-logger`                     |

---

### 🏛️ Architecture Overview

The system follows a modern, decoupled client-server architecture, ideal for scalable and resilient task processing.

```mermaid
flowchart TD
    A[Client] -- HTTP POST Request --> B{FastAPI API};
    B -- Creates Report (Status: PENDING) --> C[(PostgreSQL DB)];
    B -- Dispatches Task --> D((Redis Broker));
    E[Celery Worker] -- Fetches Task --> D;
    E -- Updates Status (PROCESSING) --> C;
    E -- Parses File & Runs Analysis --> E;
    E -- Saves Results & Updates Status (COMPLETED/FAILED) --> C;
```

**Workflow:**
1.  A client submits a log file path to the FastAPI `/api/reports` endpoint.
2.  The API creates an `AnalysisReport` record in PostgreSQL with a `PENDING` status.
3.  A task is immediately dispatched to the Redis message broker. The API returns a `202Accepted` response to the client.
4.  A Celery worker, running as a separate process, picks up the task from Redis.
5.  The worker updates the report status to `PROCESSING`, performs the full analysis, and finally updates the report to `COMPLETED` with the results or `FAILED` if an error occurred.

---

### 🚀 Getting Started

#### Prerequisites

*   Python 3.10+
*   PostgreSQL Server
*   Redis Server

#### 1. Clone the Repository

```bash
git clone https://github.com/luka535/log-guardian.git
cd log-guardian
```

#### 2. Set Up Environment

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Configure Environment Variables

Create a `.env` file in the project root. Use the `env.example` as a template.

```
# .env
DATABASE_URL="postgresql+psycopg2://log_guardian_user:your_password@localhost/log_guardian_db"
CELERY_BROKER_URL="redis://localhost:6379/0"
CELERY_RESULT_BACKEND="redis://localhost:6379/0"
```

#### 4. Run the Services

You will need four separate terminals for this:

**Terminal 1: Run PostgreSQL & Redis (if not running as background services)**

**Terminal 2: Run the Celery Worker**
```bash
celery -A log_guardian.celery_worker.celery_app worker --loglevel=info --pool=gevent
```

**Terminal 3: Run the FastAPI Server**
```bash
uvicorn log_guardian.main:app --reload
```

#### 5. Interact with the API

Open your browser to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to access the interactive Swagger UI and submit analysis jobs.

---

### ✅ Running the Tests

To ensure code quality and correctness, the project includes a suite of unit tests. To run them:

```bash
pytest
```