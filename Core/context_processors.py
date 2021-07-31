from Chat.models import Message
from Auth.models import LastSeen
from Branches.models import Branch
from datetime import timedelta


def allcontext(request):
    # Return offline user
    def off_users():
        offline_user = LastSeen.get_user_offline(timedelta(seconds=180)).exclude(
            user__id=request.user.id)  # to exclude instanc user
        return offline_user

    # Return online user
    def on_users():
        online_user = LastSeen.get_user_active(timedelta(seconds=180)).exclude(
            user__id=request.user.id)  # to exclude instanc user
        return online_user

    def All_branches():
        queryset = Branch.objects.all()
        return queryset

    def all_message():
        all = Message.objects.filter(receiver__id=request.user.id).order_by('-timestamp')[:1]
        return all

    return {
        'off': off_users(),
        'on': on_users(),
        'all_branches': All_branches(),
        # 'message' : read_message() ,
        'all': all_message(),
        'count': Message.objects.filter(is_read=False, receiver__id=request.user.id).count()
    }
