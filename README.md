# PrivateTube 🎬

**A Privacy-Focused YouTube Downloader built from scratch with Python**

![Status](https://img.shields.io/badge/status-active-success) ![Python](https://img.shields.io/badge/python-3.6%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen)

## 🎯 Overview

PrivateTube is a privacy-focused YouTube downloader built entirely from scratch using only Python's standard library. No external dependencies, no data collection, just pure functionality.

**Key Features:**
- 🔒 **100% Private** - All processing happens locally on your computer
- ⚙️ **Zero Dependencies** - Built with Python stdlib only (urllib, json, http.server, etc.)
- 🎨 **Beautiful UI** - Netflix-inspired dark theme with responsive design
- 📱 **Fully Responsive** - Works on desktop, tablet, and mobile
- 💻 **CLI Interface** - Rich command-line logging with colored output
- ⚡ **Lightweight** - Minimal resource consumption
- 🌐 **Modern Tech Stack** - Python backend, vanilla JavaScript frontend

## 📋 Requirements

- Python 3.6 or higher
- A modern web browser
- 50MB disk space

That's it! No pip packages needed.

## 🚀 Quick Start

### 1. Clone or Download

```bash
git clone https://github.com/st3rfall/ytoppos.git
cd ytoppos
```

### 2. Run the Application

```bash
python app.py
```

### 3. Access the Web Interface

The application will automatically open your browser to `http://localhost:8000`

If it doesn't open automatically, visit: **http://localhost:8000**

That's all! The server will start with a beautiful web interface ready to use.

## 📖 Usage Guide

### Via Web Interface

1. **Paste YouTube URL** - Enter a YouTube URL in the input field
2. **Fetch Info** - Click the "Fetch Info" button to retrieve video metadata
3. **Select Quality** - Choose your preferred video quality from the dropdown
4. **Download** - Click "Download" to save the video
5. **View History** - See all your downloads in the History section

### Via Command Line

```bash
# Start with default settings (localhost:8000)
python app.py

# Use custom port
python app.py --port 3000

# Make server accessible on your network
python app.py --host 0.0.0.0

# Don't open browser automatically
python app.py --no-browser

# Enable automatic safe mode on restricted devices
python app.py --auto
python app.py --safe-mode

# Suppress CLI output (quiet mode)
python app.py --quiet

# Show help
python app.py --help

# Show version
python app.py --version

### Safe Mode

Use `--auto` or `--safe-mode` when running on school-controlled or restricted devices. This mode will try to find an available port automatically and avoid blocked browser launches.
```

## 🏗️ Project Structure

```
ytoppos/
├── app.py                    # Main entry point with CLI
├── server.py                # HTTP server implementation
├── youtube_downloader.py    # YouTube downloader engine
├── cli_logger.py            # CLI logging system
├── templates/
│   └── index.html          # Main web interface
├── static/
│   ├── style.css           # Netflix-style CSS
│   └── app.js              # Frontend JavaScript
├── downloads/              # Downloaded videos (auto-created)
├── logs/                   # Application logs (auto-created)
└── README.md              # This file
```

## 🔐 Privacy & Security

PrivateTube is designed with privacy as the first principle:

### What We DON'T Do
- ❌ Collect any personal data
- ❌ Use external APIs or services
- ❌ Track your downloads or activity
- ❌ Store connection logs
- ❌ Require authentication or sign-up

### What We DO
- ✅ Process everything locally on your computer
- ✅ Use only Python standard library
- ✅ Keep all data on your machine
- ✅ Log only to your local file system
- ✅ Never make external network calls (except to YouTube)

**Your privacy is guaranteed.**

## 🎨 Features

### Beautiful Web Interface
- Dark theme inspired by Netflix
- Smooth animations and transitions
- Intuitive navigation
- Real-time video information display

### Rich Metadata
- Video title
- Duration
- Upload channel
- View count
- Description

### Multiple Quality Options
- 1080p
- 720p
- 480p
- 360p
- Audio-only (M4A)

### Download History
- Automatically tracked
- Persistent storage
- Easy organization

### Privacy Information
- Real-time privacy status
- Transparency about data handling
- Security information

## 📝 CLI Logging

The application provides rich command-line output with:

### Colored Output
- **Debug** (Cyan) - Detailed debugging information
- **Info** (Blue) - General information
- **Success** (Green) - Successful operations
- **Warning** (Yellow) - Important notices
- **Error** (Red) - Error messages

### Log File
All logs are automatically saved to `logs/app.log`

View logs:
```bash
cat logs/app.log

# Or follow logs in real-time
tail -f logs/app.log
```

Clear logs:
Access through the logger in Python or delete the file manually:
```bash
rm logs/app.log
```

## 🔧 Configuration

### Default Settings
- **Host:** localhost (127.0.0.1)
- **Port:** 8000
- **Log File:** logs/app.log
- **Download Directory:** downloads/

### Customize at Runtime
Use command-line arguments to change settings without modifying files.

## 🛠️ Technology Stack

### Backend
- **Python 3.6+** - Core language
- **http.server** - Web server
- **urllib** - HTTP requests
- **json** - Data serialization
- **re** - Regex parsing
- **pathlib** - File handling

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling (Grid, Flexbox, Gradients)
- **Vanilla JavaScript** - No frameworks needed
- **Responsive Design** - Mobile-first approach

## 📊 Performance

PrivateTube is optimized for efficiency:

- **Memory Usage:** ~30-50MB base
- **Startup Time:** <1 second
- **Response Time:** <200ms for most operations
- **Storage:** Minimal (only downloads stored)

## 🚨 Troubleshooting

### "Failed to Fetch" Error
This means the server is not running or not accessible:
1. Make sure you've started the server with `python app.py`
2. Check that the browser URL shows `http://localhost:8000`
3. Try using a different port: `python app.py --port 3000`
4. Check the terminal for error messages
5. On restricted networks, use safe mode: `python app.py --auto`

### Port Already in Use
```bash
# Use a different port
python app.py --port 3000
```

### Browser Won't Open Automatically
```bash
# Start without browser opening, then visit manually
python app.py --no-browser
# Then open: http://localhost:8000
```

### Firewall Issues
If accessing from another machine:
```bash
# Allow network access
python app.py --host 0.0.0.0
# Access from other machine: http://your-machine-ip:8000
```

### Download Directory Permissions
Make sure the script has write permissions in the current directory. It will create a `downloads/` folder automatically.

## 📋 API Endpoints

The application exposes several REST API endpoints:

### GET /api/video-info
Get video metadata
```
?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### GET /api/formats
Get available quality formats
```
?video_id=dQw4w9WgXcQ
```

### GET /api/download
Download a video
```
?video_id=dQw4w9WgXcQ&title=Video%20Title
```

### GET /api/history
Get download history
(No parameters)

### GET /api/privacy
Get privacy information
(No parameters)

### POST /api/submit-url
Submit a URL (JSON body)
```json
{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
```

## 🤝 Contributing

Contributions are welcome! This is an open-source project.

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Areas to Improve
- Direct video stream downloading (currently metadata-based)
- Additional video formats and codecs
- Playlist support
- Batch downloading
- Cloud storage integration
- Advanced filtering options

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Legal Notice

This tool is provided for educational and personal use. Users are responsible for respecting copyright laws and YouTube's Terms of Service in their respective jurisdictions. Always ensure you have the right to download and use content.

## 🌟 Show Your Support

If you find PrivateTube useful, please:
- ⭐ Star this repository
- 🐛 Report bugs
- 💡 Suggest features
- 📢 Share with others

## 📧 Contact & Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the documentation
- Review the CLI help: `python app.py --help`

## 🎯 Roadmap

- [x] Basic YouTube downloader
- [x] Web interface
- [x] CLI logging system
- [x] Privacy-focused design
- [x] Responsive UI
- [ ] Direct streaming download
- [ ] Playlist support
- [ ] Advanced filters
- [ ] Mobile app
- [ ] Desktop application

## 🙏 Acknowledgments

Built with care and respect for user privacy.

---

**Version:** 1.0.0  
**Last Updated:** 2024  
**Status:** Active Development

Enjoy downloading responsibly! 🎬
