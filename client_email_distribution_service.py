import grpc

from proto import email_distribution_service_pb2_grpc, email_distribution_service_pb2


def client_send_mail(template_name: str, recipients: list[str], variables: dict[str, str]) -> None:
    try:
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = email_distribution_service_pb2_grpc.EmailDistributionStub(channel)
            response = stub.SendMail(
                email_distribution_service_pb2.SendMailRequest(
                    template_name=template_name,
                    recipients=recipients,
                    variables=variables
                )
            )
            print("Ответ от сервера:\n" + str(response.results))
    except grpc.RpcError as e:
        print(f"gRPC ошибка: {e.code()} - {e.details()}")
        return None

def client_get_stats(email_recipient: str):
    try:
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = email_distribution_service_pb2_grpc.EmailDistributionStub(channel)
            response = stub.GetStatsByEmail(
                email_distribution_service_pb2.GetStatsByEmailRequest(
                    email=email_recipient
                )
            )
            print("Ответ от сервера:\n" + str(response))
    except grpc.RpcError as e:
        print(f"gRPC ошибка: {e.code()} - {e.details()}")
        return None


if __name__ == "__main__":
    # укажите свои разные почтовые ящики
    email_recipient1 = ''
    email_recipient2 = ''
    email_recipient3 = ''
    email_recipient4 = ''
    
    separator = "-----------------------------------------------------"
    print(f"{separator}\nОтсутствующий шаблон")
    client_send_mail("unavailable_template", [email_recipient1], {})
    print(f"{separator}\nОтсутствие некоторых переменных")
    client_send_mail("welcome_letter", [email_recipient1], {})
    print(f"{separator}\nРассылка на несколько ящиков")
    client_send_mail("reset_password",
                     [email_recipient1, email_recipient3],
                     {
                         "user_name": "Nikita",
                         "reset_link": "https://i.pinimg.com/736x/f1/32/f0/f132f0ce56a26e59589c6fdb5f573987.jpg",
                         "expires_in": "1"
                     })
    print(f"{separator}\nПовторная отправка письма, но с добавлением нового ящика")
    client_send_mail("reset_password",
                     [email_recipient1, email_recipient3, email_recipient2],
                     {
                         "user_name": "Nikita",
                         "reset_link": "https://i.pinimg.com/736x/f1/32/f0/f132f0ce56a26e59589c6fdb5f573987.jpg",
                         "expires_in": "1"
                     })
    print(f"{separator}\nПовторная отправка письма, но с другими переменными")
    client_send_mail("reset_password",
                     [email_recipient1, email_recipient3],
                     {
                         "user_name": "Ne Nikita",
                         "reset_link": "https://i.pinimg.com/736x/f1/32/f0/f132f0ce56a26e59589c6fdb5f573987.jpg",
                         "expires_in": "1"
                     })
    print(f"{separator}\nПолучение статистики по ящику")
    client_get_stats(email_recipient1)
    print(f"{separator}\nПолучение статистики по ящику на который ничего не отправлялось")
    client_get_stats("nik_babin2@inbox.ru")