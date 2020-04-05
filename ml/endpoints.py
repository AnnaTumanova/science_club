from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework.views import APIView
from rest_framework.response import Response

from home.tokens import account_activation_token


class ActivateAPIView(APIView):
    def get(self, request, uidb64, token, format=None):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and user.is_active is False and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return Response('Thank you for your email confirmation. Now you can log in to your account.')
        else:
            return Response('Activation link is invalid or expired!')
