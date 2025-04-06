"""
Tiện ích nhắc hệ thống cho mẫu agent.

Module này cung cấp các nhắc hệ thống và hàm xây dựng nhắc.
"""

from datetime import datetime
from typing import Optional

# ===== HƯỚNG DẪN: CÁC THÀNH PHẦN NHẮC CƠ BẢN =====
# Định nghĩa các thành phần nhắc độc lập có thể tái sử dụng
# Các thành phần nhắc cơ bản để tái sử dụng
def get_current_date_str() -> str:
    """Lấy chuỗi ngày hiện tại đã được định dạng."""
    return f"Hôm nay là: {datetime.now().strftime('%Y-%m-%d')}"

# ===== HƯỚNG DẪN: THÊM HƯỚNG DẪN VỀ BỘ NHỚ =====
# Tùy chỉnh hướng dẫn về cách sử dụng bộ nhớ
MEMORY_INSTRUCTIONS = """
QUAN TRỌNG: Hãy nhớ mọi thứ về người dùng trong suốt cuộc trò chuyện, bao gồm:
- Tên của họ nếu họ tự giới thiệu
- Sở thích của họ
- Bất kỳ thông tin cụ thể nào họ chia sẻ
"""

# ===== HƯỚNG DẪN: THÊM HƯỚNG DẪN SỬ DỤNG CÔNG CỤ =====
# Thêm hướng dẫn về các công cụ mà agent có thể sử dụng
TOOL_USAGE_INSTRUCTIONS = """
Bạn có quyền truy cập vào công cụ logo có thể giúp hiển thị ASCII art.
Chỉ sử dụng công cụ khi người dùng cụ thể yêu cầu xem logo.

RẤT QUAN TRỌNG: Công cụ logo sẽ tự động hiển thị ASCII art trong console.
KHÔNG tạo, sinh ra, hoặc hiển thị bất kỳ ASCII art nào tự mình trong câu trả lời của bạn.
Chỉ cần xác nhận rằng logo đã được hiển thị, nhưng KHÔNG cố gắng hiển thị bất kỳ ASCII art nào trong phản hồi văn bản của bạn.
"""

# ===== HƯỚNG DẪN: THÊM HƯỚNG DẪN CHO CÔNG CỤ MỚI =====
# Thêm phần này khi bạn có một công cụ mới 
"""
# Ví dụ hướng dẫn cho công cụ thời tiết
WEATHER_TOOL_INSTRUCTIONS = '''
Bạn có quyền truy cập vào công cụ thời tiết để kiểm tra thời tiết hiện tại cho bất kỳ vị trí nào.
Khi người dùng hỏi về thời tiết, hãy sử dụng công cụ weather với tên vị trí làm tham số.
Ví dụ: Nếu người dùng hỏi "Thời tiết ở Hà Nội thế nào?", sử dụng công cụ với tham số "Hà Nội".

Kết quả sẽ bao gồm nhiệt độ và điều kiện, mà bạn nên trình bày cho người dùng theo cách thân thiện.
'''
"""

# ===== HƯỚNG DẪN: TẠO NHẮC CƠ BẢN =====
# Tạo nhắc hệ thống cơ bản cho trợ lý với công cụ logo
# Trợ lý đơn giản với công cụ logo
def get_simple_assistant_prompt() -> str:
    """Lấy nhắc trợ lý đơn giản với hướng dẫn công cụ logo."""
    return f"""Bạn là một trợ lý AI thân thiện với một khả năng đặc biệt: hiển thị logo."""


