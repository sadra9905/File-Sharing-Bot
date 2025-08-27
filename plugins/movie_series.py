# Movie and Series Upload Handler
# Enhanced functionality for Persian movie/series uploading

import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from helper_func import encode

# Persian/Farsi messages for movie/series functionality
MOVIE_UPLOAD_MSG = "🎬 فیلم با موفقیت آپلود شد!\n\n📋 نام فیلم: {title}\n⏰ مدت زمان: {duration}\n📊 کیفیت: {quality}\n💾 حجم فایل: {size}\n\n🔗 لینک اشتراک گذاری:"

SERIES_UPLOAD_MSG = "📺 قسمت سریال با موفقیت آپلود شد!\n\n📋 نام سریال: {series_name}\n🔢 فصل {season} - قسمت {episode}\n⏰ مدت زمان: {duration}\n📊 کیفیت: {quality}\n💾 حجم فایل: {size}\n\n🔗 لینک اشتراک گذاری:"

WAITING_MSG = "⏳ در حال آپلود و پردازش فایل...\nلطفا صبر کنید..."

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('movie'))
async def upload_movie(client: Client, message: Message):
    """Handle movie upload with Persian interface"""
    
    # Ask for movie file
    try:
        movie_msg = await client.ask(
            text="🎬 لطفا فایل فیلم خود را ارسال کنید:",
            chat_id=message.from_user.id,
            filters=filters.video | filters.document,
            timeout=300
        )
    except:
        await message.reply("❌ زمان انتظار تمام شد. دوباره تلاش کنید.")
        return
    
    # Ask for movie title
    try:
        title_msg = await client.ask(
            text="📝 نام فیلم را وارد کنید:",
            chat_id=message.from_user.id,
            filters=filters.text,
            timeout=60
        )
        movie_title = title_msg.text
    except:
        movie_title = "فیلم"
    
    # Process the upload
    reply_text = await message.reply_text(WAITING_MSG, quote=True)
    
    try:
        # Copy to database channel with enhanced caption
        enhanced_caption = await create_movie_caption(movie_msg, movie_title)
        
        post_message = await movie_msg.copy(
            chat_id=client.db_channel.id, 
            caption=enhanced_caption,
            disable_notification=True
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)
        post_message = await movie_msg.copy(
            chat_id=client.db_channel.id, 
            caption=enhanced_caption,
            disable_notification=True
        )
    except Exception as e:
        print(f"Movie upload error: {e}")
        await reply_text.edit_text("❌ خطا در آپلود فیلم!")
        return
    
    # Generate shareable link
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    
    # Create response with Persian text
    file_info = await get_file_info(movie_msg)
    
    success_msg = MOVIE_UPLOAD_MSG.format(
        title=movie_title,
        duration=file_info['duration'],
        quality=file_info['quality'], 
        size=file_info['size']
    )
    
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 اشتراک گذاری", url=f'https://telegram.me/share/url?url={link}')],
        [InlineKeyboardButton("📋 کپی لینک", callback_data=f"copy_{base64_string}")]
    ])
    
    await reply_text.edit_text(f"{success_msg}\n\n{link}", reply_markup=reply_markup, disable_web_page_preview=True)
    
    # Add button to original file if enabled
    if not DISABLE_CHANNEL_BUTTON:
        try:
            await post_message.edit_reply_markup(reply_markup)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await post_message.edit_reply_markup(reply_markup)
        except Exception:
            pass

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('series'))
async def upload_series(client: Client, message: Message):
    """Handle series episode upload with Persian interface"""
    
    # Ask for series file
    try:
        series_msg = await client.ask(
            text="📺 لطفا فایل قسمت سریال را ارسال کنید:",
            chat_id=message.from_user.id,
            filters=filters.video | filters.document,
            timeout=300
        )
    except:
        await message.reply("❌ زمان انتظار تمام شد. دوباره تلاش کنید.")
        return
    
    # Ask for series details
    try:
        series_name_msg = await client.ask(
            text="📝 نام سریال را وارد کنید:",
            chat_id=message.from_user.id,
            filters=filters.text,
            timeout=60
        )
        series_name = series_name_msg.text
    except:
        series_name = "سریال"
    
    try:
        season_msg = await client.ask(
            text="🔢 شماره فصل را وارد کنید:",
            chat_id=message.from_user.id,
            filters=filters.text,
            timeout=60
        )
        season = season_msg.text
    except:
        season = "1"
    
    try:
        episode_msg = await client.ask(
            text="🔢 شماره قسمت را وارد کنید:",
            chat_id=message.from_user.id,
            filters=filters.text,
            timeout=60
        )
        episode = episode_msg.text
    except:
        episode = "1"
    
    # Process the upload
    reply_text = await message.reply_text(WAITING_MSG, quote=True)
    
    try:
        # Copy to database channel with enhanced caption
        enhanced_caption = await create_series_caption(series_msg, series_name, season, episode)
        
        post_message = await series_msg.copy(
            chat_id=client.db_channel.id, 
            caption=enhanced_caption,
            disable_notification=True
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)
        post_message = await series_msg.copy(
            chat_id=client.db_channel.id, 
            caption=enhanced_caption,
            disable_notification=True
        )
    except Exception as e:
        print(f"Series upload error: {e}")
        await reply_text.edit_text("❌ خطا در آپلود سریال!")
        return
    
    # Generate shareable link
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    
    # Create response with Persian text
    file_info = await get_file_info(series_msg)
    
    success_msg = SERIES_UPLOAD_MSG.format(
        series_name=series_name,
        season=season,
        episode=episode,
        duration=file_info['duration'],
        quality=file_info['quality'],
        size=file_info['size']
    )
    
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 اشتراک گذاری", url=f'https://telegram.me/share/url?url={link}')],
        [InlineKeyboardButton("📋 کپی لینک", callback_data=f"copy_{base64_string}")]
    ])
    
    await reply_text.edit_text(f"{success_msg}\n\n{link}", reply_markup=reply_markup, disable_web_page_preview=True)
    
    # Add button to original file if enabled
    if not DISABLE_CHANNEL_BUTTON:
        try:
            await post_message.edit_reply_markup(reply_markup)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await post_message.edit_reply_markup(reply_markup)
        except Exception:
            pass

