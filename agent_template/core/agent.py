"""
Triển khai core agent sử dụng pydantic-ai.

Module này định nghĩa chức năng cốt lõi của agent, các công cụ và runtime.
"""

import os
from typing import Union, Dict, Any, Optional
from datetime import datetime

import logfire
from pydantic_ai import Agent, RunContext
from pydantic_ai.settings import ModelSettings
from dotenv import load_dotenv
from httpx import AsyncClient

from agent_template.tools.logo import LogoResult, get_logo, display_logo
from agent_template.utils.prompts import get_simple_assistant_prompt, get_technical_assistant_prompt
from agent_template.memory.persistence import (
    Deps, Memory, Message, save_memory, load_memory
)
from agent_template.config import AppConfig

# Tải biến môi trường
load_dotenv()
logfire.configure(send_to_logfire='if-token-present')

# ===== HƯỚNG DẪN: CẤU HÌNH MODEL =====
# Cấu hình model mặc định
MODEL_NAME = os.environ.get('MODEL_NAME', 'openai:gpt-4o-mini')
ADVANCE_NAME = os.environ.get('ADVANCE_NAME', 'openai:gpt-4o')
LIGHT_MODEL = os.environ.get('LIGHT_MODEL', 'openai:gpt-4o-mini')

# Centralize model settings
def get_model_settings(model_type="default") -> ModelSettings:
    """Tạo model settings dựa trên loại model và biến môi trường."""
    if model_type == "advanced":
        return ModelSettings(
            temperature=float(os.environ.get('ADVANCED_TEMPERATURE', '0.6')),
            max_tokens=int(os.environ.get('ADVANCED_MAX_TOKENS', '4000')),
        )
    elif model_type == "light":
        return ModelSettings(
            temperature=float(os.environ.get('LIGHT_TEMPERATURE', '0.8')),
            max_tokens=int(os.environ.get('LIGHT_MAX_TOKENS', '500')),
        )
    else:  # default
        return ModelSettings(
            temperature=float(os.environ.get('TEMPERATURE', '0.7')),
            max_tokens=int(os.environ.get('MAX_TOKENS', '1000')),
        )

# Centralize system prompts
def get_system_prompt(prompt_type="default") -> str:
    """Lấy system prompt dựa trên loại và biến môi trường."""
    custom_prompt = os.environ.get(f'{prompt_type.upper()}_PROMPT', None)
    
    if custom_prompt:
        return custom_prompt
        
    if prompt_type == "advanced":
        return get_technical_assistant_prompt()
    elif prompt_type == "light":
        return os.environ.get('LIGHT_PROMPT', 
               "Bạn là một trợ lý AI nhỏ gọn cho các câu trả lời nhanh và súc tích.")
    else:  # default
        return get_simple_assistant_prompt()

# ===== ĐỊNH NGHĨA CÁC AGENT =====
# Agent chính - sử dụng cấu hình từ biến môi trường
agent = Agent[
    Deps,  # Kiểu dependency 
    Union[str, LogoResult]  # Kiểu kết quả
](
    MODEL_NAME,
    system_prompt=get_system_prompt("default"),
    model_settings=get_model_settings("default"),
    retries=int(os.environ.get('RETRIES', '2')),
)

# Định nghĩa agent nâng cao cho nhiệm vụ phức tạp
advanced_agent = Agent[
    Deps,  
    Union[str, LogoResult]
](
    ADVANCE_NAME,
    system_prompt=get_system_prompt("advanced"),
    model_settings=get_model_settings("advanced"),
    retries=int(os.environ.get('ADVANCED_RETRIES', '2')),
)

# Định nghĩa agent nhỏ gọn cho nhiệm vụ đơn giản
light_agent = Agent[
    Deps,
    Union[str, LogoResult]
](
    LIGHT_MODEL,
    system_prompt=get_system_prompt("light"),
    model_settings=get_model_settings("light"),
    retries=int(os.environ.get('LIGHT_RETRIES', '1')),
)

# Lấy agent phù hợp dựa trên cấu hình
def get_agent_for_config(config: AppConfig) -> Agent:
    """Trả về agent phù hợp dựa trên cấu hình."""
    if config.use_advanced_model:
        return advanced_agent
    elif config.use_light_model:
        return light_agent
    else:
        return agent

