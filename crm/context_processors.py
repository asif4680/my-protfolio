from core import models as m


def sidebar_counts(request):
    if not (request.user.is_authenticated and request.user.is_staff):
        return {}
    return {"dash_unread": m.ContactMessage.objects.filter(is_read=False).count()}
