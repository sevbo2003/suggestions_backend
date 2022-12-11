from django.conf import settings

from .loader import get_revison


def site(request):
    return {'SITE_URL': settings.SITE_URL}


def application_info(request):
    """
    Context processor to return application informations
    """

    return {
        'APP_NAME': settings.APP_NAME,
        'APP_VERSION': f'v{settings.APP_VERSION}',
        'APP_DESCRIPTION': settings.APP_DESCRIPTION,
        'APP_SOURCE_REVISION': get_revison(),
    }
