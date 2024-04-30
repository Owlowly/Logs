from .models import Message

def unread_messages_count(request):
    if request.user.is_authenticated:
        unread_count = Message.objects.filter(recipient=request.user, read=False).count()
    else:
        unread_count = 0
    return {'unread_count': unread_count}
