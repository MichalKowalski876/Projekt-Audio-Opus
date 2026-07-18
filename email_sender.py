import os
import smtplib
import json
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_CONFIG_FILE = "smtp_config.json"
MSG_CONFIG_FILE = "msg_config.json"


def load_smtp_config():
    if os.path.exists(SMTP_CONFIG_FILE):
        try:
            with open(SMTP_CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Błąd ładowania konfiguracji SMTP: {e}")

    return {
        "SMTP_SERVER": "smtp.gmail.com",
        "SMTP_PORT": 465,
        "SENDER_EMAIL": "",
        "SENDER_PASSWORD": ""
    }

def load_msg_config():
    if os.path.exists(MSG_CONFIG_FILE):
        try:
            with open(MSG_CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Błąd ładowania konfiguracji wiadomości: {e}")

    return {
        "EMAIL_SUBJECT": "Zbiorczy raport rozliczeniowy Audio Opus",
        "EMAIL_BODY": "Dzień dobry,\n\nW załączniku znajduje się aktualny raport rozliczeniowy wygenerowany przez system Audio Opus."
    }


def send_report_email(receiver_email, attachment_path):
    smtp_config = load_smtp_config()
    msg_config = load_msg_config()

    SMTP_SERVER = smtp_config.get("SMTP_SERVER", "smtp.gmail.com")

    try:
        SMTP_PORT = int(smtp_config.get("SMTP_PORT", 465))
    except ValueError:
        SMTP_PORT = 465

    SENDER_EMAIL = smtp_config.get("SENDER_EMAIL", "")
    SENDER_PASSWORD = smtp_config.get("SENDER_PASSWORD", "")

    EMAIL_SUBJECT = msg_config.get("EMAIL_SUBJECT", "Zbiorczy raport rozliczeniowy Audio Opus")
    EMAIL_BODY_RAW = msg_config.get("EMAIL_BODY", "Dzień dobry,\n\nW załączniku znajduje się raport.")

    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("Błąd: Skonfiguruj e-mail i hasło nadawcy w ustawieniach aplikacji!")
        return False

    if not os.path.exists(attachment_path):
        print(f"Błąd: Plik {attachment_path} nie istnieje!")
        return False

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = EMAIL_SUBJECT

    formatted_body = EMAIL_BODY_RAW.replace('\n', '<br>')

    body_html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; font-size: 14px;">
            {formatted_body}
        </body>
    </html>
    """
    msg.attach(MIMEText(body_html, "html"))

    file_name = os.path.basename(attachment_path)

    try:
        with open(attachment_path, "rb") as f:
            attachment = MIMEApplication(f.read(), _subtype="octet-stream")
            attachment.add_header(
                "Content-Disposition", "attachment", filename=file_name
            )
            msg.attach(attachment)
    except Exception as e:
        print(f"Błąd podczas pakowania załącznika: {e}")
        return False

    try:
        print(f"Łączenie z serwerem SMTP ({SMTP_SERVER})...")
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        print("E-mail został wysłany pomyślnie na skrzynkę odbiorcy.")
        return True
    except Exception as e:
        print(f"Błąd podczas wysyłania maila: {e}")
        return False
"""

if __name__ == "__main__":
    print("TEST KONTROLNY")

    test_file = "raport_kontrolny.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("test")

    MAIL_ODBIORCY = "          "

    sukces = send_report_email(
        receiver_email=MAIL_ODBIORCY,
        attachment_path=test_file
    )

    if sukces:
        print("email został pomyślnie wysłany na skrzynkę testową.")
    else:
        print("test kontrolny nie powiódł się.")

        
"""
