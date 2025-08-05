#!/usr/bin/env python3
"""查找可用的聊天ID"""

import asyncio
import pyrogram
from loguru import logger

async def find_chat_ids():
    """查找可用的聊天ID"""
    try:
        logger.info("创建机器人客户端...")
        client = pyrogram.Client(
            "media_downloader",
            api_id=26645966,
            api_hash="4da03a108492e1d45d18f21eded76cfc",
            bot_token="7768865131:AAHArbvzadeXr4yP8voqiO-IFYe83gif0bA",
            workdir="sessions"
        )
        
        logger.info("启动机器人...")
        await client.start()
        
        # 测试一些常见的公共频道
        test_channels = [
            "me",  # 自己的收藏夹
            "@telegram",  # Telegram官方频道
            "@durov",  # Telegram创始人频道
            "@python",  # Python官方频道
            "@github",  # GitHub官方频道
            "@microsoft",  # Microsoft官方频道
            "@google",  # Google官方频道
            "@apple",  # Apple官方频道
            "@tesla",  # Tesla官方频道
            "@spacex",  # SpaceX官方频道
        ]
        
        logger.info("测试可用的聊天ID...")
        for chat_id in test_channels:
            try:
                chat = await client.get_chat(chat_id)
                logger.success(f"✅ 可用: {chat_id} -> {chat.title if hasattr(chat, 'title') else chat.first_name}")
            except Exception as e:
                logger.warning(f"❌ 不可用: {chat_id} -> {e}")
        
        await client.stop()
        
    except Exception as e:
        logger.error(f"查找聊天ID失败: {e}")

if __name__ == "__main__":
    logger.info("开始查找可用的聊天ID...")
    asyncio.run(find_chat_ids()) 