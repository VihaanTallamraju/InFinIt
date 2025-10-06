/**
 * FinLit - Games JavaScript
 * Interactive functionality for financial literacy games
 * Enhanced with mobile touch support
 */

// Global game state and utilities
const FinLitGames = {
    // Configuration
    config: {
        localStoragePrefix: 'finlit_',
        animationDuration: 300,
        fadeDelay: 150,
        isMobile: /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent),
        isTouch: 'ontouchstart' in window
    },
    
    // Utility functions
    utils: {
        /**
         * Format currency with proper comma separation
         * @param {number} amount 
         * @returns {string}
         */
        formatCurrency: function(amount) {
            return new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
            }).format(amount);
        },
        
        /**
         * Format percentage with one decimal place
         * @param {number} percent 
         * @returns {string}
         */
        formatPercent: function(percent) {
            return `${percent.toFixed(1)}%`;
        },
        
        /**
         * Animate number counting up
         * @param {HTMLElement} element 
         * @param {number} start 
         * @param {number} end 
         * @param {number} duration 
         */
        animateNumber: function(element, start, end, duration = 1000) {
            const range = end - start;
            const increment = range / (duration / 16);
            let current = start;
            
            const timer = setInterval(() => {
                current += increment;
                if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
                    current = end;
                    clearInterval(timer);
                }
                
                if (element.textContent.includes('$')) {
                    element.textContent = this.formatCurrency(current);
                } else if (element.textContent.includes('%')) {
                    element.textContent = this.formatPercent(current);
                } else {
                    element.textContent = Math.round(current);
                }
            }, 16);
        },
        
        /**
         * Show loading state on element
         * @param {HTMLElement} element 
         */
        showLoading: function(element) {
            element.classList.add('loading');
            const originalText = element.innerHTML;
            element.dataset.originalText = originalText;
            element.innerHTML = '<i class="bi bi-hourglass"></i> Loading...';
        },
        
        /**
         * Hide loading state on element
         * @param {HTMLElement} element 
         */
        hideLoading: function(element) {
            element.classList.remove('loading');
            if (element.dataset.originalText) {
                element.innerHTML = element.dataset.originalText;
                delete element.dataset.originalText;
            }
        },
        
        /**
         * Smooth scroll to element
         * @param {HTMLElement} element 
         */
        scrollToElement: function(element) {
            element.scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
        },
        
        /**
         * Show success message
         * @param {string} message 
         */
        showSuccess: function(message) {
            this.showAlert(message, 'success');
        },
        
        /**
         * Show error message
         * @param {string} message 
         */
        showError: function(message) {
            this.showAlert(message, 'danger');
        },
        
        /**
         * Show alert message
         * @param {string} message 
         * @param {string} type 
         */
        showAlert: function(message, type = 'info') {
            const alertHtml = `
                <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                    ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
            
            // Insert at top of page
            const container = document.querySelector('.container');
            if (container) {
                container.insertAdjacentHTML('afterbegin', alertHtml);
                
                // Auto-dismiss after 5 seconds
                setTimeout(() => {
                    const alert = container.querySelector('.alert');
                    if (alert) {
                        alert.remove();
                    }
                }, 5000);
            }
        }
    },
    
    // Local storage management
    storage: {
        /**
         * Get value from localStorage with prefix
         * @param {string} key 
         * @returns {any}
         */
        get: function(key) {
            const fullKey = FinLitGames.config.localStoragePrefix + key;
            const value = localStorage.getItem(fullKey);
            try {
                return JSON.parse(value);
            } catch (e) {
                return value;
            }
        },
        
        /**
         * Set value in localStorage with prefix
         * @param {string} key 
         * @param {any} value 
         */
        set: function(key, value) {
            const fullKey = FinLitGames.config.localStoragePrefix + key;
            const stringValue = typeof value === 'string' ? value : JSON.stringify(value);
            localStorage.setItem(fullKey, stringValue);
        },
        
        /**
         * Increment a numeric value in storage
         * @param {string} key 
         * @param {number} increment 
         */
        increment: function(key, increment = 1) {
            const current = parseInt(this.get(key)) || 0;
            this.set(key, current + increment);
            return current + increment;
        }
    },
    
    // Progress tracking
    progress: {
        /**
         * Update game play count
         * @param {string} gameType 
         */
        updateGameCount: function(gameType) {
            const key = `${gameType}_games_played`;
            const newCount = FinLitGames.storage.increment(key);
            
            // Update any progress displays on the page
            this.updateProgressDisplays();
            
            return newCount;
        },
        
        /**
         * Get total games played
         * @returns {number}
         */
        getTotalGamesPlayed: function() {
            const budget = parseInt(FinLitGames.storage.get('budget_games_played')) || 0;
            const saving = parseInt(FinLitGames.storage.get('saving_games_played')) || 0;
            const invest = parseInt(FinLitGames.storage.get('invest_games_played')) || 0;
            
            return budget + saving + invest;
        },
        
        /**
         * Update progress displays on current page
         */
        updateProgressDisplays: function() {
            const progressElement = document.getElementById('progress-text');
            if (progressElement) {
                const budget = parseInt(FinLitGames.storage.get('budget_games_played')) || 0;
                const saving = parseInt(FinLitGames.storage.get('saving_games_played')) || 0;
                const invest = parseInt(FinLitGames.storage.get('invest_games_played')) || 0;
                const total = budget + saving + invest;
                
                if (total > 0) {
                    progressElement.innerHTML = `
                        Games played: ${total} | 
                        Budget: ${budget} | 
                        Saving: ${saving} | 
                        Investment: ${invest}
                    `;
                }
            }
        },
        
        /**
         * Get achievement level based on games played
         * @returns {object}
         */
        getAchievementLevel: function() {
            const total = this.getTotalGamesPlayed();
            
            if (total >= 20) {
                return { level: 'Expert', badge: 'success', icon: 'trophy-fill' };
            } else if (total >= 10) {
                return { level: 'Advanced', badge: 'warning', icon: 'award-fill' };
            } else if (total >= 5) {
                return { level: 'Intermediate', badge: 'info', icon: 'star-fill' };
            } else if (total >= 1) {
                return { level: 'Beginner', badge: 'primary', icon: 'circle-fill' };
            } else {
                return { level: 'New User', badge: 'secondary', icon: 'circle' };
            }
        }
    },
    
    // API helpers
    api: {
        /**
         * Make API request with error handling
         * @param {string} url 
         * @param {object} data 
         * @param {object} options 
         * @returns {Promise}
         */
        post: async function(url, data, options = {}) {
            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        ...options.headers
                    },
                    body: JSON.stringify(data),
                    ...options
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                return await response.json();
            } catch (error) {
                console.error('API request failed:', error);
                FinLitGames.utils.showError('Sorry, there was a problem processing your request. Please try again.');
                throw error;
            }
        }
    },
    
    // Animation helpers
    animations: {
        /**
         * Fade in element
         * @param {HTMLElement} element 
         * @param {number} duration 
         */
        fadeIn: function(element, duration = 300) {
            element.style.opacity = '0';
            element.style.display = 'block';
            
            let opacity = 0;
            const increment = 1 / (duration / 16);
            
            const timer = setInterval(() => {
                opacity += increment;
                if (opacity >= 1) {
                    opacity = 1;
                    clearInterval(timer);
                }
                element.style.opacity = opacity;
            }, 16);
        },
        
        /**
         * Fade out element
         * @param {HTMLElement} element 
         * @param {number} duration 
         */
        fadeOut: function(element, duration = 300) {
            let opacity = 1;
            const decrement = 1 / (duration / 16);
            
            const timer = setInterval(() => {
                opacity -= decrement;
                if (opacity <= 0) {
                    opacity = 0;
                    element.style.display = 'none';
                    clearInterval(timer);
                }
                element.style.opacity = opacity;
            }, 16);
        },
        
        /**
         * Pulse element
         * @param {HTMLElement} element 
         * @param {number} times 
         */
        pulse: function(element, times = 3) {
            let count = 0;
            const interval = setInterval(() => {
                element.style.transform = 'scale(1.05)';
                setTimeout(() => {
                    element.style.transform = 'scale(1)';
                }, 150);
                
                count++;
                if (count >= times) {
                    clearInterval(interval);
                }
            }, 300);
        }
    }
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Mobile-specific enhancements
    if (FinLitGames.config.isMobile || FinLitGames.config.isTouch) {
        // Add touch-friendly button feedback
        document.querySelectorAll('.btn, .card, .list-group-item-action').forEach(element => {
            element.addEventListener('touchstart', function() {
                this.style.opacity = '0.8';
                this.style.transform = 'scale(0.98)';
            });
            
            element.addEventListener('touchend', function() {
                setTimeout(() => {
                    this.style.opacity = '';
                    this.style.transform = '';
                }, 150);
            });
            
            element.addEventListener('touchcancel', function() {
                this.style.opacity = '';
                this.style.transform = '';
            });
        });
        
        // Prevent 300ms delay on double-tap zoom
        document.addEventListener('touchstart', function() {}, true);
        
        // Enhanced focus handling for mobile accessibility
        document.querySelectorAll('input, select, textarea, button').forEach(element => {
            element.addEventListener('focus', function() {
                this.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'center',
                    inline: 'nearest'
                });
            });
        });
    }
    
    // Update any progress displays
    FinLitGames.progress.updateProgressDisplays();
    
    // Add smooth scrolling to all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                FinLitGames.utils.scrollToElement(target);
            }
        });
    });
    
    // Add loading states to forms
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                FinLitGames.utils.showLoading(submitBtn);
            }
        });
    });
    
    // Add hover effects to cards (desktop) and touch feedback (mobile)
    document.querySelectorAll('.card').forEach(card => {
        if (!FinLitGames.config.isMobile) {
            // Desktop hover effects
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px)';
                this.style.transition = 'transform 0.3s ease';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        } else {
            // Mobile: add subtle touch feedback that's already handled above
            card.style.transition = 'transform 0.15s ease, opacity 0.15s ease';
        }
    });
    
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Add achievement badge to navigation if user has played games
    const achievementLevel = FinLitGames.progress.getAchievementLevel();
    if (achievementLevel.level !== 'New User') {
        const navbar = document.querySelector('.navbar-nav');
        if (navbar) {
            const badgeHtml = `
                <li class="nav-item">
                    <span class="nav-link">
                        <i class="bi bi-${achievementLevel.icon} text-${achievementLevel.badge}"></i>
                        ${achievementLevel.level}
                    </span>
                </li>
            `;
            navbar.insertAdjacentHTML('beforeend', badgeHtml);
        }
    }
});

// Performance monitoring (simple)
window.addEventListener('load', function() {
    const loadTime = performance.now();
    console.log(`FinLit app loaded in ${Math.round(loadTime)}ms`);
    
    // Log page view (for analytics if needed)
    const page = window.location.pathname;
    FinLitGames.storage.set('last_visit', Date.now());
    
    // Update visit count
    const visits = FinLitGames.storage.increment('page_visits');
    if (visits === 1) {
        FinLitGames.utils.showSuccess('Welcome to FinLit! Start your financial literacy journey today.');
    }
});

// Export for global use
window.FinLitGames = FinLitGames;