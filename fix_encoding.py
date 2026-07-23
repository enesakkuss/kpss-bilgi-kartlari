import csv
import json
import os

base_dir = r"c:\Users\enes.akkus\Desktop\bilgi kartları"

files_map = [
    {
        "id": "deck-karma",
        "title": "Karma",
        "description": "160+ Adet Genel Karma Türkçe, Tarih, Coğrafya ve Vatandaşlık Bilgi Kartları",
        "category": "Karma",
        "file": "karma_bilgi_kartlari.csv"
    },
    {
        "id": "deck-turkce",
        "title": "Türkçe",
        "description": "85 Adet Türkçe Anlam Bilgisi ve Sözcükte Anlam Bilgi Kartları",
        "category": "Türkçe",
        "file": "turkce_anlam_bilgisi.csv"
    },
    {
        "id": "deck-cografya",
        "title": "Coğrafya",
        "description": "80 Adet Türkiye Konumu, İklim ve Fiziki Coğrafya Bilgi Kartları",
        "category": "Coğrafya",
        "file": "cografya_bilgi_kartlari.csv"
    },
    {
        "id": "deck-tarih",
        "title": "Tarih",
        "description": "102 Adet İslamiyet Öncesi ve Türk-İslam Tarihi Bilgi Kartları",
        "category": "Tarih",
        "file": "tarih_bilgi_kartlari.csv"
    },
    {
        "id": "deck-vatandaslik",
        "title": "Vatandaşlık",
        "description": "75 Adet Anayasa Hukuku, Seçimler ve Kamu Hakları Bilgi Kartları",
        "category": "Vatandaşlık",
        "file": "vatandaslik_bilgi_kartlari.csv"
    }
]

decks = []

for item in files_map:
    file_path = os.path.join(base_dir, item["file"])
    cards = []
    if os.path.exists(file_path):
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for idx, row in enumerate(reader, 1):
                if len(row) >= 2:
                    front = row[0].strip()
                    back = row[1].strip()
                    if front and back:
                        cards.append({
                            "id": f"c_{idx}_{item['id']}",
                            "front": front,
                            "back": back,
                            "mastered": False
                        })
    print(f"{item['title']}: {len(cards)} kart yüklendi.")
    decks.append({
        "id": item["id"],
        "title": item["title"],
        "description": item["description"],
        "category": item["category"],
        "createdAt": "2026-07-23T12:00:00.000Z",
        "cards": cards
    })

samples_js_path = os.path.join(base_dir, "js", "samples.js")
js_content = f"// Örnek Desteler (NotebookLM Flashcards)\nconst SAMPLE_DECKS = {json.dumps(decks, ensure_ascii=False, indent=4)};\n"

with open(samples_js_path, mode="w", encoding="utf-8") as f:
    f.write(js_content)

print("js/samples.js Karma destesiyle birlikte mükemmel oluşturuldu!")