async def create_movie_caption(message: Message, title: str) -> str:
    """Create enhanced caption for movie files"""
    original_caption = message.caption or ""
    file_info = await get_file_info(message)
    
    enhanced_caption = f"🎬 **{title}**\n\n"
    
    if file_info['duration']:
        enhanced_caption += f"⏰ مدت زمان: {file_info['duration']}\n"
    if file_info['quality']:
        enhanced_caption += f"📊 کیفیت: {file_info['quality']}\n"
    if file_info['size']:
        enhanced_caption += f"💾 حجم: {file_info['size']}\n"
    
    if original_caption:
        enhanced_caption += f"\n📝 توضیحات:\n{original_caption}"
    
    enhanced_caption += f"\n\n🏷️ #فیلم #{title.replace(' ', '_')}"
    
    return enhanced_caption

async def create_series_caption(message: Message, series_name: str, season: str, episode: str) -> str:
    """Create enhanced caption for series episode files"""
    original_caption = message.caption or ""
    file_info = await get_file_info(message)
    
    enhanced_caption = f"📺 **{series_name}**\n"
    enhanced_caption += f"🔢 فصل {season} - قسمت {episode}\n\n"
    
    if file_info['duration']:
        enhanced_caption += f"⏰ مدت زمان: {file_info['duration']}\n"
    if file_info['quality']:
        enhanced_caption += f"📊 کیفیت: {file_info['quality']}\n"
    if file_info['size']:
        enhanced_caption += f"💾 حجم: {file_info['size']}\n"
    
    if original_caption:
        enhanced_caption += f"\n📝 توضیحات:\n{original_caption}"
    
    enhanced_caption += f"\n\n🏷️ #سریال #{series_name.replace(' ', '_')} #فصل{season} #قسمت{episode}"
    
    return enhanced_caption

async def get_file_info(message: Message) -> dict:
    """Extract file information for videos and documents"""
    info = {
        'duration': 'نامشخص',
        'quality': 'نامشخص', 
        'size': 'نامشخص'
    }
    
    if message.video:
        # Extract video metadata
        if message.video.duration:
            duration_mins = message.video.duration // 60
            duration_secs = message.video.duration % 60
            info['duration'] = f"{duration_mins}:{duration_secs:02d}"
        
        if message.video.width and message.video.height:
            info['quality'] = f"{message.video.width}x{message.video.height}"
        
        if message.video.file_size:
            info['size'] = format_file_size(message.video.file_size)
    
    elif message.document:
        # Extract document metadata
        if message.document.file_size:
            info['size'] = format_file_size(message.document.file_size)
        
        # Try to extract quality from filename
        filename = message.document.file_name or ""
        if any(q in filename.lower() for q in ['1080p', '720p', '480p', '360p']):
            for q in ['1080p', '720p', '480p', '360p']:
                if q in filename.lower():
                    info['quality'] = q.upper()
                    break
    
    return info

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes/1024:.1f} KB"
    elif size_bytes < 1024**3:
        return f"{size_bytes/(1024**2):.1f} MB"
    else:
        return f"{size_bytes/(1024**3):.1f} GB"

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('help_movie'))
async def help_movie(client: Client, message: Message):
    """Show help for movie/series commands"""
    help_text = """
🎬 **راهنمای آپلود فیلم و سریال**

📋 **دستورات موجود:**
• `/movie` - آپلود فیلم
• `/series` - آپلود قسمت سریال
• `/help_movie` - نمایش این راهنما

🎯 **نحوه استفاده:**
1️⃣ برای آپلود فیلم: `/movie` را ارسال کنید
2️⃣ فایل ویدیو یا مستند خود را ارسال کنید
3️⃣ نام فیلم را وارد کنید
4️⃣ لینک اشتراک گذاری دریافت کنید

📺 **برای سریال:**
1️⃣ دستور `/series` را ارسال کنید
2️⃣ فایل قسمت را ارسال کنید
3️⃣ نام سریال، شماره فصل و قسمت را وارد کنید
4️⃣ لینک اشتراک گذاری دریافت کنید

✨ **ویژگی‌ها:**
• پشتیبانی از فایل‌های ویدیو و مستند
• استخراج اطلاعات مدت زمان و کیفیت
• ایجاد کپشن فارسی بهبود یافته
• تگ‌گذاری خودکار
• لینک اشتراک گذاری آسان
"""
    
    await message.reply_text(help_text, disable_web_page_preview=True)