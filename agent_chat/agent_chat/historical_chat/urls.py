# historical_chat/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls', namespace='chat')),  # 包含 chat 应用的 URL
    path('accounts/', include('django.contrib.auth.urls')),   # 添加认证 URL
]
