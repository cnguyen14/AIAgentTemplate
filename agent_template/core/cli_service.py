"""
Service CLI.

Module này định nghĩa lớp service để quản lý giao diện dòng lệnh (CLI)
và tương tác với AgentService.
"""

import asyncio
import os
import sys
from typing import Optional, Dict, Any

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

from agent_template.config import AppConfig
from agent_template.core.agent_service import AgentService
from agent_template.tools.logo import display_logo

class CLIService:
    """Service để quản lý giao diện dòng lệnh.
    
    Class này cung cấp giao diện dòng lệnh để tương tác với agent.
    """
    
    def __init__(self, agent_service: AgentService, config: AppConfig):
        """Khởi tạo CLI service.
        
        Args:
            agent_service: Service agent để xử lý tin nhắn
            config: Cấu hình ứng dụng
        """
        self.agent_service = agent_service
        self.config = config
        self.console = Console()
        self.running = False
        self.thread_id = config.thread_id
    
    async def start(self):
        """Khởi động giao diện dòng lệnh."""
        self.running = True
        
        # Hiển thị logo
        display_logo()
        
        # Hiển thị thông tin khởi động
        self.console.print(
            Panel(
                f"[bold green]Agent Template[/bold green] đã khởi động!\n"
                f"ID hội thoại: [bold]{self.thread_id}[/bold]\n"
                f"Chế độ xử lý: [bold]{'Legacy' if self.config.use_legacy else 'LangGraph'}[/bold]\n\n"
                "Gõ [bold blue]/help[/bold blue] để xem danh sách lệnh."
            )
        )
        
        # Vòng lặp chính
        while self.running:
            try:
                # Nhận đầu vào từ người dùng
                user_input = await self._get_user_input()
                
                # Kiểm tra nếu người dùng muốn thoát
                if user_input.lower() == "/exit":
                    result = await self.agent_service.process_message(user_input, self.thread_id)
                    self.console.print(Markdown(result["message"]))
                    self.running = False
                    break
                
                # Xử lý tin nhắn
                await self._process_and_display(user_input)
                
            except KeyboardInterrupt:
                self.console.print("\n[bold yellow]Đã phát hiện Ctrl+C. Thoát...[/bold yellow]")
                self.running = False
                break
            except Exception as e:
                self.console.print(f"[bold red]Lỗi: {str(e)}[/bold red]")
    
    async def _get_user_input(self) -> str:
        """Nhận đầu vào từ người dùng.
        
        Returns:
            Chuỗi đầu vào từ người dùng
        """
        return Prompt.ask("[bold green]Bạn[/bold green]")
    
    async def _process_and_display(self, user_input: str):
        """Xử lý tin nhắn và hiển thị kết quả.
        
        Args:
            user_input: Đầu vào từ người dùng
        """
        # Hiển thị thông báo đang xử lý
        with self.console.status("[bold blue]Đang xử lý...[/bold blue]"):
            # Gửi tin nhắn đến agent
            result = await self.agent_service.process_message(user_input, self.thread_id)
        
        # Xử lý kết quả dựa trên loại tin nhắn
        if result["success"]:
            # Nếu là lệnh hệ thống
            if "command" in result:
                await self._handle_command_result(result)
            # Nếu là phản hồi thông thường
            else:
                self.console.print("[bold purple]Agent[/bold purple]:")
                self.console.print(Markdown(result["response"]))
        else:
            # Hiển thị lỗi
            self.console.print(f"[bold red]Lỗi: {result.get('error', 'Không xác định')}[/bold red]")
    
    async def _handle_command_result(self, result: Dict[str, Any]):
        """Xử lý kết quả từ lệnh hệ thống.
        
        Args:
            result: Kết quả từ lệnh hệ thống
        """
        command = result.get("command", "")
        
        # Lệnh exit được xử lý trong vòng lặp chính
        
        # Lệnh help
        if command == "help":
            self.console.print(Markdown(result["message"]))
        
        # Lệnh history
        elif command == "history":
            self.console.print(Markdown(result["history"]))
        
        # Lệnh conversations
        elif command == "conversations":
            conversations = result["conversations"]
            
            if not conversations:
                self.console.print("[yellow]Không có hội thoại nào.[/yellow]")
            else:
                self.console.print("[bold]Danh sách hội thoại:[/bold]")
                for convo in conversations:
                    is_current = convo["id"] == self.thread_id
                    marker = "[bold green]*[/bold green] " if is_current else "  "
                    self.console.print(f"{marker}ID: [bold]{convo['id']}[/bold] ({convo['created']})")
        
        # Lệnh load
        elif command == "load":
            self.console.print(f"[green]{result['message']}[/green]")
            # Cập nhật thread_id hiện tại
            self.thread_id = result["thread_id"]
        
        # Lệnh delete
        elif command == "delete":
            self.console.print(f"[green]{result['message']}[/green]")
            # Nếu xóa hội thoại hiện tại, cập nhật thread_id mới
            if result.get("is_current", False):
                self.thread_id = result["thread_id"]
                self.console.print(f"[bold]Đã chuyển sang hội thoại mới với ID: {self.thread_id}[/bold]")
        
        # Lệnh graph và legacy
        elif command in ["graph", "legacy"]:
            self.console.print(f"[green]{result['message']}[/green]")
        
        # Lệnh new
        elif command == "new":
            self.console.print(f"[green]{result['message']}[/green]")
            # Cập nhật thread_id mới
            self.thread_id = result["thread_id"]
            
        # Lệnh không xác định
        else:
            if "error" in result:
                self.console.print(f"[bold red]{result['error']}[/bold red]")
            elif "message" in result:
                self.console.print(result["message"]) 