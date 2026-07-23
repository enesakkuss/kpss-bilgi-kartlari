import os
import json
import csv

base_dir = r"c:\Users\enes.akkus\Desktop\bilgi kartları"

# Read CSS
with open(os.path.join(base_dir, "styles.css"), "r", encoding="utf-8") as f:
    css_content = f.read()

# Add Multiple Choice Quiz Mode CSS
mc_css = """
/* ==========================================================================
   MULTIPLE CHOICE QUIZ MODE STYLES
   ========================================================================== */

.mc-mode-wrapper {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    max-width: 820px;
    margin: 0 auto;
}

.mc-header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--bg-card);
    padding: 0.85rem 1.5rem;
    border-radius: var(--radius-md);
    border: 1px solid var(--glass-border);
}

.mc-score-badge {
    display: flex;
    gap: 1.5rem;
    font-weight: 600;
}

.mc-card-box {
    background: var(--bg-card);
    backdrop-filter: blur(12px);
    border: 2px solid var(--glass-border);
    padding: 2.25rem 2rem;
    border-radius: var(--radius-lg);
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    transition: all 0.3s ease;
}

.mc-card-box.correct-border {
    border-color: var(--emerald-accent);
    box-shadow: 0 0 25px rgba(16, 185, 129, 0.4);
}

.mc-card-box.wrong-border {
    border-color: var(--rose-accent);
    box-shadow: 0 0 25px rgba(244, 63, 94, 0.4);
}

.mc-question-text {
    font-size: 1.25rem;
    font-weight: 700;
    line-height: 1.6;
    color: #ffffff;
    border-bottom: 1px solid var(--glass-border);
    padding-bottom: 1rem;
}

.mc-options-grid {
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
}

.mc-option-btn {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: rgba(15, 23, 42, 0.6);
    border: 2px solid var(--glass-border);
    padding: 1rem 1.25rem;
    border-radius: var(--radius-md);
    color: #ffffff;
    font-size: 1.05rem;
    font-weight: 600;
    text-align: left;
    cursor: pointer;
    transition: all 0.2s ease;
}

.mc-option-btn:hover:not(:disabled) {
    background: rgba(6, 182, 212, 0.15);
    border-color: var(--cyan-accent);
    transform: translateX(4px);
}

.mc-option-badge {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: var(--bg-card);
    border: 1px solid var(--glass-border);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    color: var(--cyan-accent);
    flex-shrink: 0;
}

.mc-option-btn.selected-correct {
    background: rgba(16, 185, 129, 0.25) !important;
    border-color: var(--emerald-accent) !important;
    color: #6ee7b7 !important;
}

.mc-option-btn.selected-correct .mc-option-badge {
    background: var(--emerald-accent);
    color: #0f172a;
}

.mc-option-btn.selected-wrong {
    background: rgba(244, 63, 94, 0.25) !important;
    border-color: var(--rose-accent) !important;
    color: #fca5a5 !important;
}

.mc-option-btn.selected-wrong .mc-option-badge {
    background: var(--rose-accent);
    color: #ffffff;
}

.mc-feedback-msg {
    padding: 1.2rem;
    border-radius: var(--radius-md);
    font-size: 1.1rem;
    line-height: 1.5;
}

.mc-feedback-msg.success {
    background: rgba(16, 185, 129, 0.2);
    border: 1px solid var(--emerald-accent);
    color: #6ee7b7;
}

.mc-feedback-msg.error {
    background: rgba(244, 63, 94, 0.2);
    border: 1px solid var(--rose-accent);
    color: #fca5a5;
}
"""

css_combined = css_content + "\n" + mc_css

# Read JS modules
def read_js(rel_path):
    with open(os.path.join(base_dir, rel_path), "r", encoding="utf-8") as f:
        return f.read()

parser_js = read_js("js/parser.js")

