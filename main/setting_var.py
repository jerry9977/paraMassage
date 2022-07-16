from django.conf import settings

#add to TEMPLATE_CONTEXT_PROCESSORS
def setting_var(request):
    return {
        "DEBUG": settings.DEBUG
    }
