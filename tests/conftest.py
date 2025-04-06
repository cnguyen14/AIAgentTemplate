"""
Cấu hình pytest cho các tests của agent template.

Cung cấp các fixtures và thiết lập cho việc chạy tests API.
"""

import os
import sys
import pytest
import requests
from unittest.mock import MagicMock

# Thêm thư mục gốc vào sys.path để import các module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_template.config import AppConfig

@pytest.fixture(scope="session")
def api_url():
    """Trả về URL của API cho tests."""
    return os.environ.get("API_URL", "http://localhost:5000")

@pytest.fixture(scope="function")
def thread_id(api_url):
    """Tạo một thread ID mới cho test API."""
    # Tạo một thread mới
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{api_url}/conversations", headers=headers)
    data = response.json()
    thread_id = data.get("thread_id")
    
    yield thread_id
    
    # Dọn dẹp: xóa thread sau khi test xong
    requests.delete(f"{api_url}/conversations/{thread_id}", headers=headers)

@pytest.fixture(scope="session", autouse=True)
def setup_environment():
    """Thiết lập môi trường cho tất cả tests."""
    # Thiết lập biến môi trường
    os.environ.setdefault("ANTHROPIC_API_KEY", "dummy_key_for_testing")
    os.environ.setdefault("OPENAI_API_KEY", "dummy_key_for_testing")
    
    # Kiểm tra xem API đã chạy chưa
    api_url = os.environ.get("API_URL", "http://localhost:5000")
    try:
        response = requests.get(f"{api_url}/health", timeout=2)
        if response.status_code != 200:
            pytest.skip(f"API server không hoạt động tại {api_url}")
    except requests.RequestException:
        pytest.skip(f"Không thể kết nối đến API server tại {api_url}")
    
    yield

@pytest.fixture(scope="function")
def headers():
    """Headers chuẩn cho API requests."""
    return {"Content-Type": "application/json"} 