# 🎬 File-Sharing-Bot (Movie & Series Uploader)

<p align="center">
  <img src="https://telegra.ph/file/14d3013fda21281c54b61.jpg" alt="File Sharing Bot">
</p>

<p align="center">
  <b>Telegram Bot for Movie and Series Uploading with Persian/Farsi Interface</b><br>
  <i>Enhanced for storing movies and series in Telegram hosting infrastructure</i>
</p>

## 🌟 Features

- **🎬 Movie Upload**: Specialized movie upload with metadata extraction
- **📺 Series Management**: Episode-based series uploading with season/episode organization  
- **🔗 Smart Link Generation**: Create shareable links for all uploaded content
- **🏷️ Auto-Tagging**: Automatic hashtag generation for better organization
- **⏰ Duration & Quality**: Extract video duration and quality information
- **🇮🇷 Persian Interface**: Full Persian/Farsi language support
- **📊 Enhanced Captions**: Rich captions with video metadata
- **🔒 Force Subscription**: Optional channel subscription requirement
- **🛡️ Content Protection**: Prevent file forwarding (optional)
- **⏱️ Auto-Delete**: Configurable automatic file deletion

## 🚀 Admin Commands

### Movie & Series Commands
- `/movie` - Upload a new movie with enhanced metadata
- `/series` - Upload a series episode with season/episode info
- `/help_movie` - Show movie/series upload guide

### General Commands  
- `/help` - Show admin command reference
- `/start` - Start the bot
- `/stats` - View bot statistics
- `/genlink` - Generate link for single post
- `/batch` - Generate link for multiple posts

## 📚 Usage Guide

### 🎬 Movie Upload Process
1. Send `/movie` command
2. Upload your movie file (video or document)
3. Enter movie title
4. Receive shareable link with Persian metadata

### 📺 Series Upload Process
1. Send `/series` command  
2. Upload episode file
3. Enter series name
4. Specify season and episode numbers
5. Get organized link with episode info

### 📁 Regular File Upload
Simply send any file directly to get a basic shareable link.

## ⚙️ Configuration

### Required Environment Variables
- `TG_BOT_TOKEN` - Bot token from @BotFather
- `API_ID` - API ID from my.telegram.org
- `API_HASH` - API Hash from my.telegram.org  
- `CHANNEL_ID` - Database channel ID (e.g., -100xxxxxxxx)
- `OWNER_ID` - Your Telegram user ID
- `DATABASE_URL` - PostgreSQL database URL

### Optional Variables
- `ADMINS` - Space-separated admin user IDs
- `FORCE_SUB_CHANNEL` - Force subscription channel ID (0 to disable)
- `PROTECT_CONTENT` - Prevent file forwarding (True/False)
- `AUTO_DELETE_TIME` - Auto-delete time in seconds (0 to disable)
- `MOVIE_SERIES_ENABLED` - Enable movie/series features (True/False)
- `CUSTOM_CAPTION` - Custom caption template
- `START_MESSAGE` - Custom start message
- `FORCE_SUB_MESSAGE` - Custom force subscription message

## 🛠️ Installation

### Deploy on Railway
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/1jKLr4)

### Manual Deployment
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables
4. Run: `python main.py`

### Database Setup
The bot requires PostgreSQL for user management. Set `DATABASE_URL` to your PostgreSQL connection string.

## 🇮🇷 Persian Language Support

This enhanced version includes full Persian/Farsi language support with:
- Persian interface messages
- Farsi video metadata extraction  
- Persian error messages and notifications
- RTL-friendly formatting
- Iranian movie/series terminology

## 📖 Example Usage

```
User: /movie
Bot: 🎬 لطفا فایل فیلم خود را ارسال کنید:

User: [sends video file]
Bot: 📝 نام فیلم را وارد کنید:

User: فیلم سینمایی جدید
Bot: ✅ فیلم با موفقیت آپلود شد!
     📋 نام فیلم: فیلم سینمایی جدید  
     ⏰ مدت زمان: 120:30
     📊 کیفیت: 1920x1080
     💾 حجم فایل: 2.1 GB
     🔗 لینک اشتراک گذاری: https://t.me/bot?start=...
```

## 🔧 Technical Details

- **Framework**: Pyrogram (Python)
- **Database**: PostgreSQL with SQLAlchemy
- **File Storage**: Telegram's hosting infrastructure
- **Language**: Python 3.7+
- **Async Support**: Full async/await implementation

## 📝 License

This project is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE) for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For support and updates:
- Channel: [@CodeXBotz](https://t.me/CodeXBotz)  
- Support Group: [@CodeXBotzSupport](https://t.me/CodeXBotzSupport)

---
<p align="center">
  <b>⭐ Star this repository if you found it helpful!</b>
</p>
