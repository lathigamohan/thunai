// Finla - Main JavaScript Functions

// Global variables
let isOnline = navigator.onLine;
let installPrompt = null;

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    checkOnlineStatus();
});

function initializeApp() {
    console.log('🏆 Finla - Premium Finance Tracker Initialized');
    
    // Load user preferences
    loadUserPreferences();
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-hide alerts after 5 seconds
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            if (alert.classList.contains('alert-success')) {
                bootstrap.Alert.getOrCreateInstance(alert).close();
            }
        });
    }, 5000);
    
    // Add loading animation class to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
}

function setupEventListeners() {
    // PWA install prompt
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        installPrompt = e;
        showInstallButton();
    });
    
    // Online/offline status
    window.addEventListener('online', () => {
        isOnline = true;
        showStatus('Connected', 'success');
    });
    
    window.addEventListener('offline', () => {
        isOnline = false;
        showStatus('Offline Mode', 'warning');
    });
    
    // Form validations
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', validateForm);
    });
    
    // Number input formatting
    const amountInputs = document.querySelectorAll('input[type="number"]');
    amountInputs.forEach(input => {
        input.addEventListener('blur', formatCurrency);
    });
    
    // Auto-save form data
    const formInputs = document.querySelectorAll('input, select, textarea');
    formInputs.forEach(input => {
        input.addEventListener('change', autoSaveFormData);
    });
}

function checkOnlineStatus() {
    if (!isOnline) {
        showStatus('You are currently offline. Some features may be limited.', 'warning');
    }
}

function showStatus(message, type = 'info') {
    const statusDiv = document.createElement('div');
    statusDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    statusDiv.style.cssText = 'top: 80px; right: 20px; z-index: 1050; min-width: 250px;';
    statusDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(statusDiv);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        if (statusDiv.parentNode) {
            statusDiv.remove();
        }
    }, 3000);
}

function showInstallButton() {
    const installBtn = document.createElement('button');
    installBtn.className = 'btn btn-warning btn-sm position-fixed';
    installBtn.style.cssText = 'bottom: 20px; right: 20px; z-index: 1050;';
    installBtn.innerHTML = '<i class="fas fa-download me-2"></i>Install App';
    installBtn.onclick = installApp;
    
    document.body.appendChild(installBtn);
}

async function installApp() {
    if (installPrompt) {
        installPrompt.prompt();
        const result = await installPrompt.userChoice;
        
        if (result.outcome === 'accepted') {
            console.log('PWA installed');
            showStatus('App installed successfully!', 'success');
        }
        
        installPrompt = null;
        // Remove install button
        const installBtn = document.querySelector('.btn[onclick="installApp()"]');
        if (installBtn) installBtn.remove();
    }
}

