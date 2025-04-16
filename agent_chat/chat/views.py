# views.py
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import HistoricalFigure, Conversation, Message
import bleach
import logging
from .utils import ChatService
from asgiref.sync import async_to_sync

# 配置日志记录器
logger = logging.getLogger('chat')

# 实例化 ChatService
chat_service = ChatService()

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

# views.py

@csrf_exempt
def ask_difficult_question(request):
    """
    接收问题并调用 Processor 中的异步函数进行处理
    """
    if request.method == "POST":
        try:
            # 获取前端传递的 JSON 数据
            data = json.loads(request.body)
            question = data.get('question', '')

            # 检查问题是否为空
            if not question:
                logger.error("未提供问题")
                return JsonResponse({
                    'status': 'error',
                    'message': '未提供问题'
                }, status=400)

            # 使用 async_to_sync 将异步函数转换为同步
            answer = async_to_sync(chat_service.handle_question)(question)

            # 返回问题的答案
            return JsonResponse({
                'status': 'success',
                'response': answer
            }, status=200)

        except json.JSONDecodeError:
            logger.error("请求数据不是有效的 JSON 格式")
            return JsonResponse({
                'status': 'error',
                'message': '请求数据不是有效的 JSON 格式'
            }, status=400)

        except Exception as e:
            logger.error(f"处理问题时发生错误: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    else:
        logger.error("无效的请求方法")
        return JsonResponse({
            'status': 'error',
            'message': '无效的请求方法'
        }, status=405)
@csrf_exempt
@login_required
@csrf_exempt
@login_required
def ask_question(request):
    """
    处理用户提问历史人物的问题
    """
    if request.method == "POST":
        user_question = bleach.clean(request.POST.get('question', '').strip())
        figure_id = request.POST.get('figure_id')

        logger.debug(f"用户 {request.user.username} 提问: {user_question}, 历史人物ID: {figure_id}")

        # 验证输入
        if not user_question:
            logger.warning("用户提交了空的问题")
            return JsonResponse({'status': 'fail', 'message': '问题不能为空'}, status=400)
        if not figure_id:
            logger.warning("用户未提交历史人物ID")
            return JsonResponse({'status': 'fail', 'message': '历史人物ID不能为空'}, status=400)

        try:
            # 找到对应的历史人物
            figure = HistoricalFigure.objects.get(id=figure_id)
            logger.debug(f"找到历史人物: {figure.name}")
        except HistoricalFigure.DoesNotExist:
            logger.error(f"历史人物ID {figure_id} 不存在")
            return JsonResponse({'status': 'fail', 'message': '历史人物不存在'}, status=404)

        # 获取或创建 Conversation 对象
        conversation, created = Conversation.objects.get_or_create(
            user=request.user,
            historical_figure=figure
        )
        if created:
            logger.debug("创建新的会话记录")

        # 将提问保存到数据库（Message）
        message = Message(
            conversation=conversation,
            sender='user',  # 发送者是用户
            content=user_question
        )
        message.save()
        logger.debug("保存用户提问到数据库")

        # 构建提示词：历史人物系统消息 + 会话记忆 + 用户问题
        try:
            # 获取会话记忆（之前的消息内容）
            previous_messages = Message.objects.filter(conversation=conversation).order_by('id')
            memory = "\n".join(
                f"{msg.sender}: {msg.content}" for msg in previous_messages
            )

            # 使用 `prompt` 字段作为历史人物的引导信息
            figure_prompt = figure.prompt

            # 构造提示词
            prompt = (
                f"{figure_prompt}\n\n以下是你与用户的对话：\n"
                f"{memory}\n"
                f"用户的问题是：{user_question}\n"
                f"请基于你的角色身份和上下文做出回答。"
            )
            logger.debug(f"生成的提示词：{prompt}")

            # 使用 ChatService 获取回应
            response = async_to_sync(chat_service.get_response)(prompt)
            logger.debug(f"获取到AI回应: {response}")
        except Exception as e:
            logger.error(f"获取AI回应时出错: {e}")
            return JsonResponse({'status': 'fail', 'message': '无法获取AI回应'}, status=500)

        # 保存 AI 回复到数据库（Message）
        response_message = Message(
            conversation=conversation,
            sender='assistant',  # 发送者是 AI
            content=response
        )
        response_message.save()
        logger.debug("保存AI回应到数据库")

        return JsonResponse({'status': 'success', 'response': response})

    logger.warning("收到非POST请求")
    return JsonResponse({'status': 'fail', 'message': 'Invalid request'}, status=400)


@csrf_exempt
@login_required
def handle_clear_memory(request):
    """
    清除历史人物的记忆（假设清除的是与用户相关的会话）
    """
    if request.method == "POST":
        figure_id = request.POST.get('figure_id')

        # 验证输入
        if not figure_id:
            logger.warning("用户未提交历史人物ID")
            return JsonResponse({'status': 'fail', 'message': '历史人物ID不能为空'}, status=400)

        try:
            figure = HistoricalFigure.objects.get(id=figure_id)
            # 清除历史人物相关的所有对话记录
            Message.objects.filter(conversation__user=request.user, conversation__historical_figure=figure).delete()

            logger.debug(f"用户 {request.user.username} 清除 {figure.name} 的记忆")

            return JsonResponse({'status': 'success', 'message': f'{figure.name} 的记忆已清除'})
        except HistoricalFigure.DoesNotExist:
            logger.error(f"历史人物ID {figure_id} 不存在")
            return JsonResponse({'status': 'fail', 'message': '历史人物不存在'}, status=404)
        except Exception as e:
            logger.error(f"清除记忆时出错: {e}")
            return JsonResponse({'status': 'fail', 'message': '清除记忆时发生错误'}, status=500)

    logger.warning("收到非POST请求")
    return JsonResponse({'status': 'fail', 'message': 'Invalid request'}, status=400)

@csrf_exempt
@login_required
def get_answer(request):
    """
    获取用户提问的 AI 回答
    """
    if request.method == "POST":
        user_question = bleach.clean(request.POST.get('question', '').strip())

        # 验证输入
        if not user_question:
            logger.warning("用户提交了空的问题")
            return JsonResponse({'status': 'fail', 'message': '问题不能为空'}, status=400)

        # 获取 AI 回答（使用 async_to_sync 调用异步函数）
        try:
            response = async_to_sync(chat_service.get_response)(user_question)  # 直接传递字符串
            logger.debug(f"获取到AI回应: {response}")
        except Exception as e:
            logger.error(f"获取AI回应时出错: {e}")
            return JsonResponse({'status': 'fail', 'message': '无法获取AI回应'}, status=500)

        return JsonResponse({'status': 'success', 'response': response})

    logger.warning("收到非POST请求")
    return JsonResponse({'status': 'fail', 'message': 'Invalid request'}, status=400)

@csrf_exempt
@login_required
def clear_memory(request):
    """
    清除与某个历史人物的所有对话记录
    """
    if request.method == 'POST':
        figure_id = request.POST.get('figure_id')
        if not figure_id:
            logger.warning("用户未提交历史人物ID")
            return JsonResponse({'status': 'fail', 'message': '历史人物ID不能为空'}, status=400)

        try:
            # 获取历史人物
            historical_figure = HistoricalFigure.objects.get(id=figure_id)
            # 删除与该历史人物相关的对话记录
            deleted, _ = Conversation.objects.filter(
                user=request.user,
                historical_figure=historical_figure
            ).delete()
            logger.debug(f"用户 {request.user.username} 清除 {historical_figure.name} 的记忆")

            return JsonResponse({
                'status': 'success',
                'message': '聊天记忆已清除。',
                'deleted_conversations': deleted
            })
        except HistoricalFigure.DoesNotExist:
            logger.error(f"历史人物ID {figure_id} 不存在")
            return JsonResponse({'status': 'fail', 'message': '指定的历史人物不存在'}, status=404)
        except Exception as e:
            logger.error(f"清除记忆时出错: {e}")
            return JsonResponse({'status': 'fail', 'message': '清除记忆时发生错误'}, status=500)

    logger.warning("收到非POST请求")
    return JsonResponse({'status': 'fail', 'message': 'Invalid request'}, status=400)
