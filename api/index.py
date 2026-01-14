from flask import Flask, request, jsonify
import yt_dlp
import time

app = Flask(__name__)

# 只处理 API 请求，不再处理首页
@app.route('/api/check', methods=['GET'])
def check_url():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "请提供链接"}), 400

    ydl_opts = {
        'socket_timeout': 9,
        'retries': 3,
        'simulate': True,
        'skip_download': True,
        'force_json': True,
        'extract_flat': True,
        'nocheckcertificate': True,
        'source_address': '0.0.0.0',
        'quiet': True,
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats_found = []
            if 'formats' in info:
                for f in info['formats']:
                    if f.get('resolution') != 'audio only' or 'm3u8' in f.get('protocol', '') or f.get('ext') == 'm3u8':
                        note = f.get('format_note') or f.get('resolution') or f.get('height')
                        formats_found.append({
                            "resolution": str(note),
                            "ext": f.get('ext'),
                            "proto": f.get('protocol', 'unknown')
                        })
            return jsonify({
                "status": "success",
                "title": info.get('title', 'Unknown Title'),
                "extractor": info.get('extractor', 'Unknown'),
                "formats": formats_found
            })
    except Exception as e:
        return jsonify({"error": f"解析失败: {str(e)[:100]}"}), 500

# 这是一个 Vercel 需要的入口
app.debug = False