# Fixed 3D Flashcard Mode JS Logic
flashcard_js = """
class FlashcardMode {
    constructor(containerEl, deck) {
        this.container = containerEl;
        this.deck = deck;
        this.cards = deck ? [...deck.cards] : [];
        this.currentIndex = 0;
        this.isFlipped = false;
        this.speechSynth = window.speechSynthesis;
        window.flashcardMode = this;

        this.render();
    }

    render() {
        if (!this.cards || this.cards.length === 0) {
            this.container.innerHTML = `
                <div class="empty-mode-state" style="text-align:center; padding: 3rem; background: var(--bg-card); border-radius: var(--radius-lg);">
                    <div class="empty-icon" style="font-size:3rem; margin-bottom:1rem;">🎴</div>
                    <h3>Bu destede henüz kart bulunmuyor</h3>
                    <p style="color:var(--text-muted); margin-top:0.5rem;">Lütfen başka bir deste seçin.</p>
                </div>
            `;
            return;
        }

        const card = this.cards[this.currentIndex];
        const progressPercent = Math.round(((this.currentIndex + 1) / this.cards.length) * 100);

        this.container.innerHTML = `
            <div class="flashcard-mode-wrapper">
                <div class="mode-header-bar">
                    <div class="card-counter">
                        <span class="current-num">${this.currentIndex + 1}</span> / <span class="total-num">${this.cards.length}</span> Kart
                    </div>
                    <div class="progress-container">
                        <div class="progress-bar-fill" style="width: ${progressPercent}%;"></div>
                    </div>
                    <div class="mastered-badge ${card.mastered ? 'active' : ''}">
                        ${card.mastered ? '⭐ Öğrenildi' : '🎯 Öğreniliyor'}
                    </div>
                </div>

                <div class="card-stage">
                    <div class="flashcard-3d ${this.isFlipped ? 'flipped' : ''}" id="mainFlashcard">
                        <div class="card-face card-front">
                            <div class="card-header-tag">
                                <span class="tag-label">Soru / Kavram</span>
                                <button class="tts-btn" title="Sesli Oku" onclick="event.stopPropagation(); window.flashcardMode.speakCurrent('front');">
                                    🔊
                                </button>
                            </div>
                            <div class="card-body-content">
                                ${this.escapeHtml(card.front)}
                            </div>
                            <div class="card-footer-hint">
                                <span>💡 Çevirmek için tıklayın veya SPACE'e basın</span>
                            </div>
                        </div>

                        <div class="card-face card-back">
                            <div class="card-header-tag">
                                <span class="tag-label">Cevap / Açıklama</span>
                                <button class="tts-btn" title="Sesli Oku" onclick="event.stopPropagation(); window.flashcardMode.speakCurrent('back');">
                                    🔊
                                </button>
                            </div>
                            <div class="card-body-content">
                                ${this.escapeHtml(card.back)}
                            </div>
                            <div class="card-footer-hint">
                                <span>💡 Çevirmek için tekrar tıklayın</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="flashcard-controls">
                    <button class="ctrl-btn secondary-btn" onclick="window.flashcardMode.prevCard()" ${this.currentIndex === 0 ? 'disabled' : ''}>
                        ← Önceki
                    </button>
                    
                    <button class="ctrl-btn flip-action-btn" onclick="window.flashcardMode.toggleFlip()">
                        🔄 Çevir (Space)
                    </button>

                    <button class="ctrl-btn toggle-master-btn ${card.mastered ? 'is-mastered' : ''}" onclick="window.flashcardMode.toggleMastered()">
                        ${card.mastered ? '✅ Öğrenildi Olarak İşaretli' : '⭐ Öğrenildi İşaretle'}
                    </button>

                    <button class="ctrl-btn secondary-btn" onclick="window.flashcardMode.nextCard()" ${this.currentIndex === this.cards.length - 1 ? 'disabled' : ''}>
                        Sonraki →
                    </button>
                </div>
            </div>
        `;

        const cardEl = document.getElementById('mainFlashcard');
        if (cardEl) {
            cardEl.addEventListener('click', () => this.toggleFlip());
        }
    }

    toggleFlip() {
        this.isFlipped = !this.isFlipped;
        const cardEl = document.getElementById('mainFlashcard');
        if (cardEl) {
            if (this.isFlipped) {
                cardEl.classList.add('flipped');
            } else {
                cardEl.classList.remove('flipped');
            }
        }
    }

    nextCard() {
        if (this.currentIndex < this.cards.length - 1) {
            this.currentIndex++;
            this.isFlipped = false;
            this.render();
            DeckStorage.recordStudySession(1, 0);
        }
    }

    prevCard() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.isFlipped = false;
            this.render();
        }
    }

    toggleMastered() {
        const card = this.cards[this.currentIndex];
        card.mastered = !card.mastered;
        
        const activeDeck = DeckStorage.getDeckById(this.deck.id);
        if (activeDeck) {
            const targetCard = activeDeck.cards.find(c => c.id === card.id);
            if (targetCard) {
                targetCard.mastered = card.mastered;
                DeckStorage.saveDeck(activeDeck);
            }
        }

        DeckStorage.recordStudySession(0, card.mastered ? 1 : -1);
        this.render();
    }

    speakCurrent(side) {
        if (!this.speechSynth) return;
        const card = this.cards[this.currentIndex];
        const text = side === 'front' ? card.front : card.back;
        
        this.speechSynth.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'tr-TR';
        utterance.rate = 0.95;
        this.speechSynth.speak(utterance);
    }

    escapeHtml(str) {
        if (!str) return '';
        return str
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
}
"""

