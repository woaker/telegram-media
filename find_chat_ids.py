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
            
            # 视频平台和媒体频道
            "@youtube",  # YouTube官方
            "@netflix",  # Netflix官方
            "@disney",  # Disney官方
            "@marvel",  # Marvel官方
            "@starwars",  # Star Wars官方
            "@pixar",  # Pixar官方
            "@warnerbros",  # Warner Bros官方
            "@sonypictures",  # Sony Pictures官方
            "@universalpictures",  # Universal Pictures官方
            "@paramount",  # Paramount官方
            
            # 科技视频频道
            "@verge",  # The Verge科技媒体
            "@techcrunch",  # TechCrunch科技媒体
            "@wired",  # Wired科技媒体
            "@ars",  # Ars Technica科技媒体
            "@engadget",  # Engadget科技媒体
            "@gizmodo",  # Gizmodo科技媒体
            "@mashable",  # Mashable科技媒体
            "@thenextweb",  # The Next Web科技媒体
            
            # 游戏视频频道
            "@nintendo",  # Nintendo官方
            "@playstation",  # PlayStation官方
            "@xbox",  # Xbox官方
            "@steam",  # Steam官方
            "@epicgames",  # Epic Games官方
            "@ubisoft",  # Ubisoft官方
            "@ea",  # Electronic Arts官方
            "@activision",  # Activision官方
            "@rockstargames",  # Rockstar Games官方
            
            # 音乐视频频道
            "@spotify",  # Spotify官方
            "@apple_music",  # Apple Music官方
            "@youtube_music",  # YouTube Music官方
            "@tidal",  # Tidal官方
            "@deezer",  # Deezer官方
            "@soundcloud",  # SoundCloud官方
            "@bandcamp",  # Bandcamp官方
            
            # 教育视频频道
            "@khanacademy",  # Khan Academy教育
            "@coursera",  # Coursera在线教育
            "@edx",  # edX在线教育
            "@udemy",  # Udemy在线教育
            "@skillshare",  # Skillshare在线教育
            "@masterclass",  # MasterClass在线教育
            "@ted",  # TED演讲
            "@tedx",  # TEDx演讲
            
            # 新闻视频频道
            "@cnn",  # CNN新闻
            "@bbc",  # BBC新闻
            "@reuters",  # Reuters新闻
            "@ap",  # Associated Press新闻
            "@bloomberg",  # Bloomberg新闻
            "@cnbc",  # CNBC财经新闻
            "@foxnews",  # Fox News新闻
            "@msnbc",  # MSNBC新闻
            
            # 体育视频频道
            "@espn",  # ESPN体育
            "@nfl",  # NFL官方
            "@nba",  # NBA官方
            "@mlb",  # MLB官方
            "@nhl",  # NHL官方
            "@fifa",  # FIFA官方
            "@uefa",  # UEFA官方
            "@olympics",  # 奥运会官方
            
            # 中国视频平台
            "@tencent",  # 腾讯官方频道
            "@baidu",  # 百度官方频道
            "@alibaba",  # 阿里巴巴官方频道
            "@jd",  # 京东官方频道
            "@meituan",  # 美团官方频道
            "@didi",  # 滴滴官方频道
            "@bilibili",  # B站官方
            "@douyin",  # 抖音官方
            "@kuaishou",  # 快手官方
            "@xiaohongshu",  # 小红书官方
            "@weibo",  # 微博官方
            "@zhihu",  # 知乎官方
            
            # 其他热门频道
            "@yyybbb",  
            "dyjs01"
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