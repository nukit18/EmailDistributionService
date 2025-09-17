import hashlib
import json

from django.db import models
from django.utils import timezone


class MailTemplates(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True, null=False, blank=False)
    subject = models.CharField(max_length=100, null=False, blank=False)
    html_body_template = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'mail_templates'


class MailTemplatesParams(models.Model):
    template = models.ForeignKey(MailTemplates, null=False, on_delete=models.CASCADE, related_name='params')
    name = models.CharField(max_length=100, db_index=True, null=False, blank=False)
    is_required = models.BooleanField(default=True, null=False)

    class Meta:
        db_table = 'mail_templates_params'
        unique_together = ('template', 'name')


class SentMails(models.Model):
    recipient_email = models.CharField(max_length=200, null=False, blank=False, db_index=True)
    template = models.ForeignKey(MailTemplates, on_delete=models.CASCADE, related_name='sent_mails', null=False)
    template_params_hash = models.CharField(max_length=64,
                                            help_text="SHA-256 хэш параметров письма для проверки дубликатов")
    sent_at = models.DateTimeField(default=timezone.now, null=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'sent_mails'
        unique_together = ('recipient_email', 'template', 'template_params_hash')

    @staticmethod
    def template_params_to_hash(params: dict) -> str:
        """
        Вычисляет SHA-256 хэш от словаря параметров письма.
        """
        json_str = json.dumps(params, sort_keys=True)
        return hashlib.sha256(json_str.encode('utf-8')).hexdigest()