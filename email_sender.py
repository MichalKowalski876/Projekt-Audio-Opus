import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_report_email(receiver_email, attachment_path):
    SMTP_SERVER = "smtp.gmail.com"  #<---- przykladowo gmail
    SMTP_PORT = 465 

    SENDER_EMAIL = "audioopus@gmail.com"  #<----- przykładowy adres email, pozniej zostanie zmieniony 
    SENDER_PASSWORD = "          " #<----- haslo do aplikacji, pozniej zostanie dodane

    if not os.path.exists(attachment_path):
        print(f"Błąd: Plik {attachment_path} nie istnieje!")
        return False

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = "Zbiorczy raport rozliczeniowy Audio Opus"

    body = """
    <html>
        <body>
            <p>Dzień dobry,</p>
            <p>W załączniku znajduje się aktualny raport rozliczeniowy wygenerowany przez system <b>Audio Opus</b>.</p>
        </body>
    </html>
    """
    msg.attach(MIMEText(body, "html"))

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