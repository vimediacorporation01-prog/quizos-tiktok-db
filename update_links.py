import json
import subprocess
import datetime

# --- KONFIGURASI ---
# Ganti dengan username TikTok target (pakai @)
TIKTOK_USER = "@jkt48.official" 
# Jumlah video yang mau diambil
LIMIT = 5 

def get_tiktok_links():
    print(f"Sedang mengambil video dari {TIKTOK_USER}...")
    
    # Perintah yt-dlp untuk mengambil data JSON tanpa download video
    # flat-playlist: biar cepat
    # dump-json: output data text
    cmd = [
        "yt-dlp",
        f"https://www.tiktok.com/{TIKTOK_USER}",
        "--flat-playlist",
        "--dump-json",
        "--playlist-end", str(LIMIT)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        videos = []
        
        # Proses setiap baris output
        for line in result.stdout.strip().split('\n'):
            if line:
                data = json.loads(line)
                
                # Kita butuh direct link video. 
                # Karena link TikTok sering expire, kita simpan Link Asli TikToknya
                # Nanti di HTML kita perlu cara khusus, atau kita ambil url langsung
                # Untuk cara paling stabil di HTML5 Video Player biasa, kita butuh link MP4.
                # Kita gunakan yt-dlp -g (get-url) nanti di client, atau disini kita ambil URL asli.
                
                # Untuk tutorial ini, kita simpan URL MP4 langsung (NOTE: Link ini bisa expired dalam 24 jam)
                # Jadi script ini harus jalan sering (tiap jam).
                
                # Mendapatkan direct link mp4 (membutuhkan request tambahan)
                direct_url_cmd = ["yt-dlp", "-g", data['url']]
                direct_res = subprocess.run(direct_url_cmd, capture_output=True, text=True)
                mp4_url = direct_res.stdout.strip()
                
                video_obj = {
                    "title": data.get('title', 'Video TikTok'),
                    "url": mp4_url, # Ini link streaming langsung
                    "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "original_link": data.get('url')
                }
                
                if mp4_url: # Cuma simpan kalau sukses dapat link
                    videos.append(video_obj)
                    print(f"Dapat: {data.get('title')}")
                    
        return videos

    except Exception as e:
        print(f"Error: {e}")
        return []

# --- PROSES UTAMA ---
new_shorts = get_tiktok_links()

if new_shorts:
    # Buka database lama
    try:
        with open('vl_data.json', 'r') as f:
            db = json.load(f)
    except:
        db = {"shorts": [], "complex": []}

    # Update (Timpa data lama dengan yang baru biar linknya segar terus)
    # Karena link TikTok cepat mati, kita refresh total untuk list teratas
    db['shorts'] = new_shorts
    
    # Simpan kembali
    with open('vl_data.json', 'w') as f:
        json.dump(db, f, indent=2)
    print("Database berhasil diupdate!")
else:
    print("Tidak ada video yang ditemukan.")
