# historical_chat/urls.py

from django.contrib import admin
from django.urls import path, include
from chat import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls', namespace='chat')),  # 包含 chat 应用的 URL
    path('accounts/', include('django.contrib.auth.urls')),   # 添加认证 URL
path('', views.index, name='home'),  # 为空路径设置视图
]
