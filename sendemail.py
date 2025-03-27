import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "dm5022001@gmail.com"
EMAIL_PASSWORD = "yzvg ouep dkzx mgeb"  # Лучше использовать OAuth или .env

# TODO: cvxl slil vqis bckp
# TODO: gvgp oudp rhkc acde

# TODO: yzvg ouep dkzx mgeb


def send_email(receiver_email, subject, message):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Использование
send_email("edmondaghajanayan@gmail.com", "Привет!", "Как Ваше ничего?.")
