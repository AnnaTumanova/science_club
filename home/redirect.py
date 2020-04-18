from django.http import HttpResponseRedirect


def get_home_redirect_response():
    return HttpResponseRedirect('/')
