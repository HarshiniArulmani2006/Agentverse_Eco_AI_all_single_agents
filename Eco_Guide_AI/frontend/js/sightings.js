/**
 * WildGuard AI – Sightings Module
 */
const Sightings = {
    initialized: false,

    init() {
        if (this.initialized) return;
        this.initialized = true;

        document.getElementById('sighting-submit-btn')?.addEventListener('click', () => this.submit());
        this.loadSightings();
    },

    async submit() {
        const species = document.getElementById('sighting-species')?.value.trim();
        const scientific = document.getElementById('sighting-scientific')?.value.trim();
        const locationName = document.getElementById('sighting-location')?.value.trim();
        const observer = document.getElementById('sighting-observer')?.value.trim() || 'Anonymous';
        const notes = document.getElementById('sighting-notes')?.value.trim();
        const status = document.getElementById('sighting-status')?.value || 'Unknown';
        const lat = parseFloat(document.getElementById('sighting-lat')?.value) || null;
        const lng = parseFloat(document.getElementById('sighting-lng')?.value) || null;

        if (!species) {
            App.toast('Please enter a species name', 'error');
            return;
        }

        const btn = document.getElementById('sighting-submit-btn');
        btn.disabled = true;
        btn.innerHTML = '<div class="spinner"></div> Logging...';

        try {
            await App.api('/sightings/', {
                method: 'POST',
                body: JSON.stringify({
                    species_name: species,
                    scientific_name: scientific,
                    latitude: lat,
                    longitude: lng,
                    location_name: locationName,
                    observer_name: observer,
                    notes,
                    conservation_status: status,
                }),
            });

            App.toast('Sighting logged successfully!', 'success');
            this.clearForm();
            this.loadSightings();
        } catch (e) {
            App.toast('Failed to log sighting: ' + e.message, 'error');
        } finally {
            btn.disabled = false;
            btn.innerHTML = '📍 Log Sighting';
        }
    },

    clearForm() {
        ['sighting-species', 'sighting-scientific', 'sighting-location',
         'sighting-observer', 'sighting-notes', 'sighting-lat', 'sighting-lng']
            .forEach(id => { const el = document.getElementById(id); if (el) el.value = ''; });
    },

    async loadSightings() {
        const listDiv = document.getElementById('sightings-list');
        const statsDiv = document.getElementById('sightings-stats');

        try {
            const [sightings, stats] = await Promise.all([
                App.api('/sightings/'),
                App.api('/sightings/stats'),
            ]);

            // Stats
            if (statsDiv) {
                statsDiv.innerHTML = `
                    <div class="stat-card"><div class="stat-value">${stats.total_sightings}</div><div class="stat-label">Total Sightings</div></div>
                    <div class="stat-card"><div class="stat-value">${stats.unique_species}</div><div class="stat-label">Unique Species</div></div>
                    <div class="stat-card"><div class="stat-value">${stats.by_status?.Endangered || 0}</div><div class="stat-label">Endangered Spotted</div></div>
                    <div class="stat-card"><div class="stat-value">${stats.by_status?.['Critically Endangered'] || 0}</div><div class="stat-label">Critical Spotted</div></div>
                `;
            }

            // List
            if (listDiv) {
                if (sightings.length === 0) {
                    listDiv.innerHTML = `
                        <div class="empty-state">
                            <div class="empty-icon">🦜</div>
                            <div class="empty-title">No sightings yet</div>
                            <div class="empty-text">Log your first wildlife sighting using the form above!</div>
                        </div>`;
                    return;
                }

                listDiv.innerHTML = sightings.reverse().map(s => {
                    const rarity = s.analysis?.rarity_score || 0;
                    const rarityClass = rarity >= 65 ? 'rarity-high' : rarity >= 40 ? 'rarity-medium' : 'rarity-low';
                    const icon = this.getSpeciesIcon(s.species_name);
                    return `
                        <div class="sighting-item">
                            <div class="sighting-icon">${icon}</div>
                            <div class="sighting-info">
                                <div class="sighting-name">${s.species_name}</div>
                                <div class="sighting-sci">${s.scientific_name || 'N/A'}</div>
                                <div class="sighting-meta">
                                    📍 ${s.location?.name || 'Unknown'} · 👤 ${s.observer_name} · 🕐 ${s.timestamp_readable || ''}
                                </div>
                                ${s.analysis?.flags?.length ? `<div style="margin-top:4px; font-size:0.78rem; color: var(--red);">${s.analysis.flags.join(' · ')}</div>` : ''}
                            </div>
                            <div class="rarity-score ${rarityClass}">${rarity}</div>
                        </div>`;
                }).join('');
            }
        } catch (e) {
            if (listDiv) listDiv.innerHTML = `<p style="color: var(--text-muted);">Unable to load sightings.</p>`;
        }
    },

    getSpeciesIcon(name) {
        const n = (name || '').toLowerCase();
        if (n.includes('tiger') || n.includes('lion') || n.includes('leopard') || n.includes('cat')) return '🐯';
        if (n.includes('elephant')) return '🐘';
        if (n.includes('bird') || n.includes('eagle') || n.includes('peacock') || n.includes('bustard')) return '🦅';
        if (n.includes('whale') || n.includes('dolphin')) return '🐋';
        if (n.includes('snake') || n.includes('crocodile') || n.includes('turtle') || n.includes('reptile')) return '🐊';
        if (n.includes('monkey') || n.includes('gorilla') || n.includes('orangutan')) return '🐒';
        if (n.includes('panda') || n.includes('bear')) return '🐻';
        if (n.includes('rhino')) return '🦏';
        if (n.includes('deer') || n.includes('tahr')) return '🦌';
        if (n.includes('butterfly') || n.includes('insect')) return '🦋';
        if (n.includes('tree') || n.includes('plant') || n.includes('flower')) return '🌿';
        return '🦁';
    },
};