# Multiple Choice Quiz Mode JS Logic
multiplechoice_js = """
class MultipleChoiceMode {
    constructor(container, deck) {
        this.container = container;
        this.deck = deck;
        this.cards = deck ? [...deck.cards] : [];
        this.currentIndex = 0;
        this.score = { correct: 0, wrong: 0 };
        this.answered = false;
        
        this.init();
    }

    init() {
        if (!this.cards || this.cards.length === 0) {
            this.container.innerHTML = `
                <div class="empty-state" style="text-align:center; padding: 3rem; background: var(--bg-card); border-radius: var(--radius-lg);">
                    <h3>Bu destede henüz soru bulunmuyor.</h3>
                    <p style="color: var(--text-muted); margin-top: 0.5rem;">Lütfen geçerli bir test destesi seçin.</p>
                </div>
            `;
            return;
        }

        this.cards = [...this.cards];
        this.currentIndex = 0;
        this.score = { correct: 0, wrong: 0 };

        this.renderStage();
        this.loadNextQuestion();
    }

    shuffleArray(arr) {
        return arr.sort(() => Math.random() - 0.5);
    }

    renderStage() {
        this.container.innerHTML = `
            <div class="mc-mode-wrapper">
                <div class="mc-header-bar">
                    <div class="mc-progress-info">
                        Soru <strong id="mcCurrentNum">1</strong> / ${this.cards.length}
                    </div>
                    <div class="mc-score-badge">
                        <span style="color: var(--emerald-accent);">✅ Doğru: <strong id="mcCorrectScore">0</strong></span>
                        <span style="color: var(--rose-accent);">❌ Yanlış: <strong id="mcWrongScore">0</strong></span>
                    </div>
                </div>

                <div class="mc-card-box" id="mcCardBox">
                    <div class="mc-question-text" id="mcQuestionText">
                        Soru yükleniyor...
                    </div>
                    <div class="mc-options-grid" id="mcOptionsGrid"></div>
                    <div class="mc-feedback-msg" id="mcFeedbackMsg" style="display:none;"></div>
                </div>
            </div>
        `;
    }

    loadNextQuestion() {
        if (this.currentIndex >= this.cards.length) {
            this.showResults();
            return;
        }

        this.answered = false;
        const currentCard = this.cards[this.currentIndex];

        let options = currentCard.options;
        let correctLetter = currentCard.correctOption || 'A';

        if (!options || options.length < 2) {
            const otherCards = this.cards.filter(c => c.id !== currentCard.id);
            const shuffledOthers = this.shuffleArray([...otherCards]).slice(0, 4);
            
            const rawOptions = [
                { text: currentCard.back, isCorrect: true },
                ...shuffledOthers.map(c => ({ text: c.back, isCorrect: false }))
            ];
            const shuffledOptions = this.shuffleArray(rawOptions);
            const letters = ['A', 'B', 'C', 'D', 'E'];
            
            options = shuffledOptions.map((opt, idx) => {
                if (opt.isCorrect) correctLetter = letters[idx];
                return { letter: letters[idx], text: opt.text };
            });
        }

        this.currentQuestion = {
            card: currentCard,
            options: options,
            correctLetter: correctLetter,
            correctText: options.find(o => o.letter === correctLetter)?.text || currentCard.back
        };

        document.getElementById('mcCurrentNum').textContent = this.currentIndex + 1;
        document.getElementById('mcQuestionText').textContent = currentCard.front;

        const optionsGrid = document.getElementById('mcOptionsGrid');
        optionsGrid.innerHTML = options.map(opt => `
            <button class="mc-option-btn" data-letter="${opt.letter}" onclick="window.multipleChoiceMode.selectOption('${opt.letter}')">
                <span class="mc-option-badge">${opt.letter}</span>
                <span>${this.escapeHtml(opt.text)}</span>
            </button>
        `).join('');

        const feedbackEl = document.getElementById('mcFeedbackMsg');
        feedbackEl.style.display = 'none';

        const cardBox = document.getElementById('mcCardBox');
        cardBox.className = 'mc-card-box';

        window.multipleChoiceMode = this;
    }

    selectOption(selectedLetter) {
        if (this.answered) return;
        this.answered = true;

        const isCorrect = (selectedLetter === this.currentQuestion.correctLetter);
        const cardBox = document.getElementById('mcCardBox');
        const feedbackEl = document.getElementById('mcFeedbackMsg');
        const optionBtns = document.querySelectorAll('.mc-option-btn');

        optionBtns.forEach(btn => {
            btn.disabled = true;
            const letter = btn.getAttribute('data-letter');
            if (letter === this.currentQuestion.correctLetter) {
                btn.classList.add('selected-correct');
            } else if (letter === selectedLetter) {
                btn.classList.add('selected-wrong');
            }
        });

        if (isCorrect) {
            this.score.correct++;
            document.getElementById('mcCorrectScore').textContent = this.score.correct;
            cardBox.classList.add('correct-border');
            feedbackEl.className = 'mc-feedback-msg success';
            feedbackEl.innerHTML = `🎉 <strong>Tebrikler, Doğru Cevap!</strong> (${this.currentQuestion.correctLetter})`;
        } else {
            this.score.wrong++;
            document.getElementById('mcWrongScore').textContent = this.score.wrong;
            cardBox.classList.add('wrong-border');
            feedbackEl.className = 'mc-feedback-msg error';
            feedbackEl.innerHTML = `❌ <strong>Yanlış Seçim!</strong><br>👉 Gerçek Doğru Cevap: <strong>${this.currentQuestion.correctLetter}) ${this.escapeHtml(this.currentQuestion.correctText)}</strong>`;
        }

        feedbackEl.style.display = 'block';
        DeckStorage.recordStudySession(1, isCorrect ? 1 : 0);

        const containerBox = document.getElementById('mcCardBox');
        const nextBtn = document.createElement('button');
        nextBtn.className = 'ctrl-btn next-btn';
        nextBtn.style.marginTop = '1rem';
        nextBtn.style.padding = '1rem';
        nextBtn.style.fontSize = '1.2rem';
        nextBtn.innerHTML = 'Sonraki Soruya Geç ➔';
        nextBtn.onclick = () => {
            this.currentIndex++;
            this.loadNextQuestion();
        };

        containerBox.appendChild(nextBtn);
    }

    showResults() {
        const total = this.cards.length;
        const percent = Math.round((this.score.correct / total) * 100) || 0;

        this.container.innerHTML = `
            <div class="quiz-results-box" style="max-width: 600px; margin: 2rem auto; text-align: center; background: var(--bg-card); padding: 2.5rem; border-radius: var(--radius-lg); border: 1px solid var(--glass-border);">
                <h2>🎉 Çoktan Seçmeli Test Tamamlandı!</h2>
                <div style="font-size: 3.5rem; margin: 1.5rem 0;">
                    ${percent >= 70 ? '🏆' : '📚'}
                </div>
                <p style="font-size: 1.25rem; margin-bottom: 1rem;">Başarı Oranınız: <strong>%${percent}</strong></p>
                <div style="display: flex; justify-content: center; gap: 2rem; margin-bottom: 2rem; font-size: 1.15rem;">
                    <span style="color: var(--emerald-accent);">✅ Doğru: <strong>${this.score.correct}</strong></span>
                    <span style="color: var(--rose-accent);">❌ Yanlış: <strong>${this.score.wrong}</strong></span>
                </div>
                <button class="ctrl-btn primary-btn" id="restartMCBtn">
                    🔄 Testi Tekrar Başlat
                </button>
            </div>
        `;

        document.getElementById('restartMCBtn').addEventListener('click', () => this.init());
    }

    escapeHtml(str) {
        if (!str) return '';
        return str
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
}
"""

