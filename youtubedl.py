import sys
import subprocess
import os
import re
from pytube import YouTube
import youtube_dl
import yt_dlp as youtube_dl_2

# ファイル名に使えない文字を削除する関数
def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

# MP4をMP3に変換する関数
def convert_mp4_to_mp3(mp4_file_path, mp3_file_name):
    mp3_file_path = mp3_file_name + '.mp3'
    command = ['ffmpeg', '-i', mp4_file_path, '-vn', '-ab', '128k', '-ar', '44100', '-y', mp3_file_path]
    subprocess.run(command)
    print(f"Converted {mp4_file_path} to {mp3_file_path}")
    # 中間ファイル（MP4）を削除
    os.remove(mp4_file_path)
    print(f"Deleted intermediate file {mp4_file_path}")

# MP4ファイルを最終的な名前にリネームする関数
def rename_video_file(temp_file_path, final_name):
    final_file_path = final_name + '.mp4'
    os.rename(temp_file_path, final_file_path)
    print(f"Saved video as {final_file_path}")
    return final_file_path

# 字幕をダウンロードする関数
def download_subtitles(url, title):
    # まず動画情報を取得してオリジナル言語を特定
    try:
        with youtube_dl_2.YoutubeDL({'quiet': True}) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            # オリジナル言語を取得（利用可能な場合）
            original_lang = info_dict.get('language', 'ja')  # デフォルトは日本語
            print(f"Detected original language: {original_lang}")
    except:
        original_lang = 'ja'  # 取得できない場合は日本語をデフォルト
    
    ydl_opts = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': [original_lang],  # オリジナル言語のみ
        'skip_download': True,
        'outtmpl': title + '.%(ext)s',
        'subtitlesformat': 'vtt',
    }
    try:
        with youtube_dl_2.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            print("Downloaded subtitles with yt_dlp")
            
            # VTTファイルをテキストファイルに変換
            vtt_file = f"{title}.{original_lang}.vtt"
            auto_vtt_file = f"{title}.{original_lang}-auto.vtt"
            
            target_vtt_file = None
            if os.path.exists(vtt_file):
                target_vtt_file = vtt_file
            elif os.path.exists(auto_vtt_file):
                target_vtt_file = auto_vtt_file
            
            if target_vtt_file:
                txt_file_path = title + '.txt'
                all_text = []
                
                with open(target_vtt_file, 'r', encoding='utf-8') as vtt:
                    lines = vtt.readlines()
                    for line in lines:
                        # VTTのヘッダー、タイムスタンプ、制御文字を除去
                        line = line.strip()
                        if (not line.startswith('WEBVTT') and
                            not line.startswith('NOTE') and
                            not line.startswith('Kind:') and
                            not line.startswith('Language:') and
                            '-->' not in line and
                            line and
                            not re.match(r'^\d+$', line)):
                            # タイムスタンプタグを除去
                            clean_line = re.sub(r'<[^>]*>', '', line)
                            if clean_line.strip():
                                all_text.append(clean_line.strip())
                
                # VTTファイルを削除
                os.remove(target_vtt_file)
                
                # 重複を除去し、テキストのみを保存
                unique_text = []
                for text in all_text:
                    if text not in unique_text:
                        unique_text.append(text)
                
                with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write('\n'.join(unique_text))
                
                print(f"Saved subtitles as {txt_file_path}")
                return txt_file_path
            else:
                print("No subtitles found")
                return None
    except Exception as e:
        print(f"Subtitle download failed: {e}")
        return None

# YouTube動画をpytubeでダウンロードする関数
def download_with_pytube(url):
    try:
        yt = YouTube(url)
        # まず最高画質のMP4を試す
        stream = yt.streams.filter(file_extension='mp4').get_highest_resolution()
        if not stream:
            # MP4がない場合は、最高画質の動画を取得
            stream = yt.streams.get_highest_resolution()
        if not stream:
            # それでもない場合は、最初に見つかった動画を取得
            stream = yt.streams.first()
        
        title = sanitize_filename(yt.title)
        stream.download(filename='movie.mp4')
        print("Downloaded with pytube")
        return 'movie.mp4', title
    except Exception as e:
        print(f"pytube failed: {e}")
        return None, None

# YouTube動画をyoutube_dlでダウンロードする関数
def download_with_youtube_dl(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'movie.mp4',
        'noplaylist': True,
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            print("Downloaded with youtube_dl")
            return 'movie.mp4', sanitize_filename(info_dict['title'])
    except Exception as e:
        print(f"youtube_dl failed: {e}")
        return None, None

# YouTube動画をyt_dlpでダウンロードする関数
def download_with_yt_dlp(url):
    ydl_opts = {
        'format': '(bestvideo[height<=720]+bestaudio/best[height<=720])/best',
        'outtmpl': 'movie.%(ext)s',
        'noplaylist': True,
        'merge_output_format': 'mp4',
    }
    try:
        with youtube_dl_2.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            print("Downloaded with yt_dlp")
            return 'movie.mp4', sanitize_filename(info_dict['title'])
    except Exception as e:
        print(f"yt_dlp failed: {e}")
        return None, None

# 対話的に出力形式を選択する関数
def interactive_format_selection():
    print("\n出力形式を選択してください:")
    print("1. MP4 (動画ファイル)")
    print("2. MP3 (音声ファイル)")
    print("3. TXT (字幕ファイル)")
    
    while True:
        try:
            choice = input("\n選択 (1-3): ").strip()
            if choice == '1':
                return 'mp4'
            elif choice == '2':
                return 'mp3'
            elif choice == '3':
                return 'txt'
            else:
                print("無効な選択です。1、2、または3を入力してください。")
        except KeyboardInterrupt:
            print("\n\n処理を中断しました。")
            sys.exit(0)

# メイン処理
if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python youtubedl.py <youtube url> [format]")
        print("format: 'mp4', 'mp3', or 'txt'")
        print("オプションなしの場合は対話的に選択できます。")
        sys.exit(1)

    url = sys.argv[1]
    
    # 出力形式の決定
    if len(sys.argv) == 3:
        output_format = sys.argv[2].lower()
        if output_format not in ['mp3', 'mp4', 'txt']:
            print("Error: format must be 'mp3', 'mp4', or 'txt'")
            sys.exit(1)
    else:
        output_format = interactive_format_selection()
    
    print(f"\nDownloading and processing as {output_format.upper()}...")
    
    if output_format == 'txt':
        # 字幕のみをダウンロード
        # まず動画情報を取得してタイトルを得る
        try:
            with youtube_dl_2.YoutubeDL({'quiet': True}) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                title = sanitize_filename(info_dict['title'])
            download_subtitles(url, title)
        except Exception as e:
            print(f"Failed to download subtitles: {e}")
    else:
        # 動画をダウンロード
        mp4_file_path, title = download_with_pytube(url)
        if not mp4_file_path:
            mp4_file_path, title = download_with_youtube_dl(url)
        if not mp4_file_path:
            mp4_file_path, title = download_with_yt_dlp(url)
        
        if mp4_file_path and title:
            if output_format == 'mp3':
                # MP4からMP3へ変換
                convert_mp4_to_mp3(mp4_file_path, title)
            else:
                # MP4ファイルを最終的な名前にリネーム
                rename_video_file(mp4_file_path, title)
        else:
            print("Failed to download the video.")
