from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from pathlib import Path
from typing import Any

import aiosmtplib
from jinja2 import Template

from app.core.config import settings


class EmailService:
    @classmethod
    async def send_email(cls,
                         email_to: str,
                         subject_template: str = "",
                         html_template: str = "",
                         environment: dict[str, Any] = {},
                         ) -> None:
        assert settings.EMAILS_ENABLED, "no provided configuration for email variables"

        smtp = aiosmtplib.SMTP(hostname=settings.SMTP_HOST, port=settings.SMTP_PORT, use_tls=True)
        html = Template(html_template)
        content = html.render(**environment)

        message = MIMEMultipart()
        message['From'] = settings.EMAILS_FROM_NAME
        message['To'] = email_to
        message['Subject'] = subject_template
        message['Date'] = formatdate(localtime=True)
        message.attach(MIMEText(content, "html"))
        body = message.as_string()
        #message.attach(MIMEText(body, "plain"))
        await smtp.connect()
        await smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        respone = await smtp.sendmail(settings.EMAILS_FROM_EMAIL, email_to, body)
        await smtp.quit()

    @classmethod
    async def send_verify_email_code(cls, email_to: str, code: str) -> None:
        project_name = settings.PROJECT_NAME
        subject = f"Подтверждение Email для регистрации на university-helper"
        with open(Path(settings.EMAIL_TEMPLATES_DIR) / "verify_email_code.html") as f:
            template_str = f.read()
        await cls.send_email(
            email_to=email_to,
            subject_template=subject,
            html_template=template_str,
            environment={"code": code},
        )

    @classmethod
    async def send_notification_about_test(cls, email_to: str, test_uuid: str, test_title: str, test_external_id: int):
        """Оповещение об завершении формировании теста"""
        subject = f"Ответы на тест получены"
        with open(Path(settings.EMAIL_TEMPLATES_DIR) / "finish_test.html") as f:
            template_str = f.read()
        await cls.send_email(
            email_to=email_to,
            subject_template=subject,
            html_template=template_str,
            environment={
                'test_uuid': test_uuid,
                'test_title': test_title,
                'test_id': test_external_id,
                'test_url': settings.SERVER_HOST,
            }
        )

    @classmethod
    async def send_notification_about_error_test(cls, email_to: str,
                                                 test_external_id: int):
        """Оповещение об завершении формировании теста"""
        subject = f"Ошибка при получении ответов на тест"
        with open(Path(settings.EMAIL_TEMPLATES_DIR) / "error_test.html") as f:
            template_str = f.read()
        await cls.send_email(
            email_to=email_to,
            subject_template=subject,
            html_template=template_str,
            environment={
                'test_id': test_external_id,
                'test_url': settings.SERVER_HOST,
            }
        )
