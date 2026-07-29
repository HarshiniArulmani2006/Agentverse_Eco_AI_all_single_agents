/**
 * WildGuard AI – Species Identification Module
 */
const Identify = {
    initialized: false,
    selectedFile: null,

    init() {
        if (this.initialized) return;
        this.initialized = true;

        const zone = document.getElementById('identify-upload-zone');
        const fileInput = document.getElementById('identify-file-input');
        const analyzeBtn = document.getElementById('identify-analyze-btn');

        // Click to upload
        zone?.addEventListener('click', () => fileInput?.click());

        // File selected
        fileInput?.addEventListener('change', (e) => {
            if (e.target.files[0]) this.handleFile(e.target.files[0]);
        });

        // Drag & drop
        zone?.addEventListener('dragover', (e) => {
            e.preventDefault();
            zone.classList.add('dragover');
        });
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
        const preview = document.getElementById('identify-preview');
        const fileName = document.getElementById('identify-filename');
        const analyzeBtn = document.getElementById('identify-analyze-btn');

        if (preview) {
            preview.src = URL.createObjectURL(file);
            preview.style.display = 'block';
        }
        if (fileName) fileName.textContent = `📁 ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
        if (analyzeBtn) analyzeBtn.disabled = false;

        // Clear previous result
        document.getElementById('identify-result').innerHTML = '';
    },

    async analyze() {
        if (!this.selectedFile) return;
        const resultDiv = document.getElementById('identify-result');
        const btn = document.getElementById('identify-analyze-btn');

        btn.disabled = true;
        btn.innerHTML = '<div class="spinner"></div> Identifying species...';
        resultDiv.innerHTML = '<div class="shimmer" style="height: 200px;"></div>';

        try {
            const data = await App.apiUpload('/identify/', this.selectedFile);
            resultDiv.innerHTML = `<div class="result-content">${App.renderMarkdown(data.result)}</div>`;
            App.toast('Species identification complete!', 'success');
        } catch (e) {
            resultDiv.innerHTML = `<div class="result-content"><p>⚠️ <strong>Error:</strong> ${e.message}</p></div>`;
            App.toast('Identification failed: ' + e.message, 'error');
        } finally {
            btn.disabled = false;
            btn.innerHTML = '🔬 Identify Species';
        }
    },
};
