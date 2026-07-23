import os
import csv
import re

base_dir = r"c:\Users\enes.akkus\Desktop\bilgi kartları"

files = [
    "karma_bilgi_kartlari.csv",
    "turkce_anlam_bilgisi.csv",
    "cografya_bilgi_kartlari.csv",
    "tarih_bilgi_kartlari.csv",
    "vatandaslik_bilgi_kartlari.csv"
]

def normalize_text(text):
    # Düzensiz tırnak, boşluk ve parantez temizliği
    text = re.sub(r'\[\d+\]', '', text)  # [1], [2] gibi kaynak numaralarını kaldır
    text = text.replace('"', '').replace("'", "").strip().lower()
    return text

total_removed = 0

for file_name in files:
    file_path = os.path.join(base_dir, file_name)
    if not os.path.exists(file_path):
        continue
    
    unique_rows = []
    seen_questions = set()
    removed_count = 0
    
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        
        for row in reader:
            if len(row) >= 2:
                q = row[0].strip()
                a = row[1].strip()
                norm_q = normalize_text(q)
                
                if norm_q and norm_q not in seen_questions:
                    seen_questions.add(norm_q)
                    unique_rows.append([q, a])
                else:
                    removed_count += 1
    
    # Dosyayı tekrarlardan arındırılmış haliyle kaydet
    with open(file_path, "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Soru/Kavram", "Cevap/Açıklama"])
        for r in unique_rows:
            writer.writerow(r)
            
    total_removed += removed_count
    print(f"{file_name}: {removed_count} adet mükerrer (aynı) soru temizlendi. Kalan benzersiz soru: {len(unique_rows)}")

print(f"\nTOPLAM TEMİZLENEN MÜKERRER SORU SAYISI: {total_removed}")
