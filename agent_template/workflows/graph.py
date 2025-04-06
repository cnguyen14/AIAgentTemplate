"""
Triển khai luồng công việc LangGraph.

Định nghĩa các thành phần máy trạng thái sử dụng LangGraph đồng thời tích hợp với pydantic-ai.
"""

from typing import Dict, List, Union, Any, TypedDict, Annotated, Literal
from datetime import datetime

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from httpx import AsyncClient
from langchain.schema import HumanMessage, AIMessage, BaseMessage

from agent_template.tools.logo import LogoResult
from agent_template.core.agent import agent
from agent_template.memory.persistence import (
    Deps, Memory, Message, save_memory, load_memory
)

# ===== HƯỚNG DẪN: ĐỊNH NGHĨA TRẠNG THÁI =====
# Định nghĩa TypedDict cho trạng thái trong luồng công việc
# Thêm các trường mới vào đây khi bạn mở rộng chức năng
# Định nghĩa schema trạng thái cho LangGraph
class AgentState(TypedDict):
    """Trạng thái được duy trì trong suốt luồng công việc của agent."""
    messages: Annotated[List[Union[HumanMessage, AIMessage, Dict[str, Any]]], add_messages]
    memory: Memory
    thread_id: str
    status: str
    tool_calls: List[Dict[str, Any]]

# ===== HƯỚNG DẪN: TẠO NODE XỬ LÝ =====
# Node này xử lý đầu vào người dùng và gọi agent để tạo phản hồi
# Định nghĩa nút xử lý chính
async def process_node(state: AgentState) -> AgentState:
    """Xử lý đầu vào của người dùng thông qua agent.
    
    Hàm này nhận trạng thái hiện tại, trích xuất tin nhắn mới nhất,
    gọi agent để xử lý và cập nhật trạng thái với kết quả.
    """
    # Trích xuất giá trị trạng thái
    thread_id = state["thread_id"]
    memory = state["memory"]
    messages = state["messages"]
    
    # Lấy tin nhắn người dùng mới nhất - có thể là dict hoặc HumanMessage
    latest_message = messages[-1] if messages else None
    if not latest_message:
        return state
    
    # Kiểm tra xem có phải tin nhắn người dùng không - xử lý cả hai định dạng dict và HumanMessage
    is_human_message = False
    user_input = ""
    
    if isinstance(latest_message, dict) and latest_message.get("role") == "human":
        is_human_message = True
        user_input = latest_message.get("content", "")
    elif isinstance(latest_message, HumanMessage):
        is_human_message = True
        user_input = latest_message.content
    
    if not is_human_message:
        # Không có tin nhắn người dùng để xử lý
        return state
    
    # Tạo dependencies
    deps = Deps(client=AsyncClient())
    
    # Xây dựng prompt với lịch sử hội thoại
    history_str = memory.get_history_str()
    context_prompt = f"Cuộc trò chuyện trước đó:\n{history_str}\n\nCâu hỏi hiện tại: {user_input}"
    
    # Xử lý với agent
    result = await agent.run(context_prompt, deps=deps)
    
    # ===== HƯỚNG DẪN: XỬ LÝ KẾT QUẢ TOOL =====
    # Thêm điều kiện ở đây để xử lý kết quả từ các công cụ khác nhau
    # Xử lý phản hồi
    if isinstance(result.data, LogoResult):
        # Ghi lại lệnh gọi công cụ
        state["tool_calls"].append({
            "tool": "logo", 
            "style": result.data.style,
            "timestamp": datetime.now().isoformat()
        })
        
        # Tạo nội dung xác nhận hiển thị logo
        content = f"Tôi đã hiển thị logo kiểu {result.data.style} cho bạn. Tôi có thể giúp gì thêm không?"
    
    # ===== HƯỚNG DẪN: THÊM XỬ LÝ TOOL MỚI =====
    # Sao chép và sửa đổi mẫu này cho công cụ mới
    # elif isinstance(result.data, YourToolResultType):
    #     # Ghi lại thông tin cuộc gọi công cụ
    #     state["tool_calls"].append({
    #         "tool": "your_tool_name",
    #         "param1": result.data.param1,
    #         "timestamp": datetime.now().isoformat()
    #     })
    #     
    #     # Định dạng nội dung phản hồi
    #     content = f"Kết quả từ công cụ của bạn: {result.data.some_field}"
    else:
        content = result.data
    
    # Thêm vào tin nhắn - sử dụng AIMessage trực tiếp thay vì dict
    state["messages"].append(AIMessage(content=content))
    
    # Lưu vào bộ nhớ
    memory.add_message("human", user_input)
    memory.add_message("ai", content)
    save_memory(thread_id, memory)
    
    # Cập nhật trạng thái
    state["memory"] = memory
    state["status"] = "completed"
    
    return state

