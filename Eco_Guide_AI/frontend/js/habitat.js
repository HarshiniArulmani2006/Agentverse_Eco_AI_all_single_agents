/**
 * WildGuard AI – Habitat Analysis Module
 */
const Habitat = {
    initialized: false,
    selectedFile: null,

    init() {
        if (this.initialized) return;
        this.initialized = true;

        const zone = document.getElementById('habitat-upload-zone');
        const fileInput = document.getElementById('habitat-file-input');
        const analyzeBtn = document.getElementById('habitat-analyze-btn');

        zone?.addEventListener('click', () => fileInput?.click());

        fileInput?.addEventListener('change', (e) => {
            if (e.target.files[0]) this.handleFile(e.target.files[0]);
        });

        zone?.addEventListener('dragover', (e) => { e.preventDefault(); zone.classList.add('dragover'); });
        zone?.addEventListener('dragleave', () => zone.classList.remove('dragover'));
        zone?.addEventListener('drop', (e) => {
            e.preventDefault();
            zone.classList.remove('dragover');
            if (e.dataTransfer.files[0]) this.handleFile(e.dataTransfer.files[0]);
        });

        analyzeBtn?.addEventListener('click', () => this.analyze());
    },

    handleFile(file) {
        this.selectedFile = file;
        const preview = document.getElementById('habitat-preview');
        const fileName = document.getElementById('habitat-filename');
        const analyzeBtn = document.getElementById('habitat-analyze-btn');

        if (preview) { preview.src = URL.createObjectURL(file); preview.style.display = 'block'; }
        if (fileName) fileName.textContent = `📁 ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
        if (analyzeBtn) analyzeBtn.disabled = false;

        document.getElementById('habitat-result').innerHTML = '';
    },

    async analyze() {
        if (!this.selectedFile) return;
        const resultDiv = document.getElementById('habitat-result');
        const btn = document.getElementById('habitat-analyze-btn');

        btn.disabled = true;
        btn.innerHTML = '<div class="spinner"></div> Analyzing habitat...';
        resultDiv.innerHTML = '<div class="shimmer" style="height: 200px;"></div>';

        try {
            const data = await App.apiUpload('/habitat/', this.selectedFile);
            resultDiv.innerHTML = `<div class="result-content">${App.renderMarkdown(data.result)}</div>`;
            App.toast('Habitat analysis complete!', 'success');
        } catch (e) {
            resultDiv.innerHTML = `<div class="result-content"><p>⚠️ <strong>Error:</strong> ${e.message}</p></div>`;
            App.toast('Habitat analysis failed', 'error');
        } finally {
            btn.disabled = false;
            btn.innerHTML = '🏞️ Analyze Habitat';
        }
    },
};
