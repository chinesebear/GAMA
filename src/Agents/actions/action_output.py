def chat_completion_to_dict(completion):
    # 将每个部分的内容转换为字典格式
    return {
        'id': completion.id,
        'choices': [
            {
                'finish_reason': choice.finish_reason,
                'index': choice.index,
                'logprobs': choice.logprobs,
                'message': {
                    'content': choice.message.content,
                    'role': choice.message.role,
                    'function_call': choice.message.function_call,
                    'tool_calls': choice.message.tool_calls
                }
            } for choice in completion.choices
        ],
        'created': completion.created,
        'model': completion.model,
        'object': completion.object,
        'service_tier': getattr(completion, 'service_tier', 'default_tier'),
        'system_fingerprint': completion.system_fingerprint,
        'usage': {
            'completion_tokens': completion.usage.completion_tokens,
            'prompt_tokens': completion.usage.prompt_tokens,
            'total_tokens': completion.usage.total_tokens
        }
    }