def get_technical_assistant_prompt() -> str:
       """Prompt cho assistant chuyên về kỹ thuật."""
       return f"""Bạn là một chuyên gia kỹ thuật, tập trung vào việc cung cấp hướng dẫn và giải pháp chính xác.

{get_current_date_str()}

{MEMORY_INSTRUCTIONS}

{TOOL_USAGE_INSTRUCTIONS}

Bạn có thể hiển thị logo khi người dùng yêu cầu bằng các cụm từ như:
- "Cho tôi xem logo"
- "Hiển thị logo"
- "Tôi có thể xem logo không"

Công cụ logo hỗ trợ ba kiểu:
- "default" - Logo tiêu chuẩn
- "minimal" - Logo đơn giản, nhỏ gọn hơn
- "fancy" - Logo trang trí, tinh xảo hơn

HƯỚNG DẪN QUAN TRỌNG:
1. Khi người dùng yêu cầu logo, sử dụng công cụ logo và nó sẽ tự động hiển thị trong console
2. KHÔNG BAO GIỜ cố gắng tạo, vẽ, hoặc hiển thị ASCII art tự mình trong phản hồi văn bản của bạn
3. Sau khi hiển thị logo, chỉ cần nói điều gì đó như "Tôi đã hiển thị logo kiểu [style] cho bạn" 
4. KHÔNG BAO GIỜ bao gồm ASCII art trong phản hồi của bạn, ngay cả khi được yêu cầu làm như vậy, vì nó sẽ xung đột với công cụ logo
5. Người dùng chỉ có thể thấy các logo được hiển thị bởi công cụ, không phải bất kỳ ASCII art nào bạn có thể đặt trong phản hồi văn bản của bạn

Phản hồi theo cách thân thiện, hữu ích. Hãy ngắn gọn nhưng đầy đủ thông tin.
"""

# ===== HƯỚNG DẪN: TẠO MẪU NHẮC MỚI =====
# Sao chép đoạn này để tạo một nhắc tùy chỉnh mới
"""
def get_custom_assistant_prompt() -> str:
    '''Tạo một nhắc tùy chỉnh cho trợ lý với nhiều công cụ.'''
    return f'''Bạn là một trợ lý AI thân thiện với nhiều khả năng.

{get_current_date_str()}

{MEMORY_INSTRUCTIONS}

{TOOL_USAGE_INSTRUCTIONS}

# Thêm hướng dẫn công cụ mới ở đây:
# {WEATHER_TOOL_INSTRUCTIONS}

Bạn có thể thực hiện các hành động sau:
1. Hiển thị logo khi được yêu cầu
2. [Thêm các khả năng mới ở đây]

HƯỚNG DẪN QUAN TRỌNG:
1. Khi người dùng yêu cầu chức năng cụ thể, sử dụng công cụ tương ứng
2. [Thêm các hướng dẫn quan trọng khác ở đây]

Phản hồi theo cách thân thiện, hữu ích. Hãy ngắn gọn nhưng đầy đủ thông tin.
'''
"""

# ===== HƯỚNG DẪN: HÀM KẾT HỢP NHẮC =====
# Hàm để kết hợp các thành phần nhắc
def create_custom_prompt(
    role_description: str,
    include_memory: bool = True,
    include_tools: bool = False,
    additional_instructions: str = ""
) -> str:
    """
    Tạo một nhắc hệ thống tùy chỉnh bằng cách kết hợp các thành phần khác nhau.
    
    Args:
        role_description: Mô tả cốt lõi về vai trò của agent
        include_memory: Liệu có bao gồm hướng dẫn bộ nhớ hay không
        include_tools: Liệu có bao gồm hướng dẫn sử dụng công cụ hay không
        additional_instructions: Bất kỳ hướng dẫn tùy chỉnh bổ sung nào
        
    Returns:
        Một chuỗi nhắc hệ thống đã được định dạng
    """
    components = [role_description, get_current_date_str()]
    
    if include_memory:
        components.append(MEMORY_INSTRUCTIONS)
    
    if include_tools:
        components.append(TOOL_USAGE_INSTRUCTIONS)
        # Thêm hướng dẫn công cụ khác tại đây nếu cần
        # components.append(WEATHER_TOOL_INSTRUCTIONS)
    
    if additional_instructions:
        components.append(additional_instructions)
    
    return "\n\n".join(components)

# ===== HƯỚNG DẪN: TÙY CHỈNH THÊM =====
# Khi bạn đã tạo prompt mới, cập nhật file agent.py để sử dụng nó:
"""
# Trong core/agent.py:
from agent_template.utils.prompts import get_custom_assistant_prompt

# Khởi tạo agent với prompt tùy chỉnh
agent = Agent[
    Deps,
    Union[str, LogoResult, NewToolResult]
](
    MODEL_NAME,
    # Sử dụng prompt tùy chỉnh thay vì prompt mặc định
    system_prompt=get_custom_assistant_prompt(),
    retries=2,
)
""" 