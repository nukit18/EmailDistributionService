import logging

from grpc import ServicerContext, StatusCode

from emails.custom_errors import InvalidRequestError
from emails.mail_services.mail_service import MailService
from proto import email_distribution_service_pb2, email_distribution_service_pb2_grpc

logger = logging.getLogger(__name__)


class EmailDistributionHandler(email_distribution_service_pb2_grpc.EmailDistributionServicer):
    def SendMail(self,
                 request: email_distribution_service_pb2.SendMailRequest,
                 context: ServicerContext):
        try:
            results = MailService.send_mails(list(request.recipients),
                                             request.template_name,
                                             dict(request.variables))
            return email_distribution_service_pb2.SendMailResponse(results=results)

        except InvalidRequestError as e:
            context.abort(StatusCode.INVALID_ARGUMENT, str(e))
        except Exception as e:
            logger.error("Произошла ошибка при отправке письма", exc_info=True)
            context.abort(StatusCode.INTERNAL, "internal server error")

    def GetStatsByEmail(self,
                 request: email_distribution_service_pb2.GetStatsByEmailRequest,
                 context: ServicerContext):
         try:
            total_sent, stats_by_template = MailService.get_stats(request.email)
            return email_distribution_service_pb2.GetStatsByEmailResponse(
                total_sent=total_sent, by_template=stats_by_template)
         except Exception as e:
             logger.error("Произошла ошибка при получении статистики", exc_info=True)
             context.abort(StatusCode.INTERNAL, "internal server error")