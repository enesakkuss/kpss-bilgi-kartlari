import csv
import json
import os

base_dir = r"c:\Users\enes.akkus\Desktop\bilgi kartları"

files_map = [
    {
        "id": "deck-karma",
        "title": "Karma",
        "description": "195 Adet Genel Karma Türkçe, Tarih, Coğrafya ve Vatandaşlık Bilgi Kartları",
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

# index.html dosyasına doğrudan SAMPLE_DECKS göm ki GitHub klasör yükleme sorununda dahi %100 çalışsın!
index_html_path = os.path.join(base_dir, "index.html")

html_content = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NotebookLM Bilgi Kartları - İnteraktif Öğrenme Platformu</title>
    <meta name="description" content="NotebookLM özet ve bilgi kartlarınızı kolayca yükleyip 3D kartlar, testler ve eşleştirme oyunlarıyla çalışabileceğiniz modern web platformu.">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="app-container">
        <!-- Header -->
        <header class="app-header">
            <div class="logo-area">
                <span class="logo-icon">🎴</span>
                <h1>NotebookLM Kartları</h1>
                <span class="badge-tag">v2.0 AI Ready</span>
            </div>
            <div class="header-actions">
                <div class="global-stats" id="globalStatsDisplay">
                    🔥 Toplam Çalışılan: <strong>0</strong> | Öğrenilen: <strong>0</strong>
                </div>
            </div>
        </header>

        <!-- Deste Seçimi & İçe Aktarma Barı -->
        <section class="deck-selector-bar">
            <div class="deck-select-group">
                <label for="deckSelect">Aktif Çalışma Destesi</label>
                <select id="deckSelect" class="custom-select">
                    <!-- JavaScript ile dinamik dolacak -->
                </select>
                <div class="deck-desc-text" id="deckDesc">Deste açıklaması burada görünecek...</div>
            </div>
            <div class="btn-group">
                <button class="ctrl-btn primary-btn" id="openUploadModalBtn">
                    ✨ + NotebookLM Kart Yükle
                </button>
                <button class="ctrl-btn secondary-btn" id="newDeckBtn">
                    📁 Yeni Deste
                </button>
            </div>
        </section>

        <!-- Öğrenme Modu Sekmeleri -->
        <nav class="mode-tabs">
            <button class="tab-btn active" data-mode="flashcard">
                <span>🎴</span> 3D Kart Modu
            </button>
            <button class="tab-btn" data-mode="quiz">
                <span>📝</span> Test Modu (Quiz)
            </button>
            <button class="tab-btn" data-mode="match">
                <span>🧩</span> Eşleştirme Oyunu
            </button>
            <button class="tab-btn" data-mode="manage">
                <span>⚙️</span> Kart Yönetimi
            </button>
        </nav>

        <!-- Ana Mod Alanı -->
        <main class="mode-stage" id="modeContainer">
            <!-- İlgili mod JS tarafından buraya yüklenecektir -->
        </main>

        <!-- Footer -->
        <footer class="app-footer">
            <p>NotebookLM Bilgi Kartı Platformu • Yerel Tarayıcı Veri Depolamalı (LocalStorage)</p>
        </footer>
    </div>

    <!-- NotebookLM Kart Yükleme Modalı -->
    <div class="modal-overlay" id="uploadModal">
        <div class="modal-container">
            <div class="modal-header">
                <h3>NotebookLM Kart / Metin Yükle</h3>
                <button class="close-modal-btn" id="closeUploadModalBtn">&times;</button>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <label for="importDeckTitle">Deste Başlığı</label>
                    <input type="text" id="importDeckTitle" class="text-input" placeholder="Örn: Yapay Zeka Notları, Tarih Sınavı...">
                </div>

                <div class="form-group">
                    <label for="importTextarea">Metin Yapıştır (Soru/Cevap, Tablo, Q/A veya Liste Biçimi)</label>
                    <textarea id="importTextarea" class="textarea-input" placeholder="NotebookLM'den kopyaladığınız metni buraya yapıştırın. Örnek biçimler:&#10;Soru: LLM nedir?&#10;Cevap: Devasa dil modelleridir.&#10;&#10;Veya:&#10;Kavram - Açıklama&#10;| Soru | Cevap |"></textarea>
                </div>

                <div class="form-group">
                    <label>Veya Dosya Yükleyin (.json, .csv, .txt, .md)</label>
                    <div class="file-drop-zone" onclick="document.getElementById('fileInput').click();">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📄</div>
                        <p>Dosyayı buraya sürükleyin veya <strong>Bilgisayardan Seçin</strong></p>
                        <input type="file" id="fileInput" accept=".json,.csv,.txt,.md" style="display: none;">
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button class="ctrl-btn secondary-btn" onclick="document.getElementById('uploadModal').classList.remove('active');">İptal</button>
                <button class="ctrl-btn primary-btn" id="processImportBtn">🚀 Kartları İçe Aktar</button>
            </div>
        </div>
    </div>

    <!-- Örnek Kartlar Dahili Olarak Tanımlanır (GitHub 404 Önleyici) -->
    <script charset="utf-8">
        const SAMPLE_DECKS = {json.dumps(decks, ensure_ascii=False, indent=4)};
    </script>
    <script src="js/parser.js" charset="utf-8"></script>
    <script src="js/storage.js" charset="utf-8"></script>
    <script src="js/modes/flashcard.js" charset="utf-8"></script>
    <script src="js/modes/quiz.js" charset="utf-8"></script>
    <script src="js/modes/match.js" charset="utf-8"></script>
    <script src="js/app.js" charset="utf-8"></script>
</body>
</html>
"""

with open(index_html_path, mode="w", encoding="utf-8") as f:
    f.write(html_content)

print("index.html dahili SAMPLE_DECKS ile güncellendi!")
