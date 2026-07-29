/**
 * WildGuard AI – App Controller
 * Main application controller, routing, and utilities.
 */
const API_BASE = window.location.origin;

const App = {
    currentPage: 'chat',
    sessionId: null,
    geminiReady: false,

    init() {
        this.sessionId = localStorage.getItem('wg_session') || null;
        this.bindNav();
        this.bindMenuToggle();
        this.checkHealth();
        this.navigateTo('chat');
    },

    // ─── Navigation ──────────────────────────────────────────────────────
    bindNav() {
        document.querySelectorAll('.nav-item[data-page]').forEach(item => {
            item.addEventListener('click', () => {
                this.navigateTo(item.dataset.page);
                // Close sidebar on mobile
                document.querySelector('.sidebar')?.classList.remove('open');
            });
        });
    },

    navigateTo(page) {
        // Update nav
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        document.querySelector(`.nav-item[data-page="${page}"]`)?.classList.add('active');

        // Update pages
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        const el = document.getElementById(`page-${page}`);
        if (el) {
            el.classList.add('active');
            // Fire page init
            this.onPageLoad(page);
        }

        // Update top bar
        const titles = {
            chat: ['🌿 Wildlife Expert Chat', 'AI-powered RAG conversation'],
            identify: ['🔬 Species Identification', 'Upload an image to identify species'],
            habitat: ['🏞️ Habitat Health Analyzer', 'Analyze ecosystem images'],
            location: ['🗺️ Location Intelligence', 'Regional biodiversity reports'],
            sightings: ['🦁 Wildlife Sightings', 'Log & track observations'],
            education: ['📚 Education Hub', 'Quizzes, facts, and learning'],
        };
        const [title, sub] = titles[page] || ['WildGuard AI', ''];
        document.getElementById('topbar-title').textContent = title;
        document.getElementById('topbar-subtitle').textContent = sub;

        this.currentPage = page;
    },

    onPageLoad(page) {
        switch (page) {
            case 'chat': Chat.init(); break;
            case 'identify': Identify.init(); break;
            case 'habitat': Habitat.init(); break;
            case 'location': Location.init(); break;
            case 'sightings': Sightings.init(); break;
            case 'education': Education.init(); break;
        }
    },

    bindMenuToggle() {
        document.getElementById('menu-toggle')?.addEventListener('click', () => {
            document.querySelector('.sidebar')?.classList.toggle('open');
        });
    },

    // ─── Health Check ────────────────────────────────────────────────────
    async checkHealth() {
        try {
            const res = await fetch(`${API_BASE}/health`);
            const data = await res.json();
            this.geminiReady = data.gemini_configured;

            const dot = document.getElementById('status-dot');
            const label = document.getElementById('status-label');
            const model = document.getElementById('status-model');

            if (this.geminiReady) {
                dot.className = 'status-dot online';
                label.textContent = 'AI Online';
                model.textContent = data.model || 'Gemini 2.0 Flash';
            } else {
                dot.className = 'status-dot offline';
                label.textContent = 'API Key Required';
                model.textContent = 'Configure .env';
            }
        } catch (e) {
            const dot = document.getElementById('status-dot');
            const label = document.getElementById('status-label');
            if (dot) dot.className = 'status-dot offline';
            if (label) label.textContent = 'Server Offline';
        }
    },

    // ─── API Helper ──────────────────────────────────────────────────────
    async api(endpoint, options = {}) {
        const url = `${API_BASE}${endpoint}`;
        try {
            const res = await fetch(url, {
                headers: { 'Content-Type': 'application/json', ...options.headers },
                ...options,
            });
            if (!res.ok) {
                const err = await res.json().catch(() => ({ detail: res.statusText }));
                throw new Error(err.detail || `API error ${res.status}`);
            }
            return await res.json();
        } catch (e) {
            console.error(`API Error [${endpoint}]:`, e);
            throw e;
        }
    },

    async apiUpload(endpoint, file) {
        const form = new FormData();
        form.append('file', file);
        const url = `${API_BASE}${endpoint}`;
        const res = await fetch(url, { method: 'POST', body: form });
        if (!res.ok) {
            const err = await res.json().catch(() => ({ detail: res.statusText }));
            throw new Error(err.detail || `Upload error ${res.status}`);
        }
        return await res.json();
    },

    // ─── Toast Notifications ─────────────────────────────────────────────
    toast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        container.appendChild(toast);
        setTimeout(() => {
            toast.style.animation = 'toastOut 0.3s ease forwards';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    },

    // ─── Markdown Renderer (simple) ──────────────────────────────────────
    renderMarkdown(text) {
        if (!text) return '';
        let html = text
            // Code blocks
            .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code class="lang-$1">$2</code></pre>')
            // Inline code
            .replace(/`([^`]+)`/g, '<code>$1</code>')
            // Headers
            .replace(/^#### (.+)$/gm, '<h4>$1</h4>')
            .replace(/^### (.+)$/gm, '<h3>$1</h3>')
            .replace(/^## (.+)$/gm, '<h2>$1</h2>')
            .replace(/^# (.+)$/gm, '<h1>$1</h1>')
            // Bold + italic
            .replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>')
            .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.+?)\*/g, '<em>$1</em>')
            // Links
            .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
            // Horizontal rule
            .replace(/^---$/gm, '<hr>')
            // Blockquotes
            .replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>')
            // Tables
            .replace(/^\|(.+)\|$/gm, (match) => {
                const cells = match.split('|').filter(c => c.trim());
                if (cells.every(c => /^[\s-:]+$/.test(c))) return '<!--table-sep-->';
                return cells.map(c => `<td>${c.trim()}</td>`).join('');
            });

        // Process tables
        const lines = html.split('\n');
        let inTable = false;
        let isFirstRow = true;
        const processed = [];
        for (const line of lines) {
            if (line.includes('<td>') && !inTable) {
                inTable = true;
                isFirstRow = true;
                processed.push('<table>');
                processed.push('<tr>' + line.replace(/<td>/g, '<th>').replace(/<\/td>/g, '</th>') + '</tr>');
            } else if (line === '<!--table-sep-->') {
                isFirstRow = false;
            } else if (line.includes('<td>') && inTable) {
                processed.push('<tr>' + line + '</tr>');
            } else {
                if (inTable) {
                    processed.push('</table>');
                    inTable = false;
                }
                processed.push(line);
            }
        }
        if (inTable) processed.push('</table>');
        html = processed.join('\n');

        // Lists
        html = html.replace(/^[\-\*] (.+)$/gm, '<li>$1</li>');
        html = html.replace(/(<li>.*<\/li>\n?)+/gs, (match) => `<ul>${match}</ul>`);

        // Numbered lists
        html = html.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');

        // Paragraphs
        html = html.replace(/\n\n/g, '</p><p>');
        html = html.replace(/\n/g, '<br>');

        return `<p>${html}</p>`;
    },
};

// Boot
document.addEventListener('DOMContentLoaded', () => App.init());
