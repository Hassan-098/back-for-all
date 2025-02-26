rom flask import Flask, request, jsonify, Response
import yt_dlp
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    type = data.get('type', 'video')

    if not url:
        return jsonify({"success": False, "error": "يجب إدخال رابط الفيديو"}), 400

    output_filename = "downloaded_video.mp4" if type == "video" else "downloaded_audio.mp3"
    
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best' if type == "video" else 'bestaudio/best',
        'outtmpl': output_filename,
        'noplaylist': False if type == "playlist" else True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        def generate():
            with open(output_filename, 'rb') as f:
                while chunk := f.read(8192):  
                    yield chunk

        return Response(generate(), content_type="video/mp4", headers={
            "Content-Disposition": f"attachment; filename={output_filename}"
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if name == '__main__':
    app.run()
