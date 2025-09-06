# Example Run Flow

app.py runs Streamlit.

User logs in via Descope → auth/descope_auth.py.

Dashboard loads from ui/dashboard.py.

Events fetched via services/calendar_service.py.

If missing → ask for timetable → parse in timetable_service.py.

User clicks “Add Wellness Break” → handled in wellness_service.py.

Notifications scheduled → notify_service.py.

Agent chat handled in agent_ui.py + agent_service.py.

# Tech Stack (Finalized)

Frontend/UI: Streamlit (simple and hackathon-friendly).

Auth: Descope (login/signup, outbound apps for Google + Twilio).

Agent Bot: LangChain (or simple rules if time is short).

Database: SQLite3 (lightweight, no setup).

Notifications: Twilio (SMS/call), SMTP (email).

Calendar Data: Google Calendar API via Descope Outbound App.