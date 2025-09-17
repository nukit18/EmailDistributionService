from django.core.management.base import BaseCommand
from django.utils import timezone

from emails.models import MailTemplates, MailTemplatesParams

class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **kwargs):
        welcome_template, _ = MailTemplates.objects.get_or_create(
            name="welcome_letter",
            defaults={
                "subject": "Здравствуйте!",
                "html_body_template": (
                    "<p>Здравствуйте, {{ user_name }}. Спасибо, что присоединились к {{ project_name }}.</p>"
                    "<p>Рады видеть вас — загляните в личный кабинет, чтобы начать.</p>"
                ),
                "created_at": timezone.now()
            }
        )

        MailTemplatesParams.objects.get_or_create(template=welcome_template, name="user_name")
        MailTemplatesParams.objects.get_or_create(template=welcome_template, name="project_name")

        reset_template, _ = MailTemplates.objects.get_or_create(
            name="reset_password",
            defaults={
                "subject": "Сброс пароля",
                "html_body_template": (
                    '<p>Привет, {{ user_name }}. Для восстановления пароля перейдите по ссылке: '
                    '<a href="{{ reset_link }}">{{ reset_link }}</a>.</p>'
                    '<p>Ссылка действительна {{ expires_in }} часов — если не вы запрашивали, просто проигнорируйте это письмо.</p>'
                ),
                "created_at": timezone.now()
            }
        )

        MailTemplatesParams.objects.get_or_create(template=reset_template, name="user_name")
        MailTemplatesParams.objects.get_or_create(template=reset_template, name="reset_link")
        MailTemplatesParams.objects.get_or_create(template=reset_template, name="expires_in")

        order_template, _ = MailTemplates.objects.get_or_create(
            name="order_confirmation",
            defaults={
                "subject": "Данные по вашему заказу",
                "html_body_template": (
                    "<p>Здравствуйте, {{ user_name }}. Мы получили ваш заказ №{{ order_id }} и скоро начнём его обработку.</p>"
                    "<p>Спасибо, что выбрали {{ store_name }} — мы свяжемся с вами, как только заказ будет отправлен.</p>"
                ),
                "created_at": timezone.now()
            }
        )

        MailTemplatesParams.objects.get_or_create(template=order_template, name="user_name")
        MailTemplatesParams.objects.get_or_create(template=order_template, name="order_id")
        MailTemplatesParams.objects.get_or_create(template=order_template, name="store_name")