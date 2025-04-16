# chat/urls.py

from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),                            # 聊天首页
    path('ask/', views.ask_question, name='ask'),                  # 处理提问
    path('register/', views.register, name='register'),            # 用户注册
    path('clear_memory/', views.clear_memory, name='clear_memory'),# 清除记忆
]
