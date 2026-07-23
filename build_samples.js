const fs = require('fs');
const path = require('path');

function parseCSV(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n').map(l => l.trim()).filter(Boolean);
    const cards = [];

    // Header atla
    for (let i = 1; i < lines.length; i++) {
        const line = lines[i];
        if (!line) continue;

        // CSV parselama (tırnak içindeki virgülleri koruyarak)
        const match = line.match(/^"(.*?)","?(.*?)"?$/);
        if (match) {
            let front = match[1].replace(/""/g, '"').trim();
            let back = match[2].replace(/""/g, '"').trim();
            if (front && back) {
                cards.push({
                    id: `c_${i}_${Date.now()}`,
                    front,
                    back,
                    mastered: false
                });
            }
        } else {
            // Basit ayırma
            const parts = line.split(',');
            if (parts.length >= 2) {
                cards.push({
                    id: `c_${i}_${Date.now()}`,
                    front: parts[0].replace(/"/g, '').trim(),
                    back: parts.slice(1).join(',').replace(/"/g, '').trim(),
                    mastered: false
                });
            }
        }
    }
    return cards;
}

const baseDir = __dirname;

const decks = [
    {
        id: 'sample-vatandaslik-full',
        title: 'Vatandaşlık & Anayasa Hukuku Tarihi',
        description: '1921, 1924 ve 1961 Anayasaları, Seçimler, Kadın Hakları (BMV), YSK ve Hukuk 75+ soru ve cevabı.',
        category: 'Vatandaşlık',
        createdAt: new Date().toISOString(),
        file: 'vatandaslik_bilgi_kartlari.csv'
    },
    {
        id: 'sample-cografya-full',
        title: 'Coğrafya - Türkiye Konumu, İklim ve Fiziki Coğrafya',
        description: 'Matematik/Göreceli Konum, Sınır Kapıları, Saatler, Yer Şekilleri ve Jeoloji 80+ soru ve cevabı.',
        category: 'Coğrafya',
        createdAt: new Date().toISOString(),
        file: 'cografya_bilgi_kartlari.csv'
    },
    {
        id: 'sample-tarih-full',
        title: 'Tarih - İslamiyet Öncesi ve Türk-İslam Tarihi',
        description: 'Orta Asya Türk Devletleri, Türk-İslam Bilginleri, Selçuklular ve Beylikler 100+ soru ve cevabı.',
        category: 'Tarih',
        createdAt: new Date().toISOString(),
        file: 'tarih_bilgi_kartlari.csv'
    },
    {
        id: 'sample-turkce-anlam',
        title: 'Türkçe Anlam Bilgisi & Sözcükte Anlam',
        description: 'Gerçek/Mecaz Anlam, Yan Anlam, Ad Aktarması, Dolaylama, Kinaye, Duyu Aktarımı ve İkilemeler 85+ soru ve cevabı.',
        category: 'Türkçe',
        createdAt: new Date().toISOString(),
        file: 'turkce_anlam_bilgisi.csv'
    }
];

const compiledDecks = decks.map(d => {
    const cards = parseCSV(path.join(baseDir, d.file));
    console.log(`${d.title}: ${cards.length} kart okundu.`);
    return {
        id: d.id,
        title: d.title,
        description: d.description,
        category: d.category,
        createdAt: d.createdAt,
        cards: cards
    };
});

const fileContent = `// Örnek Desteler (Sample Decks for NotebookLM Flashcards)
const SAMPLE_DECKS = ${JSON.stringify(compiledDecks, null, 4)};
`;

fs.writeFileSync(path.join(baseDir, 'js', 'samples.js'), fileContent, 'utf8');
console.log('js/samples.js başarıyla tüm kartlarla oluşturuldu!');