# Fixed Match Mode JS Logic
match_js = """
class MatchMode {
    constructor(containerEl, deck) {
        this.container = containerEl;
        this.deck = deck;
        this.tiles = [];
        this.selectedTile = null;
        this.matchesCount = 0;
        this.totalPairs = 0;
        this.timer = 0;
        this.timerInterval = null;
        this.isCompleted = false;
        window.matchMode = this;

        this.init(deck);
    }

    init(deck) {
        this.deck = deck;
        this.selectedTile = null;
        this.matchesCount = 0;
        this.timer = 0;
        this.isCompleted = false;
        clearInterval(this.timerInterval);

        if (!deck || !deck.cards || deck.cards.length < 2) {
            this.container.innerHTML = `
                <div class="empty-mode-state" style="text-align:center; padding: 3rem; background: var(--bg-card); border-radius: var(--radius-lg);">
                    <div class="empty-icon" style="font-size:3rem; margin-bottom:1rem;">🧩</div>
                    <h3>Eşleştirme Oyunu İçin En Az 2 Kart Gereklidir</h3>
                    <p style="color:var(--text-muted); margin-top:0.5rem;">Eşleştirme oyunu oynamak için destenizde daha fazla bilgi kartı olduğundan emin olun.</p>
                </div>
            `;
            return;
        }

        const selectedCards = [...deck.cards].sort(() => 0.5 - Math.random()).slice(0, 8);
        this.totalPairs = selectedCards.length;

        const tileList = [];
        selectedCards.forEach(card => {
            tileList.push({
                id: `front-${card.id}`,
                cardId: card.id,
                type: 'front',
                text: card.front,
                matched: false
            });
            tileList.push({
                id: `back-${card.id}`,
                cardId: card.id,
                type: 'back',
                text: card.back,
                matched: false
            });
        });

        this.tiles = tileList.sort(() => 0.5 - Math.random());

        this.startTimer();
        this.render();
    }

    startTimer() {
        this.timerInterval = setInterval(() => {
            if (!this.isCompleted) {
                this.timer++;
                const timerEl = document.getElementById('matchTimerVal');
                if (timerEl) {
                    timerEl.innerText = `${this.timer} sn`;
                }
            }
        }, 1000);
    }

    render() {
        if (this.isCompleted) {
            this.renderVictory();
            return;
        }

        this.container.innerHTML = `
            <div class="match-mode-wrapper">
                <div class="mode-header-bar">
                    <div class="card-counter">
                        Eşleşen: <span class="current-num" id="matchPairsVal">${this.matchesCount}</span> / <span class="total-num">${this.totalPairs}</span>
                    </div>
                    <div class="score-live-badge">
                        ⏱️ Süre: <span id="matchTimerVal">${this.timer} sn</span>
                    </div>
                </div>

                <div class="match-grid">
                    ${this.tiles.map((tile, idx) => `
                        <div class="match-tile ${tile.type} ${tile.matched ? 'matched' : ''} ${this.selectedTile && this.selectedTile.id === tile.id ? 'selected' : ''}"
                             onclick="window.matchMode.handleTileClick(${idx})">
                            <div class="tile-content">${this.escapeHtml(tile.text)}</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    handleTileClick(index) {
        const tile = this.tiles[index];
        if (tile.matched || (this.selectedTile && this.selectedTile.id === tile.id)) return;

        if (!this.selectedTile) {
            this.selectedTile = tile;
            this.render();
        } else {
            const first = this.selectedTile;
            const second = tile;

            if (first.cardId === second.cardId && first.type !== second.type) {
                first.matched = true;
                second.matched = true;
                this.matchesCount++;
                this.selectedTile = null;

                if (this.matchesCount === this.totalPairs) {
                    this.isCompleted = true;
                    clearInterval(this.timerInterval);
                }
                this.render();
            } else {
                this.selectedTile = null;
                this.render();
            }
        }
    }

    renderVictory() {
        this.container.innerHTML = `
            <div class="match-victory-box" style="text-align:center; padding:3rem; background:var(--bg-card); border-radius:var(--radius-lg);">
                <div class="result-icon" style="font-size:3.5rem; margin-bottom:1rem;">⚡</div>
                <h2>Harika! Tüm Kartları Eşleştirdiniz!</h2>
                <p style="margin:1rem 0; font-size:1.15rem;">Tüm kavram ve tanımları <strong>${this.timer} saniyede</strong> başarıyla tamamladınız.</p>
                <div class="result-actions">
                    <button class="ctrl-btn primary-btn" onclick="window.matchMode.init(window.matchMode.deck)">
                        🎮 Yeniden Oyna
                    </button>
                </div>
            </div>
        `;
        DeckStorage.recordStudySession(this.totalPairs * 2, this.totalPairs);
    }

    escapeHtml(text) {
        if (!text) return '';
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
}
"""

