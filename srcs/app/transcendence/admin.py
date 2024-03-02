from django.contrib import admin
# 👇 1. Add this line import notification model
from .models import Notification
from .models import *

# 👇 2. Add this line to add the notification
admin.site.register(Notification)
admin.site.register(CustomUser)
admin.site.register(FriendRequest)
admin.site.register(Game)
admin.site.register(Stat_Game)
admin.site.register(Lobby)
admin.site.register(Party)
admin.site.register(UserInLobby)
admin.site.register(Tournament)
admin.site.register(Stat_User_by_Game)