# ===== ĐĂNG KÝ CÔNG CỤ =====
# Công cụ cho tất cả các agent
@agent.tool
@advanced_agent.tool
@light_agent.tool
async def logo(
    ctx: RunContext[Deps],
    style: str = "default",
    color: bool = True
) -> LogoResult:
    """In một logo ASCII art trong CLI.
    
    Args:
        ctx: Run context với các dependencies
        style: Kiểu logo để in ('default', 'minimal', hoặc 'fancy')
        color: Liệu có sử dụng màu trong đầu ra hay không
    
    Returns:
        LogoResult với thông tin về logo đã hiển thị
    """
    # Lấy logo từ hàm tiện ích
    logo_text, used_style = get_logo(style, color)
    
    # Hiển thị logo
    display_logo(logo_text)
    
    # Trả về kết quả có cấu trúc
    return LogoResult(
        displayed=True,
        style=used_style,
        timestamp=datetime.now().isoformat()
    )

# Công cụ chỉ dành cho advanced_agent
@advanced_agent.tool
async def complex_analysis(
    ctx: RunContext[Deps],
    data: str,
    depth: int = 3
) -> str:
    """Thực hiện phân tích dữ liệu phức tạp (chỉ có ở agent nâng cao).
    
    Args:
        ctx: Run context với các dependencies
        data: Dữ liệu cần phân tích
        depth: Độ sâu phân tích (1-5)
        
    Returns:
        Kết quả phân tích chi tiết
    """
    # Trong thực tế, đây sẽ là một phân tích phức tạp
    return f"Phân tích chi tiết: {data} với độ sâu {depth}"

# Helper function để đăng ký tool cho tất cả agent
def register_for_all_agents(func):
    """Đăng ký một tool cho tất cả các agent."""
    agent.tool(func)
    advanced_agent.tool(func)
    light_agent.tool(func)
    return func

# Ví dụ về đăng ký tool cho tất cả agent
@register_for_all_agents
async def get_current_time(ctx: RunContext[Deps]) -> str:
    """Lấy thời gian hiện tại."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ===== XỬ LÝ ĐẦU VÀO =====
async def process_input(
    thread_id: str, 
    user_input: str, 
    memory: Memory,
    config: Optional[AppConfig] = None
) -> str:
    """
    Xử lý đầu vào người dùng thông qua agent phù hợp.
    
    Args:
        thread_id: Định danh luồng duy nhất
        user_input: Tin nhắn của người dùng
        memory: Đối tượng Memory với lịch sử hội thoại
        config: Cấu hình ứng dụng (tùy chọn)
        
    Returns:
        Phản hồi của trợ lý
    """
    # Tạo dependencies
    deps = Deps(client=AsyncClient())
    
    # Xây dựng prompt với lịch sử hội thoại
    history_str = memory.get_history_str()
    context_prompt = f"Cuộc trò chuyện trước đó:\n{history_str}\n\nCâu hỏi hiện tại: {user_input}"
    
    # Chọn agent phù hợp dựa trên cấu hình và/hoặc nội dung yêu cầu
    active_agent = agent  # Mặc định
    model_type = "default"
    
    if config:
        active_agent = get_agent_for_config(config)
        if config.use_advanced_model:
            model_type = "advanced"
        elif config.use_light_model:
            model_type = "light"
    elif "phân tích chi tiết" in user_input.lower() or "advanced" in user_input.lower():
        active_agent = advanced_agent
        model_type = "advanced"
    elif len(user_input) < 30 or "quick" in user_input.lower():
        active_agent = light_agent
        model_type = "light"
    
    # Lấy phản hồi từ agent phù hợp
    result = await active_agent.run(
        context_prompt, 
        deps=deps,
        model_settings=get_model_settings(model_type)
    )
    
    # Xử lý các loại phản hồi khác nhau
    if isinstance(result.data, LogoResult):
        # Xác nhận rằng logo đã được hiển thị
        content = f"Tôi đã hiển thị logo kiểu {result.data.style} cho bạn. Tôi có thể giúp gì thêm không?"
    else:
        content = result.data
    
    # Lưu tin nhắn vào bộ nhớ
    memory.add_message("human", user_input)
    memory.add_message("ai", content)
    save_memory(thread_id, memory)
    
    return content 