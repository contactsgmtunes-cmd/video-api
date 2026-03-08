from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/")
def home():
    return "Video Downloader API Running"

@app.route("/analyze")
def analyze():

    url = request.args.get("url")

    if not url:
        return jsonify({
            "status": "error",
            "message": "No URL provided"
        })

    try:

        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "nocheckcertificate": True,
            "geo_bypass": True,
            "noplaylist": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = []

        for f in info.get("formats", []):
            if f.get("url") and f.get("ext") in ["mp4", "m4a", "webm"]:
                formats.append({
                    "format_id": f.get("format_id"),
                    "quality": f.get("format_note"),
                    "ext": f.get("ext"),
                    "filesize": f.get("filesize"),
                    "url": f.get("url")
                })

        data = {
            "status": "success",
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "formats": formats
        }

        return jsonify(data)

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
