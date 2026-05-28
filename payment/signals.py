import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from pathlib import Path

from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.dispatch import Signal, receiver

from accounts.functions import send_sms

# import ghasedakpack

# ==========================================
# تعریف سیگنال‌ها
# ==========================================
order_paid = Signal()  # سیگنال برای زمانی که پرداخت سفارش موفقیت‌آمیز است
return_requested = Signal()  # سیگنال برای زمانی که کاربر درخواست مرجوعی ثبت می‌کند


# ==========================================
# توابع کمکی
# ==========================================
def get_client_ip(request):
    """
    Extract client IP address from request considering various headers.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR", "0.0.0.0")
    return ip


def send_mail(
    send_from,
    send_to,
    subject,
    message,
    files=[],
    server="smtp.gmail.com",
    port=587,
    username="",
    password="",
    use_tls=True,
):
    """Compose and send email with provided info and attachments."""
    msg = MIMEMultipart()
    msg["From"] = send_from
    msg["To"] = COMMASPACE.join(send_to)
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = subject
    msg.attach(MIMEText(message))

    for path in files:
        part = MIMEBase("application", "octet-stream")
        with open(path, "rb") as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", f"attachment; filename={Path(path).name}"
        )
        msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()


# ==========================================
# گیرنده‌های سیگنال (Receivers)
# ==========================================


@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    if not user or not request:
        return
    email = user.email
    if not email:
        return
    try:
        ip = get_client_ip(request)
    except Exception:
        ip = "Unknown"

    subject = "ورود به سایت"
    message = f"ورود جدید از آی‌پی {ip} به سایت شما"

    try:
        send_mail(
            send_from="Laptop Store shop",
            send_to=[email],
            subject=subject,
            message=message,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
        )
        print("Login email sent!")
    except Exception as e:
        print(f"something went wrong about login email: {e}")


@receiver(order_paid)
def handle_order_paid(request, *args, **kwargs):
    order = kwargs["order"]
    receiver_email = kwargs.get("email")

    # استخراج مقادیر با استفاده از روابط مدل
    first_name = order.user.first_name if order.user else "کاربر"
    last_name = order.user.last_name if order.user else "گرامی"
    tracking_code = getattr(order, "tracking_code", "نامشخص")
    phone_number = str(order.user.phone_number)

    message = f"{first_name} {last_name} عزیز! سفارش شما با موفقیت ثبت شد. کد پیگیری: {tracking_code}"
    response = send_sms(request, message=message, receptor=phone_number)
    print(response)

    # ارسال پیامک (در صورت نیاز کامنت‌ها را بردارید)
    # if phone_number:
    #     sms = ghasedakpack.Ghasedak(settings.GHASEDAK_API_KEY)
    #     try:
    #         sms.send({'message': message, 'receptor': phone_number, 'linenumber': settings.MY_LINE_NUMBER_ON_GHASEDAK_1})
    #         print('sms sent by line 1!')
    #     except:
    #         try:
    #             sms.send({'message': message, 'receptor': phone_number, 'linenumber': settings.MY_LINE_NUMBER_ON_GHASEDAK_2})
    #             print('sms sent by line 2!')
    #         except Exception as e:
    #             print(f'something went wrong about sms: {e}')

    # ارسال ایمیل
    if receiver_email:
        try:
            send_mail(
                send_from="Laptop Store shop",
                send_to=[receiver_email],
                subject="سفارش موفق",
                message=message,
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
            )
            print("Order paid email sent!")
        except Exception as e:
            print(f"something went wrong about order paid email: {e}")


@receiver(return_requested)
def handle_return_requested(request, *args, **kwargs):
    order = kwargs["order"]
    receiver_email = kwargs.get("email")

    first_name = order.user.first_name if order.user else "کاربر"
    last_name = order.user.last_name if order.user else "گرامی"
    tracking_code = getattr(order, "tracking_code", "نامشخص")
    phone_number = str(order.user.phone_number)

    message = f"{first_name} {last_name} عزیز! درخواست مرجوعی شما برای سفارش به شماره پیگیری {tracking_code} با موفقیت در سیستم ثبت شد و در حال بررسی است."
    response = send_sms(request, message=message, receptor=phone_number)
    print(response)
    # ارسال پیامک مرجوعی
    # if phone_number:
    #     sms = ghasedakpack.Ghasedak(settings.GHASEDAK_API_KEY)
    #     try:
    #         sms.send({'message': message, 'receptor': phone_number, 'linenumber': settings.MY_LINE_NUMBER_ON_GHASEDAK_1})
    #         print('Return request sms sent by line 1!')
    #     except:
    #         pass

    # ارسال ایمیل مرجوعی
    if receiver_email:
        try:
            send_mail(
                send_from="Laptop Store shop",
                send_to=[receiver_email],
                subject="ثبت درخواست مرجوعی",
                message=message,
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
            )
            print("Return requested email sent!")
        except Exception as e:
            print(f"something went wrong about return requested email: {e}")
