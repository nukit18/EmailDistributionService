import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.core.mail import EmailMessage, get_connection

from core import settings

logger = logging.getLogger(__name__)


def send_single_email(recipient, subject, body) -> tuple[str, bool]:
    """Отправка письма ОДНОМУ получателю"""
    # еще можно добавить сохранение письма в отправленные, но нужно для конкретного почтового сервиса настраивать
    try:
        with get_connection() as connection:
            email = EmailMessage(subject, body, to=[recipient], connection=connection)
            email.content_subtype = "html"
            return recipient, bool(email.send(fail_silently=True))
    except Exception as e:
        logger.error(e)
        return recipient, False

def send_emails(recipients, subject, body) -> dict[str, bool]:
    """Отправка письма нескольким получателям.

    Отправка идет в несколько потоков.
    """
    # в дальнейшем лучше на celery перенести
    results = {}
    with ThreadPoolExecutor(max_workers=settings.SEND_MAIL_MAX_THREADS) as executor:
        futures = [executor.submit(send_single_email, r, subject, body)
                   for r in recipients]
        for future in as_completed(futures):
            recipient, status = future.result()
            results[recipient] = status
    return results
