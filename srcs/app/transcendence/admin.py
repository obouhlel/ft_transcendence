from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(FriendRequest)
admin.site.register(Game)
admin.site.register(Stat_Game)
admin.site.register(Lobby)
admin.site.register(Party)
admin.site.register(UserInLobby)
admin.site.register(Tournament)
admin.site.register(Stat_User_by_Game)
