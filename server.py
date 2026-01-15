# server.py - M3U8 工具箱专用后端 (Ultimate Pro版)
# 核心功能：全能解析 + 极速响应 + 防风控 + 封面提取 + 音频支持
# 运行端口：5000
import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

# --- 1. 基础环境设置 ---
# 关闭 Flask 和 Werkzeug 的调试日志，保持控制台清爽
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
# 允许跨域请求，确保 GitHub Pages 前端能连接到这个本地后端
CORS(app)

# --- 2. 核心解析路由 ---
@app.route('/api/check', methods=['GET'])
def check_url():
    # 获取前端传来的 url 参数
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "请提供链接 (URL is required)"}), 400

    print(f"\n📡 [收到请求] 正在深度分析: {url}")

    # --- 3. yt-dlp 深度优化配置 (性能与稳定性的平衡) ---
    ydl_opts = {
        # > 网络稳定性配置
        'socket_timeout': 20,       # 延长超时，适应移动数据网络
        'retries': 5,               # 失败重试次数增加到 5 次
        'nocheckcertificate': True, # 忽略 SSL 证书错误 (老旧设备救星)
        
        # > 核心功能配置：只解析，不下载
        'simulate': True,           # 模拟模式
        'skip_download': True,      # 跳过下载
        'force_json': True,         # 强制输出 JSON 格式
        
        # > 性能优化配置
        'quiet': True,              # 静默模式，减少 I/O
        'no_warnings': True,        # 忽略非致命警告
        'noplaylist': True,         # 禁止解析播放列表，只取当前单集 (提速 10倍!)
        'extract_flat': False,      # 必须深度解析才能拿到 m3u8 真实地址
        
        # > 防风控伪装配置 (模拟真实用户)
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        },
        # 针对 YouTube 的特殊优化：伪装成安卓客户端
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
                'player_skip': ['webpage', 'configs', 'js'], # 跳过不必要的页面加载
            }
        }
    }

    try:
        # 初始化下载器
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 执行解析
            info = ydl.extract_info(url, download=False)
            
            # --- 4. 智能格式清洗与分类 ---
            formats_cleaned = []
            if 'formats' in info:
                for f in info['formats']:
                    # 获取编码信息
                    vcodec = f.get('vcodec', 'none')
                    acodec = f.get('acodec', 'none')
                    ext = f.get('ext', '')
                    proto = f.get('protocol', '')
                    fid = f.get('format_id', '')

                    # 判定逻辑：
                    # 1. 视频: 有视频编码 (vcodec != none)
                    # 2. 音频: 无视频编码但有音频编码 (纯音频流)
                    # 3. 直播: 协议包含 m3u8
                    is_video = vcodec != 'none'
                    is_audio_only = (vcodec == 'none' and acodec != 'none')
                    is_m3u8 = 'm3u8' in proto or ext == 'm3u8'
                    
                    # 过滤掉完全无效的流 (无音无画)
                    if is_video or is_audio_only or is_m3u8:
                        # 生成易读的标签 (Format Note)
                        raw_note = f.get('format_note') or f.get('resolution') or str(f.get('height', '?')) + 'p'
                        
                        if is_audio_only:
                            # 给音频加上独特的 Emoji 提示，前端绿色 Badge 显示
                            display_label = "🎵 纯音频 (Audio)"
                        elif is_m3u8:
                            display_label = f"🔴 直播 ({raw_note})"
                        else:
                            # 普通视频，直接显示画质 (如 1080p, HDR)
                            display_label = raw_note

                        # 构造精简数据返回给前端
                        formats_cleaned.append({
                            "format_id": fid,
                            "ext": ext,
                            "resolution": f.get('resolution'),
                            "format_note": display_label, # 前端直接展示这个字段
                            "url": f.get('url'),
                            "protocol": proto,
                            "is_audio": is_audio_only
                        })

            # --- 5. 获取关键元数据 ---
            title = info.get('title', '未知标题')
            duration = info.get('duration')       # 视频时长 (秒)
            extractor = info.get('extractor', '未知来源')
            thumbnail = info.get('thumbnail')     # 封面图 (新增功能)

            print(f"✅ [解析成功] {title[:30]}... (来源: {extractor}, 格式数: {len(formats_cleaned)})")
            
            # --- 6. 返回标准 JSON ---
            return jsonify({
                "status": "success",
                "title": title,
                "extractor": extractor,
                "duration": duration,
                "thumbnail": thumbnail,     # 返回封面给前端
                "webpage_url": info.get('webpage_url'),
                "formats": formats_cleaned  # 清洗后的格式列表
            })

    except Exception as e:
        err_msg = str(e)
        print(f"❌ [解析失败] {err_msg[:60]}...")
        
        # 针对常见错误的智能提示
        if "Sign in" in err_msg:
            return jsonify({"error": "⚠️ 访问受限：该视频需要登录 (Cookies失效) 或被平台风控"}), 403
        if "Video unavailable" in err_msg:
            return jsonify({"error": "❌ 视频无效：已被删除或设置为私享"}), 404
        if "Geo-restricted" in err_msg:
            return jsonify({"error": "🌍 地区限制：当前服务器节点无法观看此视频"}), 403
        if "Live event will begin" in err_msg:
            return jsonify({"error": "⏳ 直播未开始：请稍后再试"}), 403
            
        # 其他未知错误
        return jsonify({"error": f"解析错误: {err_msg[:100]}"}), 500

if __name__ == '__main__':
    print("="*50)
    print("🚀 M3U8 工具箱后端 (Ultimate Edition) 已启动")
    print("📍 监听端口: 5000 (允许局域网/穿透访问)")
    print("⚡ 功能状态: 音频支持[√] 封面提取[√] 防风控[√]")
    print("="*50)
    # host='0.0.0.0' 让手机变成服务器，允许外部访问
    app.run(host='0.0.0.0', port=5000)
