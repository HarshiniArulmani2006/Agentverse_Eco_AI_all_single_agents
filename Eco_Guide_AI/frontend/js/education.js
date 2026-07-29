/**
 * WildGuard AI – Education Hub Module
 */
const Education = {
    initialized: false,
    currentQuiz: null,
    currentQuestionIndex: 0,
    score: 0,
    answered: false,

    init() {
        if (this.initialized) return;
        this.initialized = true;

        // Fact of the day
        this.loadDailyFact();

        // Quiz difficulty buttons
        document.querySelectorAll('.quiz-difficulty-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.quiz-difficulty-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.startQuiz(btn.dataset.difficulty);
            });
        });

        // Species of the Day
        document.getElementById('edu-species-btn')?.addEventListener('click', () => this.loadSpeciesOfDay());

        // Custom quiz
        document.getElementById('edu-custom-quiz-btn')?.addEventListener('click', () => this.generateCustomQuiz());

        // Conservation report
        document.getElementById('edu-report-btn')?.addEventListener('click', () => this.generateReport());
    },

    async loadDailyFact() {
        try {
            const fact = await App.api('/education/daily-fact');
            const container = document.getElementById('daily-fact');
            if (container) {
                container.innerHTML = `
                    <div class="fact-card">
                        <div class="fact-category">${fact.category}</div>
                        <div class="fact-text">${fact.fact}</div>
                        <div class="fact-species">— ${fact.species}</div>
                    </div>`;
            }
        } catch (e) {
            console.log('Could not load daily fact');
        }
    },

    async startQuiz(difficulty) {
        const container = document.getElementById('quiz-area');
        container.innerHTML = '<div class="shimmer" style="height: 100px;"></div>';

        try {
            this.currentQuiz = await App.api(`/education/quiz/${difficulty}?count=5`);
            this.currentQuestionIndex = 0;
            this.score = 0;
            this.showQuestion();
        } catch (e) {
            container.innerHTML = `<p style="color: var(--text-muted);">Failed to load quiz.</p>`;
        }
    },

    showQuestion() {
        const container = document.getElementById('quiz-area');
        if (!this.currentQuiz || this.currentQuestionIndex >= this.currentQuiz.length) {
            this.showResults();
            return;
        }

        const q = this.currentQuiz[this.currentQuestionIndex];
        this.answered = false;

        container.innerHTML = `
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <span style="font-size: 0.8rem; color: var(--text-muted);">Question ${this.currentQuestionIndex + 1} of ${this.currentQuiz.length}</span>
                    <span style="font-size: 0.8rem; color: var(--accent-secondary); font-weight: 700;">Score: ${this.score}/${this.currentQuestionIndex}</span>
                </div>
                <h3 style="margin-bottom: 18px; line-height: 1.5;">${q.q}</h3>
                <div class="quiz-options" style="display: flex; flex-direction: column; gap: 8px;">
                    ${q.options.map((opt, i) => `
                        <div class="quiz-option" data-index="${i}" onclick="Education.answer(${i})">
                            <span class="option-letter">${String.fromCharCode(65 + i)}</span>
                            <span>${opt}</span>
                        </div>
                    `).join('')}
                </div>
                <div id="quiz-explanation" style="margin-top: 16px; display: none;"></div>
            </div>`;
    },

    answer(index) {
        if (this.answered) return;
        this.answered = true;

        const q = this.currentQuiz[this.currentQuestionIndex];
        const correct = q.options.indexOf(q.answer);
        const isCorrect = index === correct;

        if (isCorrect) this.score++;

        // Highlight
        document.querySelectorAll('.quiz-option').forEach((opt, i) => {
            if (i === correct) opt.classList.add('correct');
            if (i === index && !isCorrect) opt.classList.add('incorrect');
        });

        // Show explanation
        const explDiv = document.getElementById('quiz-explanation');
        explDiv.style.display = 'block';
        explDiv.innerHTML = `
            <div style="padding: 14px; border-radius: var(--radius-md); background: ${isCorrect ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)'}; border: 1px solid ${isCorrect ? 'var(--accent-primary)' : 'var(--red)'};">
                <strong>${isCorrect ? '✅ Correct!' : '❌ Incorrect'}</strong>
                <p style="margin-top: 6px; font-size: 0.88rem; color: var(--text-secondary);">${q.explanation}</p>
            </div>
            <button class="btn btn-primary btn-sm" style="margin-top: 12px;" onclick="Education.nextQuestion()">
                ${this.currentQuestionIndex < this.currentQuiz.length - 1 ? 'Next Question →' : 'See Results'}
            </button>`;
    },

    nextQuestion() {
        this.currentQuestionIndex++;
        this.showQuestion();
    },

    showResults() {
        const container = document.getElementById('quiz-area');
        const pct = Math.round((this.score / this.currentQuiz.length) * 100);
        const emoji = pct >= 80 ? '🏆' : pct >= 60 ? '👍' : pct >= 40 ? '📖' : '💪';

        container.innerHTML = `
            <div class="glass-card" style="text-align: center; padding: 40px;">
                <div style="font-size: 4rem; margin-bottom: 16px;">${emoji}</div>
                <h2 style="margin-bottom: 8px;">Quiz Complete!</h2>
                <div class="stat-value" style="font-size: 3rem; margin: 16px 0;">${this.score}/${this.currentQuiz.length}</div>
                <p style="color: var(--text-secondary); margin-bottom: 20px;">You scored ${pct}%</p>
                <button class="btn btn-primary" onclick="Education.startQuiz('beginner')">Try Again</button>
            </div>`;
    },

    async loadSpeciesOfDay() {
        const container = document.getElementById('species-of-day-result');
        const btn = document.getElementById('edu-species-btn');
        btn.disabled = true;
        btn.innerHTML = '<div class="spinner"></div> Generating...';
        container.innerHTML = '<div class="shimmer" style="height: 200px;"></div>';

        try {
            const data = await App.api('/education/species-of-the-day');
            container.innerHTML = `<div class="result-content">${App.renderMarkdown(data.content)}</div>`;
        } catch (e) {
            container.innerHTML = `<p style="color: var(--text-muted);">Failed to load species of the day.</p>`;
        } finally {
            btn.disabled = false;
            btn.innerHTML = '🌟 Generate Species of the Day';
        }
    },

    async generateCustomQuiz() {
        const topic = document.getElementById('edu-custom-topic')?.value.trim();
        if (!topic) { App.toast('Enter a topic for the quiz', 'error'); return; }

        const container = document.getElementById('custom-quiz-result');
        const btn = document.getElementById('edu-custom-quiz-btn');
        btn.disabled = true;
        btn.innerHTML = '<div class="spinner"></div> Generating...';
        container.innerHTML = '<div class="shimmer" style="height: 200px;"></div>';

        try {
            const data = await App.api('/education/custom-quiz', {
                method: 'POST',
                body: JSON.stringify({ topic, difficulty: 'intermediate' }),
            });
            container.innerHTML = `<div class="result-content">${App.renderMarkdown(data.quiz)}</div>`;
        } catch (e) {
            container.innerHTML = `<p style="color: var(--text-muted);">Failed to generate quiz.</p>`;
        } finally {
            btn.disabled = false;
            btn.innerHTML = '🧠 Generate Quiz';
        }
    },

    async generateReport() {
        const topic = document.getElementById('edu-report-topic')?.value.trim();
        if (!topic) { App.toast('Enter a topic for the report', 'error'); return; }

        const container = document.getElementById('report-result');
        const btn = document.getElementById('edu-report-btn');
        btn.disabled = true;
        btn.innerHTML = '<div class="spinner"></div> Generating...';
        container.innerHTML = '<div class="shimmer" style="height: 200px;"></div>';

        try {
            const data = await App.api('/education/conservation-report', {
                method: 'POST',
                body: JSON.stringify({ topic }),
            });
            container.innerHTML = `<div class="result-content">${App.renderMarkdown(data.report)}</div>`;
        } catch (e) {
            container.innerHTML = `<p style="color: var(--text-muted);">Failed to generate report.</p>`;
        } finally {
            btn.disabled = false;
            btn.innerHTML = '📝 Generate Report';
        }
    },
};
