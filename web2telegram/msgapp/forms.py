from django import forms
from msgapp.models import TelegramMsg, TelegramBot, Recipient, UserProfileInfo
from django.contrib.auth.models import User

# Insert forms here
class TelegramMsgModelForm(forms.ModelForm):
    telegram_bot_id = forms.ModelChoiceField(queryset=TelegramBot.objects.all(), initial=0, widget=forms.Select(attrs={'class': 'form-control'}))
    recipient_id = forms.ModelChoiceField(queryset=Recipient.objects.all(), initial=0, widget=forms.Select(attrs={'class': 'form-control'}))
    msg_text = forms.Textarea()
    # is_reply = forms.BooleanField()

    class Meta():
        model = TelegramMsg
        fields = ["telegram_bot_id", "recipient_id", "msg_text"]

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
    
class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_picture',)

class TelegramBotModelForm(forms.ModelForm):
    bot_name = forms.CharField()
    api_key = forms.CharField()

    class Meta():
        model = TelegramBot
        fields = ['bot_name', 'api_key']

class RecipientModelForm(forms.ModelForm):
    telegram_id = forms.CharField()
    username = forms.CharField()

    class Meta():
        model = Recipient
        fields = ['telegram_id', 'username']