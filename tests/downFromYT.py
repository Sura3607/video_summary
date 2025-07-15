import yt_dlp
import os

def download_youtube_video(url: str, save_path: str) -> str:
    try:
        os.makedirs(save_path, exist_ok=True)

        ydl_opts = {
            'format': 'best[ext=mp4]',  # Chỉ lấy stream đã có sẵn cả video + audio
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'merge_output_format': 'mp4',  
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            print(f"Tải thành công: {file_path}")
            return file_path

    except Exception as e:
        print(f"Lỗi khi tải video: {e}")
        return ""

# Ví dụ sử dụng
if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=jgyTwWtvMdE"  # Thay link thật vào đây
    save_path = r"D:\Project_Management\video_summary\data"
    download_youtube_video(url, save_path)
