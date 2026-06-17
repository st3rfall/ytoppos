/**
 * PrivateTube - JavaScript Application
 * Main application logic and API communication
 */

class PrivateTubeApp {
    constructor() {
        this.currentVideoId = null;
        this.currentTitle = null;
        this.init();
    }

    init() {
        this.cacheDOM();
        this.bindEvents();
        this.loadHistory();
        this.loadPrivacyInfo();
    }

    cacheDOM() {
        this.urlInput = document.getElementById('urlInput');
        this.fetchBtn = document.getElementById('fetchBtn');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.videoInfo = document.getElementById('videoInfo');
        this.errorMessage = document.getElementById('errorMessage');
        this.downloadStatus = document.getElementById('downloadStatus');
        this.videoTitle = document.getElementById('videoTitle');
        this.videoDuration = document.getElementById('videoDuration');
        this.videoUploader = document.getElementById('videoUploader');
        this.videoViews = document.getElementById('videoViews');
        this.qualitySelect = document.getElementById('qualitySelect');
        this.historyContainer = document.getElementById('historyContainer');
        this.privacyInfo = document.getElementById('privacyInfo');
        this.btnLoader = document.getElementById('btnLoader');
        this.downloadLoader = document.getElementById('downloadLoader');
    }

    bindEvents() {
        this.fetchBtn.addEventListener('click', () => this.fetchVideoInfo());
        this.downloadBtn.addEventListener('click', () => this.downloadVideo());
        this.urlInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.fetchVideoInfo();
        });
    }

    async fetchVideoInfo() {
        const url = this.urlInput.value.trim();
        
        if (!url) {
            this.showError('Please enter a YouTube URL');
            return;
        }

        this.showLoading(this.fetchBtn, this.btnLoader);

        try {
            const response = await fetch(`/api/video-info?url=${encodeURIComponent(url)}`);
            
            if (!response.ok) {
                this.showError(`Server error: ${response.status} ${response.statusText}`);
                this.hideLoading(this.fetchBtn, this.btnLoader);
                return;
            }
            
            const data = await response.json();

            if (data.error) {
                this.showError(data.error);
                this.hideLoading(this.fetchBtn, this.btnLoader);
                return;
            }

            this.currentVideoId = data.video_id;
            this.currentTitle = data.title;
            this.displayVideoInfo(data);
            await this.loadFormats();

            this.videoInfo.classList.remove('hidden');
            this.errorMessage.classList.add('hidden');
        } catch (error) {
            this.showError(`Failed to fetch video info: ${error.message || 'Network error'}`);
            console.error('Fetch error:', error);
        } finally {
            this.hideLoading(this.fetchBtn, this.btnLoader);
        }
    }

    displayVideoInfo(data) {
        this.videoTitle.textContent = data.title || 'Unknown Title';
        this.videoDuration.textContent = data.duration || '--:--';
        this.videoUploader.textContent = data.uploader || 'Unknown';
        this.videoViews.textContent = this.formatViews(data.view_count);
    }

    formatViews(viewCount) {
        if (!viewCount || viewCount === 'Unknown') return '0';
        
        // If it's already formatted with commas, return as is
        if (typeof viewCount === 'string' && viewCount.includes(',')) {
            return viewCount;
        }

        const num = parseInt(viewCount);
        if (isNaN(num)) return '0';

        if (num >= 1000000) {
            return (num / 1000000).toFixed(1).replace(/\.0$/, '') + 'M';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1).replace(/\.0$/, '') + 'K';
        }
        return num.toString();
    }

    async loadFormats() {
        try {
            const response = await fetch(
                `/api/formats?video_id=${encodeURIComponent(this.currentVideoId)}`
            );
            
            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }
            
            const data = await response.json();

            this.qualitySelect.innerHTML = '';
            data.formats.forEach((format, index) => {
                const option = document.createElement('option');
                option.value = index;
                option.textContent = `${format.quality} - ${format.codec} (${format.size_mb})`;
                this.qualitySelect.appendChild(option);
            });
        } catch (error) {
            console.error('Failed to load formats:', error);
            this.qualitySelect.innerHTML = '<option>Default Format</option>';
        }
    }

    async downloadVideo() {
        if (!this.currentVideoId || !this.currentTitle) {
            this.showError('Please fetch video info first');
            return;
        }

        this.showLoading(this.downloadBtn, this.downloadLoader);

        try {
            const response = await fetch(
                `/api/download?video_id=${encodeURIComponent(this.currentVideoId)}&title=${encodeURIComponent(this.currentTitle)}`
            );
            
            if (!response.ok) {
                this.showError(`Server error: ${response.status} ${response.statusText}. Make sure the server is running.`);
                this.hideLoading(this.downloadBtn, this.downloadLoader);
                return;
            }
            
            const data = await response.json();

            if (data.success) {
                this.showStatus(data.message || 'Video downloaded successfully!', 'success');
                this.downloadStatus.classList.remove('hidden');
                this.errorMessage.classList.add('hidden');
                
                // Reload history
                setTimeout(() => this.loadHistory(), 1000);
            } else {
                this.showError(data.error || 'Download failed');
            }
        } catch (error) {
            this.showError(`Failed to download video: ${error.message || 'Check if server is running at http://localhost:8000'}`);
            console.error('Download error:', error);
        } finally {
            this.hideLoading(this.downloadBtn, this.downloadLoader);
        }
    }

    async loadHistory() {
        try {
            const response = await fetch('/api/history');
            
            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }
            
            const data = await response.json();

            this.historyContainer.innerHTML = '';

            if (data.history.length === 0) {
                this.historyContainer.innerHTML = `
                    <div class="loading-placeholder" style="grid-column: 1/-1;">
                        <span>No downloads yet. Start downloading videos!</span>
                    </div>
                `;
                return;
            }

            data.history.forEach(item => {
                const card = this.createHistoryCard(item);
                this.historyContainer.appendChild(card);
            });
        } catch (error) {
            console.error('Failed to load history:', error);
            this.historyContainer.innerHTML = `
                <div class="loading-placeholder" style="grid-column: 1/-1;">
                    <span>Failed to load history</span>
                </div>
            `;
        }
    }

    createHistoryCard(item) {
        const card = document.createElement('div');
        card.className = 'history-item';
        
        const title = item.title || 'Unknown Title';
        const time = new Date(item.download_time).toLocaleDateString();
        
        card.innerHTML = `
            <div class="history-title" title="${title}">${title}</div>
            <div class="history-meta">Downloaded on ${time}</div>
        `;
        
        return card;
    }

    async loadPrivacyInfo() {
        try {
            const response = await fetch('/api/privacy');
            
            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }
            
            const data = await response.json();

            this.privacyInfo.innerHTML = '';

            Object.entries(data).forEach(([key, value]) => {
                if (key !== 'description') {
                    const item = document.createElement('div');
                    item.className = 'privacy-item';
                    
                    const label = key
                        .replace(/_/g, ' ')
                        .replace(/\b\w/g, char => char.toUpperCase());
                    
                    item.innerHTML = `
                        <strong>${label}</strong>
                        <span>${value}</span>
                    `;
                    
                    this.privacyInfo.appendChild(item);
                }
            });

            // Add description at the end
            if (data.description) {
                const descItem = document.createElement('div');
                descItem.className = 'privacy-item';
                descItem.innerHTML = `
                    <strong>About This Downloader</strong>
                    <span>${data.description}</span>
                `;
                this.privacyInfo.appendChild(descItem);
            }
        } catch (error) {
            console.error('Failed to load privacy info:', error);
            this.privacyInfo.innerHTML = `
                <div class="loading-placeholder">
                    <span>Failed to load privacy information</span>
                </div>
            `;
        }
    }

    showError(message) {
        this.errorMessage.textContent = message;
        this.errorMessage.classList.remove('hidden');
        this.downloadStatus.classList.add('hidden');
    }

    showStatus(message, type = 'info') {
        this.downloadStatus.textContent = message;
        this.downloadStatus.classList.remove('hidden');
        this.errorMessage.classList.add('hidden');
    }

    showLoading(button, loader) {
        button.disabled = true;
        loader.classList.remove('hidden');
    }

    hideLoading(button, loader) {
        button.disabled = false;
        loader.classList.add('hidden');
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new PrivateTubeApp();
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            
            // Update active nav link
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
            });
            this.classList.add('active');
        }
    });
});

// Update active nav link on scroll
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section[id]');
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        
        if (window.scrollY >= sectionTop - 100 && window.scrollY < sectionTop + sectionHeight - 100) {
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
            });
            
            const activeLink = document.querySelector(`.nav-link[href="#${section.id}"]`);
            if (activeLink) {
                activeLink.classList.add('active');
            }
        }
    });
});
