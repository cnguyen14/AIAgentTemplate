# AI Agent Template by Chien Nguyen

## 📖 Giới thiệu

Framework mẫu để xây dựng các agent thông minh sử dụng Large Language Models (LLM) với hỗ trợ đầy đủ cho CLI, API HTTP và tích hợp LangGraph. Được thiết kế để giúp bạn nhanh chóng xây dựng ứng dụng AI mạnh mẽ với khả năng mở rộng cao.

## 📬 Liên hệ

Email: hmchien.nguyen@gmail.com
YouTube: [Where The Idea Is Unlimited](https://www.youtube.com/@wheretheideaisunlimited)

## 🌟 Tính năng

- 🧠 **Memory Persistence**: Lưu trữ và khôi phục lịch sử hội thoại tự động
- 🔄 **LangGraph Integration**: Xây dựng luồng công việc phức tạp dựa trên đồ thị trạng thái
- 🤖 **Pydantic-AI Support**: Định nghĩa tool và schema dễ dàng với type-checking
- 🛠️ **Extensible Architecture**: Dễ dàng thêm công cụ, luồng xử lý và khả năng mới
- 💻 **Rich CLI**: Tương tác trực tiếp qua terminal với các lệnh hệ thống
- 🌐 **REST API**: API hoàn chỉnh để tích hợp với các ứng dụng web và mobile
- 🔀 **Dual Mode**: Chạy cả chế độ CLI và API trên cùng một instance

## 🚀 Bắt đầu hành trình

### ⚙️ Cài đặt

1. Clone repository:
```bash
git clone [https://github.com/yourusername/agent-template.git](https://github.com/cnguyen14/AIAgentTemplate.git)
cd AIAgentTemplate
```

2. Cài đặt các phụ thuộc:
```bash
pip install -r requirements.txt
```

3. Thiết lập môi trường:
```bash
cp .env.example .env
```

4. Cập nhật file `.env` với API key của bạn:
```
# Chọn một trong các provider sau
OPENAI_API_KEY=your_openai_api_key
#Thêm tùy chọn
#ANTHROPIC_API_KEY=your_anthropic_api_key

# Tùy chỉnh model (mặc định là openai:gpt-4o-mini)
MODEL_NAME=openai:gpt-4o
TEMPERATURE=0.7
```

## 🚀 Khởi động hệ thống

### Chế độ tương tác (mới)

```bash
# Khởi động trong chế độ tương tác để lựa chọn CLI hay API
python -m agent_template.main
```

Khi chạy mà không có tham số, agent sẽ hỏi bạn muốn chạy ở chế độ CLI hay API, và các tùy chọn khác như port và processing mode.

### Chỉ định chế độ qua command line

```bash
# Khởi tạo hệ thống với giao diện CLI
python -m agent_template.main

# Chạy API server
python -m agent_template.main --api --port 5000

# Chạy trong chế độ tương tác với cờ 
python -m agent_template.main --interactive
```

### Tham số dòng lệnh

| Tham số | Mô tả |
|---------|-------|
| `--api`, `-a` | Chạy ứng dụng dưới dạng API server |
| `--port`, `-p` | Chỉ định port cho API server (mặc định: 8000) |
| `--host` | Chỉ định host cho API server (mặc định: 0.0.0.0) |
| `--legacy`, `-l` | Sử dụng chế độ xử lý legacy thay vì LangGraph |
| `--thread`, `-t` | Chỉ định thread ID để tiếp tục hội thoại |
| `--interactive`, `-i` | Chạy trong chế độ tương tác, hỏi người dùng chọn CLI hay API |

## 💬 Tương tác với Agent

### Sử dụng CLI - Giao diện dòng lệnh

Khi khởi động CLI, bạn có thể sử dụng các lệnh sau:

| Lệnh | Mô tả |
|------|-------|
| `/help` | Hiển thị danh sách lệnh |
| `/exit` | Thoát ứng dụng |
| `/history` | Hiển thị lịch sử hội thoại |
| `/conversations` | Liệt kê tất cả hội thoại đã lưu |
| `/load ID` | Tải một hội thoại từ ID |
| `/delete ID` | Xóa hội thoại |
| `/new` | Tạo hội thoại mới |
| `/graph` | Chuyển sang chế độ xử lý LangGraph |
| `/legacy` | Chuyển sang chế độ xử lý legacy |
| `/logo [style]` | Hiển thị logo (kiểu: default, minimal, fancy) |

## 🌐 REST API

Khi chạy ở chế độ API server, các endpoint sau có sẵn:

### Endpoints

| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/health` | GET | Kiểm tra trạng thái API |
| `/send_message` | POST | Gửi tin nhắn đến agent |
| `/conversations` | GET | Lấy danh sách hội thoại |
| `/conversations` | POST | Tạo hội thoại mới |
| `/conversations/{thread_id}` | DELETE | Xóa một hội thoại |
| `/conversations/{thread_id}/history` | GET | Lấy lịch sử hội thoại |
| `/config` | GET | Lấy cấu hình hiện tại |
| `/config` | POST | Cập nhật cấu hình |

### Ví dụ sử dụng API

```python
import requests

# Địa chỉ API
API_URL = "http://localhost:5000"

# Tạo một hội thoại mới
response = requests.post(f"{API_URL}/conversations")
thread_id = response.json()["thread_id"]

# Gửi tin nhắn
response = requests.post(
    f"{API_URL}/send_message",
    json={
        "message": "Xin chào, bạn có thể giúp tôi không?",
        "thread_id": thread_id
    }
)
print(response.json()["response"])

# Lấy lịch sử hội thoại
response = requests.get(f"{API_URL}/conversations/{thread_id}/history")
history = response.json()["history"]
```

### Tài liệu API

Khi API server đang chạy, bạn có thể truy cập tài liệu tương tác tại:
```
http://localhost:5000/docs
```

## 🧩 Khám phá kiến trúc và tùy biến

### Cấu trúc dự án

```
agent_template/
├── config.py               # Cấu hình ứng dụng
├── main.py                 # Điểm vào chính
├── core/                   # Module cốt lõi
│   ├── agent.py            # Định nghĩa agent và tools
│   ├── agent_service.py    # Service xử lý tin nhắn
│   ├── cli_service.py      # Giao diện dòng lệnh
│   └── api_service.py      # REST API service
├── memory/                 # Hệ thống bộ nhớ
│   └── persistence.py      # Lưu trữ và khôi phục bộ nhớ
├── tools/                  # Các công cụ của agent
│   ├── logo.py             # Công cụ hiển thị logo
│   └── tool_template.py    # Mẫu để tạo công cụ mới
├── utils/                  # Tiện ích
│   └── prompts.py          # Định nghĩa prompt hệ thống
└── workflows/              # Luồng công việc LangGraph
    └── graph.py            # Định nghĩa đồ thị trạng thái
```

## 🎯 Cấu hình và tùy chỉnh Prompt

### Cấu trúc Prompt hệ thống

Prompt hệ thống là thành phần quan trọng quyết định cách AI hoạt động. File `utils/prompts.py` chứa định nghĩa các prompt mặc định:

```python
def get_simple_assistant_prompt() -> str:
    """Trả về prompt hệ thống đơn giản cho assistant."""
    return """Bạn là một trợ lý AI hữu ích. Trả lời các câu hỏi của người dùng một cách chi tiết và chính xác.
    
    Khi cần thiết, bạn có thể sử dụng các công cụ được cung cấp để hoàn thành nhiệm vụ.
    
    Luôn duy trì một giọng điệu thân thiện và chuyên nghiệp.
    """
```

### Tùy chỉnh Prompt qua biến môi trường

Hệ thống được thiết kế để dễ dàng tùy chỉnh prompt và settings thông qua biến môi trường, không cần chỉnh sửa code:

```env
# System Prompts - Optional
DEFAULT_PROMPT=Bạn là một trợ lý AI hữu ích, chuyên về trả lời câu hỏi về AI.
ADVANCED_PROMPT=Bạn là một chuyên gia kỹ thuật với kiến thức sâu rộng về lập trình.
LIGHT_PROMPT=Bạn là một trợ lý AI nhỏ gọn cho các câu trả lời nhanh và súc tích.

# Model Settings
TEMPERATURE=0.7
MAX_TOKENS=1000
RETRIES=2
```

Cấu trúc centralized cho phép bạn:
1. **Ghi đè prompt mặc định**: Thông qua biến môi trường `DEFAULT_PROMPT`, `ADVANCED_PROMPT`, `LIGHT_PROMPT`
2. **Điều chỉnh model settings**: Thay đổi `TEMPERATURE`, `MAX_TOKENS`, `RETRIES` cho từng loại model
3. **Dễ dàng A/B testing**: Thử nghiệm nhiều prompt khác nhau mà không cần sửa code

### Cách tùy chỉnh Prompt

1. **Tùy chỉnh prompt đơn giản**:
   Mở file `utils/prompts.py` và sửa đổi nội dung của hàm `get_simple_assistant_prompt()`:

   ```python
   def get_simple_assistant_prompt() -> str:
       """Trả về prompt hệ thống tùy chỉnh."""
       return """Bạn là Chien AI Assistant, một trợ lý thông minh chuyên về xử lý ngôn ngữ tự nhiên và lập trình.
       
       Nguyên tắc hoạt động của bạn:
       1. Luôn phân tích kỹ yêu cầu người dùng trước khi trả lời
       2. Cung cấp nội dung chính xác, cấu trúc rõ ràng và dễ hiểu
       3. Khi được yêu cầu viết code, đảm bảo code có comment và tuân thủ best practices
       4. Sử dụng công cụ có sẵn khi cần thiết để tăng độ chính xác
       
       Phong cách giao tiếp:
       - Chuyên nghiệp nhưng thân thiện
       - Sử dụng ngôn ngữ dễ hiểu, tránh quá chuyên môn nếu không cần thiết
       - Trình bày thông tin có cấu trúc, sử dụng bullet points và mã định dạng khi phù hợp
       """
   ```

2. **Tạo nhiều loại prompt khác nhau**:
   Bạn có thể tạo các hàm prompt khác nhau phù hợp với từng ngữ cảnh sử dụng:

   ```python
   def get_technical_assistant_prompt() -> str:
       """Prompt cho assistant chuyên về kỹ thuật."""
       return """Bạn là một chuyên gia kỹ thuật, tập trung vào việc cung cấp hướng dẫn và giải pháp chính xác.
       Luôn ưu tiên độ chính xác kỹ thuật và tuân thủ best practices trong các câu trả lời.
       """
   
   def get_creative_assistant_prompt() -> str:
       """Prompt cho assistant sáng tạo."""
       return """Bạn là một trợ lý sáng tạo, chuyên giúp người dùng phát triển ý tưởng mới và tiếp cận vấn đề theo hướng độc đáo.
       Khuyến khích tư duy phá cách và cung cấp nhiều góc nhìn đa dạng.
       """
   ```

3. **Sử dụng prompt tùy chỉnh với agent**:
   Sau khi tạo prompt, cập nhật agent để sử dụng prompt mới:

   ```python
   # Trong agent.py
   from agent_template.utils.prompts import get_technical_assistant_prompt
   
   # Sử dụng prompt kỹ thuật cho agent
   agent = Agent[Deps, Union[str, LogoResult]](
       MODEL_NAME,
       system_prompt=get_technical_assistant_prompt(),
       retries=2,
   )
   ```

### Cấu trúc Prompt hiệu quả

Một system prompt hiệu quả thường bao gồm các thành phần sau:

1. **Định nghĩa vai trò**: Mô tả agent là ai, chuyên về lĩnh vực gì
2. **Nguyên tắc hoạt động**: Các quy tắc cốt lõi agent nên tuân theo
3. **Phong cách giao tiếp**: Cách thức agent nên trả lời (ngắn gọn, chi tiết, chuyên môn...)
4. **Giới hạn**: Những gì agent nên tránh hoặc không được làm
5. **Định dạng output**: Cấu trúc kết quả mong muốn nếu cần theo format cụ thể

Ví dụ prompt toàn diện:

```python
def get_comprehensive_assistant_prompt() -> str:
    return """
    # Định nghĩa vai trò
    Bạn là Advanced AI Assistant, một trợ lý thông minh được phát triển bởi Chien Nguyen, chuyên về hỗ trợ người dùng trong các tác vụ lập trình, xử lý dữ liệu và tư vấn công nghệ.
    
    # Nguyên tắc hoạt động
    1. Phân tích: Luôn phân tích kỹ yêu cầu trước khi trả lời
    2. Chính xác: Cung cấp thông tin chính xác và cập nhật
    3. Toàn diện: Xem xét nhiều khía cạnh của vấn đề
    4. Thực tế: Tập trung vào giải pháp khả thi và có thể triển khai
    5. Công cụ: Sử dụng công cụ có sẵn khi cần để tăng độ chính xác
    
    # Phong cách giao tiếp
    - Chuyên nghiệp nhưng thân thiện
    - Cấu trúc rõ ràng, dễ theo dõi
    - Kết hợp lý thuyết và ví dụ thực tế
    - Đưa ra giải thích ở nhiều cấp độ (cơ bản đến nâng cao) khi phù hợp
    
    # Giới hạn
    - Không đưa ra thông tin sai lệch hoặc gây hiểu nhầm
    - Nêu rõ khi không chắc chắn về thông tin
    - Không quá chi tiết về những khía cạnh không liên quan trực tiếp
    
    # Định dạng output
    Với câu hỏi phức tạp, cấu trúc câu trả lời như sau:
    1. Tóm tắt ngắn gọn (1-2 câu)
    2. Phân tích chi tiết
    3. Ví dụ minh họa nếu cần thiết
    4. Kết luận và đề xuất bước tiếp theo nếu phù hợp
    
    Với yêu cầu viết code:
    1. Giải thích ngắn gọn cách tiếp cận
    2. Cung cấp code đầy đủ với comment
    3. Giải thích các phần quan trọng hoặc phức tạp
    4. Đề xuất cách kiểm thử hoặc mở rộng nếu phù hợp
    """
```

### Sử dụng Prompt động

Bạn có thể tạo prompt động dựa trên ngữ cảnh hoặc cấu hình:

```python
def get_dynamic_prompt(language="vi", expertise_level="intermediate", focus_area=None):
    """Tạo prompt động dựa trên tham số."""
    
    # Cơ sở prompt
    base_prompt = "Bạn là một trợ lý AI thông minh."
    
    # Thêm ngôn ngữ
    if language == "en":
        base_prompt = "You are an intelligent AI assistant."
    
    # Thêm cấp độ chuyên môn
    if expertise_level == "beginner":
        if language == "vi":
            base_prompt += "\nSử dụng ngôn ngữ đơn giản, tránh thuật ngữ kỹ thuật phức tạp."
        else:
            base_prompt += "\nUse simple language, avoid complex technical terms."
    elif expertise_level == "expert":
        if language == "vi":
            base_prompt += "\nSử dụng ngôn ngữ chuyên môn, đi sâu vào chi tiết kỹ thuật khi cần thiết."
        else:
            base_prompt += "\nUse technical language, dive into technical details when necessary."
    
    # Thêm lĩnh vực chuyên sâu
    if focus_area:
        if language == "vi":
            base_prompt += f"\nTập trung vào lĩnh vực: {focus_area}."
        else:
            base_prompt += f"\nFocus on the domain: {focus_area}."
    
    return base_prompt

# Sử dụng trong cấu hình
agent = Agent[Deps, Union[str, LogoResult]](
    MODEL_NAME,
    system_prompt=get_dynamic_prompt(
        language="vi",
        expertise_level="intermediate",
        focus_area="Machine Learning"
    ),
    retries=2,
)
```

### Thay đổi model và cấu hình

#### Cấu hình qua file .env

Cách đơn giản nhất để thay đổi model là cập nhật file `.env`:

```
# Chọn model - thay đổi ở đây
MODEL_NAME=openai:gpt-4o
# hoặc
MODEL_NAME=anthropic:claude-3-opus-20240229

# Điều chỉnh temperature
TEMPERATURE=0.7
```

#### Sửa đổi trong code

Mở file `agent_template/core/agent.py` và cập nhật các biến cấu hình:

```python
# ===== HƯỚNG DẪN: THAY ĐỔI MODEL =====
# Nếu bạn muốn thay đổi model, hãy cập nhật MODEL_NAME tại đây
# Ví dụ: 'openai:gpt-4-turbo-2024-04-09', 'anthropic:claude-3-opus-20240229'
MODEL_NAME = os.environ.get('MODEL_NAME', 'openai:gpt-4o-mini')
TEMPERATURE = float(os.environ.get('TEMPERATURE', '0.7'))
```

#### Sử dụng model và provider với Pydantic-AI

Pydantic-AI sử dụng cú pháp `provider:model_name` để xác định model, và đã tích hợp sẵn một số provider chính như OpenAI và Anthropic. Không cần phải import các provider riêng lẻ.

1. **Chỉ định model trong cấu hình**:

   ```python
   # Trong agent.py
   MODEL_NAME = os.environ.get('MODEL_NAME', 'openai:gpt-4o-mini')
   
   # Khởi tạo agent với model
   agent = Agent[
       Deps,  # Kiểu dependency 
       Union[str, LogoResult]  # Kiểu kết quả
   ](
       MODEL_NAME,  # Sử dụng cú pháp "provider:model_name"
       system_prompt=get_simple_assistant_prompt(),
       retries=2,
   )
   ```

2. **Cấu hình trong file .env**:

   ```
   # Các model được hỗ trợ sẵn
   MODEL_NAME=openai:gpt-4o
   # hoặc
   MODEL_NAME=anthropic:claude-3-opus-20240229
   # hoặc
   MODEL_NAME=google-gla:gemini-1.5-flash
   ```

#### Thêm setting cho model cụ thể

Pydantic-AI cho phép cấu hình model chi tiết thông qua `model_settings`:

```python
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings

# Cấu hình model khi khởi tạo agent
agent = Agent[Deps, str](
    'openai:gpt-4o',
    model_settings=ModelSettings(
        temperature=0.7,
        max_tokens=1000,
        timeout=30.0,
    ),
    system_prompt="Bạn là một trợ lý AI hữu ích."
)

# Hoặc cấu hình khi gọi
response = await agent.run(
    "Hôm nay thời tiết thế nào?",
    model_settings={"temperature": 0.2}  # Ghi đè setting cho lần chạy này
)
```

#### Sử dụng nhiều model trong cùng một dự án

Bạn có thể định nghĩa nhiều agent khác nhau với các model khác nhau trong một dự án:

```python
# Trong agent.py hoặc module tùy chỉnh

# Định nghĩa agent sử dụng GPT-4o cho nhiệm vụ phức tạp
advanced_agent = Agent[Deps, Union[str, LogoResult]](
    'openai:gpt-4o',
    system_prompt="Bạn là một trợ lý AI cao cấp với khả năng xử lý các vấn đề phức tạp.",
    model_settings=ModelSettings(temperature=0.7)
)

# Định nghĩa agent sử dụng model nhẹ hơn cho nhiệm vụ đơn giản
light_agent = Agent[Deps, Union[str, LogoResult]](
    'openai:gpt-4o-mini',
    system_prompt="Bạn là một trợ lý AI nhỏ gọn cho các câu trả lời nhanh.",
    model_settings=ModelSettings(temperature=0.9, max_tokens=500)
)

# Định nghĩa agent với Claude của Anthropic
creative_agent = Agent[Deps, Union[str, LogoResult]](
    'anthropic:claude-3-opus-20240229',
    system_prompt="Bạn là một trợ lý AI sáng tạo, chuyên về nội dung nghệ thuật.",
    model_settings=ModelSettings(temperature=1.0)
)
```

#### Chỉ định tool cho từng model cụ thể

Bạn có thể sử dụng decorator để đăng ký tool với các agent cụ thể, cho phép mỗi agent có các công cụ khác nhau:

```python
# Đăng ký tool cho agent nâng cao
@advanced_agent.tool
async def complex_analysis(
    ctx: RunContext[Deps],
    data: str,
    depth: int = 3
) -> str:
    """Thực hiện phân tích dữ liệu phức tạp (chỉ có ở agent nâng cao)."""
    # Triển khai phân tích phức tạp
    return f"Phân tích chi tiết: {data} với độ sâu {depth}"

# Đăng ký tool cho agent sáng tạo
@creative_agent.tool
async def generate_poem(
    ctx: RunContext[Deps],
    theme: str,
    style: str = "free_verse"
) -> str:
    """Tạo một bài thơ dựa trên chủ đề (chỉ có ở agent sáng tạo)."""
    # Triển khai tạo thơ
    return f"Bài thơ về {theme} theo phong cách {style}"

# Đăng ký tool dùng chung cho tất cả các agent
@advanced_agent.tool
@light_agent.tool
@creative_agent.tool
async def get_current_time(ctx: RunContext[Deps]) -> str:
    """Lấy thời gian hiện tại (có sẵn ở tất cả các agent)."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
```

Bạn cũng có thể tạo helper function để đăng ký tool cho nhiều agent cùng lúc:

```python
def register_for_all_agents(func):
    """Đăng ký một tool cho tất cả các agent."""
    advanced_agent.tool(func)
    light_agent.tool(func)
    creative_agent.tool(func)
    return func

@register_for_all_agents
async def search_web(ctx: RunContext[Deps], query: str) -> str:
    """Tìm kiếm thông tin trên web (có sẵn ở tất cả các agent)."""
    # Triển khai tìm kiếm web
    return f"Kết quả tìm kiếm cho '{query}'"
```

Sau đó, bạn có thể triển khai logic để chọn đúng agent dựa trên yêu cầu người dùng:

```python
async def process_with_optimal_agent(user_input: str, context: dict) -> str:
    """Chọn agent tối ưu dựa trên đầu vào và ngữ cảnh của người dùng."""
    
    # Phân tích đầu vào để xác định loại nhiệm vụ
    if is_creative_task(user_input):
        # Sử dụng agent sáng tạo cho các nhiệm vụ liên quan đến nghệ thuật
        result = await creative_agent.run(user_input, deps=context.get('deps'))
    elif is_complex_task(user_input):
        # Sử dụng agent nâng cao cho các nhiệm vụ phức tạp
        result = await advanced_agent.run(user_input, deps=context.get('deps'))
    else:
        # Sử dụng agent nhẹ cho các câu hỏi đơn giản
        result = await light_agent.run(user_input, deps=context.get('deps'))
    
    return result.data
```

Bạn cũng có thể cấu hình để chọn model động dựa trên cấu hình:

```python
def get_agent_for_config(config: AppConfig) -> Agent:
    """Trả về agent phù hợp dựa trên cấu hình."""
    
    model_name = config.model_name
    
    # Tạo agent với model được chỉ định trong cấu hình
    agent = Agent[Deps, Union[str, LogoResult]](
        model_name,
        system_prompt=get_simple_assistant_prompt(),
        model_settings=ModelSettings(temperature=config.temperature)
    )
    
    return agent

# Trong AgentService
def __init__(self, config: AppConfig):
    self.config = config
    self.agent = get_agent_for_config(config)
```

#### Tích hợp model tùy chỉnh/local

Để tích hợp mô hình tự host (như Ollama, LM Studio):

1. **Tạo custom provider** bằng cách kế thừa từ `BaseProvider`:

```python
from pydantic_ai.providers.base import BaseProvider
from typing import Any, Dict, Optional
import httpx

class OllamaProvider(BaseProvider):
    """Provider cho mô hình Ollama local."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model_name: str = "llama3"):
        self.base_url = base_url
        self.model_name = model_name
        
    async def complete(
        self, 
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Gửi yêu cầu đến Ollama API."""
        async with httpx.AsyncClient() as client:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = await client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model_name,
                    "messages": messages,
                    "temperature": temperature,
                    "stream": False
                }
            )
            response.raise_for_status()
            result = response.json()
            
            return {
                "content": result["message"]["content"],
                "model": result["model"]
            }

# Sử dụng provider tùy chỉnh
ollama_provider = OllamaProvider(model_name="llama3")

# Khởi tạo agent với provider tùy chỉnh
agent = Agent[Deps, Union[str, LogoResult]](
    "custom:llama3",  # Sử dụng tên tùy ý khi có custom provider
    system_prompt=get_simple_assistant_prompt(),
    retries=2,
    provider=ollama_provider
)
```

2. **Cập nhật file `.env.example` và `.env`** để thêm các biến môi trường mới:

```
# Local Model Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL_NAME=llama3
```

### Thay đổi system prompt

1. Mở file `agent_template/utils/prompts.py`
2. Sửa đổi hàm `get_simple_assistant_prompt()` để thay đổi system prompt:

```python
def get_simple_assistant_prompt() -> str:
    """Trả về prompt hệ thống đơn giản cho assistant."""
    return """Bạn là một trợ lý AI hữu ích. Trả lời các câu hỏi của người dùng một cách chi tiết và chính xác.
    
    Khi cần thiết, bạn có thể sử dụng các công cụ được cung cấp để hoàn thành nhiệm vụ.
    
    Luôn duy trì một giọng điệu thân thiện và chuyên nghiệp.
    """
```

### Tạo agent mới hoàn toàn

Để tạo một agent mới từ đầu:

1. Tạo file `my_agent.py` trong thư mục `agent_template/core/`:

```python
"""
Triển khai agent tùy chỉnh mới.
"""

import os
from typing import Union, Dict, Any
from datetime import datetime

import logfire
from pydantic_ai import Agent, RunContext
from dotenv import load_dotenv

# Tải biến môi trường
load_dotenv()
logfire.configure(send_to_logfire='if-token-present')

# Cấu hình model
MODEL_NAME = "openai:gpt-4o"
TEMPERATURE = 0.7

# Khởi tạo agent
custom_agent = Agent[
    CustomDeps,  # Định nghĩa dependencies của bạn
    Union[str, CustomResult]  # Các loại kết quả có thể trả về
](
    MODEL_NAME,
    system_prompt="Prompt hệ thống tùy chỉnh của bạn",
    temperature=TEMPERATURE,
    retries=2,
)

# Đăng ký tools
@custom_agent.tool
async def custom_tool(
    ctx: RunContext[CustomDeps],
    param1: str
) -> CustomResult:
    """Mô tả công cụ tùy chỉnh."""
    # Triển khai logic
    return CustomResult(result="Kết quả công cụ")

# Hàm xử lý đầu vào
async def process_with_custom_agent(user_input: str) -> str:
    """Xử lý đầu vào với agent tùy chỉnh."""
    # Triển khai logic xử lý
    result = await custom_agent.run(user_input)
    return result.data
```

2. Tích hợp agent mới vào `agent_service.py`:

```python
from agent_template.core.my_agent import process_with_custom_agent

# Trong AgentService
async def process_message(self, message: str, thread_id: Optional[str] = None):
    # ...
    if self.config.use_custom_agent:
        # Sử dụng agent tùy chỉnh
        response = await process_with_custom_agent(message)
    # ...
```

### Tạo công cụ mới

1. Tạo một file mới trong `agent_template/tools/`
2. Định nghĩa lớp kết quả sử dụng Pydantic
3. Triển khai các hàm tiện ích
4. Trong `agent.py`, đăng ký công cụ mới với `@agent.tool` decorator:

```python
@agent.tool
async def your_tool_name(
    ctx: RunContext[Deps],
    param1: str,
    param2: int = 0
) -> YourResultType:
    """Mô tả công cụ của bạn."""
    # Triển khai logic
    result = your_utility_function(param1, param2)
    return YourResultType(result=result)
```

### Tùy chỉnh Workflow LangGraph

Nếu muốn thêm các node hoặc edge mới vào đồ thị LangGraph:

1. Mở `agent_template/workflows/graph.py`
2. Thêm các node và edge mới:
```python
# Thêm node mới
workflow.add_node("my_custom_node", my_custom_function)

# Thêm edge
workflow.add_edge("process", "my_custom_node")
workflow.add_edge("my_custom_node", "continue")
```

## 🚀 Hướng dẫn xây dựng Agent hoàn chỉnh từ A-Z

### Bước 1: Thiết lập cơ bản

1. Clone repo và cài đặt dependencies:
   ```bash
   git clone https://github.com/yourusername/agent-template.git
   cd agent-template
   pip install -r requirements.txt
   ```

2. Cấu hình API keys và model:
   ```bash
   cp .env.example .env
   # Chỉnh sửa file .env với API key và model của bạn
   ```

### Bước 2: Tùy chỉnh Agent

1. **Chọn model phù hợp**:
   - Cập nhật `MODEL_NAME` trong `.env` hoặc `agent.py`
   - Cân nhắc sử dụng nhiều model cho các tác vụ khác nhau

2. **Điều chỉnh system prompt**:
   - Sửa đổi hàm `get_simple_assistant_prompt()` trong `utils/prompts.py`
   - Định hình personality và khả năng của agent

3. **Tạo tools cần thiết**:
   - Tạo file mới trong `tools/` cho mỗi khả năng
   - Định nghĩa kết quả trả về sử dụng Pydantic
   - Đăng ký tool với decorator `@agent.tool`

### Bước 3: Triển khai giao diện

1. **Chọn giữa CLI và API hoặc cả hai**:
   - Tùy chỉnh các lệnh CLI hoặc endpoint API nếu cần
   - Tích hợp bộ nhớ để lưu trữ hội thoại

2. **Tích hợp bộ nhớ**:
   - Cấu hình `memory_dir` trong `.env` hoặc `config.py`
   - Tùy chỉnh cách lưu trữ và khôi phục bộ nhớ nếu cần

### Bước 4: Mở rộng và nâng cao

1. **Scale với nhiều model**:
   ```python
   # Trong agent.py
   advanced_agent = Agent[Deps, Union[str, Result]](
       'openai:gpt-4o',
       system_prompt="...",
       model_settings=ModelSettings(temperature=0.7)
   )
   
   light_agent = Agent[Deps, Union[str, Result]](
       'openai:gpt-4o-mini',
       system_prompt="...",
       model_settings=ModelSettings(temperature=0.8)
   )
   ```

2. **Phân phối tool theo nhu cầu**:
   ```python
   # Tool cho tất cả agent
   @register_for_all_agents
   async def common_tool(ctx, param): ...
   
   # Tool chỉ cho advanced agent
   @advanced_agent.tool
   async def complex_tool(ctx, param): ...
   ```

3. **Triển khai logic chọn agent**:
   ```python
   # Trong process_input
   if "phức tạp" in user_input or len(user_input) > 200:
       active_agent = advanced_agent
   else:
       active_agent = light_agent
   ```

### Bước 5: Kiểm thử và triển khai

1. **Kiểm thử**:
   - Kiểm tra các tool riêng lẻ
   - Thử nghiệm các luồng hội thoại hoàn chỉnh

2. **Triển khai**:
   - CLI: Chạy `python -m agent_template.main`
   - API: Chạy `python -m agent_template.main --api`
   - Hoặc tích hợp agent vào ứng dụng lớn hơn

### Bước 6: Giám sát và cải tiến

1. **Thu thập feedback**:
   - Lưu lịch sử hội thoại và phân tích
   - Sử dụng LogFire để giám sát nếu cần

2. **Cải tiến liên tục**:
   - Cập nhật prompt hệ thống
   - Thêm tool mới
   - Điều chỉnh cấu hình model

Theo quy trình này, bạn có thể xây dựng một agent hoàn chỉnh, phù hợp với nhu cầu cụ thể và có khả năng mở rộng theo thời gian.

## 🧪 Kiểm thử

```bash
# Test API
python -m pytest tests/test_api.py -v

# Test workflow
python -m pytest tests/test_workflows.py -v
```

## 📚 Tài nguyên

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Pydantic-AI Documentation](https://docs.pydantic-ai.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
