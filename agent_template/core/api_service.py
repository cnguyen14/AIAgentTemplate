"""
Service API HTTP.

Module này định nghĩa lớp service để quản lý API HTTP
và tương tác với AgentService.
"""

import asyncio
import json
import logging
import os
from typing import Optional, Dict, Any, List

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Body, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from agent_template.config import AppConfig
from agent_template.core.agent_service import AgentService

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Định nghĩa models Pydantic
class UserMessage(BaseModel):
    """Model cho tin nhắn gửi từ người dùng."""
    message: str
    thread_id: Optional[str] = None

class AgentResponse(BaseModel):
    """Model cho phản hồi từ agent."""
    success: bool
    response: Optional[str] = None
    error: Optional[str] = None
    thread_id: str
    command: Optional[str] = None
    message: Optional[str] = None

class Conversation(BaseModel):
    """Model cho thông tin hội thoại."""
    id: str
    created: str
    last_updated: Optional[str] = None
    message_count: int

class APIService:
    """Service để quản lý API HTTP.
    
    Class này cung cấp API HTTP để tương tác với agent từ xa.
    """
    
    def __init__(self, agent_service: AgentService, config: AppConfig):
        """Khởi tạo API service.
        
        Args:
            agent_service: Service agent để xử lý tin nhắn
            config: Cấu hình ứng dụng
        """
        self.agent_service = agent_service
        self.config = config
        self.app = self._create_app()
    
    def _create_app(self) -> FastAPI:
        """Tạo ứng dụng FastAPI.
        
        Returns:
            Đối tượng FastAPI đã cấu hình
        """
        app = FastAPI(
            title="Agent Template API",
            description="API để tương tác với Agent Template",
            version="1.0.0"
        )
        
        # Thêm CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Cho phép tất cả nguồn gốc trong môi trường phát triển
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Định nghĩa routes
        @app.get("/", tags=["Root"])
        async def root():
            return {
                "name": "Agent Template API",
                "version": "1.0.0",
                "status": "running",
                "docs_url": "/docs"
            }
        
        @app.get("/health", tags=["Health"])
        async def health_check():
            """Kiểm tra trạng thái API.
            
            Returns:
                Trạng thái API
            """
            return {
                "status": "ok",
                "version": "1.0.0"
            }
        
        @app.post("/send_message", response_model=AgentResponse, tags=["Messaging"])
        async def send_message(message: UserMessage):
            """Gửi tin nhắn đến agent.
            
            Args:
                message: Nội dung tin nhắn và thread_id tùy chọn
                
            Returns:
                Phản hồi từ agent
            """
            try:
                result = await self.agent_service.process_message(message.message, message.thread_id)
                return result
            except Exception as e:
                logger.exception("Lỗi khi xử lý tin nhắn")
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.get("/conversations", tags=["Conversations"])
        async def list_conversations():
            """Lấy danh sách tất cả các cuộc hội thoại.
            
            Returns:
                Danh sách các cuộc hội thoại
            """
            try:
                thread_ids = self.agent_service.get_all_conversations()
                conversations = []
                
                for thread_id in thread_ids:
                    # Lấy lịch sử hội thoại để đếm số tin nhắn
                    history = self.agent_service.get_conversation_history(thread_id)
                    message_count = len(history) if history else 0
                    
                    conversations.append(Conversation(
                        id=thread_id,
                        created=thread_id,  # Sử dụng thread_id làm timestamp vì thread_id đã là timestamp
                        message_count=message_count  # Đếm số lượng tin nhắn thực tế
                    ))
                
                return {"conversations": conversations}  # Đóng gói trong key "conversations" theo mong đợi của test
            except Exception as e:
                logger.exception("Lỗi khi lấy danh sách hội thoại")
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.post("/conversations", response_model=Dict[str, str], tags=["Conversations"])
        async def create_conversation():
            """Tạo một cuộc hội thoại mới.
            
            Returns:
                ID của hội thoại mới
            """
            try:
                thread_id = await self.agent_service.create_new_conversation()
                return {"thread_id": thread_id}
            except Exception as e:
                logger.exception("Lỗi khi tạo hội thoại mới")
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.delete("/conversations/{thread_id}", tags=["Conversations"])
        async def delete_conversation(thread_id: str):
            """Xóa một cuộc hội thoại.
            
            Args:
                thread_id: ID của hội thoại cần xóa
                
            Returns:
                Thông báo thành công
            """
            try:
                result = await self.agent_service.process_message(f"/delete {thread_id}")
                if not result["success"]:
                    raise HTTPException(status_code=404, detail=f"Không tìm thấy hội thoại: {thread_id}")
                return {"message": f"Đã xóa hội thoại: {thread_id}"}
            except Exception as e:
                logger.exception(f"Lỗi khi xóa hội thoại {thread_id}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.get("/conversations/{thread_id}/history", tags=["Conversations"])
        async def get_conversation_history(thread_id: str):
            """Lấy lịch sử hội thoại.
            
            Args:
                thread_id: ID của hội thoại
                
            Returns:
                Lịch sử hội thoại
            """
            try:
                result = await self.agent_service.process_message("/history", thread_id)
                if not result["success"]:
                    raise HTTPException(status_code=404, detail=f"Không tìm thấy hội thoại: {thread_id}")
                return {"history": result.get("raw_history", [])}
            except Exception as e:
                logger.exception(f"Lỗi khi lấy lịch sử hội thoại {thread_id}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.get("/config", tags=["Config"])
        async def get_config():
            """Lấy cấu hình hiện tại của agent.
            
            Returns:
                Cấu hình hiện tại
            """
            try:
                # Trả về phiên bản đã lọc của cấu hình đóng gói trong key "config"
                return {
                    "config": {
                        "use_legacy": self.config.use_legacy,
                        "model_name": self.config.model_name,
                        "temperature": self.config.temperature
                    }
                }
            except Exception as e:
                logger.exception("Lỗi khi lấy cấu hình")
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.post("/config", tags=["Config"])
        async def update_config(config_data: Dict[str, Any] = Body(...)):
            """Cập nhật cấu hình agent.
            
            Args:
                config_data: Dữ liệu cấu hình cần cập nhật
                
            Returns:
                Cấu hình đã cập nhật
            """
            try:
                updates = {}
                if "use_legacy" in config_data:
                    updates["use_legacy"] = config_data["use_legacy"]
                if "model_name" in config_data:
                    updates["model_name"] = config_data["model_name"]
                if "temperature" in config_data:
                    updates["temperature"] = config_data["temperature"]
                
                # Chỉ cập nhật nếu có thay đổi
                if updates:
                    self.config.update(updates)
                
                # Trả về cấu hình mới đóng gói trong key "config"
                return {
                    "config": {
                        "use_legacy": self.config.use_legacy,
                        "model_name": self.config.model_name,
                        "temperature": self.config.temperature
                    }
                }
            except Exception as e:
                logger.exception("Lỗi khi cập nhật cấu hình")
                raise HTTPException(status_code=500, detail=str(e))
        
        return app
    
    async def start(self):
        """Khởi động máy chủ API."""
        config = uvicorn.Config(
            self.app,
            host=self.config.api_host,
            port=self.config.api_port,
            log_level="info"
        )
        server = uvicorn.Server(config)
        
        logger.info(f"API server đang chạy tại http://{self.config.api_host}:{self.config.api_port}")
        await server.serve()
    
    def run(self):
        """Chạy máy chủ API một cách đồng bộ."""
        uvicorn.run(
            self.app,
            host=self.config.api_host,
            port=self.config.api_port,
            log_level="info"
        ) 