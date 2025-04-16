# chat/views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import HistoricalFigure, Conversation, Message
from django.utils import timezone
import bleach
from asgiref.sync import sync_to_async

from src.Agents.API_info import ChatActionRunner

import logging

# 配置日志记录器
logger = logging.getLogger('chat')

# 实例化 ChatActionRunner
runner = ChatActionRunner()

def register(request):
    """
    处理用户注册
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 注册后自动登录
            logger.debug(f"新用户注册并登录: {user.username}")
            return redirect('chat:index')
    else:
        form = UserCreationForm()
    return render(request, 'chat/register.html', {'form': form})

@login_required
def index(request):
    """
    渲染聊天首页，展示前端页面
    """
    historical_figures = HistoricalFigure.objects.all()
    logger.debug(f"用户 {request.user.username} 访问聊天首页，历史人物数量: {historical_figures.count()}")
    return render(request, 'chat/index.html', {'historical_figures': historical_figures})

# chat/views.py

from django.http import JsonResponse
from asgiref.sync import sync_to_async
from .models import HistoricalFigure, Conversation, Message
import logging

# 配置日志记录器

# 实例化 ChatActionRunner
runner = ChatActionRunner()

@csrf_exempt  # 如果你处理的是 POST 请求，并且不希望 CSRF 校验阻止请求
async def handle_ask_question(request):
    """
    处理提问逻辑的辅助函数
    """
    logger.debug("开始处理提问请求")
    user_question = bleach.clean(request.POST.get('question', '').strip())
    figure_id = request.POST.get('figure_id')

    # 如果有需要同步的操作，使用 sync_to_async
    figure = await sync_to_async(HistoricalFigure.objects.get)(id=figure_id)

    # 处理提问的具体逻辑，这里假设你使用 runner 执行某些操作
    try:
        response = await runner.run(user_question, figure)  # 需要保证 ChatActionRunner 支持异步
        logger.debug(f"获取到的回答: {response}")
        return JsonResponse({'answer': response})
    except Exception as e:
        logger.error(f"处理提问时出错: {e}")
        return JsonResponse({'error': '处理提问时发生错误'}, status=500)


@csrf_exempt
@login_required
async def ask_question(request):
    if request.method == 'POST':
        try:
            # 异步获取请求数据
            data = await request.json()  # 假设请求体是 JSON 格式
        except Exception as e:
            logger.error(f"获取请求数据失败: {e}")
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        # 获取问题内容
        question = data.get('question')

        if not question:
            return JsonResponse({'error': 'Question is required'}, status=400)

        # 异步调用同步方法 runner.process_question
        response = await sync_to_async(runner.process_question)(question)

        # 返回处理结果
        return JsonResponse({'response': response})

    # 处理非POST请求
    return JsonResponse({'error': 'Invalid request method'}, status=400)
async def handle_clear_memory(request):
    """
    处理清除记忆逻辑的辅助函数
    """
    logger.debug("开始处理清除记忆请求")
    figure_id = request.POST.get('figure_id')

    logger.debug(f"清除记忆的历史人物ID: {figure_id}")

    if not figure_id:
        logger.debug("未指定历史人物")
        return JsonResponse({"error": "未指定历史人物。"}, status=400)

    try:
        historical_figure = await sync_to_async(HistoricalFigure.objects.get)(id=figure_id)
        logger.debug(f"找到历史人物: {historical_figure.name}")
    except HistoricalFigure.DoesNotExist:
        logger.debug("指定的历史人物不存在")
        return JsonResponse({"error": "指定的历史人物不存在。"}, status=400)
    except Exception as e:
        logger.error(f"获取历史人物时出错: {str(e)}")
        return JsonResponse({"error": "获取历史人物时出错。"}, status=500)

    try:
        # 删除相关的 Conversation 和 Message
        deleted, _ = await sync_to_async(Conversation.objects.filter(user=request.user, historical_figure=historical_figure).delete)()
        logger.debug(f"删除了 {deleted} 个对话记录")
    except Exception as e:
        logger.error(f"删除对话记录时出错: {str(e)}")
        return JsonResponse({"error": "无法删除对话记录。"}, status=500)

    return JsonResponse({"message": "聊天记忆已清除。", "deleted_conversations": deleted})

@csrf_exempt
@login_required
async def clear_memory(request):
    """
    处理 AJAX 清除记忆请求的视图
    """
    logger.debug("进入 clear_memory 视图函数")
    if request.method == 'POST':
        logger.debug("处理清除记忆 POST 请求")
        response = await handle_clear_memory(request)
        logger.debug("成功处理清除记忆 POST 请求")
        return response
    logger.debug("无效的请求方法")
    return JsonResponse({"error": "无效的请求方法。"}, status=400)
