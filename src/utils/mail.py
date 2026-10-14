from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi import FastAPI
from pydantic import EmailStr, BaseModel
from html import escape
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class EmailSchema(BaseModel):
    email: List[EmailStr]

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", "587")),
    MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
    MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME", "Your Name"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def send_email(name: str, emails: List[str]):
    safe_name = escape(name)

    html = f"""
    <html>
        <body style="margin:0; padding:24px;
                     font-family:Arial,sans-serif;
                     color:#333333; line-height:1.6;">

            <h2 style="color:#2563eb;">Welcome aboard, {safe_name}!</h2>

            <p>Hi {safe_name},</p>

            <p>
                Thank you for registering with our
                <strong>Task Management App</strong>.
                We're excited to have you with us!
            </p>

            <p>
                Your registration has been received successfully.
                You can now get started on organizing your tasks,
                tracking your progress, and staying productive.
            </p>

            <p>
                If you need any assistance, our team will be happy
                to help.
            </p>

            <p>
                Welcome to the community, and happy task managing!
            </p>

            <p>
                Best regards,<br>
                <strong>Abhijeet Raj</strong><br>
                Task Management Team
            </p>
        </body>
    </html>
    """

    message = MessageSchema(
        subject="Welcome to Task Management App!",
        recipients=emails,
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    print("Registration email sent successfully.")
