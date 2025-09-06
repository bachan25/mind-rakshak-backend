
# MindRakshak Backend Service

This is the **backend service** for **MindRakshak – Guardian of Mental Wellbeing**, built with **FastAPI + SQLite3 + LangGraph**.
It powers the student dashboard, wellness scheduler, Google Calendar integration, and AI assistant features.

## Team

#### Team Name: MindRakshak

<b>Member 1:</b> Bachan Nayak <b>[Team Lead]</b>

## Hackathon Theme / Challenge

- <b>Theme 1: </b> Secure API integration with Descope Outbound Apps

- <b>Use Case Addressed:</b> Mental Health Scheduler – promoting balance between study and wellbeing.

## What We Built

- Authentication via Descope Outbound Apps (no hardcoded tokens).

- Manage student schedules & sync with Google Calendar.

- Wellness breaks auto-scheduled into calendar.

- Agent API endpoints for answering queries (class timings, breaks, reminders).

- Email reminders (via Google Gmail).

- SQLite3 + SQLAlchemy ORM for persistence.

- The <b>Architecture </b>
<img width="1968" height="924" alt="image" src="https://github.com/user-attachments/assets/3daf5357-e7d3-427b-9d35-f319ea6a9b8f" />

## How to Run
1. **Backend (FastAPI) + Agent**
- Clone repository
```
  #!/bin/bash
git clone https://github.com/bachan25/mind-rakshak-backend.git
cd mind-rakshak-backend
```
- create virtual envirnoment and activate it
```
venv -m venv
.\venv\Scripts\activate
```
- Install dependency
```
pip install -r .\requirements.txt
```
- Create Database
```
python .\init_db.py
```
- update the below API key in .env file
  ```
  TAVILY_API_KEY= <YOUR_TAVILY_API_KEY>
  OPENAI_API_KEY= <YOUR_OPENAI_API_KEY>
  ```
- Run Application
```
python run.py
```

2. **Frontend (Angular 18+)**
   - Please visit the repository [MindRakshak Web](https://github.com/bachan25/mind-rakshak-web.git)

## Tech Stack
- **Framework**: FastAPI (Python 3.10+)

- **Database**: SQLite3 + SQLAlchemy

- **Authentication**: Descope Outbound Apps

- **External API**: Google Calendar, Gmail API

- **Agent**: LangGraph

## 🎥 Demo Video

👉 [Watch Demo](https://youtu.be/nput9WaXqI0)

## API Endpoints



## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# 🧑‍💻 Built With ❤️ for the [Global MCP Hackathon 2025](https://www.hackerearth.com/challenges/hackathon/mcp-hackathon/)

