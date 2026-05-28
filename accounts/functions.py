from typing import Union

from django.contrib import messages


def send_sms(request, message: str, receptor: str = None) -> Union[dict, None]:
    messages.info(request=request, message=message)
    # return {"message": message, "receptor": receptor}

    # get kavenegar api key and uncomment this codes
    # api = kavenegar.KavenegarAPI(settings.KAVENEGAR_API_KEY)
    # params = {
    #     "sender": settings.KAVENEGAR_SENDER,
    #     "receptor": receptor,
    #     "message": message,
    # }
    # response = api.sms_send(params)
    # return response
