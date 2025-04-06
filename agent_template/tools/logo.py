"""
Các hàm tiện ích cho công cụ logo.

Cung cấp chức năng hiển thị logo ASCII art trong CLI.
"""

from datetime import datetime
from typing import Tuple, Dict, Optional
from pydantic import BaseModel

# ===== HƯỚNG DẪN: TẠO MẪU KẾT QUẢ TOOL =====
# Mỗi tool cần định nghĩa một class kết quả kế thừa từ BaseModel
# Class này sẽ xác định dữ liệu được trả về từ tool
class LogoResult(BaseModel):
    """Kết quả trả về bởi công cụ logo."""
    displayed: bool
    style: str
    timestamp: str = None
    
    def __init__(self, **data):
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().isoformat()
        super().__init__(**data)

# ===== HƯỚNG DẪN: TẠO DATA CHO TOOL =====
# Nếu tool của bạn cần dữ liệu tĩnh, định nghĩa nó tại đây
# Từ điển các kiểu logo
LOGO_STYLES: Dict[str, str] = {
    "default": """
    _    ___ 
   / \\  |_ _|
  / _ \\  | | 
 / ___ \\ | | 
/_/   \\_\\___|
    AGENT    
    """,
    "minimal": """
  /\\  
 /  \\ 
/----\\
  AI  
    """,
    "fancy": """
 █████╗ ██╗
██╔══██╗██║
███████║██║
██╔══██║██║
██║  ██║██║
╚═╝  ╚═╝╚═╝
 ASSISTANT 
    """
}

# ===== HƯỚNG DẪN: TẠO HÀM TIỆN ÍCH =====
# Tạo các hàm tiện ích để thực hiện chức năng thực tế của tool
# Lưu ý: Các hàm này sẽ được gọi bởi @agent.tool trong core/agent.py
def get_logo(style: str = "default", color: bool = True) -> Tuple[str, str]:
    """Lấy văn bản logo dựa trên kiểu.
    
    Args:
        style: Kiểu logo để lấy ('default', 'minimal', hoặc 'fancy')
        color: Liệu có áp dụng màu cho logo hay không
    
    Returns:
        Tuple gồm (logo_text, style_used)
    """
    # Lấy logo hoặc mặc định nếu không tìm thấy kiểu
    logo = LOGO_STYLES.get(style, LOGO_STYLES["default"])
    used_style = style if style in LOGO_STYLES else "default"
    
    # Áp dụng màu ANSI nếu được yêu cầu
    if color:
        # Màu xanh dương
        logo = f"\033[34m{logo}\033[0m"
    
    return logo, used_style

# ===== HƯỚNG DẪN: TẠO TOOL HOÀN CHỈNH =====
# Tạo các hàm thực hiện hành động cuối cùng của tool
# Ví dụ: trong trường hợp này, hiển thị logo
def display_logo(logo_text: str = None) -> None:
    """Hiển thị logo trong console.
    
    Args:
        logo_text: Văn bản logo để hiển thị (tùy chọn)
    """
    if logo_text is None:
        logo_text, _ = get_logo()
    print(logo_text)

# ===== HƯỚNG DẪN: TẠO TOOL MỚI =====
# Để tạo một tool mới, hãy tạo file mới trong thư mục tools/
# Ví dụ: tools/weather.py

"""
from pydantic import BaseModel
from datetime import datetime
import requests  # hoặc thư viện phù hợp khác

# 1. Định nghĩa class kết quả
class WeatherResult(BaseModel):
    '''Kết quả trả về từ công cụ thời tiết.'''
    location: str
    temperature: float
    conditions: str
    timestamp: str = None
    
    def __init__(self, **data):
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().isoformat()
        super().__init__(**data)

# 2. Định nghĩa hàm tiện ích chính
def get_weather(location: str) -> tuple[float, str]:
    '''
    Hàm này sẽ gọi API thời tiết thực tế.
    '''
    # API key từ biến môi trường
    # api_key = os.environ.get("WEATHER_API_KEY")
    
    # Gọi API thời tiết
    # response = requests.get(f"https://api.example.com/weather?location={location}&key={api_key}")
    # data = response.json()
    
    # Trong ví dụ này, chúng ta giả lập kết quả
    temp = 25.5
    conditions = "Nắng"
    
    return temp, conditions
""" 