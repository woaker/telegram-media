#!/usr/bin/env python3
"""测试Telegram认证状态"""

import asyncio
import pyrogram
from loguru import logger

async def test_auth():
    """测试认证状态"""
    try:
        # 使用相同的配置
        client = pyrogram.Client(
            "media_downloader",
            api_id=26645966,
            api_hash="4da03a108492e1d45d18f21eded76cfc",
            workdir="sessions"
        )
        
        await client.start()
        
        # 获取用户信息
        me = await client.get_me()
        logger.success(f"认证成功！用户信息: {me}")
        
        # 测试获取聊天信息
        try:
            # 测试获取自己的收藏夹
            chat = await client.get_chat("me")
            logger.success(f"成功获取收藏夹信息: {chat}")
        except Exception as e:
            logger.error(f"获取收藏夹失败: {e}")
        
        # 测试获取其他聊天
        test_chat_ids = ["me", -1001234567890, 123456789]  # 示例ID
        
        for chat_id in test_chat_ids:
            try:
                chat = await client.get_chat(chat_id)
                logger.success(f"成功获取聊天 {chat_id}: {chat.title if hasattr(chat, 'title') else chat}")
            except Exception as e:
                logger.warning(f"无法获取聊天 {chat_id}: {e}")
        
        await client.stop()
        
    except Exception as e:
        logger.error(f"认证测试失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_auth()) 