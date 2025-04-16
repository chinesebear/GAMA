from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('ask/', views.ask_question, name='ask_question'),
    path('clear_memory/', views.clear_memory, name='clear_memory'),
    path('get_answer/', views.get_answer, name='get_answer'),
    path('register/', views.register, name='register'),  # 添加注册视图的 URL
    path('ask_difficult_question/', views.ask_difficult_question, name='ask_difficult_question'),
]
