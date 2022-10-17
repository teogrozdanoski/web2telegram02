from django.contrib import admin
from msgapp.models import TelegramBot, Recipient, TelegramMsg, UserProfileInfo

# Register your models here.
admin.site.register(TelegramBot)
admin.site.register(Recipient)
admin.site.register(TelegramMsg)
admin.site.register(UserProfileInfo)