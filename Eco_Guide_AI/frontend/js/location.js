/**
 * WildGuard AI – Location Intelligence Module
 */
const Location = {
    initialized: false,

    init() {
        if (this.initialized) return;
        this.initialized = true;

        document.getElementById('location-search-btn')?.addEventListener('click', () => this.search());
        document.getElementById('location-input')?.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') this.search();
        });

        // Quick buttons
        document.querySelectorAll('.location-quick-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.getElementById('location-input').value = btn.dataset.location;
                this.search();
            });
        });
    },

    async search() {
        const input = document.getElementById('location-input');
        const location = input?.value.trim();
        if (!location) return;

        const resultDiv = document.getElementById('location-result');
        const btn = document.getElementById('location-search-btn');

        btn.disabled = true;
        btn.innerHTML = '<div class="spinner"></div> Generating report...';
        resultDiv.innerHTML = '<div class="shimmer" style="height: 300px;"></div>';

        try {
            const data = await App.api('/location/', {
                method: 'POST',
                body: JSON.stringify({ location, include_protected_areas: true }),
            });
            resultDiv.innerHTML = `<div class="result-content">${App.renderMarkdown(data.report)}</div>`;
            App.toast(`Wildlife report for ${location} generated!`, 'success');
        } catch (e) {
            resultDiv.innerHTML = `<div class="result-content"><p>⚠️ <strong>Error:</strong> ${e.message}</p></div>`;
            App.toast('Location report failed', 'error');
        } finally {
            btn.disabled = false;
            btn.innerHTML = '🔍 Generate Report';
        }
    },
};
