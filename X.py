import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from pytube import Playlist
import threading

def browse_folder():
    global download_folder
    download_folder = filedialog.askdirectory()
    folder_label.config(text=f"Download Folder: {download_folder}")

def download_playlist():
    playlist_url = playlist_url_entry.get()
    playlist = Playlist(playlist_url)
    
    def download_videos():
        total_videos = len(playlist.video_urls)
        downloaded_videos = 0

        for video in playlist.videos:
            video_title = video.title
            download_status_label.config(text=f"Downloading: {video_title}")
            video.streams.get_highest_resolution().download(output_path=download_folder)
            downloaded_videos += 1
            progress = (downloaded_videos / total_videos) * 100
            progress_bar["value"] = progress
            download_status_label.config(text=f"Downloaded: {video_title} ({int(progress)}%)")

        download_status_label.config(text="Download completed!")
        progress_bar["value"] = 0

    # Tạo một luồng riêng biệt để thực hiện tải xuống
    download_thread = threading.Thread(target=download_videos)
    download_thread.start()

# Tạo cửa sổ tkinter
root = tk.Tk()
root.title("YouTube Playlist Downloader")
root.geometry("500x500")

# Đặt cửa sổ giao diện vào giữa màn hình
window_width = 500
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
# Tạo các thành phần giao diện
playlist_url_label = tk.Label(root, text="Playlist URL:")
playlist_url_label.pack()

playlist_url_entry = tk.Entry(root, width=50)
playlist_url_entry.pack()

browse_button = tk.Button(root, text="Browse Folder", command=browse_folder)
browse_button.pack()

folder_label = tk.Label(root, text="Download Folder: None")
folder_label.pack()

download_button = tk.Button(root, text="Download Playlist", command=download_playlist)
download_button.pack()

download_status_label = tk.Label(root, text="")
download_status_label.pack()

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack()

# Khởi chạy ứng dụng
root.mainloop()
