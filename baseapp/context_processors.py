
from django.conf import settings

def constant_context(request):
    return {'app_role': settings.CRED[0]}