from flask import Flask, request, send_file, render_template
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url', '').strip()
    if not url:
        return "URL tidak boleh kosong!", 400

    try:
        # Generate nama file unik
        filename = f"{uuid.uuid4().hex}.mp4"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)

        # Opsi yt-dlp
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': filepath,
            'quiet': True,
            'noplaylist': True,
            'merge_output_format': 'mp4',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'video')

        # Kirim file ke user
        return send_file(
            filepath,
            as_attachment=True,
            download_name=f"{title[:50]}.mp4",
            mimetype='video/mp4'
        )

    except Exception as e:
        return f"❌ Gagal download: {str(e)}", 500
    finally:
        # Hapus file setelah 1 menit (opsional — bisa pakai cron/worker)
        # Untuk project kecil, biarkan saja — atau hapus manual
        pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)