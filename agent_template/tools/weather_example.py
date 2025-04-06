"""
Công cụ thời tiết đơn giản.

Cung cấp thông tin thời tiết cho các địa điểm khác nhau.
"""

from datetime import datetime
from typing import Dict, Any, Tuple, Optional
from pydantic import BaseModel
import random  # Trong ví dụ này, chúng ta sẽ dùng random để giả lập dữ liệu

# 1. ĐỊNH NGHĨA KẾT QUẢ TOOL
class WeatherResult(BaseModel):
    """Kết quả trả về từ công cụ thời tiết."""
    location: str              # Địa điểm yêu cầu
    temperature: float         # Nhiệt độ tính bằng độ C
    conditions: str            # Điều kiện thời tiết (nắng, mưa, v.v.)
    humidity: Optional[int]    # Độ ẩm (%)
    timestamp: str = None      # Thời gian lấy dữ liệu
    
    def __init__(self, **data):
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().isoformat()
        super().__init__(**data)

# 2. CÁC HẰNG SỐ VÀ DỮ LIỆU TĨNH
WEATHER_CONDITIONS = [
    "Nắng", "Mây", "Mưa nhẹ", "Mưa", "Giông bão", 
    "Tuyết", "Sương mù", "Nhiều mây", "Nắng nhẹ"
]

KNOWN_LOCATIONS = {
    "hà nội": {"min_temp": 15, "max_temp": 35},
    "hồ chí minh": {"min_temp": 22, "max_temp": 38},
    "đà nẵng": {"min_temp": 18, "max_temp": 34},
    "huế": {"min_temp": 17, "max_temp": 33},
    "nha trang": {"min_temp": 20, "max_temp": 35},
}

# 3. HÀM TIỆN ÍCH CHÍNH
def get_weather(location: str) -> Tuple[bool, Dict[str, Any]]:
    """Lấy thông tin thời tiết cho một địa điểm.
    
    Trong ví dụ này, chúng ta giả lập dữ liệu thời tiết.
    Trong thực tế, hàm này sẽ gọi API thời tiết.
    
    Args:
        location: Tên địa điểm cần lấy thông tin thời tiết
        
    Returns:
        Tuple gồm (success, weather_data)
    """
    try:
        # Chuẩn hóa tên địa điểm
        location_lower = location.lower().strip()
        
        # Kiểm tra nếu địa điểm có trong danh sách đã biết
        if location_lower in KNOWN_LOCATIONS:
            temp_range = KNOWN_LOCATIONS[location_lower]
            temperature = round(random.uniform(temp_range["min_temp"], temp_range["max_temp"]), 1)
        else:
            # Địa điểm không được biết đến, tạo dữ liệu ngẫu nhiên
            temperature = round(random.uniform(15, 35), 1)
        
        # Tạo dữ liệu thời tiết
        weather_data = {
            "location": location,
            "temperature": temperature,
            "conditions": random.choice(WEATHER_CONDITIONS),
            "humidity": random.randint(40, 95)
        }
        
        # Trong thực tế, đây là nơi bạn sẽ gọi API thời tiết
        # Ví dụ:
        # api_key = os.environ.get("WEATHER_API_KEY")
        # response = requests.get(
        #     f"https://api.weatherservice.com/v1/current",
        #     params={"q": location, "key": api_key}
        # )
        # if response.status_code == 200:
        #     data = response.json()
        #     weather_data = {
        #         "location": data["location"]["name"],
        #         "temperature": data["current"]["temp_c"],
        #         "conditions": data["current"]["condition"]["text"],
        #         "humidity": data["current"]["humidity"]
        #     }
        #     return True, weather_data
        # else:
        #     return False, f"Lỗi API: {response.status_code}"
        
        return True, weather_data
        
    except Exception as e:
        # Xử lý lỗi
        return False, str(e)

# 4. CÁC HÀM PHỤ TRỢ
def validate_location(location: str) -> bool:
    """Kiểm tra tính hợp lệ của địa điểm.
    
    Args:
        location: Tên địa điểm cần kiểm tra
        
    Returns:
        True nếu hợp lệ, False nếu không
    """
    # Trong ví dụ đơn giản này, chúng ta chỉ kiểm tra độ dài
    # Trong thực tế, bạn có thể kiểm tra xem địa điểm có tồn tại không
    return location and len(location) >= 2 and len(location) <= 100

def format_weather_message(weather_data: Dict[str, Any]) -> str:
    """Định dạng thông tin thời tiết thành tin nhắn thân thiện.
    
    Args:
        weather_data: Dữ liệu thời tiết
        
    Returns:
        Chuỗi tin nhắn đã định dạng
    """
    return (
        f"Thời tiết tại {weather_data['location']}: "
        f"{weather_data['temperature']}°C, {weather_data['conditions']}, "
        f"độ ẩm {weather_data['humidity']}%."
    ) 