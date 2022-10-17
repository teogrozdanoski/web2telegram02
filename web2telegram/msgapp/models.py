from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class TelegramBot(models.Model):
    bot_name = models.CharField(max_length=60, unique=True)
    api_key = models.CharField(max_length=60, unique=True)
    bot_hdlr_cmd = models.CharField(max_length=60)
    # changes
    sent_via_bot = models.BigIntegerField(default=0)

    def __str__(self):
        return self.bot_name
    
    def get_absolute_url(self):
        return reverse('detail_t_bot', kwargs={'pk':self.pk})

class Recipient(models.Model):
    telegram_id = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('detail_recipient', kwargs={'pk':self.pk})

class TelegramMsg(models.Model):
    message_id = models.CharField(max_length=20, default='', unique=True)
    telegram_bot_id = models.ForeignKey(TelegramBot, related_name='message', on_delete=models.CASCADE)
    recipient_id = models.ForeignKey(Recipient,  related_name='message', on_delete=models.CASCADE)
    msg_text = models.TextField()
    is_reply = models.BooleanField(default=True)
    send_date = models.DateTimeField(default=timezone.now)
    # delivery_date = models.DateTimeField()
    # read_date = models.DateTimeField()

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # define additional fields
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)

    def __str__(self):
        return self.user.username

