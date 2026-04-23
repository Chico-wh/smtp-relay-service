import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .config import settings
from .schemas import EmailPayload

logger = logging.getLogger(__name__)


def send_email(payload: EmailPayload) -> None:
    """
    Envia um email via SMTP Hostinger.
    Lança exceção em caso de falha — quem chama decide o que fazer.
    """
    msg = MIMEMultipart("alternative")
    msg["Subject"] = payload.subject
    msg["From"]    = f"{settings.smtp_from_name} <{settings.smtp_from}>"
    msg["To"]      = payload.to

    if payload.reply_to:
        msg["Reply-To"] = payload.reply_to

    # Plaintext fallback
    plain = payload.text or _html_to_plain(payload.html)
    msg.attach(MIMEText(plain, "plain", "utf-8"))
    msg.attach(MIMEText(payload.html, "html", "utf-8"))

    logger.info("Enviando email para %s | assunto: %s", payload.to, payload.subject)

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=15) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(settings.smtp_user, settings.smtp_pass)
        server.sendmail(settings.smtp_from, payload.to, msg.as_string())

    logger.info("Email entregue para %s", payload.to)


def _html_to_plain(html: str) -> str:
    """Remove tags HTML de forma simples para gerar plaintext."""
    import re
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    return text