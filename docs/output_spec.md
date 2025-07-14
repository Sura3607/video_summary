## 1. Cấu trúc thư mục đầu ra

Khi nhập đầu vào là **một thư mục chứa nhiều video**, ví dụ:

```
input_videos/
├── video1.mp4
├── video2.mp4
└── ...
```

Thì hệ thống sẽ xuất ra:

```
output/
├── video1.json
├── video2.json
└── ...
```

Mỗi file `.json` tương ứng với một video gốc, được đặt tên theo `video_id`.

---

## 2. Định dạng JSON

### Cấu trúc tổng thể

```json
{
  "video_id": "abc123",
  "source_path": "input_videos/abc123.mp4",
  "duration": 812.45,
  "chunks": [
    {
      "start": 12.3,
      "end": 45.6,
      "transcript": "...",
      "summary": "...",
      "keywords": ["..."],
      "vector": [0.1, 0.2, ...],
      "frame": "data:image/jpeg;base64,...",
      "meta": {
        "chunk_index": 0,
        "length": 33.3
      }
    }
  ]
}
```

---

### Trường bắt buộc trong mỗi chunk

| Tên trường   | Kiểu dữ liệu    | Bắt buộc | Mô tả                                        |
| ------------ | --------------- | -------- | -------------------------------------------- |
| `start`      | float           | ✔        | Timestamp bắt đầu đoạn                       |
| `end`        | float           | ✔        | Timestamp kết thúc đoạn                      |
| `transcript` | string          | ✔        | Nội dung thoại từ Whisper                    |
| `summary`    | string          | ✔        | Tóm tắt đoạn                                 |
| `keywords`   | list\[string]   | ✔        | Từ khoá chính                                |
| `vector`     | list\[float]    | ✔        | Embedding FLAVA (L2-normalized)              |
| `frame`      | string (base64) | ✖        | Ảnh keyframe (tuỳ chọn)                      |
| `meta`       | dict            | ✔        | Metadata bổ sung (chunk index, duration,...) |

---

## 3. Ràng buộc kỹ thuật

* Mỗi file `.json` phải là **valid UTF-8 JSON**, đọc được bằng `json.load()`
* Tất cả vector phải được **L2 chuẩn hóa**, có độ dài cố định (ví dụ 768)
* `summary` không được trùng transcript
* Không được thiếu trường bắt buộc trong bất kỳ chunk nào
* `chunk_index` phải tăng dần và không trùng

---

## 4. Import được vào Vector DB?

**Có.** Toàn bộ output đã được thiết kế để tương thích trực tiếp với các Vector DB như Weaviate, Qdrant, Elasticsearch (w/ dense vector),...

Chỉ cần map từng chunk thành một object trong DB với:

* `vector` → indexed field
* `summary`, `keywords`, `transcript` → searchable field
* `start`, `end`, `video_id` → filter/sort metadata

Có thể truy vấn semantic theo vector hoặc hybrid search theo từ khóa.

---

## 5. Khi đầu vào là thư mục?

Nếu bạn truyền vào một thư mục (ví dụ `"./videos"`), hệ thống sẽ:

* Duyệt toàn bộ `.mp4`, `.mov` trong thư mục
* Xử lý từng video theo pipeline: chunk → extract → embed → enrich → format
* Lưu mỗi video thành 1 file `.json` trong thư mục `output/`

---

## 6. Gợi ý tên file output

| Video đầu vào             | File JSON đầu ra   |
| ------------------------- | ------------------ |
| `video1.mp4`              | `video1.json`      |
| `abc/xyz/video_final.mp4` | `video_final.json` |

> Nếu `video_id` được xác định tự động → dùng tên file gốc (không đuôi)