# App JS with Strict Deck Filtering based on Active Mode
app_js = """
class FlashcardApp {
    constructor() {
        this.activeMode = 'multiplechoice';
        this.activeDeckId = 'deck-tarih-cikmis';
        this.activeModeInstance = null;

        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadActiveMode();
    }

    renderDeckSelectOptions() {
        const allDecks = DeckStorage.getDecks();
        const selectEl = document.getElementById('deckSelect');
        const descEl = document.getElementById('deckDesc');

        if (!selectEl) return;

        // Mod bazlı filtreleme:
        // Eğer Çoktan Seçmeli Test ise SADECE Test desteleri (Tarih Çıkmış Sorular & Vatandaşlık Çıkmış Sorular)
        // Eğer 3D Kart / Eşleştirme / Yönetim ise SADECE 5 Bilgi Kartı destesi
        let filteredDecks = [];
        if (this.activeMode === 'multiplechoice') {
            filteredDecks = allDecks.filter(d => d.isTestDeck || d.category === 'Çıkmış Test' || d.id.includes('cikmis'));
            if (!filteredDecks.some(d => d.id === this.activeDeckId)) {
                this.activeDeckId = filteredDecks[0] ? filteredDecks[0].id : 'deck-tarih-cikmis';
            }
        } else {
            filteredDecks = allDecks.filter(d => !d.isTestDeck && d.category !== 'Çıkmış Test' && !d.id.includes('cikmis'));
            if (!filteredDecks.some(d => d.id === this.activeDeckId)) {
                this.activeDeckId = filteredDecks[0] ? filteredDecks[0].id : 'deck-karma';
            }
        }

        DeckStorage.setActiveDeckId(this.activeDeckId);

        selectEl.innerHTML = '';
        filteredDecks.forEach(deck => {
            const option = document.createElement('option');
            option.value = deck.id;
            option.textContent = `${deck.title} (${deck.cards.length} ${this.activeMode === 'multiplechoice' ? 'soru' : 'kart'})`;
            if (deck.id === this.activeDeckId) {
                option.selected = true;
            }
            selectEl.appendChild(option);
        });

        const activeDeck = DeckStorage.getDeckById(this.activeDeckId);
        if (activeDeck && descEl) {
            descEl.textContent = activeDeck.description || `${activeDeck.cards.length} içerik bulunuyor.`;
        }
    }

    setupEventListeners() {
        const selectEl = document.getElementById('deckSelect');
        if (selectEl) {
            selectEl.addEventListener('change', (e) => {
                this.activeDeckId = e.target.value;
                DeckStorage.setActiveDeckId(this.activeDeckId);
                
                const activeDeck = DeckStorage.getDeckById(this.activeDeckId);
                if (activeDeck) {
                    document.getElementById('deckDesc').textContent = activeDeck.description || `${activeDeck.cards.length} içerik bulunuyor.`;
                }

                this.loadActiveMode();
            });
        }

        const tabBtns = document.querySelectorAll('.mode-tabs .tab-btn');
        tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                tabBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                this.activeMode = btn.getAttribute('data-mode');
                this.loadActiveMode();
            });
        });
    }

    loadActiveMode() {
        this.renderDeckSelectOptions();

        const modeContainer = document.getElementById('modeContainer');
        if (!modeContainer) return;

        const activeDeck = DeckStorage.getDeckById(this.activeDeckId);

        switch (this.activeMode) {
            case 'multiplechoice':
                this.activeModeInstance = new MultipleChoiceMode(modeContainer, activeDeck);
                break;
            case 'flashcard':
                this.activeModeInstance = new FlashcardMode(modeContainer, activeDeck);
                break;
            case 'match':
                this.activeModeInstance = new MatchMode(modeContainer, activeDeck);
                break;
            case 'manage':
                this.renderDeckManager(modeContainer, activeDeck);
                break;
            default:
                this.activeModeInstance = new MultipleChoiceMode(modeContainer, activeDeck);
        }
    }

    renderDeckManager(container, deck) {
        if (!deck) {
            container.innerHTML = '<div class="empty-state"><p>Deste bulunamadı.</p></div>';
            return;
        }

        container.innerHTML = `
            <div class="deck-manager-wrapper">
                <div class="manager-actions-header">
                    <div>
                        <h2>⚙️ Deste Yönetimi: ${deck.title}</h2>
                        <p style="color: var(--text-muted); font-size: 0.9rem;">Toplam ${deck.cards.length} kart</p>
                    </div>
                    <div class="action-btn-group">
                        <button class="ctrl-btn secondary-btn" id="exportCSVBtn">📥 CSV İndir</button>
                        <button class="ctrl-btn secondary-btn" id="exportJSONBtn">📥 JSON İndir</button>
                        <button class="ctrl-btn danger-btn" id="deleteDeckBtn">🗑️ Desteyi Sil</button>
                    </div>
                </div>

                <div class="add-card-row" style="display:flex; gap: 1rem; margin-bottom: 1.5rem;">
                    <input type="text" id="newFrontInput" class="text-input" placeholder="Soru / Kavram..." style="flex:1;">
                    <input type="text" id="newBackInput" class="text-input" placeholder="Cevap / Açıklama..." style="flex:1;">
                    <button class="ctrl-btn primary-btn" id="addSingleCardBtn">+ Kart Ekle</button>
                </div>

                <div class="cards-list-table">
                    ${deck.cards.map((c, idx) => `
                        <div class="card-item-row" style="display:flex; justify-content:space-between; align-items:center; background:rgba(15,23,42,0.5); padding: 0.85rem 1.25rem; border-radius: var(--radius-sm); margin-bottom:0.5rem;">
                            <div style="flex:1; margin-right:1rem;">
                                <strong>#${idx + 1} Soru:</strong> ${c.front}<br>
                                <span style="color:var(--text-muted); font-size:0.9rem;"><strong>Cevap:</strong> ${c.back}</span>
                            </div>
                            <button class="ctrl-btn danger-btn remove-card-btn" data-card-id="${c.id}" style="padding:0.4rem 0.8rem; font-size:0.85rem;">Sil</button>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;

        document.getElementById('exportCSVBtn').addEventListener('click', () => DeckStorage.exportDeckCSV(deck));
        document.getElementById('exportJSONBtn').addEventListener('click', () => DeckStorage.exportDeckJSON(deck));
        document.getElementById('deleteDeckBtn').addEventListener('click', () => {
            if (confirm(`"${deck.title}" destesini silmek istediğinizden emin misiniz?`)) {
                DeckStorage.deleteDeck(deck.id);
                this.activeDeckId = DeckStorage.getActiveDeckId();
                this.renderDeckSelectOptions();
                this.loadActiveMode();
            }
        });

        document.getElementById('addSingleCardBtn').addEventListener('click', () => {
            const front = document.getElementById('newFrontInput').value.trim();
            const back = document.getElementById('newBackInput').value.trim();

            if (!front || !back) {
                alert('Lütfen hem Soru hem Cevap kısmını doldurun.');
                return;
            }

            deck.cards.push({
                id: 'c_' + Date.now(),
                front: front,
                back: back,
                mastered: false
            });

            DeckStorage.saveDeck(deck);
            this.renderDeckSelectOptions();
            this.renderDeckManager(container, deck);
        });

        container.querySelectorAll('.remove-card-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const cardId = e.target.getAttribute('data-card-id');
                deck.cards = deck.cards.filter(c => c.id !== cardId);
                DeckStorage.saveDeck(deck);
                this.renderDeckSelectOptions();
                this.renderDeckManager(container, deck);
            });
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.app = new FlashcardApp();
});
"""

