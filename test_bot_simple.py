#!/usr/bin/env python3
"""简单的机器人测试"""

import asyncio
import pyrogram
from loguru import logger

async def test_bot():
    """测试机器人功能"""
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
        
        # 获取机器人信息
        me = await client.get_me()
        logger.success(f"机器人信息: {me}")
        
        # 测试获取自己的聊天
        try:
            chat = await client.get_chat("me")
            logger.success(f"成功获取聊天信息: {chat}")
        except Exception as e:
            logger.error(f"获取聊天失败: {e}")
        
        # 测试发送消息到自己的聊天
        try:
            message = await client.send_message("me", "测试消息")
            logger.success(f"成功发送消息: {message.id}")
        except Exception as e:
            logger.error(f"发送消息失败: {e}")
        
        await client.stop()
        
    except Exception as e:
        logger.error(f"机器人测试失败: {e}")

if __name__ == "__main__":
    logger.info("开始测试机器人...")
    asyncio.run(test_bot()) 