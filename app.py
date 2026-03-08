from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/")
def home():
    return "Video API Running"

@app.route("/analyze")
def analyze():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "No URL provided"})

    try:
        ydl_opts = {
         "quiet": True,
    "skip_download": True,
    "nocheckcertificate": True,
    "geo_bypass": True,
    "noplaylist": True,
    "extract_flat": False
         
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = []

        for f in info.get("formats", []):
            if f.get("url"):
                formats.append({
                    "quality": f.get("format_note"),
                    "ext": f.get("ext"),
                    "url": f.get("url")
                })

        return jsonify({
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "formats": formats
        })

    except Exception as e:
        return jsonify({"error": str(e)})
