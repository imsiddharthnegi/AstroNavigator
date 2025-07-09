// AstroMissionSim - Main JavaScript File

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    console.log('AstroMissionSim initialized');
    
    // Initialize components
    initializeTooltips();
    initializeAnimations();
    initializeTheme();
    initializeNotifications();
    
    // Set up auto-refresh for analyzing missions
    checkForAnalyzingMissions();
});

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize animations
function initializeAnimations() {
    // Fade in cards on page load
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Add hover effects to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Initialize theme
function initializeTheme() {
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('astro-theme');
    if (savedTheme) {
        document.body.classList.add(savedTheme);
    }
    
    // Add theme toggle if needed
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
}

// Toggle theme
function toggleTheme() {
    const body = document.body;
    const currentTheme = body.classList.contains('light-theme') ? 'light-theme' : 'dark-theme';
    const newTheme = currentTheme === 'light-theme' ? 'dark-theme' : 'light-theme';
    
    body.classList.remove(currentTheme);
    body.classList.add(newTheme);
    
    localStorage.setItem('astro-theme', newTheme);
}

// Initialize notifications
function initializeNotifications() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

// Check for analyzing missions and auto-refresh
function checkForAnalyzingMissions() {
    const analyzingElements = document.querySelectorAll('[data-status="analyzing"]');
    
    if (analyzingElements.length > 0) {
        // Refresh page every 10 seconds if there are analyzing missions
        setTimeout(() => {
            location.reload();
        }, 10000);
    }
}

// Utility Functions
const AstroUtils = {
    // Format numbers with commas
    formatNumber: function(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },
    
    // Format dates
    formatDate: function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    },
    
    // Format duration
    formatDuration: function(days) {
        if (days < 30) {
            return `${days} days`;
        } else if (days < 365) {
            const months = Math.floor(days / 30);
            return `${months} month${months > 1 ? 's' : ''}`;
        } else {
            const years = Math.floor(days / 365);
            const remainingDays = days % 365;
            const months = Math.floor(remainingDays / 30);
            
            let result = `${years} year${years > 1 ? 's' : ''}`;
            if (months > 0) {
                result += ` ${months} month${months > 1 ? 's' : ''}`;
            }
            return result;
        }
    },
    
    // Get risk level color
    getRiskColor: function(riskLevel) {
        const colors = {
            'low': 'success',
            'medium': 'warning',
            'high': 'danger',
            'critical': 'danger'
        };
        return colors[riskLevel.toLowerCase()] || 'secondary';
    },
    
    // Get status color
    getStatusColor: function(status) {
        const colors = {
            'draft': 'secondary',
            'analyzing': 'info',
            'completed': 'success',
            'failed': 'danger'
        };
        return colors[status.toLowerCase()] || 'secondary';
    },
    
    // Show loading spinner
    showLoading: function(element) {
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner mx-auto';
        spinner.id = 'loading-spinner';
        
        element.innerHTML = '';
        element.appendChild(spinner);
    },
    
    // Hide loading spinner
    hideLoading: function(element) {
        const spinner = element.querySelector('#loading-spinner');
        if (spinner) {
            spinner.remove();
        }
    },
    
    // Show toast notification
    showToast: function(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        // Add to toast container or create one
        let toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
            toastContainer.style.zIndex = '1055';
            document.body.appendChild(toastContainer);
        }
        
        toastContainer.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remove toast after it's hidden
        toast.addEventListener('hidden.bs.toast', function() {
            toast.remove();
        });
    },
    
    // Copy to clipboard
    copyToClipboard: function(text) {
        navigator.clipboard.writeText(text).then(function() {
            AstroUtils.showToast('Copied to clipboard!', 'success');
        }, function() {
            AstroUtils.showToast('Failed to copy to clipboard', 'danger');
        });
    },
    
    // Validate form field
    validateField: function(field, validator) {
        const value = field.value.trim();
        const isValid = validator(value);
        
        if (isValid) {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
        } else {
            field.classList.remove('is-valid');
            field.classList.add('is-invalid');
        }
        
        return isValid;
    },
    
    // Debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// Chart utilities
const ChartUtils = {
    // Create feasibility chart
    createFeasibilityChart: function(canvasId, score) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        
        return new Chart(ctx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [score, 100 - score],
                    backgroundColor: ['#3f51b5', 'rgba(255, 255, 255, 0.1)'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    },
    
    // Create risk distribution chart
    createRiskChart: function(canvasId, data) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        
        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Low', 'Medium', 'High', 'Critical'],
                datasets: [{
                    data: [data.low, data.medium, data.high, data.critical],
                    backgroundColor: ['#4caf50', '#ff9800', '#f44336', '#d32f2f']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            color: '#e3f2fd'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    },
                    x: {
                        ticks: {
                            color: '#e3f2fd'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
};

// API utilities
const ApiUtils = {
    // Make API request
    request: async function(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        const mergedOptions = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(url, mergedOptions);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    },
    
    // Get mission status
    getMissionStatus: async function(missionId) {
        return await this.request(`/mission/api/status/${missionId}`);
    },
    
    // Get statistics
    getStatistics: async function() {
        return await this.request('/mission/api/statistics');
    }
};

// Export utilities for use in other files
window.AstroUtils = AstroUtils;
window.ChartUtils = ChartUtils;
window.ApiUtils = ApiUtils;

// Service Worker registration for offline functionality
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Skip service worker registration for now
        // navigator.serviceWorker.register('/sw.js');
    });
}

// Handle online/offline status
window.addEventListener('online', function() {
    AstroUtils.showToast('Connection restored', 'success');
});

window.addEventListener('offline', function() {
    AstroUtils.showToast('Connection lost - some features may be unavailable', 'warning');
});

// Global error handler
window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
    AstroUtils.showToast('An unexpected error occurred', 'danger');
});

// Handle unhandled promise rejections
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    AstroUtils.showToast('An unexpected error occurred', 'danger');
});
