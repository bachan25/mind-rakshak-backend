from langchain.tools import tool
from service import outbound_app_service

import base64
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

GMAIL_BASE_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"


@tool
def send_email(
    to: list[str],
    subject: str,
    body: str,
    cc: list[str] = None,
    bcc: list[str] = None,
    user_id: str = None,
) -> str:
    """
    Send an email using the user's Gmail account.

    Args:
        to (list[str]): Recipient email addresses.
        subject (str): Subject line of the email.
        body (str): Email body (plain text).
        cc (list[str]): CC recipients (optional).
        bcc (list[str]): BCC recipients (optional).
        user_id (str): User ID for token lookup (required).

    Returns:
        str: Success or failure message.
    """
    import base64
    import requests
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    if not user_id:
        return "❌ User ID is required to send email."

    # 1) Get OAuth access token
    response = outbound_app_service.fetch_outbound_token("gmail", user_id)
    access_token = response["token"]["accessToken"]

    # 2) Build MIME email
    msg = MIMEMultipart()
    msg["To"] = ", ".join(to)
    msg["Subject"] = subject

    if cc:
        msg["Cc"] = ", ".join(cc)
    if bcc:
        msg["Bcc"] = ", ".join(bcc)

    msg.attach(MIMEText(body, "plain"))

    # 3) Encode message in base64 (URL safe)
    raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    payload = {"raw": raw_message}

    # 4) Call Gmail API
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    resp = requests.post(GMAIL_BASE_URL, headers=headers, json=payload, timeout=20)

    try:
        data = resp.json()
    except Exception:
        data = {"raw": resp.text}

    # 5) Handle response
    if resp.ok and "id" in data:
        return f"✅ Email sent successfully to {', '.join(to)} with subject '{subject}'."
    else:
        return f"❌ Failed to send email. HTTP {resp.status_code}. Details: {data}"