# Version string for automatic cache-busting
APP_VERSION = "9.0_tarih_cikmis_sorular_173_soru_added"

# Storage JS with guaranteed auto-recovery AND automatic version-busting
storage_js = f"""
const STORAGE_KEY = 'notebooklm_flashcards_decks';
const ACTIVE_DECK_KEY = 'notebooklm_active_deck_id';
const STATS_KEY = 'notebooklm_study_stats';
const VERSION_KEY = 'notebooklm_app_version';
const CURRENT_VERSION = '{APP_VERSION}';

class DeckStorage {{
    static checkAndMigrateVersion() {{
        try {{
            const savedVersion = localStorage.getItem(VERSION_KEY);
            if (savedVersion !== CURRENT_VERSION) {{
                console.log('Yeni versiyon algılandı, yerel veriler 1240 kartlık güncel sürüme yükseltiliyor...');
                localStorage.setItem(VERSION_KEY, CURRENT_VERSION);
                if (typeof SAMPLE_DECKS !== 'undefined' && Array.isArray(SAMPLE_DECKS)) {{
                    this.saveDecks(SAMPLE_DECKS);
                }}
            }}
        }} catch (e) {{
            console.error('Sürüm kontrol hatası:', e);
        }}
    }}

    static forceResetDecks() {{
        try {{
            localStorage.removeItem(STORAGE_KEY);
            localStorage.setItem(VERSION_KEY, CURRENT_VERSION);
            if (typeof SAMPLE_DECKS !== 'undefined' && Array.isArray(SAMPLE_DECKS)) {{
                this.saveDecks(SAMPLE_DECKS);
            }}
            location.reload();
        }} catch (e) {{
            console.error('Sıfırlama hatası:', e);
        }}
    }}

    static getDecks() {{
        try {{
            this.checkAndMigrateVersion();

            const data = localStorage.getItem(STORAGE_KEY);
            let savedDecks = [];
            if (data) {{
                savedDecks = JSON.parse(data);
            }}

            const isCorrupted = (str) => str && (str.includes('Ã') || str.includes('Å') || str.includes('Â') || str.includes('½'));

            let needsReset = !data || !Array.isArray(savedDecks) || savedDecks.length === 0;

            if (!needsReset) {{
                savedDecks.forEach(d => {{
                    if (isCorrupted(d.title) || isCorrupted(d.category)) needsReset = true;
                }});
            }}

            if (needsReset || (savedDecks.length < 7 && typeof SAMPLE_DECKS !== 'undefined')) {{
                savedDecks = (typeof SAMPLE_DECKS !== 'undefined' && Array.isArray(SAMPLE_DECKS)) ? SAMPLE_DECKS : [];
                this.saveDecks(savedDecks);
                return savedDecks;
            }}

            return savedDecks;
        }} catch (e) {{
            console.error('LocalStorage okuma hatası:', e);
            return (typeof SAMPLE_DECKS !== 'undefined') ? SAMPLE_DECKS : [];
        }}
    }}

    static saveDecks(decks) {{
        try {{
            localStorage.setItem(STORAGE_KEY, JSON.stringify(decks));
        }} catch (e) {{
            console.error('LocalStorage kaydetme hatası:', e);
        }}
    }}

    static getDeckById(deckId) {{
        const decks = this.getDecks();
        return decks.find(d => d.id === deckId) || null;
    }}

    static saveDeck(deck) {{
        const decks = this.getDecks();
        const index = decks.findIndex(d => d.id === deck.id);
        if (index >= 0) {{
            decks[index] = deck;
        }} else {{
            decks.unshift(deck);
        }}
        this.saveDecks(decks);
    }}

    static deleteDeck(deckId) {{
        let decks = this.getDecks();
        decks = decks.filter(d => d.id !== deckId);
        this.saveDecks(decks);
    }}

    static getActiveDeckId() {{
        const decks = this.getDecks();
        const savedId = localStorage.getItem(ACTIVE_DECK_KEY);
        if (savedId && decks.some(d => d.id === savedId)) {{
            return savedId;
        }}
        return decks[0] ? decks[0].id : null;
    }}

    static setActiveDeckId(deckId) {{
        localStorage.setItem(ACTIVE_DECK_KEY, deckId);
    }}

    static exportDeckJSON(deck) {{
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(deck, null, 2));
        const downloadAnchor = document.createElement('a');
        downloadAnchor.setAttribute("href", dataStr);
        downloadAnchor.setAttribute("download", `${{deck.title.replace(/\\s+/g, '_')}}_destesi.json`);
        document.body.appendChild(downloadAnchor);
        downloadAnchor.click();
        downloadAnchor.remove();
    }}

    static exportDeckCSV(deck) {{
        let csvContent = "data:text/csv;charset=utf-8,Soru/Kavram,Cevap/Açıklama\\n";
        deck.cards.forEach(card => {{
            const front = `"${{card.front.replace(/"/g, '""')}}"`;
            const back = `"${{card.back.replace(/"/g, '""')}}"`;
            csvContent += `${{front}},${{back}}\\n`;
        }});

        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", `${{deck.title.replace(/\\s+/g, '_')}}_destesi.csv`);
        document.body.appendChild(link);
        link.click();
        link.remove();
    }}

    static getStats() {{
        try {{
            const data = localStorage.getItem(STATS_KEY);
            return data ? JSON.parse(data) : {{ totalStudied: 0, masteredCount: 0, streakDays: 1, lastStudied: null }};
        }} catch (e) {{
            return {{ totalStudied: 0, masteredCount: 0, streakDays: 1, lastStudied: null }};
        }}
    }}

    static recordStudySession(cardsStudied = 1, newlyMastered = 0) {{
        const stats = this.getStats();
        stats.totalStudied += cardsStudied;
        stats.masteredCount += newlyMastered;
        stats.lastStudied = new Date().toISOString();
        localStorage.setItem(STATS_KEY, JSON.stringify(stats));
    }}
}}
"""

