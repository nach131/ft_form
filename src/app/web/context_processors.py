# web/context_processors.py

from django.conf import settings


def user_context(request):
    if request.user.is_authenticated:
        return {
            'MEDIA_URL': settings.MEDIA_URL,
        }
    return {}
