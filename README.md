## Overview
youtubedl is a Python script that downloads YouTube videos in multiple formats (MP4, MP3, or subtitles as TXT). It uses multiple download methods (pytube, youtube-dl, and yt-dlp) to ensure reliable downloading, and supports interactive format selection or direct command-line specification.

## Features
- **Multiple output formats**: MP4 (video), MP3 (audio), TXT (subtitles)
- **Interactive mode**: Choose format interactively when no format is specified
- **Command-line mode**: Directly specify format as argument
- **Subtitle extraction**: Downloads original language subtitles as clean text
- **Fallback system**: Tries multiple download methods for reliability
- **Auto-conversion**: Converts video to MP3 using ffmpeg when needed

## Installation
1. Clone the repository
```bash
git clone https://github.com/daishir0/youtubedl.git
```

2. Change to the project directory
```bash
cd youtubedl
```

3. Install the required dependencies
```bash
pip install -r requirements.txt
```

4. Install ffmpeg (required for MP3 conversion)
- For Ubuntu/Debian:
```bash
sudo apt-get install ffmpeg
```
- For macOS (using Homebrew):
```bash
brew install ffmpeg
```
- For Windows:
  - Download ffmpeg from https://ffmpeg.org/download.html
  - Add ffmpeg to your system PATH

## Usage

### Interactive Mode
Run the script with only a YouTube URL to choose format interactively:
```bash
python youtubedl.py <youtube url>
```

Example:
```bash
python youtubedl.py https://www.youtube.com/watch?v=example
```

This will show a menu:
```
出力形式を選択してください:
1. MP4 (動画ファイル)
2. MP3 (音声ファイル)
3. TXT (字幕ファイル)

選択 (1-3):
```

### Command-line Mode
Directly specify the output format:
```bash
python youtubedl.py <youtube url> <format>
```

Available formats:
- `mp4` - Download video file
- `mp3` - Download and convert to audio file
- `txt` - Download subtitles as text file

Examples:
```bash
python youtubedl.py https://www.youtube.com/watch?v=example mp4
python youtubedl.py https://www.youtube.com/watch?v=example mp3
python youtubedl.py https://www.youtube.com/watch?v=example txt
```

## Output Files
- **MP4**: Video files saved with original title
- **MP3**: Audio files converted from video (128kbps, 44.1kHz)
- **TXT**: Clean subtitle text in original language (no timestamps or formatting)

## Notes
- The script requires a stable internet connection
- Downloaded files will be saved in the same directory as the script
- For MP3 conversion, intermediate MP4 files are automatically deleted
- For subtitle download, only the original spoken language is extracted
- If one download method fails, the script will automatically try the next method
- Supports YouTube videos, YouTube Shorts, and other YouTube content

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---

## 概要
youtubedlは、YouTube動画を複数の形式（MP4、MP3、字幕をTXT）でダウンロードするPythonスクリプトです。複数のダウンロード方式（pytube、youtube-dl、yt-dlp）を使用して信頼性の高いダウンロードを実現し、対話的な形式選択またはコマンドライン引数での直接指定をサポートします。

## 機能
- **複数の出力形式**: MP4（動画）、MP3（音声）、TXT（字幕）
- **対話モード**: 形式未指定時に対話的に選択可能
- **コマンドラインモード**: 引数で形式を直接指定
- **字幕抽出**: オリジナル言語の字幕をクリーンなテキストでダウンロード
- **フォールバックシステム**: 複数のダウンロード方式で信頼性を確保
- **自動変換**: 必要に応じてffmpegで動画をMP3に変換

## インストール方法
1. レポジトリをクローンする
```bash
git clone https://github.com/daishir0/youtubedl.git
```

2. プロジェクトディレクトリに移動
```bash
cd youtubedl
```

3. 必要な依存パッケージをインストール
```bash
pip install -r requirements.txt
```

4. ffmpegのインストール（MP3変換に必要）
- Ubuntu/Debian の場合:
```bash
sudo apt-get install ffmpeg
```
- macOS の場合（Homebrewを使用）:
```bash
brew install ffmpeg
```
- Windows の場合:
  - ffmpegを https://ffmpeg.org/download.html からダウンロード
  - ffmpegをシステムPATHに追加

## 使い方

### 対話モード
YouTubeのURLのみを指定して実行すると、形式を対話的に選択できます：
```bash
python youtubedl.py <youtube url>
```

例：
```bash
python youtubedl.py https://www.youtube.com/watch?v=example
```

以下のメニューが表示されます：
```
出力形式を選択してください:
1. MP4 (動画ファイル)
2. MP3 (音声ファイル)
3. TXT (字幕ファイル)

選択 (1-3):
```

### コマンドラインモード
出力形式を直接指定：
```bash
python youtubedl.py <youtube url> <形式>
```

利用可能な形式：
- `mp4` - 動画ファイルをダウンロード
- `mp3` - 音声ファイルに変換してダウンロード
- `txt` - 字幕をテキストファイルでダウンロード

例：
```bash
python youtubedl.py https://www.youtube.com/watch?v=example mp4
python youtubedl.py https://www.youtube.com/watch?v=example mp3
python youtubedl.py https://www.youtube.com/watch?v=example txt
```

## 出力ファイル
- **MP4**: 元のタイトルで保存される動画ファイル
- **MP3**: 動画から変換された音声ファイル（128kbps、44.1kHz）
- **TXT**: オリジナル言語のクリーンな字幕テキスト（タイムスタンプや書式なし）

## 注意点
- 安定したインターネット接続が必要です
- ダウンロードしたファイルは、スクリプトと同じディレクトリに保存されます
- MP3変換時、中間MP4ファイルは自動的に削除されます
- 字幕ダウンロード時は、実際に話されているオリジナル言語のみが抽出されます
- 一つのダウンロード方式が失敗した場合、自動的に次の方式を試行します
- YouTube動画、YouTube Shorts、その他のYouTubeコンテンツに対応

## ライセンス
このプロジェクトはMITライセンスの下でライセンスされています。詳細はLICENSEファイルを参照してください。
