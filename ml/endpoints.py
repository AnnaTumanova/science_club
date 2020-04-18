from django.contrib import messages
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework.views import APIView

from home.redirect import get_home_redirect_response
from home.signup import account_activation_token


class ActivateAPIView(APIView):
    def get(self, request, uidb64, token, format=None):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            permission = Permission.objects.get(codename='access_admin')
        except(TypeError, ValueError, OverflowError, User.DoesNotExist, Permission.DoesNotExist):
            user = None
            permission = None

        if user is not None and user.is_active is False and permission is not None \
                and account_activation_token.check_token(user, token):
            user.user_permissions.add(permission)
            user.is_active = True
            user.save()

            messages.success(request, 'Thank you for your email confirmation. Now you can log in to your account.')
        else:
            messages.error(request, 'Activation link is invalid or expired!')

        return get_home_redirect_response()
