#!/bin/bash

# Telegram Media Downloader 网络诊断脚本
# 用于检查网络连接和代理设置

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "🌐 Telegram Media Downloader 网络诊断工具"
echo "=========================================="
echo ""

# 检查基本网络连接
echo "📡 检查基本网络连接..."
echo "----------------------------------------"

# 检查DNS解析
echo "DNS解析测试:"
if nslookup api.telegram.org > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓ api.telegram.org 解析正常${NC}"
else
    echo -e "  ${RED}✗ api.telegram.org 解析失败${NC}"
fi

if nslookup core.telegram.org > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓ core.telegram.org 解析正常${NC}"
else
    echo -e "  ${RED}✗ core.telegram.org 解析失败${NC}"
fi

echo ""

# 检查HTTP连接
echo "HTTP连接测试:"
if curl -s --connect-timeout 10 https://api.telegram.org > /dev/null; then
    echo -e "  ${GREEN}✓ 直接连接 Telegram API 成功${NC}"
    DIRECT_CONNECTION=true
else
    echo -e "  ${RED}✗ 直接连接 Telegram API 失败${NC}"
    DIRECT_CONNECTION=false
fi

echo ""

# 检查常见代理端口
echo "🔍 检查常见代理端口..."
echo "----------------------------------------"

PROXY_PORTS=(7890 1080 8080 3128 8118 8888 10808 10809)
PROXY_FOUND=false

for port in "${PROXY_PORTS[@]}"; do
    if nc -z -w1 127.0.0.1 $port 2>/dev/null; then
        echo -e "  ${GREEN}✓ 发现代理服务在端口 $port${NC}"
        PROXY_FOUND=true
        PROXY_PORT=$port
    fi
done

if [ "$PROXY_FOUND" = false ]; then
    echo -e "  ${YELLOW}⚠ 未发现本地代理服务${NC}"
fi

echo ""

# 检查环境变量中的代理设置
echo "🌍 检查环境变量代理设置..."
echo "----------------------------------------"

if [ -n "$http_proxy" ]; then
    echo -e "  ${BLUE}📋 http_proxy: $http_proxy${NC}"
fi

if [ -n "$https_proxy" ]; then
    echo -e "  ${BLUE}📋 https_proxy: $https_proxy${NC}"
fi

if [ -n "$HTTP_PROXY" ]; then
    echo -e "  ${BLUE}📋 HTTP_PROXY: $HTTP_PROXY${NC}"
fi

if [ -n "$HTTPS_PROXY" ]; then
    echo -e "  ${BLUE}📋 HTTPS_PROXY: $HTTPS_PROXY${NC}"
fi

if [ -z "$http_proxy" ] && [ -z "$https_proxy" ] && [ -z "$HTTP_PROXY" ] && [ -z "$HTTPS_PROXY" ]; then
    echo -e "  ${YELLOW}⚠ 未设置环境变量代理${NC}"
fi

echo ""

# 测试代理连接
if [ "$PROXY_FOUND" = true ]; then
    echo "🧪 测试代理连接..."
    echo "----------------------------------------"
    
    # 测试HTTP代理
    if curl -s --connect-timeout 10 --proxy "http://127.0.0.1:$PROXY_PORT" https://api.telegram.org > /dev/null; then
        echo -e "  ${GREEN}✓ 通过HTTP代理连接成功 (端口: $PROXY_PORT)${NC}"
        HTTP_PROXY_WORKING=true
    else
        echo -e "  ${RED}✗ 通过HTTP代理连接失败 (端口: $PROXY_PORT)${NC}"
        HTTP_PROXY_WORKING=false
    fi
    
    # 测试SOCKS5代理
    if command -v curl > /dev/null && curl --version | grep -q "socks"; then
        if curl -s --connect-timeout 10 --socks5 "127.0.0.1:$PROXY_PORT" https://api.telegram.org > /dev/null; then
            echo -e "  ${GREEN}✓ 通过SOCKS5代理连接成功 (端口: $PROXY_PORT)${NC}"
            SOCKS5_PROXY_WORKING=true
        else
            echo -e "  ${RED}✗ 通过SOCKS5代理连接失败 (端口: $PROXY_PORT)${NC}"
            SOCKS5_PROXY_WORKING=false
        fi
    else
        echo -e "  ${YELLOW}⚠ 当前curl版本不支持SOCKS5代理测试${NC}"
    fi
fi

echo ""

# 提供配置建议
echo "💡 配置建议:"
echo "----------------------------------------"

if [ "$DIRECT_CONNECTION" = true ]; then
    echo -e "${GREEN}✓ 您的网络可以直接访问Telegram，无需配置代理${NC}"
    echo "  可以直接使用原始配置文件启动服务"
elif [ "$PROXY_FOUND" = true ]; then
    echo -e "${YELLOW}⚠ 建议配置代理来解决网络连接问题${NC}"
    echo ""
    echo "推荐配置 (添加到 config.yaml):"
    echo ""
    
    if [ "$HTTP_PROXY_WORKING" = true ]; then
        echo "HTTP代理配置:"
        echo "proxy:"
        echo "  scheme: \"http\""
        echo "  hostname: \"127.0.0.1\""
        echo "  port: $PROXY_PORT"
        echo "  username: \"\""
        echo "  password: \"\""
        echo ""
    fi
    
    if [ "$SOCKS5_PROXY_WORKING" = true ]; then
        echo "SOCKS5代理配置:"
        echo "proxy:"
        echo "  scheme: \"socks5\""
        echo "  hostname: \"127.0.0.1\""
        echo "  port: $PROXY_PORT"
        echo "  username: \"\""
        echo "  password: \"\""
        echo ""
    fi
    
    echo "配置完成后，重新启动服务:"
    echo "  ./start.sh start"
else
    echo -e "${RED}✗ 网络连接问题，建议:${NC}"
    echo "1. 检查网络连接"
    echo "2. 配置VPN或代理服务"
    echo "3. 联系网络管理员"
    echo ""
    echo "如果使用代理，请参考 config_proxy_example.yaml 文件"
fi

echo ""

# 检查配置文件
echo "📋 检查当前配置文件..."
echo "----------------------------------------"

if [ -f "config.yaml" ]; then
    if grep -q "proxy:" config.yaml; then
        echo -e "  ${GREEN}✓ 配置文件中已包含代理设置${NC}"
        echo "当前代理配置:"
        grep -A 5 "proxy:" config.yaml | sed 's/^/  /'
    else
        echo -e "  ${YELLOW}⚠ 配置文件中未包含代理设置${NC}"
    fi
else
    echo -e "  ${RED}✗ 配置文件不存在${NC}"
fi

echo ""
echo "=========================================="
echo "诊断完成！根据上述建议配置代理后重试启动服务。" 