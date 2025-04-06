"""
Test file for API endpoints.

Kiểm tra các REST API endpoints của agent template sử dụng requests.
"""

import os
import json
import time
import unittest
import requests

# API URL mặc định
DEFAULT_API_URL = "http://localhost:4000"
API_URL = os.environ.get("API_URL", DEFAULT_API_URL)

class TestAgentTemplateAPI(unittest.TestCase):
    """Test case cho Agent Template API."""
    
    def setUp(self):
        """Thiết lập trước mỗi test case."""
        self.base_url = API_URL
        self.headers = {
            "Content-Type": "application/json"
        }
        # Tạo một thread mới cho test
        response = requests.post(
            f"{self.base_url}/conversations",
            headers=self.headers
        )
        data = response.json()
        self.thread_id = data.get("thread_id")
        
    def tearDown(self):
        """Dọn dẹp sau mỗi test case."""
        if hasattr(self, 'thread_id'):
            # Xóa thread đã tạo
            requests.delete(
                f"{self.base_url}/conversations/{self.thread_id}",
                headers=self.headers
            )
    
    def test_health_check(self):
        """Kiểm tra health check endpoint."""
        print("\n[TEST] Kiểm tra health check...")
        response = requests.get(f"{self.base_url}/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        print("✓ Health check thành công!")
    
    def test_create_conversation(self):
        """Kiểm tra tạo cuộc trò chuyện mới."""
        print("\n[TEST] Kiểm tra tạo cuộc trò chuyện mới...")
        response = requests.post(f"{self.base_url}/conversations")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("thread_id", data)
        print(f"✓ Tạo cuộc trò chuyện mới thành công, thread_id: {data['thread_id']}")
    
    def test_send_message(self):
        """Kiểm tra gửi tin nhắn."""
        print("\n[TEST] Kiểm tra gửi tin nhắn...")
        payload = {
            "message": "Xin chào",
            "thread_id": self.thread_id
        }
        
        response = requests.post(
            f"{self.base_url}/send_message",
            headers=self.headers,
            json=payload
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("response", data)
        self.assertIn("thread_id", data)
        print(f"✓ Gửi tin nhắn thành công, nhận phản hồi: '{data['response'][:30]}...'")
    
    def test_list_conversations(self):
        """Kiểm tra danh sách cuộc trò chuyện."""
        print("\n[TEST] Kiểm tra danh sách cuộc trò chuyện...")
        response = requests.get(f"{self.base_url}/conversations")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("conversations", data)
        self.assertIsInstance(data["conversations"], list)
        print(f"✓ Lấy danh sách cuộc trò chuyện thành công, số lượng: {len(data['conversations'])}")
    
    def test_get_conversation_history(self):
        """Kiểm tra lịch sử cuộc trò chuyện."""
        print("\n[TEST] Kiểm tra lịch sử cuộc trò chuyện...")
        # Đầu tiên tạo một vài tin nhắn
        messages = ["Xin chào", "Bạn khỏe không?", "Hôm nay thế nào?"]
        
        for msg in messages:
            print(f"  - Gửi tin nhắn: '{msg}'")
            requests.post(
                f"{self.base_url}/send_message",
                headers=self.headers,
                json={"message": msg, "thread_id": self.thread_id}
            )
            # Chờ một chút để tin nhắn được xử lý
            time.sleep(1)
        
        # Kiểm tra lịch sử
        response = requests.get(
            f"{self.base_url}/conversations/{self.thread_id}/history"
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("history", data)
        self.assertGreaterEqual(len(data["history"]), len(messages))
        print(f"✓ Lấy lịch sử cuộc trò chuyện thành công, số lượng tin nhắn: {len(data['history'])}")
    
    def test_get_config(self):
        """Kiểm tra lấy cấu hình."""
        print("\n[TEST] Kiểm tra lấy cấu hình...")
        response = requests.get(f"{self.base_url}/config")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("config", data)
        self.assertIn("model_name", data["config"])
        print(f"✓ Lấy cấu hình thành công, model: {data['config']['model_name']}")

if __name__ == "__main__":
    # Nếu API đang chạy, chạy các test
    try:
        print(f"Đang kết nối tới API tại {API_URL}...")
        health_check = requests.get(f"{API_URL}/health", timeout=2)
        if health_check.status_code == 200:
            print("Kết nối thành công! Bắt đầu chạy test...")
            unittest.main()
        else:
            print(f"API không phản hồi tại {API_URL}. Hãy đảm bảo API đang chạy. Kiểm tra port nếu cấu hình không đúng")
    except requests.exceptions.RequestException:
        print(f"Không thể kết nối tới API tại {API_URL}. Hãy đảm bảo API đang chạy. Kiểm tra port nếu cấu hình không đúng") 