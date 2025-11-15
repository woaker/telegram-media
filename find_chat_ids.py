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
            "find_chat_ids",  # 使用不同的session名称避免冲突
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
            "@github",  # GitHub官方频道

            # 视频平台和媒体频道
            "@netflix",  # Netflix官方
            "@disney",  # Disney官方
            "@marvel",  # Marvel官方
            "@pixar",  # Pixar官方
            "@universalpictures",  # Universal Pictures官方

        
            # 科技视频频道
            "@verge",  # The Verge科技媒体
            "@techcrunch",  # TechCrunch科技媒体
            "@engadget",  # Engadget科技媒体
            "@gizmodo",  # Gizmodo科技媒体
            
            
            # 音乐视频频道
            "@spotify",  # Spotify官方
            "@deezer",  # Deezer官方
            
            # 教育视频频道
            "@udemy",  # Udemy在线教育
            "@skillshare",  # Skillshare在线教育
            "@masterclass",  # MasterClass在线教育

            
            # 新闻视频频道
            "@bloomberg",  # Bloomberg新闻
            "@cnbc",  # CNBC财经新闻
            "@foxnews",  # Fox News新闻
            
            # 中国视频平台
            "@tencent",  # 腾讯官方频道
            "@baidu",  # 百度官方频道
            "@alibaba",  # 阿里巴巴官方频道
            "@meituan",  # 美团官方频道
            "@dyjs01"
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