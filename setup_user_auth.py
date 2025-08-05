#!/usr/bin/env python3
"""用户认证设置脚本"""

import asyncio
import pyrogram
from loguru import logger

async def setup_user_auth():
    """设置用户认证"""
    try:
        logger.info("创建用户客户端...")
        client = pyrogram.Client(
            "user_session",
            api_id=26645966,
            api_hash="4da03a108492e1d45d18f21eded76cfc",
            workdir="sessions"
        )
        
        logger.info("开始用户认证...")
        logger.info("请输入您的Telegram手机号码（包含国家代码，如：+8613800138000）")
        await client.start()
        
        # 获取用户信息
        me = await client.get_me()
        logger.success(f"✅ 用户认证成功！用户信息: {me}")
        
        # 测试获取频道信息
        test_channels = ["telegram", "python", "github"]
        for channel in test_channels:
            try:
                chat = await client.get_chat(channel)
                logger.success(f"✅ 成功获取频道 {channel}: {chat.title}")
            except Exception as e:
                logger.warning(f"❌ 无法获取频道 {channel}: {e}")
        
        await client.stop()
        logger.success("用户认证设置完成！")
        
    except Exception as e:
        logger.error(f"用户认证设置失败: {e}")

if __name__ == "__main__":
    logger.info("开始设置用户认证...")
    asyncio.run(setup_user_auth()) 