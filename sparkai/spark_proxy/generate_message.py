from openai_types import ChatMessage, Function, FunctionCall, Tool, ToolCall
from typing import List, Optional

from spark_api import SparkAPI

s_k = "e1ba8c0c3deca84313ac8a3b6e9b9111&NGIwZTBmYjJkOTE4ZjFhNDY3N2M0YTcy&4eea957b"


def generate_message(
        *,
        messages: List[ChatMessage],
        functions: Optional[List[Function]] = None,
        tools: Optional[List[Tool]] = None,
        temperature: float = 0.7,
        model: str = None
) -> ChatMessage:
    s_api = SparkAPI(s_k, model=model, temperature=temperature)
    print('generate_message ~~~~~')
    print('messages:', messages)
    print('functions:', functions)
    print('tools:', tools)
    print('temperature:', temperature)

    function_list = []
    if functions:
        for t in functions:
            function_list.append(
                {
                    'name': t.name,
                    'description': t.description,
                    'parameters': t.parameters
                }
            )
    if tools:
        for t in tools:
            f = t.function
            function_list.append(
                {
                    'name': f.name,
                    'description': f.description,
                    'parameters': f.parameters
                }
            )
    content, function_call = s_api.call(messages, function_list)
    print("resp------------")
    print('content::', content)
    print('function_call::', function_call)
    if function_call:
        f = FunctionCall(name=function_call['name'], arguments=function_call['arguments'], id="call_" + 'a' * 24)
        return ChatMessage(
            content=content,
            role='assistant',
            tool_calls=[ToolCall(function=f)]
        )

    return ChatMessage(
        content=content,
        role='assistant')
