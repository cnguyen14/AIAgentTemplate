"""
Service xử lý agent.

Module này định nghĩa lớp service chính để tương tác với agent,
có thể được sử dụng bởi cả CLI và API.
"""

import os
from typing import Dict, Any, Optional, List, Tuple

from agent_template.config import AppConfig
from agent_template.core.agent import process_input
from agent_template.workflows.graph import process_with_graph
from agent_template.memory.persistence import (
    Memory, load_memory, save_memory, create_new_thread,
    list_conversations, delete_conversation, get_conversation_history,
    format_conversation_history
)

class AgentService:
    """Service chính để quản lý tương tác với agent.
    
    Class này cung cấp API thống nhất để tương tác với agent,
    bất kể phương thức giao tiếp là gì (CLI hoặc API HTTP).
    """
    
    def __init__(self, config: AppConfig):
        """Khởi tạo agent service.
        
        Args:
            config: Cấu hình ứng dụng
        """
        self.config = config
        
    async def process_message(self, user_input: str, thread_id: Optional[str] = None) -> Dict[str, Any]:
        """Xử lý tin nhắn từ người dùng.
        
        Args:
            user_input: Nội dung tin nhắn từ người dùng
            thread_id: ID luồng hội thoại (nếu None, sẽ dùng ID mặc định)
            
        Returns:
            Dict chứa kết quả xử lý (response và metadata)
        """
        # Sử dụng thread_id nếu được cung cấp, nếu không dùng ID mặc định
        current_thread_id = thread_id or self.config.thread_id
        
        # Kiểm tra xem tin nhắn có phải là lệnh hệ thống không
        if user_input.startswith('/'):
            return await self._process_system_command(user_input, current_thread_id)
            
        # Xử lý tin nhắn thông thường
        try:
            if self.config.use_legacy:
                memory = load_memory(current_thread_id)
                response = await process_input(current_thread_id, user_input, memory)
            else:
                response = await process_with_graph(current_thread_id, user_input)
                
            return {
                "success": True,
                "response": response,
                "thread_id": current_thread_id
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "thread_id": current_thread_id
            }
    
    async def _process_system_command(self, command: str, thread_id: str) -> Dict[str, Any]:
        """Xử lý các lệnh hệ thống.
        
        Args:
            command: Lệnh từ người dùng (bắt đầu bằng '/')
            thread_id: ID luồng hội thoại hiện tại
            
        Returns:
            Dict chứa kết quả xử lý lệnh
        """
        cmd = command.lower()
        
        # Lệnh exit
        if cmd == '/exit':
            return {
                "success": True,
                "command": "exit",
                "message": "Cảm ơn đã sử dụng Agent Template! Tạm biệt!",
                "thread_id": thread_id
            }
        
        # Lệnh help
        elif cmd == '/help':
            return {
                "success": True,
                "command": "help",
                "message": self._get_help_text(thread_id),
                "thread_id": thread_id
            }
        
        # Lệnh history
        elif cmd == '/history':
            history = get_conversation_history(thread_id)
            formatted_history = format_conversation_history(history)
            return {
                "success": True,
                "command": "history",
                "history": formatted_history,
                "raw_history": history,
                "thread_id": thread_id
            }
        
        # Lệnh conversations
        elif cmd == '/conversations':
            convos = list_conversations()
            return {
                "success": True,
                "command": "conversations",
                "conversations": convos,
                "thread_id": thread_id
            }
        
        # Lệnh load
        elif cmd.startswith('/load '):
            new_id = command[6:].strip()
            convos = list_conversations()
            if new_id in convos:
                return {
                    "success": True,
                    "command": "load",
                    "message": f"Đã tải hội thoại có ID: {new_id}",
                    "previous_thread_id": thread_id,
                    "thread_id": new_id
                }
            else:
                return {
                    "success": False,
                    "command": "load",
                    "error": f"Không tìm thấy hội thoại có ID: {new_id}",
                    "thread_id": thread_id
                }
        
        # Lệnh delete
        elif cmd.startswith('/delete '):
            del_id = command[8:].strip()
            convos = list_conversations()
            if del_id in convos:
                delete_conversation(del_id)
                new_thread_id = thread_id
                
                # Nếu xóa hội thoại hiện tại, tạo một cái mới
                if del_id == thread_id:
                    new_thread_id = create_new_thread()
                    
                return {
                    "success": True,
                    "command": "delete",
                    "message": f"Đã xóa hội thoại có ID: {del_id}",
                    "is_current": del_id == thread_id,
                    "thread_id": new_thread_id
                }
            else:
                return {
                    "success": False,
                    "command": "delete",
                    "error": f"Không tìm thấy hội thoại có ID: {del_id}",
                    "thread_id": thread_id
                }
        
        # Lệnh graph
        elif cmd == '/graph':
            self.config.use_legacy = False
            return {
                "success": True,
                "command": "graph",
                "message": "Đã chuyển sang chế độ xử lý LangGraph.",
                "thread_id": thread_id
            }
        
        # Lệnh legacy
        elif cmd == '/legacy':
            self.config.use_legacy = True
            return {
                "success": True,
                "command": "legacy",
                "message": "Đã chuyển sang chế độ xử lý legacy (không dùng LangGraph).",
                "thread_id": thread_id
            }
        
        # Lệnh new
        elif cmd == '/new':
            new_thread_id = create_new_thread()
            return {
                "success": True,
                "command": "new",
                "message": f"Đã tạo hội thoại mới với ID: {new_thread_id}",
                "previous_thread_id": thread_id,
                "thread_id": new_thread_id
            }
            
        # Lệnh không hợp lệ
        else:
            return {
                "success": False,
                "command": "unknown",
                "error": f"Lệnh không hợp lệ: {command}",
                "thread_id": thread_id
            }
    
    def _get_help_text(self, thread_id: str) -> str:
        """Lấy văn bản trợ giúp.
        
        Args:
            thread_id: ID luồng hội thoại hiện tại
            
        Returns:
            Chuỗi markdown với thông tin trợ giúp
        """
        current_processor = "legacy" if self.config.use_legacy else "graph"
        
        return f"""# Trợ giúp

## Lệnh
- `/exit` - Thoát ứng dụng
- `/help` - Hiển thị tin nhắn trợ giúp này
- `/history` - Hiển thị lịch sử hội thoại hiện tại
- `/conversations` - Liệt kê tất cả các hội thoại
- `/load ID` - Tải một hội thoại từ ID
- `/delete ID` - Xóa hội thoại có ID đã cho
- `/new` - Tạo hội thoại mới
- `/graph` - Chuyển sang xử lý LangGraph
- `/legacy` - Chuyển sang xử lý legacy (không dùng LangGraph)

## Thông tin hiện tại
- Chế độ xử lý: {current_processor}
- ID hội thoại: {thread_id}
"""

    async def create_new_conversation(self) -> str:
        """Tạo một cuộc hội thoại mới.
        
        Returns:
            ID của luồng hội thoại mới
        """
        thread_id = create_new_thread()
        self.config.thread_id = thread_id
        return thread_id
    
    def get_all_conversations(self) -> List[Dict[str, Any]]:
        """Lấy danh sách tất cả các cuộc hội thoại.
        
        Returns:
            Danh sách các cuộc hội thoại với metadata
        """
        return list_conversations()

    def get_conversation_history(self, thread_id: str) -> List[Dict[str, Any]]:
        """Lấy lịch sử hội thoại cho một thread ID cụ thể.
        
        Args:
            thread_id: ID của luồng hội thoại
            
        Returns:
            Danh sách các tin nhắn trong hội thoại
        """
        return get_conversation_history(thread_id) 