# Helper function to load test cards from CSV
def load_test_cards(csv_file_name, prefix):
    file_path = os.path.join(base_dir, csv_file_name)
    cards = []
    if os.path.exists(file_path):
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for idx, row in enumerate(reader, 1):
                if len(row) >= 7:
                    question = row[0].strip()
                    optA = row[1].strip()
                    optB = row[2].strip()
                    optC = row[3].strip()
                    optD = row[4].strip()
                    optE = row[5].strip()
                    answerLetter = row[6].strip().upper()

                    optionsMap = { 'A': optA, 'B': optB, 'C': optC, 'D': optD, 'E': optE }
                    correctText = optionsMap.get(answerLetter, optA)

                    cards.append({
                        "id": f"c_{prefix}_{idx}",
                        "front": question,
                        "back": f"Doğru Cevap: {answerLetter}) {correctText}",
                        "correctOption": answerLetter,
                        "options": [
                            { "letter": "A", "text": optA },
                            { "letter": "B", "text": optB },
                            { "letter": "C", "text": optC },
                            { "letter": "D", "text": optD },
                            { "letter": "E", "text": optE }
                        ],
                        "mastered": False
                    })
    return cards

tarih_cikmis_cards = load_test_cards("tarih_cikmis_sorular.csv", "tarihcikmis")
vatandaslik_cikmis_cards = load_test_cards("vatandaslik_cikmis_sorular.csv", "vatandaslikcikmis")

print(f"Tarih Çıkmış Sorular: {len(tarih_cikmis_cards)} soru yüklendi.")
print(f"Vatandaşlık Çıkmış Sorular: {len(vatandaslik_cikmis_cards)} soru yüklendi.")

