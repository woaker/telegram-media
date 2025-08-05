#!/usr/bin/env python3
"""测试用户认证"""

import asyncio
import pyrogram
from loguru import logger

async def test_user_auth():
    """测试用户认证"""
    try:
        logger.info("创建用户客户端...")
        # 创建用户客户端
        client = pyrogram.Client(
            "user_session",
            api_id=26645966,
            api_hash="4da03a108492e1d45d18f21eded76cfc",
            workdir="sessions"
        )
        
        logger.info("开始用户认证...")
        await client.start()
        
        # 获取用户信息
        me = await client.get_me()
        logger.success(f"用户认证成功！用户信息: {me}")
        
        # 测试获取收藏夹
        try:
            chat = await client.get_chat("me")
            logger.success(f"成功获取收藏夹信息: {chat}")
        except Exception as e:
            logger.error(f"获取收藏夹失败: {e}")
        
        # 测试获取消息历史
        try:
            # 获取最近的消息
            messages = await client.get_chat_history("me", limit=1)
            for msg in messages:
                logger.success(f"成功获取消息: {msg.id}")
        except Exception as e:
            logger.error(f"获取消息历史失败: {e}")
        
        await client.stop()
        
    except Exception as e:
        logger.error(f"用户认证测试失败: {e}")

if __name__ == "__main__":
    logger.info("开始测试用户认证...")
    asyncio.run(test_user_auth()) 