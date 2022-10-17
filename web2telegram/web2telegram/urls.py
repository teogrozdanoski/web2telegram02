"""web2telegram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from msgapp import views
from django.conf import settings

app_name = 'msgapp'

urlpatterns = [
    # now cbv class for index
    # path('', views.index, name='index'),
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.user_register, name='user_register'),
    path('send/', views.send, name='send'),
    # path('view_msgs/', views.view_msgs, name='view_msgs'),
    path('view_msgs/', views.MessageListView.as_view(), name='view_msgs'),
    path('view_t_bots/', views.TelegramBotListView.as_view(), name='view_t_bots'),
    path('view_recipients/', views.RecipientListView.as_view(), name='view_recipients'),
    # path('add_t_bot/', views.add_t_bot, name='add_t_bot'),
    path('add_t_bot/', views.TelegramBotCreateView.as_view(), name='add_t_bot'),
    path('add_t_recipient/', views.RecipientCreateView.as_view(), name='add_t_recipient'),
    # path('add_t_recipient/', views.add_t_recipient, name='add_t_recipient'),
    path('update_t_bot/<int:pk>/', views.TelegramBotUpdateView.as_view(), name='update_t_bot'),
    path('update_recipient/<int:pk>/', views.RecipientUpdateView.as_view(), name='update_recipient'),
    path('delete_t_bot/<int:pk>/', views.TelegramBotDeleteView.as_view(), name='delete_t_bot'),
    path('delete_recipient/<int:pk>/', views.RecipientDeleteView.as_view(), name='delete_recipient'),
    path('view_msgs/<int:pk>/', views.MessageDetailView.as_view(), name='detail_msg'),
    path('view_t_bots/<int:pk>/', views.TelegramBotDetailView.as_view(), name='detail_t_bot'),
    path('view_recipients/<int:pk>/', views.RecipientDetailView.as_view(), name='detail_recipient'),
    path('admin/', admin.site.urls),
]

if(settings.DEBUG):
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
