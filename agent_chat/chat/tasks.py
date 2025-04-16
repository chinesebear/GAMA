from celery import shared_task
from .utils import ChatService
import asyncio

@shared_task
def get_ai_response_task(messages):
    chat_service = ChatService()
    return asyncio.run(chat_service.get_response(messages))
