from django.shortcuts import render, redirect
from msgapp.models import TelegramMsg, TelegramBot, Recipient, UserProfileInfo
from msgapp.forms import RecipientModelForm, TelegramBotModelForm, TelegramMsgModelForm, UserForm, UserProfileInfoForm
import telebot
import uuid
import plotly.express as px

# login, register, logout logic imports
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here.

# index view
class IndexView(TemplateView):
    template_name = 'msgapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bots_msg_count = {}
        bots = TelegramBot.objects.all()
        for b in bots:
            bots_msg_count[b.bot_name] = b.sent_via_bot

        fig = px.bar(
            x=[bot for bot in bots_msg_count],
            y=[bots_msg_count[bot] for bot in bots_msg_count],
        ).update_layout(
            xaxis_title="Telegram bot", yaxis_title="Total messages sent"
        )

        chart = fig.to_html()

        context['chart'] = chart

        return context


# OLD FUNCTION BASED VIEW
# def index(request):
#     bots_msg_count = {}
#     bots = TelegramBot.objects.all()
#     for b in bots:
#         bots_msg_count[b.bot_name] = b.sent_via_bot

#     fig = px.bar(
#         x=[bot for bot in bots_msg_count],
#         y=[bots_msg_count[bot] for bot in bots_msg_count],
#     ).update_layout(
#         xaxis_title="Telegram bot", yaxis_title="Total messages sent"
#     )

#     chart = fig.to_html()

#     content = {'chart': chart}

#     return render(request, "msgapp/index.html", context=content)
# END OF OLD FUNCTION VIEW

class MessageListView(LoginRequiredMixin, ListView):
    # paginate_by = 10
    context_object_name = 'short_messages'
    model = TelegramMsg
    def get_context_data(self, **kwargs):
        all_messages = TelegramMsg.objects.prefetch_related('telegram_bot_id').all()
        short_messages = all_messages
        for smsg in short_messages:
            if (len(smsg.msg_text) > 100):
                smsg.msg_text = smsg.msg_text[:97] + '...'

        context = {'messages': all_messages, 'short_messages': short_messages}

        return context

class TelegramBotListView(LoginRequiredMixin, ListView):
    # paginate_by = 10
    context_object_name = 'telegram_bots'
    model = TelegramBot
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class RecipientListView(LoginRequiredMixin, ListView):
    # paginate_by = 10
    context_object_name = 'recipients'
    model = Recipient
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class MessageDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'detail_messages'
    model = TelegramMsg
    template_name = 'msgapp/telegrammsg_detail.html'

class TelegramBotDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'detail_telegram_bot'
    model = TelegramBot
    template_name = 'msgapp/telegrambot_detail.html'

class RecipientDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'detail_recipient'
    model = Recipient
    template_name = 'msgapp/recipient_detail.html'

# OLD MESSAGE VIEWS
# @login_required
# def view_msgs(request):
#     all_messages = TelegramMsg.objects.prefetch_related('telegram_bot_id').all()
#     short_messages = all_messages
#     for smsg in short_messages:
#         if (len(smsg.msg_text) > 100):
#             smsg.msg_text = smsg.msg_text[:97] + '...'

#     content = {'messages': all_messages, 'short_messages': short_messages}
#     return render(request, "msgapp/view_messages.html", context=content)

class TelegramBotCreateView(LoginRequiredMixin, CreateView):
    fields = ('bot_name', 'api_key')
    model = TelegramBot


# OLD BOT CREATE
# @login_required
# def add_t_bot(request):
#     form = TelegramBotModelForm()

#     if(request.method == "POST"):
#         form = TelegramBotModelForm(request.POST)
#         if(form.is_valid()):
#             form.save(commit=True)
            
#             return redirect('index')
#         else:
#             print("New Telegram bot form invalid")
    
#     content = {'form': form}
#     return render(request, "msgapp/add_telegram_bot.html", context=content)

class RecipientCreateView(LoginRequiredMixin, CreateView):
    fields = ('telegram_id', 'username')
    model = Recipient

# OLD RECIPIENT CREATE
# @login_required
# def add_t_recipient(request):
#     form = RecipientModelForm()

#     if(request.method == "POST"):
#         form = RecipientModelForm(request.POST)
#         if(form.is_valid()):
#             form.save(commit=True)
            
#             return redirect('index')
#         else:
#             print("New Telegram recipient form invalid")
    
#     content = {'form': form}
#     return render(request, "msgapp/add_telegram_bot.html", context=content)

class TelegramBotUpdateView(UpdateView):
    fields = ('bot_name', 'api_key')
    model = TelegramBot

class RecipientUpdateView(UpdateView):
    fields = ('telegram_id', 'username')
    model = Recipient

class TelegramBotDeleteView(DeleteView):
    model = TelegramBot
    success_url = reverse_lazy('view_t_bots')

class RecipientDeleteView(DeleteView):
    model = Recipient
    success_url = reverse_lazy('view_recipients')

@login_required
def send(request):
    form = TelegramMsgModelForm()

    if (request.method == "POST"):
        form = TelegramMsgModelForm(request.POST)
        if (form.is_valid()):
            # update message count for bots
            bot_used = TelegramBot.objects.get(
                pk=request.POST["telegram_bot_id"])
            bot_used.sent_via_bot += 1
            bot_used.save()

            # generate a random id for client messages
            generated_msg_id = uuid.uuid1()

            # extra step to insert generated_msg_id
            tmp_msg = form.save(commit=False)
            tmp_msg.message_id = generated_msg_id

            # commit to database
            tmp_msg.save()

            # send to Telegram user logic
            # initialie a Telegram  bot
            telegram_bot = telebot.TeleBot(TelegramBot.objects.get(
                pk=request.POST["telegram_bot_id"]).api_key)
            telegram_bot.config['api_key'] = TelegramBot.objects.get(
                pk=request.POST["telegram_bot_id"]).api_key
            # send the message
            telegram_bot.send_message(Recipient.objects.get(
                pk=request.POST["recipient_id"]).telegram_id, request.POST["msg_text"])

            # redirect to home page after completion
            return redirect('index')

        else:
            print("ERROR, FORM INVALID!")

    content = {'form': form}
    return render(request, "msgapp/send_message.html", context=content)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):
    if request.method == 'POST':
        curr_username = request.POST.get('username')
        curr_password = request.POST.get('password')

        user = authenticate(username=curr_username, password=curr_password)

        if(user):
            if(user.is_active):
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account is not active")
        else:
            print("someone tried to login and failed: ", curr_username, " and password: ", curr_password)
    
    else:
        return render(request, 'msgapp/login.html', {})

def user_register(request):
    registered = False
    if(request.method == 'POST'):
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if(user_form.is_valid() and profile_form.is_valid()):
        # if(user_form.is_valid()):
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # extra user profile details, not needed now
            profile = profile_form.save(commit=False)
            profile.user = user

            if('profile_picture' in request.FILES):
                profile.profile_picture = request.FILES['profile_picture']
            
            profile.save()
            registered = True
        
        else:
            print(user_form.errors, profile_form.errors)
    
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    
    return render(request, 'msgapp/registration.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
