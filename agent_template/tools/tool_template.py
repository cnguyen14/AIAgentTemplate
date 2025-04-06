"""
Template cho công cụ mới.

Hướng dẫn:
1. Sao chép file này với tên mới (ví dụ: weather.py)
2. Thay đổi tên class, biến và hàm
3. Cập nhật docstrings và logic
4. Import công cụ trong core/agent.py và đăng ký với @agent.tool
5. Xử lý kết quả trong process_input() và process_node()
"""

from datetime import datetime
from typing import Dict, Any, Tuple, List, Optional
from pydantic import BaseModel

# 1. ĐỊNH NGHĨA KẾT QUẢ TOOL
class ToolResult(BaseModel):
    """Kết quả trả về bởi công cụ.
    
    Đây là lớp định nghĩa cấu trúc dữ liệu trả về từ công cụ.
    """
    # Thêm các trường dữ liệu cần thiết ở đây
    success: bool
    data: Any  # Thay thế bằng kiểu dữ liệu cụ thể (str, int, Dict, v.v.)
    timestamp: str = None
    
    def __init__(self, **data):
        # Tự động thêm timestamp nếu không được cung cấp
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().isoformat()
        super().__init__(**data)

# 2. CÁC HẰNG SỐ VÀ DỮ LIỆU TĨNH (nếu cần)
TOOL_CONFIG: Dict[str, Any] = {
    "option1": "giá_trị_1",
    "option2": "giá_trị_2",
    "max_items": 5
}

# 3. HÀM TIỆN ÍCH CHÍNH
def process_tool_logic(param1: str, param2: int = 0) -> Tuple[bool, Any]:
    """Xử lý logic chính của công cụ.
    
    Hàm này thực hiện chức năng cốt lõi của tool. Trong trường hợp thực tế, 
    đây có thể là nơi gọi API, xử lý dữ liệu, truy vấn cơ sở dữ liệu, v.v.
    
    Args:
        param1: Tham số đầu tiên mô tả
        param2: Tham số thứ hai với giá trị mặc định
        
    Returns:
        Tuple gồm (success, result_data)
    """
    try:
        # Xử lý logic công cụ ở đây
        # Ví dụ:
        result = f"Đã xử lý {param1} với tham số {param2}"
        
        # Có thể gọi API hoặc dịch vụ bên ngoài
        # response = requests.get(f"https://api.example.com/?q={param1}")
        # data = response.json()
        
        return True, result
    except Exception as e:
        # Xử lý lỗi
        return False, str(e)

# 4. CÁC HÀM PHỤ TRỢ (nếu cần)
def validate_input(param1: str) -> bool:
    """Kiểm tra tính hợp lệ của đầu vào.
    
    Args:
        param1: Tham số cần kiểm tra
        
    Returns:
        True nếu hợp lệ, False nếu không
    """
    # Ví dụ về logic kiểm tra
    return param1 and len(param1) <= 100

def format_output(data: Any) -> str:
    """Định dạng dữ liệu đầu ra thành chuỗi có thể đọc được.
    
    Args:
        data: Dữ liệu cần định dạng
        
    Returns:
        Chuỗi đã được định dạng
    """
    return f"Kết quả: {data}"

# 5. HƯỚNG DẪN ĐĂNG KÝ TOOL
"""
# Trong file core/agent.py, thêm:

from agent_template.tools.tool_name import ToolResult, process_tool_logic

@agent.tool
async def tool_name(
    ctx: RunContext[Deps],
    param1: str,
    param2: int = 0
) -> ToolResult:
    '''Mô tả chức năng của tool.
    
    Args:
        ctx: Run context với các dependencies
        param1: Mô tả tham số 1
        param2: Mô tả tham số 2
    
    Returns:
        ToolResult với thông tin về kết quả
    '''
    # Kiểm tra đầu vào nếu cần
    if not validate_input(param1):
        return ToolResult(
            success=False,
            data="Đầu vào không hợp lệ"
        )
        
    # Gọi hàm logic chính của tool
    success, result = process_tool_logic(param1, param2)
    
    # Trả về kết quả có cấu trúc
    return ToolResult(
        success=success,
        data=result
    )
"""

# 6. HƯỚNG DẪN XỬ LÝ KẾT QUẢ
"""
# Trong file core/agent.py, trong hàm process_input:

if isinstance(result.data, ToolResult):
    if result.data.success:
        content = f"Kết quả từ công cụ: {result.data.data}"
    else:
        content = f"Không thể xử lý yêu cầu: {result.data.data}"
"""

# 7. HƯỚNG DẪN THÊM NODE CHO LANGGRAPH
"""
# Trong file workflows/graph.py:

async def tool_node(state: AgentState) -> AgentState:
    '''Node để xử lý công cụ cụ thể.'''
    # Trích xuất thông tin cuộc gọi công cụ
    tool_calls = state["tool_calls"]
    if not tool_calls or tool_calls[-1].get("tool") != "tool_name":
        return state
    
    # Xử lý thông tin từ cuộc gọi công cụ
    tool_call = tool_calls[-1]
    param1 = tool_call.get("param1", "")
    param2 = tool_call.get("param2", 0)
    
    # Gọi logic xử lý công cụ
    success, result = process_tool_logic(param1, param2)
    
    # Tạo phản hồi
    if success:
        content = f"Kết quả từ công cụ: {result}"
    else:
        content = f"Không thể xử lý yêu cầu: {result}"
    
    # Cập nhật trạng thái
    state["messages"].append(AIMessage(content=content))
    state["memory"].add_message("ai", content)
    save_memory(state["thread_id"], state["memory"])
    
    return state

# Thêm vào hàm create_workflow()
workflow.add_node("tool_node", tool_node)

# Tạo hàm định tuyến
def route_tools(state: AgentState) -> Literal["process", "tool_node", "end"]:
    tool_calls = state.get("tool_calls", [])
    if not tool_calls:
        return "end"
    
    latest_tool = tool_calls[-1].get("tool", "")
    if latest_tool == "tool_name":
        return "tool_node"
    
    return "process"

# Cập nhật cạnh điều kiện
workflow.add_conditional_edges(
    "process",
    route_tools,
    {
        "tool_node": "tool_node",
        "process": "process",
        "end": END
    }
)

# Thêm cạnh từ tool_node quay lại process
workflow.add_edge("tool_node", "process")
"""

# 8. HƯỚNG DẪN THÊM PROMPT
"""
# Trong file utils/prompts.py:

TOOL_INSTRUCTIONS = '''
Bạn có quyền truy cập vào công cụ mới để [mô tả chức năng].
Khi người dùng yêu cầu [mô tả trường hợp sử dụng], hãy sử dụng công cụ này.

Cú pháp sử dụng:
- Tham số 1: [mô tả]
- Tham số 2: [mô tả] (tùy chọn, mặc định là 0)
'''

# Cập nhật prompt
def get_custom_assistant_prompt() -> str:
    return f'''...
    
{TOOL_INSTRUCTIONS}

...
'''
""" 