Tài liệu này mô tả chi tiết vai trò, input/output, yêu cầu kỹ thuật, kiểm thử và sơ đồ kết nối giữa các thành phần trong hệ thống
---

## Mô tả luồng xử lý tổng thể

```
graph TD
    A[Input: .mp4 video] --> B[chunking.py]
    B --> C[extract.py]
    C --> D[embed.py]
    C --> E[enrich.py]
    D --> F[formatter.py]
    E --> F
    F --> G[Output: JSON file]
````

---

## 1. `core/chunking.py`

* **Vai trò:** Tách video thành các cảnh (scene)
* **Input:** `video_path: str`
* **Output:** `List[Dict[float, float]]` (start/end time)
* **Lưu ý:** Không có cảnh < 2s. Timestamp không được trùng.
* **Test:** Các cảnh tuần tự và hợp lệ.

---

## 2. `core/extract.py`

* **Vai trò:** Trích xuất keyframe và transcript (Whisper)
* **Input:** `video_path: str`, `start`, `end`
* **Output:** `PIL.Image`, `str`
* **Lưu ý:** Whisper,docling,v.v; chọn frame ở giữa đoạn.
* **Test:** Không rỗng, không lỗi âm thanh.

---

## 3. `core/embed.py`

* **Vai trò:** Sinh embedding vector từ text và image (FLAVA)
* **Input:** `text: str`, `image: PIL.Image`
* **Output:** `np.ndarray`, L2-normalized vector
* **Yêu cầu:** Kích thước cố định (thường 768/1024)
* **Test:** Cosine similarity cao, vector chuẩn hóa.

---

## 4. `core/enrich.py`

* **Vai trò:** Tóm tắt và sinh từ khóa từ đoạn transcript
* **Input:** `text: str`
* **Output:** `summary: str`, `keywords: List[str]`
* **Giới hạn:** Summary ≤ 30 từ, max 5 keywords
* **Test:** Không chứa stopwords, khác transcript gốc.

---

## 5. `core/formatter.py`

* **Vai trò:** Gộp kết quả và xuất ra file `.json`
* **Input:** `video_id: str`, `chunk_data_list: List[Dict]`
* **Output:** JSON dạng chuẩn có `vector`, `summary`, `timestamp`, ...
* **Test:** Kiểm tra schema, số lượng chunk khớp.

---

## 6. Mối liên hệ giữa các module

| Tên module     | Gọi đến | Nhận input từ           | Trả output cho          |
| -------------- | ------- | ----------------------- | ----------------------- |
| `chunking.py`  | —       | video                   | `extract.py`            |
| `extract.py`   | Whisper | `chunking.py`           | `embed.py`, `enrich.py` |
| `embed.py`     | FLAVA   | `extract.py`            | `formatter.py`          |
| `enrich.py`    | —       | `extract.py`            | `formatter.py`          |
| `formatter.py` | —       | `embed.py`, `enrich.py` | Output                  |

---

## 7. Yêu cầu toàn hệ thống

* Tất cả vector phải có chuẩn hóa L2
* Kết quả đầu ra phải tái lập được với cùng input
* Xử lý exception rõ ràng tại mọi bước
* Không được phép ghi đè file output trừ khi có flag chỉ định
* Mọi module phải độc lập và có thể gọi riêng để test
