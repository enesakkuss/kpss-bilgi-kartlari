$utf8 = [System.Text.Encoding]::UTF8

function Get-CardsFromCSV($fileName) {
    $filePath = Join-Path $PSScriptRoot $fileName
    $lines = Get-Content $filePath -Encoding UTF8 | Where-Object { $_.Trim() -ne "" }
    $cards = @()
    
    for ($i = 1; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        if ($line -match '^"(.*?)","?(.*?)"?$') {
            $front = $matches[1].Replace('""', '"').Trim()
            $back = $matches[2].Replace('""', '"').Trim()
            if ($front -and $back) {
                $cards += @{
                    id = "c_${i}_$($fileName.Replace('.csv',''))"
                    front = $front
                    back = $back
                    mastered = $false
                }
            }
        }
    }
    return $cards
}

$turkce = Get-CardsFromCSV "turkce_anlam_bilgisi.csv"
$cografya = Get-CardsFromCSV "cografya_bilgi_kartlari.csv"
$tarih = Get-CardsFromCSV "tarih_bilgi_kartlari.csv"
$vatandaslik = Get-CardsFromCSV "vatandaslik_bilgi_kartlari.csv"

# Sadece bu 4 tek kelimelik ana deste kalacak:
$decks = @(
    @{
        id = "deck-turkce"
        title = "Türkçe"
        description = "85 Adet Türkçe Anlam Bilgisi ve Sözcükte Anlam Bilgi Kartları"
        category = "Türkçe"
        createdAt = (Get-Date).ToString("o")
        cards = $turkce
    },
    @{
        id = "deck-cografya"
        title = "Coğrafya"
        description = "80 Adet Türkiye Konumu, İklim ve Fiziki Coğrafya Bilgi Kartları"
        category = "Coğrafya"
        createdAt = (Get-Date).ToString("o")
        cards = $cografya
    },
    @{
        id = "deck-tarih"
        title = "Tarih"
        description = "102 Adet İslamiyet Öncesi ve Türk-İslam Tarihi Bilgi Kartları"
        category = "Tarih"
        createdAt = (Get-Date).ToString("o")
        cards = $tarih
    },
    @{
        id = "deck-vatandaslik"
        title = "Vatandaşlık"
        description = "75 Adet Anayasa Hukuku, Seçimler ve Kamu Hakları Bilgi Kartları"
        category = "Vatandaşlık"
        createdAt = (Get-Date).ToString("o")
        cards = $vatandaslik
    }
)

$json = $decks | ConvertTo-Json -Depth 5
$jsContent = "// Örnek Desteler (NotebookLM Flashcards)`nconst SAMPLE_DECKS = $json;"
Set-Content -Path (Join-Path $PSScriptRoot "js/samples.js") -Value $jsContent -Encoding UTF8
Write-Host "js/samples.js başarıyla tek kelimelik 4 başlıkla güncellendi!"
