from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Count

from emails.custom_errors import InvalidRequestError
from emails.mail_services.utils.render_mails import render_html_template
from emails.mail_services.utils.send_mails import send_emails
from emails.models import MailTemplates, SentMails
from proto.email_distribution_service_pb2 import RecipientSendStatus, SendStatus, TemplateCount


class MailService:
    """
    Сервис для отправки писем по шаблонам и получения статистики отправки.

    Методы:
        send_mails(recipients, template_name, variables) -> list[RecipientSendStatus]
            Отправляет письма на указанные email адреса с использованием шаблона
            и подстановкой переменных. Валидирует email и обязательные параметры шаблона.
            Не отправляет письмо, если ранее отправлялось такое же, проверяет по шаблону и переменным.

        get_stats(recipient_email) -> tuple[int, list[TemplateCount]]
            Возвращает статистику отправленных писем для указанного email.
            Возвращает общее количество отправленных писем и разбивку по шаблонам.
    """
    @staticmethod
    def send_mails(recipients: list[str],
                   template_name: str,
                   variables: dict[str, str]) -> list[RecipientSendStatus] | InvalidRequestError:
        """
        Отправляет письма на указанные email адреса.

        Не отправляет письмо, если ранее отправлялось такое же, проверяет по шаблону и переменным.

        Args:
            recipients (list[str]): Список email адресов получателей.
            template_name (str): Название шаблона письма.
            variables (dict[str, str]): Словарь переменных для подстановки в шаблон.

        Raises:
            InvalidRequestError: Если шаблон не найден или отсутствуют обязательные переменные.

        Returns:
            list[RecipientSendStatus]: Список статусов отправки для каждого получателя.
        """
        template_obj = MailTemplates.objects.filter(name=template_name).first()
        if not template_obj:
            raise InvalidRequestError(f"Template '{template_name}' not found.")

        for msg_param in template_obj.params.all():
            if not variables.get(msg_param.name) and msg_param.is_required:
                raise InvalidRequestError(f"Variable '{msg_param.name}' is required.")

        unique_recipients = set(recipients)
        invalid_recipients = set()
        for recipient_email in unique_recipients:
            try:
                validate_email(recipient_email)
            except ValidationError:
                invalid_recipients.add(recipient_email)

        hashed_params = SentMails.template_params_to_hash(variables)
        already_sent_to_emails = set(template_obj.sent_mails.filter(
            recipient_email__in=unique_recipients,
            template_params_hash=hashed_params
        ).values_list("recipient_email", flat=True))

        mail_msg_with_context = render_html_template(template_obj.html_body_template, variables)
        sent_emails = send_emails(unique_recipients - already_sent_to_emails,
                                  template_obj.subject, mail_msg_with_context)
        sent_emails_objs = []
        mail_status_list: list[RecipientSendStatus] = []
        for recipient in recipients:
            if recipient in already_sent_to_emails:
                status = SendStatus.SKIPPED_DUPLICATE
            elif recipient in sent_emails:
                sent_status = sent_emails[recipient]
                if sent_status:
                    status = SendStatus.SUCCESS
                    sent_emails_objs.append(SentMails(
                        recipient_email=recipient,
                        template=template_obj,
                        template_params_hash=hashed_params,
                    ))
                else:
                    status = SendStatus.FAILED
            elif recipient in invalid_recipients:
                status = SendStatus.FAILED
            else:
                status = SendStatus.UNSPECIFIED

            mail_status_list.append(RecipientSendStatus(email=recipient, status=status))

        SentMails.objects.bulk_create(sent_emails_objs, batch_size=1000)
        return mail_status_list

    @staticmethod
    def get_stats(recipient_email: str) -> tuple[int, list[TemplateCount]]:
        """
        Получает статистику отправленных писем для указанного email.

        Args:
            recipient_email (str): Email получателя.

        Returns:
            tuple[int, list[TemplateCount]]:
                - Общее количество отправленных писем.
                - Список TemplateCount с количеством писем по каждому шаблону.
        """
        all_mails_qs = SentMails.objects.filter(recipient_email=recipient_email)
        count_mails_by_template_qs = all_mails_qs.values('template__name').annotate(count=Count('id'))
        count_mails_by_template = []
        for stat_by_template_dict in count_mails_by_template_qs:
            count_mails_by_template.append(
                TemplateCount(
                    template_name=stat_by_template_dict['template__name'],
                    count=stat_by_template_dict['count']
                )
            )
        return all_mails_qs.count(), count_mails_by_template