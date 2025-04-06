"""
Điểm khởi chạy chính của ứng dụng Agent Template.

Module này xử lý việc khởi tạo và chạy ứng dụng.
"""

import argparse
import asyncio
import os
import sys
import uuid
import logging
from typing import Optional, Dict, Any

from agent_template.config import AppConfig
from agent_template.core.agent_service import AgentService
from agent_template.core.cli_service import CLIService
from agent_template.core.api_service import APIService
from agent_template.memory.persistence import create_new_thread, Memory

# Vô hiệu hóa logging từ httpx
logging.getLogger("httpx").setLevel(logging.WARNING)

# Cấu hình logging cơ bản
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",  # Chỉ hiển thị thông điệp, không hiển thị các thông tin khác
    handlers=[
        logging.StreamHandler()
    ]
)

# Khởi tạo memory directory nếu chưa tồn tại
os.makedirs("conversation_memory", exist_ok=True)

def ask_user_choice() -> Dict[str, Any]:
    """Hỏi người dùng muốn sử dụng CLI hay API.
    
    Returns:
        Dict chứa các tùy chọn người dùng đã chọn
    """
    print("\n===== AGENT TEMPLATE =====")
    print("Chọn chế độ chạy:")
    print("1. Command Line Interface (CLI)")
    print("2. API Server")
    
    while True:
        choice = input("\nNhập lựa chọn của bạn (1 hoặc 2): ").strip()
        if choice in ['1', '2']:
            break
        print("Lựa chọn không hợp lệ. Vui lòng nhập 1 hoặc 2.")
    
    user_args = {
        "legacy": False,  # Mặc định sử dụng LangGraph
        "thread": None,   # Thread ID mới sẽ được tạo
        "host": "0.0.0.0",
        "port": 8000
    }
    
    # Chế độ xử lý
    print("\nChọn chế độ xử lý:")
    print("1. LangGraph (mặc định, khuyến nghị)")
    print("2. Legacy")
    
    process_choice = input("\nNhập lựa chọn của bạn (1 hoặc 2, Enter để chọn mặc định): ").strip()
    if process_choice == '2':
        user_args["legacy"] = True
        print("Đã chọn chế độ xử lý Legacy.")
    else:
        print("Đã chọn chế độ xử lý LangGraph.")
    
    # Nếu người dùng chọn API Server
    if choice == '2':
        user_args["api"] = True
        
        while True:
            try:
                port_input = input(f"\nNhập port cho API server (mặc định: 8000): ").strip()
                if not port_input:
                    port = 8000
                else:
                    port = int(port_input)
                    if port < 1 or port > 65535:
                        print("Port không hợp lệ. Vui lòng nhập số từ 1 đến 65535.")
                        continue
                user_args["port"] = port
                print(f"API server sẽ chạy trên port: {port}")
                break
            except ValueError:
                print("Port không hợp lệ. Vui lòng nhập một số nguyên.")
    else:
        user_args["api"] = False
        print("\nBắt đầu giao diện dòng lệnh (CLI)...")
    
    return user_args

async def main(args: Optional[Dict[str, Any]] = None):
    """Hàm chính để khởi chạy ứng dụng.
    
    Args:
        args: Các tham số dòng lệnh đã được phân tích (tùy chọn)
    """
    # Phân tích tham số dòng lệnh nếu chưa được cung cấp
    if args is None:
        parser = argparse.ArgumentParser(description="Agent Template")
        parser.add_argument(
            "--thread", "-t", 
            help="ID của luồng hội thoại để sử dụng"
        )
        parser.add_argument(
            "--legacy", "-l", 
            action="store_true", 
            help="Sử dụng xử lý legacy thay vì LangGraph"
        )
        parser.add_argument(
            "--api", "-a", 
            action="store_true", 
            help="Chạy ứng dụng dưới dạng HTTP API thay vì CLI"
        )
        parser.add_argument(
            "--port", "-p", 
            type=int, 
            default=8000, 
            help="Cổng cho API server (mặc định: 8000)"
        )
        parser.add_argument(
            "--host", 
            type=str, 
            default="0.0.0.0", 
            help="Host cho API server (mặc định: 0.0.0.0)"
        )
        parser.add_argument(
            "--interactive", "-i",
            action="store_true",
            help="Chạy trong chế độ tương tác (hỏi người dùng muốn CLI hay API)"
        )
        parsed_args = parser.parse_args()
        
        # Nếu người dùng yêu cầu chế độ tương tác
        if parsed_args.interactive:
            args = ask_user_choice()
        else:
            # Chuyển đổi Namespace thành dict
            args = vars(parsed_args)
    
    # Tạo cấu hình ứng dụng
    config = AppConfig(
        use_legacy=args.get("legacy", False),
        thread_id=args.get("thread") or create_new_thread(),
        api_host=args.get("host", "0.0.0.0"),
        api_port=args.get("port", 8000)
    )
    
    # Tạo agent service
    agent_service = AgentService(config)
    
    # Chạy ứng dụng dựa trên tham số
    if args.get("api", False):
        # Chạy dưới dạng API server
        api_service = APIService(agent_service, config)
        print(f"\nKhởi động API server tại http://{config.api_host}:{config.api_port}")
        print("Nhấn Ctrl+C để dừng server.")
        await api_service.start()
    else:
        # Chạy dưới dạng CLI
        cli_service = CLIService(agent_service, config)
        await cli_service.start()

if __name__ == "__main__":
    # Nếu không có tham số, chuyển sang chế độ tương tác
    if len(sys.argv) == 1:
        try:
            asyncio.run(main(ask_user_choice()))
        except KeyboardInterrupt:
            print("\nĐã phát hiện Ctrl+C. Thoát ứng dụng...")
            sys.exit(0)
    else:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\nĐã phát hiện Ctrl+C. Thoát ứng dụng...")
            sys.exit(0) 