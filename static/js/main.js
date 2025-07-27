// =============================================================================
// ETKİNLİK YÖNETİMİ - ANA JAVASCRIPT DOSYASI
// =============================================================================
// Bu dosya projenin genel JavaScript fonksiyonlarını içerir

// DOM yüklendiğinde çalışacak kodlar
document.addEventListener('DOMContentLoaded', function() {
    
    // Fade-in animasyonu için
    const fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach(element => {
        element.style.opacity = '1';
    });
    
    // Form validasyonları
    initializeFormValidation();
    
    // Arama formu işlevselliği
    initializeSearchForm();
    
    // Progress bar animasyonları
    initializeProgressBars();
    
    // Tooltip'leri etkinleştir
    initializeTooltips();
    
    // Modal işlevselliği
    initializeModals();
});

// Form validasyonları
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Arama formu işlevselliği
function initializeSearchForm() {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('q');
    
    if (searchForm && searchInput) {
        // Arama input'unda debounce uygula
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                searchForm.submit();
            }, 500);
        });
    }
}

// Progress bar animasyonları
function initializeProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.width = width;
        }, 100);
    });
}

// Tooltip'leri etkinleştir
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Modal işlevselliği
function initializeModals() {
    const modals = document.querySelectorAll('.modal');
    
    modals.forEach(modal => {
        modal.addEventListener('show.bs.modal', function() {
            // Modal açılırken yapılacak işlemler
        });
        
        modal.addEventListener('hidden.bs.modal', function() {
            // Modal kapanırken yapılacak işlemler
        });
    });
}

// AJAX istekleri için yardımcı fonksiyon
function makeAjaxRequest(url, method = 'GET', data = null) {
    return fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: data ? JSON.stringify(data) : null
    })
    .then(response => response.json())
    .catch(error => {
        console.error('AJAX isteği başarısız:', error);
        showAlert('Bir hata oluştu. Lütfen tekrar deneyin.', 'danger');
    });
}

// CSRF token'ı al
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Alert gösterme fonksiyonu
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.messages') || document.body;
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.appendChild(alertDiv);
    
    // 5 saniye sonra otomatik kapat
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Loading spinner gösterme/gizleme
function showLoading(element) {
    if (element) {
        element.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Yükleniyor...';
        element.disabled = true;
    }
}

function hideLoading(element, originalText) {
    if (element) {
        element.innerHTML = originalText;
        element.disabled = false;
    }
}

// Tarih formatlama
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('tr-TR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Para formatlama
function formatCurrency(amount) {
    return new Intl.NumberFormat('tr-TR', {
        style: 'currency',
        currency: 'TRY'
    }).format(amount);
}

// Dosya yükleme önizleme
function previewImage(input, previewElement) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            previewElement.src = e.target.result;
            previewElement.style.display = 'block';
        };
        
        reader.readAsDataURL(input.files[0]);
    }
}

// Etkinlik kayıt işlevi
function registerForEvent(eventId) {
    const button = document.querySelector(`[data-event-id="${eventId}"]`);
    const originalText = button.innerHTML;
    
    showLoading(button);
    
    makeAjaxRequest(`/kayitlar/etkinlik/${eventId}/kayit/`, 'POST')
        .then(response => {
            if (response.success) {
                showAlert('Etkinliğe başarıyla kayıt oldunuz!', 'success');
                button.innerHTML = '<i class="bi bi-check-circle"></i> Kayıtlı';
                button.className = 'btn btn-success btn-sm';
                button.disabled = true;
            } else {
                showAlert(response.message || 'Kayıt işlemi başarısız!', 'danger');
                hideLoading(button, originalText);
            }
        })
        .catch(error => {
            showAlert('Bir hata oluştu. Lütfen tekrar deneyin.', 'danger');
            hideLoading(button, originalText);
        });
}

// Kayıt iptal işlevi
function cancelRegistration(registrationId) {
    if (confirm('Bu kaydı iptal etmek istediğinizden emin misiniz?')) {
        const button = document.querySelector(`[data-registration-id="${registrationId}"]`);
        const originalText = button.innerHTML;
        
        showLoading(button);
        
        makeAjaxRequest(`/kayitlar/${registrationId}/iptal/`, 'POST')
            .then(response => {
                if (response.success) {
                    showAlert('Kayıt başarıyla iptal edildi!', 'success');
                    button.closest('.card').remove();
                } else {
                    showAlert(response.message || 'İptal işlemi başarısız!', 'danger');
                    hideLoading(button, originalText);
                }
            })
            .catch(error => {
                showAlert('Bir hata oluştu. Lütfen tekrar deneyin.', 'danger');
                hideLoading(button, originalText);
            });
    }
}

// Arama filtrelerini temizle
function clearFilters() {
    const form = document.getElementById('search-form');
    if (form) {
        form.reset();
        form.submit();
    }
}

// Sayfa yüklendiğinde çalışacak ek işlevler
window.addEventListener('load', function() {
    // Lazy loading için Intersection Observer
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // Smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Global değişkenler
window.EventManagement = {
    showAlert,
    makeAjaxRequest,
    formatDate,
    formatCurrency,
    registerForEvent,
    cancelRegistration,
    clearFilters
}; 