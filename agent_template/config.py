"""
Cấu hình ứng dụng Agent Template.

Module này định nghĩa cấu hình toàn cục cho ứng dụng.
"""

import os
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

class AppConfig:
    """Lớp cấu hình ứng dụng.
    
    Lưu trữ tất cả cấu hình cần thiết cho ứng dụng.
    """
    
    def __init__(
        self,
        use_legacy: bool = False,
        thread_id: str = None,
        api_host: str = None,
        api_port: int = None,
        model_name: str = None,
        temperature: float = None,
        max_tokens: int = None,
        use_advanced_model: bool = False,
        use_light_model: bool = False
    ):
        """Khởi tạo cấu hình ứng dụng.
        
        Args:
            use_legacy: Sử dụng chế độ xử lý legacy thay vì LangGraph
            thread_id: ID của luồng hội thoại để sử dụng
            api_host: Host cho API server
            api_port: Cổng cho API server
            model_name: Tên model để sử dụng
            temperature: Nhiệt độ cho việc tạo văn bản
            max_tokens: Số token tối đa cho mỗi phản hồi
            use_advanced_model: Sử dụng model nâng cao (high-end) cho tác vụ phức tạp
            use_light_model: Sử dụng model nhẹ cho các tác vụ đơn giản
        """
        # Cấu hình chế độ xử lý
        self.use_legacy = use_legacy
        
        # Cấu hình ID luồng
        self.thread_id = thread_id
        
        # Cấu hình API server
        self.api_host = api_host or os.environ.get("API_HOST", "0.0.0.0")
        self.api_port = api_port or int(os.environ.get("API_PORT", "8000"))
        
        # Cấu hình model
        self.model_name = model_name or os.environ.get("MODEL_NAME", "openai:gpt-4o-mini")
        self.temperature = temperature or float(os.environ.get("TEMPERATURE", "0.7"))
        self.max_tokens = max_tokens or int(os.environ.get("MAX_TOKENS", "1000"))
        
        # Cấu hình lựa chọn model
        self.use_advanced_model = use_advanced_model
        self.use_light_model = use_light_model
        
        # Các cấu hình model cụ thể
        self.advanced_model = os.environ.get("ADVANCED_MODEL", "openai:gpt-4o")
        self.advanced_temperature = float(os.environ.get("ADVANCED_TEMPERATURE", "0.6"))
        self.advanced_max_tokens = int(os.environ.get("ADVANCED_MAX_TOKENS", "4000"))
        
        self.light_model = os.environ.get("LIGHT_MODEL", "openai:gpt-4o-mini")
        self.light_temperature = float(os.environ.get("LIGHT_TEMPERATURE", "0.8"))
        self.light_max_tokens = int(os.environ.get("LIGHT_MAX_TOKENS", "500"))
        
        # Thư mục lưu trữ bộ nhớ
        self.memory_dir = os.environ.get("MEMORY_DIR", "conversation_memory")
        
        # Timeout cho tool
        self.tool_timeout = int(os.environ.get("TOOL_TIMEOUT", "10"))
    
    def update(self, updates: dict):
        """Cập nhật cấu hình với một tập các thay đổi.
        
        Args:
            updates: Dict với các thay đổi cấu hình
        """
        for key, value in updates.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def get_model_settings(self) -> dict:
        """Lấy cài đặt model dựa trên cấu hình hiện tại.
        
        Returns:
            Dict chứa các cài đặt model
        """
        if self.use_advanced_model:
            return {
                "model_name": self.advanced_model,
                "temperature": self.advanced_temperature,
                "max_tokens": self.advanced_max_tokens
            }
        elif self.use_light_model:
            return {
                "model_name": self.light_model,
                "temperature": self.light_temperature,
                "max_tokens": self.light_max_tokens
            }
        else:
            return {
                "model_name": self.model_name,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            } 