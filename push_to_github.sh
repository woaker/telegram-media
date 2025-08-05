#!/bin/bash
# 推送项目到GitHub的脚本

echo "🚀 准备推送项目到GitHub..."

# 添加远程仓库
git remote add woaker https://github.com/woaker/telegram-media.git

# 推送代码
echo "📤 推送代码到GitHub..."
git push -u woaker master

echo "✅ 推送完成！"
echo "🌐 访问 https://github.com/woaker/telegram-media 查看您的仓库" 