# ===== HƯỚNG DẪN: TẠO NODE MỚI =====
# Mẫu để tạo một node mới xử lý chức năng cụ thể
"""
async def custom_tool_node(state: AgentState) -> AgentState:
    '''Node để xử lý một công cụ hoặc chức năng cụ thể.
    
    Trích xuất thông tin từ trạng thái, thực hiện xử lý,
    và cập nhật trạng thái với kết quả.
    '''
    # Trích xuất thông tin cần thiết từ trạng thái
    thread_id = state["thread_id"]
    memory = state["memory"]
    tool_calls = state["tool_calls"]
    
    # Kiểm tra xem có cuộc gọi công cụ phù hợp không
    if not tool_calls or tool_calls[-1].get("tool") != "your_tool_name":
        return state  # Không có cuộc gọi công cụ phù hợp để xử lý
    
    # Lấy thông tin từ cuộc gọi công cụ
    tool_call = tool_calls[-1]
    param1 = tool_call.get("param1", "")
    
    # Xử lý logic đặc biệt cho node này
    result = f"Đã xử lý {param1} theo cách đặc biệt"
    
    # Cập nhật trạng thái với kết quả
    state["messages"].append(AIMessage(content=result))
    memory.add_message("ai", result)
    save_memory(thread_id, memory)
    state["memory"] = memory
    
    return state
"""

# ===== HƯỚNG DẪN: TẠO HÀM ĐỊNH TUYẾN =====
# Định nghĩa hàm kiểm tra xem có nên tiếp tục xử lý hay không
def should_continue(state: AgentState) -> Literal["continue", "end"]:
    """Xác định xem chúng ta có nên tiếp tục xử lý hay kết thúc luồng công việc.
    
    Hàm này kiểm tra trạng thái để quyết định liệu có cần thực hiện thêm 
    các hành động theo dõi nào không.
    """
    # Kiểm tra xem chúng ta có cần thực hiện bất kỳ hành động theo dõi nào không
    if state["status"] == "needs_followup":
        return "continue"
    return "end"

# ===== HƯỚNG DẪN: TẠO HÀM ĐỊNH TUYẾN TÙY CHỈNH =====
# Mẫu để tạo hàm định tuyến cho nhiều node
"""
def route_by_tool(state: AgentState) -> Literal["process", "custom_tool", "other_tool", "end"]:
    '''Xác định node tiếp theo dựa trên loại công cụ được gọi.'''
    # Kiểm tra cuộc gọi công cụ gần nhất
    tool_calls = state.get("tool_calls", [])
    if not tool_calls:
        return "end"  # Không có cuộc gọi công cụ, kết thúc
    
    # Lấy cuộc gọi công cụ gần nhất
    latest_tool = tool_calls[-1].get("tool", "")
    
    # Định tuyến dựa trên loại công cụ
    if latest_tool == "your_tool_name":
        return "custom_tool"  # Đi đến node custom_tool
    elif latest_tool == "other_tool_name":
        return "other_tool"  # Đi đến node other_tool
    else:
        return "process"  # Quay lại node xử lý chính
"""

