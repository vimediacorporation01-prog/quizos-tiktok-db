import requests
import json
import datetime

# --- KONFIGURASI (GANTI INI) ---
# Masukkan Username TikTok target (tanpa @)
TARGET_USERNAME = "jkt48.official" 
# -------------------------------

def update_via_api():
    print(f"Sedang mengintip TikTok: {TARGET_USERNAME} lewat Jalur Belakang...")
    
    # Kita pakai API publik dari TikWM (Middleman)
    # Ini lebih ampuh daripada scraping langsung
    url = f"https://www.tikwm.com/api/user/posts?unique_id={TARGET_USERNAME}&count=10"
    
    try:
        # Pura-pura jadi browser biasa
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        new_videos = []
        
        if data.get("code") == 0 and "data" in data and "videos" in data["data"]:
            posts = data["data"]["videos"]
            
            for post in posts:
                # Ambil data penting
                # play: link video tanpa watermark
                # title: caption video
                # create_time: waktu upload
                
                video_url = post.get("play")
                title = post.get("title", "Video TikTok")
                
                # Konversi waktu
                timestamp = post.get("create_time", 0)
                date_str = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
                
                if video_url:
                    video_obj = {
                        "title": title,
                        "url": video_url, 
                        "date": date_str
                    }
                    new_videos.append(video_obj)
                    print(f"Dapat: {title[:30]}...")
            
            return new_videos
        else:
            print("Gagal mengambil data dari API (Mungkin user tidak ditemukan/limit).")
            return []

    except Exception as e:
        print(f"Error parah: {e}")
        return []

# --- EKSEKUSI DAN SIMPAN ---
videos = update_via_api()

if videos:
    # Siapkan struktur database
    db = {
        "shorts": videos, # Timpa data lama biar selalu fresh
        "complex": []
    }
    
    # Simpan ke file
    with open('vl_data.json', 'w') as f:
        json.dump(db, f, indent=2)
    print("SUKSES! Database berhasil diperbarui.")
else:
    print("ZONK! Tidak ada video yang didapat. File tidak diubah.")
    # Kita error-kan biar kelihatan merah di GitHub Action kalau gagal
    exit(1)