function validateForm(event) {
    const form = event.target;
    let isValid = true;
    const errors = [];
    
    // Amount validation
    const amountInputs = form.querySelectorAll('input[type="number"]');
    amountInputs.forEach(input => {
        if (input.required && (input.value <= 0 || !input.value)) {
            isValid = false;
            errors.push(`${input.labels[0]?.textContent || 'Amount'} must be greater than 0`);
            input.classList.add('is-invalid');
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    // Date validation
    const dateInputs = form.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        if (input.required && input.value) {
            const selectedDate = new Date(input.value);
            const today = new Date();
            
            if (input.name === 'target_date' && selectedDate <= today) {
                isValid = false;
                errors.push('Target date must be in the future');
                input.classList.add('is-invalid');
            } else {
                input.classList.remove('is-invalid');
            }
        }
    });
    
    // Text validation
    const textInputs = form.querySelectorAll('input[type="text"], textarea');
    textInputs.forEach(input => {
        if (input.required && input.value.trim().length < 2) {
            isValid = false;
            errors.push(`${input.labels[0]?.textContent || 'Field'} must be at least 2 characters`);
            input.classList.add('is-invalid');
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    if (!isValid) {
        event.preventDefault();
        showValidationErrors(errors);
    }
    
    return isValid;
}

function showValidationErrors(errors) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-danger alert-dismissible fade show';
    errorDiv.innerHTML = `
        <h6><i class="fas fa-exclamation-triangle me-2"></i>Please fix the following errors:</h6>
        <ul class="mb-0">
            ${errors.map(error => `<li>${error}</li>`).join('')}
        </ul>
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at the top of the main content
    const mainContent = document.querySelector('.main-content .container');
    if (mainContent) {
        mainContent.insertBefore(errorDiv, mainContent.firstChild);
    }
    
    // Scroll to top to show errors
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function formatCurrency(event) {
    const input = event.target;
    const value = parseFloat(input.value);
    
    if (!isNaN(value)) {
        // Add visual feedback for large amounts
        if (value > 10000) {
            input.classList.add('border-warning');
        } else {
            input.classList.remove('border-warning');
        }
    }
}

function autoSaveFormData() {
    if (!window.localStorage) return;
    
    const formData = {};
    const currentForm = this.closest('form');
    
    if (currentForm) {
        const formInputs = currentForm.querySelectorAll('input, select, textarea');
        formInputs.forEach(input => {
            if (input.name && input.value) {
                formData[input.name] = input.value;
            }
        });
        
        // Save to localStorage with timestamp
        const saveKey = `finla_form_${window.location.pathname}`;
        localStorage.setItem(saveKey, JSON.stringify({
            data: formData,
            timestamp: Date.now()
        }));
    }
}

function loadUserPreferences() {
    if (!window.localStorage) return;
    
    // Load saved form data (within last hour)
    const saveKey = `finla_form_${window.location.pathname}`;
    const savedData = localStorage.getItem(saveKey);
    
    if (savedData) {
        try {
            const parsed = JSON.parse(savedData);
            const hourAgo = Date.now() - (60 * 60 * 1000);
            
            if (parsed.timestamp > hourAgo) {
                // Restore form data
                Object.entries(parsed.data).forEach(([name, value]) => {
                    const input = document.querySelector(`[name="${name}"]`);
                    if (input && !input.value) {
                        input.value = value;
                    }
                });
                
                console.log('Form data restored from previous session');
            } else {
                // Clean up old data
                localStorage.removeItem(saveKey);
            }
        } catch (e) {
            console.warn('Failed to restore form data:', e);
        }
    }
}

// Utility functions
function formatAmount(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    }).format(amount);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function debounce(func, wait) {
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

function showConfirmDialog(message, callback) {
    const confirmed = confirm(message);
    if (confirmed && typeof callback === 'function') {
        callback();
    }
    return confirmed;
}

// Category prediction function
function predictCategory(description) {
    const categories = {
        'food': ['lunch', 'dinner', 'breakfast', 'restaurant', 'hotel', 'biryani', 'pizza', 'burger', 'meal', 'food'],
        'transport': ['bus', 'auto', 'taxi', 'uber', 'ola', 'metro', 'train', 'fuel', 'petrol', 'travel'],
        'education': ['book', 'course', 'fee', 'tuition', 'study', 'exam', 'college', 'school', 'education'],
        'snacks': ['tea', 'coffee', 'snacks', 'juice', 'water', 'biscuit', 'chips', 'drink'],
        'shopping': ['shirt', 'clothes', 'shopping', 'mall', 'amazon', 'flipkart', 'store'],
        'entertainment': ['movie', 'cinema', 'game', 'music', 'netflix', 'entertainment'],
        'health': ['medicine', 'doctor', 'hospital', 'pharmacy', 'health', 'medical'],
        'utilities': ['electricity', 'water', 'gas', 'internet', 'phone', 'bill'],
        'others': []
    };
    
    const desc = description.toLowerCase().trim();
    
    for (const [category, keywords] of Object.entries(categories)) {
        if (keywords.some(keyword => desc.includes(keyword))) {
            return category;
        }
    }
    
    return 'others';
}

// Export functions for global use
window.Finla = {
    formatAmount,
    formatDate,
    predictCategory,
    showConfirmDialog,
    showStatus,
    validateForm
};

// Service Worker registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/service-worker.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Notification functions
function requestNotificationPermission() {
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                console.log('Notifications enabled');
            }
        });
    }
}

function showNotification(title, options = {}) {
    if ('Notification' in window && Notification.permission === 'granted') {
        const notification = new Notification(title, {
            icon: '/static/icon-192x192.png',
            badge: '/static/icon-72x72.png',
            ...options
        });
        
        // Auto-close after 5 seconds
        setTimeout(() => notification.close(), 5000);
        
        return notification;
    }
}

// Initialize notifications on first user interaction
document.addEventListener('click', requestNotificationPermission, { once: true });

console.log('🌟 Finla Scripts Loaded Successfully');
