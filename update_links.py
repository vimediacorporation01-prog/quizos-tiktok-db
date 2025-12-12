import requests
import json
import re
import random

# --- GANTI USERNAME TIKTOK DI SINI ---
USER = "jkt48.official"
# -------------------------------------

def get_video():
    # KITA PAKAI 3 JALUR BERBEDA (Biar Tembus)
    sources = [
        f"https://www.tikwm.com/api/user/posts?unique_id={USER}&count=5",
        f"https://tikapi.herokuapp.com/user/{USER}",
        f"https://api.tiktokv.com/aweme/v1/feed/?aweme_id={USER}" # API Cadangan
    ]
    
    headers = {"User-Agent": "Mozilla/5.0"}
    videos = []

    # Coba jalur 1 (TikWM - Paling Stabil)
    try:
        print("Mencoba Jalur 1...")
        res = requests.get(sources[0], headers=headers, timeout=10)
        data = res.json()
        if data.get("data") and data["data"].get("videos"):
            for v in data["data"]["videos"]:
                videos.append({
                    "title": v.get("title", "Video TikTok"),
                    "url": v.get("play"), # Link MP4 Langsung
                    "date": "Baru Saja"
                })
            return videos
    except:
        pass # Lanjut ke jalur 2 kalau gagal

    # Coba Jalur 2 (Scraping Urlebird - Cadangan Kuat)
    try:
        print("Mencoba Jalur 2...")
        html = requests.get(f"https://urlebird.com/user/{USER}/", headers=headers).text
        links = re.findall(r'src="(https://[^"]+\.mp4[^"]*)"', html)
        captions = re.findall(r'alt="([^"]+)"', html)
        
        for i, link in enumerate(links[:5]):
            title = captions[i] if i < len(captions) else "Video Update"
            videos.append({"title": title, "url": link.replace("&amp;", "&"), "date": "Live Update"})
        
        if videos: return videos
    except:
        pass

    return []

# --- MAIN ---
data = get_video()

if data:
    db = {"shorts": data, "complex": []}
    with open('vl_data.json', 'w') as f:
        json.dump(db, f, indent=2)
    print(f"BERHASIL! Dapat {len(data)} video.")
else:
    print("GAGAL SEMUA JALUR. TikTok lagi galak.")
    # Kita tidak update file biar data lama gak ilang
