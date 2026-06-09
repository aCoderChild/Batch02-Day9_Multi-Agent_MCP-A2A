# Đáp Án Bài Tập

File này tổng hợp lời giải cho các bài tập chính trong codelab.

## Exercise 2: Tools và Knowledge Base

### 1. Thêm entry luật lao động

Thêm vào `LEGAL_KNOWLEDGE`:

```python
{
    "id": "labor_law",
    "keywords": ["lao động", "sa thải", "hợp đồng lao động", "labor", "termination"],
    "text": (
        "Theo Bộ luật Lao động Việt Nam 2019, người sử dụng lao động có thể "
        "đơn phương chấm dứt hợp đồng trong các trường hợp: (1) người lao động "
        "thường xuyên không hoàn thành công việc; (2) bị ốm đau, tai nạn đã điều trị "
        "12 tháng chưa khỏi; (3) thiên tai, hỏa hoạn; (4) người lao động đủ tuổi nghỉ hưu."
    ),
}
```

### 2. Tạo tool thời hiệu khởi kiện

```python
@tool
def check_statute_of_limitations(case_type: str) -> str:
    """Kiểm tra thời hiệu khởi kiện theo loại vụ án."""
    limits = {
        "contract": "4 năm (UCC § 2-725)",
        "hợp đồng": "4 năm (UCC § 2-725)",
        "tort": "2-3 năm tùy bang",
        "bồi thường": "2-3 năm tùy bang",
        "property": "5 năm",
        "tài sản": "5 năm",
    }
    return limits.get(case_type.lower(), "Không xác định")
```

Sau đó thêm tool vào danh sách:

```python
tools = [search_legal_knowledge, check_statute_of_limitations]
```

Và xử lý tool call:

```python
elif tool_call["name"] == "check_statute_of_limitations":
    tool_result = check_statute_of_limitations.invoke(tool_call["args"])
```

## Exercise 4: Multi-Agent với Privacy Agent

### 1. Routing theo keyword privacy

```python
if any(kw in question_lower for kw in ["data", "privacy", "gdpr", "dữ liệu"]):
    tasks.append(Send("privacy_agent", state))
```

### 2. Implement privacy agent

```python
def privacy_agent(state: State) -> dict:
    """Agent chuyên về bảo vệ dữ liệu cá nhân và GDPR."""
    llm = get_llm()
    prompt = f"""Bạn là chuyên gia về GDPR và luật bảo vệ dữ liệu cá nhân.

Câu hỏi gốc: {state['question']}
Phân tích pháp lý: {state.get('law_analysis', 'N/A')}

Hãy phân tích các vấn đề về privacy, GDPR, quyền riêng tư, data protection
và nghĩa vụ xử lý data breach nếu có."""

    response = llm.invoke([HumanMessage(content=prompt)])
    return {"privacy_analysis": response.content}
```

### 3. Kết nối vào graph

```python
graph.add_node("privacy_agent", privacy_agent)
graph.add_edge("privacy_agent", "aggregate_results")
```

Trong `aggregate_results`, thêm:

```python
if state.get("privacy_analysis"):
    sections.append(f"🔒 PHÂN TÍCH PRIVACY/GDPR:\n{state['privacy_analysis']}")
```

## Bài Tập Cộng Điểm

### Demo HTML

Mở file `demos/agent_interaction_demo.html` bằng trình duyệt để xem mô phỏng tương tác Stage 4 và Stage 5.

### Đo latency Stage 5

Chạy:

```bash
./start_all.sh
uv run python test_client.py
```

`test_client.py` sẽ in thêm dòng:

```text
Latency: <số giây>s
```

### Phương án giảm latency

Phương án chính là chạy Tax Agent và Compliance Agent song song bằng LangGraph `Send` API thay vì gọi tuần tự. Nếu gọi tuần tự, tổng thời gian xấp xỉ:

```text
law_analysis + tax_agent + compliance_agent + aggregate
```

Khi chạy song song, thời gian xấp xỉ:

```text
law_analysis + max(tax_agent, compliance_agent) + aggregate
```

Vì vậy lợi ích lớn nhất xuất hiện khi các specialist agents có thời gian xử lý gần nhau.