# Read standard 5 CSV files and build sample decks
files_map = [
    {
        "id": "deck-tarih-cikmis",
        "title": "Tarih Çıkmış Sorular",
        "description": "173 Adet ÖSYM Tarih Çıkmış Çoktan Seçmeli Test Sorusu (5 Şıklı)",
        "category": "Çıkmış Test",
        "isTestDeck": True,
        "cards": tarih_cikmis_cards
    },
    {
        "id": "deck-vatandaslik-cikmis",
        "title": "Vatandaşlık Çıkmış Sorular",
        "description": "75 Adet ÖSYM Vatandaşlık Çıkmış Çoktan Seçmeli Test Sorusu (5 Şıklı)",
        "category": "Çıkmış Test",
        "isTestDeck": True,
        "cards": vatandaslik_cikmis_cards
    },
    {
        "id": "deck-karma",
        "title": "Karma",
        "description": "195 Adet Genel Karma Türkçe, Tarih, Coğrafya ve Vatandaşlık Bilgi Kartları",
        "category": "Karma",
        "cards_file": "karma_bilgi_kartlari.csv"
    },
    {
        "id": "deck-tarih",
        "title": "Tarih",
        "description": "291 Adet İslamiyet Öncesi, Türk-İslam, Osmanlı ve İnkılap Tarihi Bilgi Kartları",
        "category": "Tarih",
        "cards_file": "tarih_bilgi_kartlari.csv"
    },
    {
        "id": "deck-cografya",
        "title": "Coğrafya",
        "description": "196 Adet Türkiye Konumu, İklim, Nüfus, Madenler ve Fiziki Coğrafya Kartları",
        "category": "Coğrafya",
        "cards_file": "cografya_bilgi_kartlari.csv"
    },
    {
        "id": "deck-turkce",
        "title": "Türkçe",
        "description": "175 Adet Anlam Bilgisi, Ses Bilgisi, Yazım Kuralları ve Dil Bilgisi Kartları",
        "category": "Türkçe",
        "cards_file": "turkce_anlam_bilgisi.csv"
    },
    {
        "id": "deck-vatandaslik",
        "title": "Vatandaşlık",
        "description": "135 Adet Anayasa Hukuku, Haklar, Yargı Organları ve İdare Hukuku Kartları",
        "category": "Vatandaşlık",
        "cards_file": "vatandaslik_bilgi_kartlari.csv"
    }
]

decks = []
for item in files_map:
    if "cards" in item:
        cards = item["cards"]
    else:
        file_path = os.path.join(base_dir, item["cards_file"])
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
        "isTestDeck": item.get("isTestDeck", False),
        "createdAt": "2026-07-23T12:00:00.000Z",
        "cards": cards
    })

decks_json = json.dumps(decks, ensure_ascii=False, indent=4)

standalone_html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NotebookLM Bilgi Kartları - İnteraktif Öğrenme Platformu</title>
    <meta name="description" content="NotebookLM özet ve bilgi kartlarınızı kolayca yükleyip 3D kartlar, Çoktan Seçmeli Testler ve eşleştirme oyunlarıyla çalışabileceğiniz modern web platformu.">
    <style>
{css_combined}
    </style>
</head>
<body>
    <div class="app-container">
        <!-- Header -->
        <header class="app-header">
            <div class="logo-area">
                <span class="logo-icon">🎴</span>
                <h1>KPSS Bilgi Kartları & Test Platformu</h1>
                <span class="badge-tag">v9.0</span>
            </div>
            <div class="header-actions">
                <button class="ctrl-btn secondary-btn" style="font-size: 0.85rem;" onclick="DeckStorage.forceResetDecks();">
                    🔄 Verileri Güncelle
                </button>
            </div>
        </header>

        <!-- Öğrenme Modu Sekmeleri -->
        <nav class="mode-tabs" style="margin-bottom: 1rem;">
            <button class="tab-btn active" data-mode="multiplechoice">
                <span>📝</span> Çoktan Seçmeli Test
            </button>
            <button class="tab-btn" data-mode="flashcard">
                <span>🎴</span> 3D Kart Modu
            </button>
            <button class="tab-btn" data-mode="match">
                <span>🧩</span> Eşleştirme Oyunu
            </button>
            <button class="tab-btn" data-mode="manage">
                <span>⚙️</span> Kart Yönetimi
            </button>
        </nav>

        <!-- Deste Seçimi Barı -->
        <section class="deck-selector-bar" style="margin-bottom: 1.5rem;">
            <div class="deck-select-group" style="width: 100%;">
                <label for="deckSelect">AKTİF ÇALIŞMA DESTESİ</label>
                <select id="deckSelect" class="custom-select">
                    <!-- JavaScript ile mod tipine göre dinamik dolacak -->
                </select>
                <div class="deck-desc-text" id="deckDesc">Deste açıklaması burada görünecek...</div>
            </div>
        </section>

        <!-- Ana Mod Alanı -->
        <main class="mode-stage" id="modeContainer">
            <!-- İlgili mod JS tarafından buraya yüklenecektir -->
        </main>

        <!-- Footer -->
        <footer class="app-footer">
            <p>KPSS Bilgi Kartları • v9.0 Tarih & Vatandaşlık Çıkmış Sorular Dahil (1240 İçerik)</p>
        </footer>
    </div>

    <!-- Örnek Kartlar ve Tüm Mantık Tam Bağımsız Entegre Edilir -->
    <script>
        const SAMPLE_DECKS = {decks_json};
    </script>
    <script>
{parser_js}
    </script>
    <script>
{storage_js}
    </script>
    <script>
{flashcard_js}
    </script>
    <script>
{multiplechoice_js}
    </script>
    <script>
{match_js}
    </script>
    <script>
{app_js}
    </script>
</body>
</html>
"""

standalone_path = os.path.join(base_dir, "index.html")
with open(standalone_path, "w", encoding="utf-8") as f:
    f.write(standalone_html)

print("index.html TARİH ÇIKMIŞ SORULAR (173 SORU) İLE BAŞARIYLA GÜNCELLENDİ!")
