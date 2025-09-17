from concurrent import futures
import time
import logging

import grpc
from django.core.management.base import BaseCommand

from emails.handlers import EmailDistributionHandler
from proto import email_distribution_service_pb2_grpc


class Command(BaseCommand):
    help = "Запускает gRPC сервер"

    def add_arguments(self, parser):
        parser.add_argument(
            "--port", type=int, default=50051,
            help="Порт, на котором запускается gRPC сервер"
        )
        parser.add_argument(
            "--workers", type=int, default=10,
            help="Количество потоков"
        )

    def handle(self, *args, **options):
        port = options["port"]
        workers = options["workers"]

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=workers))
        email_distribution_service_pb2_grpc.add_EmailDistributionServicer_to_server(EmailDistributionHandler(), server)
        server.add_insecure_port(f"[::]:{port}")
        server.start()
        self.stdout.write(self.style.SUCCESS(f"gRPC server started, listening on {port}"))
        try:
            server.wait_for_termination()
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS("gRPC server stopped"))
