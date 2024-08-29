import datetime
from random import randint

from django.core.cache import cache
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class OTP:

    def __init__(self):
        self.otp_expiry_minutes = 1

    def generate_otp(self, email):
        otp = randint(1000, 9999)
        cache.set(email, (otp, datetime.datetime.now()), self.otp_expiry_minutes * 60)
        self.send_otp(otp, email)

        return otp

    def verify_otp(self, otp, email):
        stored_otp_info = cache.get(email)
        if stored_otp_info is None:
            return False
        stored_otp, timestamp = stored_otp_info
        if stored_otp == int(otp):
            if datetime.datetime.now() - timestamp > datetime.timedelta(minutes=self.otp_expiry_minutes):
                self.clear_otp(email)
                return False
            else:
                self.clear_otp(email)
                return True
        else:
            return False

    def clear_otp(self, email):
        cache.delete(email)

    def send_otp(self, otp, email):
        mail_subject = 'فعال سازی اکانت'
        message = render_to_string('accounts/active_email.html', {
            'user': email,
            'code': otp,
        })
        to_email = email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )

        email.send()