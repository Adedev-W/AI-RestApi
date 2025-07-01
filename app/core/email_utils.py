import aiosmtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USER)

def email_verification_template(user_email: str, code: str):
    subject = "Verify Your Account Email"
    body = f"""
Hello {user_email},

Thank you for registering with our service.

To verify your email address, please enter the following code on the verification page:

Verification Code: {code}

If you did not initiate this registration, please ignore this email.

Best regards,
Support Team
"""
    return subject, body

def password_reset_template(user_email: str, token: str):
    subject = "Password Reset Request"
    body = f"""
Hello {user_email},

We received a request to reset the password for your account.

Please use the following token to reset your password:
{token}

If you did not request a password reset, please ignore this email.

Best regards,
Support Team
"""
    return subject, body

def registration_success_template(user_email: str):
    subject = "Registration Successful"
    body = f"""
Hello {user_email},

Congratulations! Your account has been successfully registered.

You can now log in using this email address. If you need any assistance, feel free to reply to this email.

Best regards,
Support Team
"""
    return subject, body

def general_notification_template(user_email: str, message: str):
    subject = "Notification from Our Service"
    body = f"""
Hello {user_email},

{message}

Best regards,
Support Team
"""
    return subject, body

def admin_register_template(user_email: str, api_key: str, code: str):
    subject = "Welcome to Our Service - Your Account Details"
    body = f"""
Hello {user_email},

Your account has been successfully created by the administrator.

Here is your API KEY:

{api_key}

Please keep this key safe. You can use it to access our API.

Verification Code: {code}

If you did not request this account, please ignore this email.

Best regards,
Support Team
"""
    return subject, body

async def send_verification_email(to_email: str, subject: str, body: str):
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASS, EMAIL_FROM]):
        raise ValueError("SMTP config is incomplete. Please check your .env file.")

    message = EmailMessage()
    message["From"] = EMAIL_FROM
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    # Choose TLS/STARTTLS mode based on port
    use_tls = SMTP_PORT == 465
    start_tls = SMTP_PORT in [587, 2525]

    try:
    await aiosmtplib.send(
        message,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        username=SMTP_USER,
        password=SMTP_PASS,
            use_tls=use_tls,
            start_tls=start_tls,
    ) 
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise 