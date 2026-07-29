/**
 * WildGuard AI – Chat Module
 * Handles the main chat interface with RAG context.
 */
const Chat = {
    initialized: false,

    init() {
        if (this.initialized) return;
        this.initialized = true;

        const input = document.getElementById('chat-input');
        const sendBtn = document.getElementById('chat-send');

        input?.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.send();
            }
        });

        // Auto-resize textarea
        input?.addEventListener('input', () => {
            input.style.height = 'auto';
            input.style.height = Math.min(input.scrollHeight, 160) + 'px';
        });

        sendBtn?.addEventListener('click', () => this.send());

        // Welcome message
        const messages = document.getElementById('chat-messages');
        if (messages && messages.children.length === 0) {
            this.addMessage('assistant', this.getWelcomeMessage(), false);
        }
    },

    getWelcomeMessage() {
        return `## 🌿 Welcome to WildGuard AI!

I'm your **Wildlife Conservation Intelligence Agent**, powered by advanced AI and verified scientific databases.

### What I can help you with:
- 🦁 **Species Information** — Full taxonomy, conservation status, habitat, threats
- 🌱 **Plant & Tree Identification** — Botanical names, medicinal uses, ecology
- 🗺️ **Location-Based Wildlife** — Regional biodiversity, protected areas, threats
- 📷 **Image Identification** — Upload photos to identify species
- 🏞️ **Habitat Analysis** — Ecosystem health scoring from images
- 📚 **Conservation Education** — Quizzes, facts, and awareness

### Try asking me:
- *"What is the scientific name of the Bengal Tiger?"*
- *"Wildlife in Coimbatore"*
- *"Tell me about the Neem tree"*
- *"What is the conservation status of the Snow Leopard?"*

---
📊 **Confidence**: My responses include confidence scores and cite verified sources (IUCN, GBIF, WWF).`;
    },

    async send() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        if (!message) return;

        // Add user message
        this.addMessage('user', message);
        input.value = '';
        input.style.height = 'auto';

        // Show loading
        const loadingId = this.addLoading();

        try {
            const data = await App.api('/chat/', {
                method: 'POST',
                body: JSON.stringify({
                    message,
                    session_id: App.sessionId,
                }),
            });

            App.sessionId = data.session_id;
            localStorage.setItem('wg_session', data.session_id);

            this.removeLoading(loadingId);
            this.addMessage('assistant', data.response, data.rag_context_used);
        } catch (e) {
            this.removeLoading(loadingId);
            this.addMessage('assistant', `⚠️ **Error**: ${e.message}\n\nPlease check that the backend server is running and your API key is configured.`, false);
        }
    },

    addMessage(role, content, ragUsed = false) {
        const container = document.getElementById('chat-messages');
        const div = document.createElement('div');
        div.className = `chat-message ${role}`;

        if (role === 'assistant') {
            let metaHtml = '<div class="msg-meta"><span>🌿 WildGuard AI</span>';
            if (ragUsed) {
                metaHtml += '<span class="rag-badge">📚 RAG Enhanced</span>';
            }
            metaHtml += '</div>';
            div.innerHTML = metaHtml + App.renderMarkdown(content);
        } else {
            div.textContent = content;
        }

        container.appendChild(div);
        container.scrollTop = container.scrollHeight;
    },

    addLoading() {
        const container = document.getElementById('chat-messages');
        const div = document.createElement('div');
        const id = 'loading-' + Date.now();
        div.id = id;
        div.className = 'chat-message assistant';
        div.innerHTML = `
            <div class="msg-meta"><span>🌿 WildGuard AI</span></div>
            <div style="display: flex; align-items: center; gap: 10px; color: var(--text-muted);">
                <div class="loading-dots"><span></span><span></span><span></span></div>
                Analyzing with RAG pipeline...
            </div>`;
        container.appendChild(div);
        container.scrollTop = container.scrollHeight;
        return id;
    },

    removeLoading(id) {
        document.getElementById(id)?.remove();
    },
};
