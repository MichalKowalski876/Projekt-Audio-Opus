import os
import smtplib
import json
import logging
from pathlib import Path
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Databases.email_log import log_send

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_DIR = Path(__file__).parent.resolve()
DB_DIR = BASE_DIR / "Databases"
SMTP_CONFIG_FILE = DB_DIR / "smtp_config.json"
MSG_CONFIG_FILE = DB_DIR / "msg_config.json"


def load_json_config(file_path: Path, default_data: dict) -> dict:
    if file_path.exists():
        try:
            with file_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logging.error(f"Plik {file_path.name} jest uszkodzony (błąd JSON): {e}")
        except Exception as e:
            logging.error(f"Nieoczekiwany błąd ładowania pliku {file_path.name}: {e}")

    return default_data


def send_report_email(receiver_email: str, attachment_path: str | Path) -> bool:
    attachment_path = Path(attachment_path)

    smtp_defaults = {
        "SMTP_SERVER": "smtp.gmail.com",
        "SMTP_PORT": 465,
        "SENDER_EMAIL": "",
        "SENDER_PASSWORD": ""
    }

    msg_defaults = {
        "EMAIL_SUBJECT": "Zbiorczy raport rozliczeniowy Audio Opus",
        "EMAIL_BODY": "Dzień dobry,\n\nW załączniku znajduje się aktualny raport rozliczeniowy wygenerowany przez system Audio Opus."
    }

    smtp_config = load_json_config(SMTP_CONFIG_FILE, smtp_defaults)
    msg_config = load_json_config(MSG_CONFIG_FILE, msg_defaults)

    server_host = smtp_config.get("SMTP_SERVER", "smtp.gmail.com")
    try:
        server_port = int(smtp_config.get("SMTP_PORT", 465))
    except ValueError:
        server_port = 465

    sender_email = os.getenv("SMTP_EMAIL") or smtp_config.get("SENDER_EMAIL")
    sender_password = os.getenv("SMTP_PASSWORD") or smtp_config.get("SENDER_PASSWORD")

    email_subject = msg_config.get("EMAIL_SUBJECT", msg_defaults["EMAIL_SUBJECT"])
    email_body_raw = msg_config.get("EMAIL_BODY", msg_defaults["EMAIL_BODY"])

    if not sender_email or not sender_password:
        logging.error("Brak danych logowania nadawcy! Ustaw e-mail i hasło w środowisku lub configu.")
        log_send(receiver_email, attachment_path.name, "error", "Brak danych logowania nadawcy")
        return False

    if not attachment_path.exists():
        logging.error(f"Plik załącznika {attachment_path} nie istnieje!")
        log_send(receiver_email, attachment_path.name, "error", "Plik załącznika nie istnieje")
        return False

    msg = MIMEMultipart("mixed")
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = email_subject

    body_part = MIMEMultipart("alternative")

    part_text = MIMEText(email_body_raw, "plain", "utf-8")

    formatted_body = email_body_raw.replace('\n', '<br>')
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; font-size: 14px;">
            {formatted_body}
        </body>
    </html>
    """
    part_html = MIMEText(html_content, "html", "utf-8")

    body_part.attach(part_text)
    body_part.attach(part_html)
    msg.attach(body_part)

    try:
        with attachment_path.open("rb") as f:
            attachment = MIMEApplication(f.read(), _subtype="octet-stream")
            attachment.add_header("Content-Disposition", "attachment", filename=attachment_path.name)
            msg.attach(attachment)
    except Exception as e:
        logging.error(f"Błąd podczas pakowania załącznika: {e}")
        log_send(receiver_email, attachment_path.name, "error", f"Błąd pakowania załącznika: {e}")
        return False

    try:
        logging.info(f"Łączenie z serwerem SMTP ({server_host}:{server_port})...")
        with smtplib.SMTP_SSL(server_host, server_port) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)

        logging.info(f"E-mail został pomyślnie wysłany na {receiver_email}.")
        log_send(receiver_email, attachment_path.name, "success")
        return True

    except smtplib.SMTPAuthenticationError:
        logging.error(
            "Błąd uwierzytelniania: nieprawidłowy e-mail lub hasło. Sprawdź, czy nie potrzebujesz 'Hasła aplikacji' (App Password).")
        log_send(receiver_email, attachment_path.name, "error", "Błąd uwierzytelniania SMTP")
        return False
    except Exception as e:
        logging.error(f"Błąd połączenia / wysyłania e-maila: {e}")
        log_send(receiver_email, attachment_path.name, "error", str(e))
        return False


# TEST KONTROLNY
# if __name__ == "__main__":
#     logging.info("START TESTU KONTROLNEGO")

#     test_file_path = Path("raport_kontrolny.txt")
#     test_file_path.write_text("Test zawartości raportu", encoding="utf-8")

#     MAIL_ODBIORCY = "test@example.com"

#     try:
#         sukces = send_report_email(
#             receiver_email=MAIL_ODBIORCY,
#             attachment_path=test_file_path
#         )
#         if sukces:
#             logging.info("Test kontrolny zakończony sukcesem.")
#         else:
#             logging.warning("Test kontrolny nie powiódł się.")
#     finally:
#         if test_file_path.exists():
#             test_file_path.unlink()
#             logging.info(f"Usunięto plik testowy: {test_file_path.name}")
