```
video_summary/
├── api/
│   ├── __init__.py
│   ├── main.py
│   └── routes/
│       └── process.py
│
├── core/
│   ├── __init__.py
│   ├── chunking.py           # Tách scene
│   ├── extract.py            # Whisper + keyframe
│   ├── embed.py              # FLAVA embedding
│   ├── enrich.py             # Summary + keywords
│   └── formatter.py          # Tạo file JSON
│
├── scripts/
│   ├── run_single_video.py   # Test flow đơn giản
│   └── run_batch.py          # Xử lý folder video
│
├── tests/
│   ├── __init__.py
│   ├── test_chunking.py
│   ├── test_extract.py
│   ├── test_embed.py
│   ├── test_enrich.py
│   └── test_formatter.py
│
├── data/
│   └── sample1.mp4           # Video mẫu để test
│
├── output/
│   └── sample1.json          # JSON kết quả sau xử lý
│
├── docs/
│   └── module_spec.md 
│
├── requirements.txt
├── Dockerfile
├── .gitignore
├── .env.example
├── README.md
└── CONTRIBUTING.md
```