# ===== HƯỚNG DẪN: TẠO ĐỒ THỊ LUỒNG CÔNG VIỆC =====
# Tạo đồ thị luồng công việc
def create_workflow() -> StateGraph:
    """Tạo đồ thị luồng công việc.
    
    Hàm này khởi tạo một đồ thị trạng thái với các nút xử lý 
    và cạnh kết nối giữa chúng.
    """
    # Khởi tạo đồ thị
    workflow = StateGraph(AgentState)
    
    # Thêm các nút
    workflow.add_node("process", process_node)
    
    # ===== HƯỚNG DẪN: THÊM NODE MỚI VÀO ĐỒ THỊ =====
    # Thêm các node tùy chỉnh của bạn vào đây
    # workflow.add_node("custom_tool", custom_tool_node)
    # workflow.add_node("other_tool", other_tool_node)
    
    # Thêm các cạnh
    workflow.add_edge(START, "process")
    
    # ===== HƯỚNG DẪN: THÊM CẠNH ĐIỀU KIỆN =====
    # Thêm điều kiện để định tuyến giữa các node
    workflow.add_conditional_edges(
        "process",
        should_continue,
        {
            "continue": "process",  # Quay lại để xử lý theo dõi
            "end": END
        }
    )
    
    # ===== HƯỚNG DẪN: THÊM CẠNH ĐIỀU KIỆN PHỨC TẠP =====
    # Ví dụ về cách thêm định tuyến phức tạp hơn
    # workflow.add_conditional_edges(
    #     "process",
    #     route_by_tool,  # Hàm định tuyến tùy chỉnh
    #     {
    #         "custom_tool": "custom_tool",  # Đi đến node custom_tool
    #         "other_tool": "other_tool",    # Đi đến node other_tool
    #         "process": "process",          # Quay lại node process
    #         "end": END                     # Kết thúc luồng công việc
    #     }
    # )
    
    # ===== HƯỚNG DẪN: THÊM CẠNH TRỰC TIẾP =====
    # Thêm cạnh trực tiếp từ node tùy chỉnh về node process
    # workflow.add_edge("custom_tool", "process")
    # workflow.add_edge("other_tool", "process")
    
    # Biên dịch đồ thị
    return workflow.compile()

# Hàm để xử lý đầu vào người dùng thông qua luồng công việc
async def process_with_graph(thread_id: str, user_input: str, memory: Memory = None) -> str:
    """Xử lý đầu vào người dùng sử dụng luồng công việc LangGraph.
    
    Hàm này khởi tạo một đồ thị luồng công việc, chạy nó với đầu vào
    của người dùng và trả về phản hồi.
    
    Args:
        thread_id: ID cuộc trò chuyện
        user_input: Tin nhắn của người dùng
        memory: Đối tượng bộ nhớ với lịch sử hội thoại
        
    Returns:
        Phản hồi của agent
    """
    try:
        # Tải bộ nhớ nếu không được cung cấp
        if memory is None:
            memory = load_memory(thread_id)
            
        # Tạo luồng công việc
        workflow = create_workflow()
        
        # ===== HƯỚNG DẪN: KHỞI TẠO TRẠNG THÁI =====
        # Tùy chỉnh trạng thái ban đầu nếu cần thêm các trường
        # Khởi tạo trạng thái với đối tượng HumanMessage trực tiếp
        # Điều này đảm bảo tính tương thích với cách xử lý của LangGraph
        state = {
            "messages": [HumanMessage(content=user_input)],
            "memory": memory,
            "thread_id": thread_id,
            "status": "started",
            "tool_calls": []
        }
        
        # Thực thi luồng công việc
        result = await workflow.ainvoke(state)
        
        # Trích xuất phản hồi của trợ lý
        assistant_messages = [
            msg for msg in result["messages"] 
            if isinstance(msg, AIMessage)
        ]
        
        if assistant_messages:
            return assistant_messages[-1].content
        else:
            return "Không có phản hồi được tạo ra."
    except Exception as e:
        import traceback
        error_msg = f"Lỗi trong luồng công việc: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)  # In lỗi chi tiết để gỡ lỗi
        
        # Lưu lỗi vào bộ nhớ
        memory.add_message("human", user_input)
        memory.add_message("ai", f"Xin lỗi, tôi đã gặp lỗi: {str(e)}")
        save_memory(thread_id, memory)
        return f"Lỗi trong luồng công việc: {str(e)}" 