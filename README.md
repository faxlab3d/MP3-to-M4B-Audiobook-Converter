# MP3 to M4B Audiobook Converter

<img width="727" height="625" alt="image" src="https://github.com/user-attachments/assets/2eb3b840-abb9-41e9-b0da-3bd687c3a26c" />

A user-friendly GUI application that converts multiple MP3 files into a single M4B audiobook file, perfect for iPhone and other audiobook players.

![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- **🎧 Convert multiple MP3s** to a single M4B audiobook file
- **📖 Automatic chapter creation** (one chapter per MP3 file)
- **🖥️ User-friendly GUI** with drag-and-drop style interface
- **📱 iPhone/iOS optimized** M4B format with proper metadata
- **🎨 Handles album art** in MP3 files without issues
- **⚙️ Configurable audio quality** (32k to 128k bitrate)
- **📊 Progress tracking** with real-time status updates
- **🔧 Smart file sorting** (handles numbered files correctly)
- **📋 Copyable error messages** for easy troubleshooting

## 🖼️ Screenshots

### Main Interface
The clean, intuitive interface makes conversion simple:
- Browse for your MP3 folder
- Set audiobook details (title, author)
- Monitor conversion progress
- Get detailed error messages if needed

## 📋 Requirements

### System Requirements
- **Python 3.6+** - [Download from python.org](https://www.python.org/downloads/)
- **FFmpeg** (must be installed and accessible from command line)

### Python Dependencies
- `tkinter` (usually included with Python)
- `pathlib` (Python 3.4+)
- `subprocess`, `threading`, `queue` (standard library)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/mp3-to-m4b-converter.git
cd mp3-to-m4b-converter
```

### 2. Install FFmpeg

#### Windows
```bash
# Using winget
winget install ffmpeg

# Or download from https://ffmpeg.org/download.html
```

#### macOS
```bash
# Using Homebrew
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

### 3. Run the Application
```bash
python audiobook_converter_gui.py
```

## 🎯 Usage

### Quick Start
1. **Launch the application**
2. **Click "Browse"** next to "Input Folder" and select your folder containing MP3 files
3. **Choose output location** (or let it auto-suggest based on folder name)
4. **Enter audiobook details** (title, author, bitrate)
5. **Click "Convert to M4B"** and wait for completion!

### Step-by-Step Guide

#### 1. Select Input Folder
- Click the **"Browse"** button next to "Input Folder"
- Navigate to and select the folder containing your MP3 files
- The application will automatically detect and list all MP3 files

#### 2. Configure Output
- **Output file**: Choose where to save your M4B file (auto-suggests based on folder name)
- **Title**: Audiobook title (auto-fills from folder name)
- **Author**: Author name (optional, defaults to "Unknown")
- **Bitrate**: Audio quality - choose from 32k, 48k, 64k, 96k, or 128k

#### 3. Review and Convert
- Check the file list to ensure all your MP3s are detected
- Files are automatically sorted in natural order (Part 1, Part 2, etc.)
- Click **"Convert to M4B"** to start the process

#### 4. Monitor Progress
- Watch the progress bar and status messages
- The interface remains responsive during conversion
- If errors occur, you'll get a detailed, copyable error message

## 📁 File Organization Tips

### Recommended MP3 Naming
```
📂 My Audiobook/
├── 01 - Chapter One.mp3
├── 02 - Chapter Two.mp3
├── 03 - Chapter Three.mp3
└── ...
```

### Supported Patterns
- `Chapter 01.mp3`, `Chapter 02.mp3`
- `Part 1.mp3`, `Part 2.mp3`
- `01.mp3`, `02.mp3`
- Any numbered sequence

## ⚙️ Technical Details

### Output Format
- **Container**: MP4 (.m4b extension)
- **Audio Codec**: AAC
- **Sample Rate**: 44.1 kHz (automatically normalized)
- **Channels**: Stereo
- **Metadata**: Includes title, author, chapters

### Chapter Creation
- Each MP3 file becomes one chapter
- Chapter titles use the filename (without extension)
- Precise timing based on actual MP3 durations
- Proper chapter navigation on iPhone/iOS

### Audio Processing
- Handles MP3s with embedded album art
- Normalizes different sample rates and formats
- Fixes timing synchronization issues
- Optimized for audiobook playback

## 🔧 Troubleshooting

### Common Issues

#### "FFmpeg not found"
**Solution**: Install FFmpeg and ensure it's in your system PATH
```bash
# Test FFmpeg installation
ffmpeg -version
```

#### "No MP3 files found"
**Solution**: 
- Ensure your folder contains `.mp3` files
- Check that files aren't in subfolders
- Verify file extensions are lowercase `.mp3`

#### "Conversion failed" with video errors
**Solution**: This is handled automatically - the app ignores embedded album art

#### Files not in correct order
**Solution**: The app sorts naturally, but ensure your files are named consistently:
- Use leading zeros: `01.mp3`, `02.mp3` instead of `1.mp3`, `2.mp3`

### Getting Help
If you encounter issues:
1. Check the **detailed error message** (copyable from the error dialog)
2. Verify your **FFmpeg installation**
3. Try with a **small test folder** first
4. **Open an issue** on GitHub with the error details

## 📱 Using Your M4B Audiobook

### On iPhone/iPad
1. **Transfer the M4B file** to your device via:
   - AirDrop
   - iTunes/Finder sync
   - Cloud storage (iCloud, Dropbox, etc.)

2. **Open in audiobook app**:
   - **Apple Books** (recommended)
   - **Audible** app
   - Other audiobook players

3. **Enjoy features**:
   - Chapter navigation
   - Bookmarks and notes
   - Playback speed control
   - Sleep timer

### On Other Devices
- **Android**: VLC, Smart AudioBook Player
- **Desktop**: iTunes, VLC, Audacity
- **Web**: Most modern browsers support M4B playback

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Ways to Contribute
- 🐛 **Report bugs** with detailed error messages
- 💡 **Suggest features** for better usability
- 📝 **Improve documentation** 
- 🔧 **Submit pull requests** with fixes or enhancements

### Development Setup
```bash
# Clone the repo
git clone https://github.com/yourusername/mp3-to-m4b-converter.git
cd mp3-to-m4b-converter

# Make your changes
# Test thoroughly with different MP3 files

# Submit a pull request
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FFmpeg** - The powerhouse behind audio/video processing
- **Python tkinter** - For the cross-platform GUI
- **The audiobook community** - For inspiration and feedback

## 📊 Project Stats

- **Language**: Python
- **GUI Framework**: tkinter
- **Audio Processing**: FFmpeg
- **Supported Formats**: MP3 → M4B
- **Platform Support**: Windows, macOS, Linux

---

**🎧 Happy listening!** If this project helps you enjoy your audiobooks, consider giving it a ⭐ star on GitHub!
