document.addEventListener('DOMContentLoaded', function() {
    // 搜索功能
    const searchBtn = document.getElementById('searchBtn');
    const searchInput = document.getElementById('searchInput');
    
    if (searchBtn && searchInput) {
        searchBtn.addEventListener('click', function() {
            const query = searchInput.value.trim();
            if (query) {
                window.location.href = `/jobs?search=${encodeURIComponent(query)}`;
            } else {
                window.location.href = '/jobs';
            }
        });
        
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchBtn.click();
            }
        });
    }
    
    // 职位卡片悬停效果
    const jobCards = document.querySelectorAll('.job-card');
    jobCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 6px 16px rgba(0, 0, 0, 0.12)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
            this.style.boxShadow = '';
        });
    });
    
    // 实时职位搜索
    if (window.location.pathname === '/jobs') {
        const searchInput = document.getElementById('jobSearch');
        const jobCards = document.querySelectorAll('.job-card');
        
        if (searchInput && jobCards.length) {
            searchInput.addEventListener('input', function() {
                const searchTerm = this.value.toLowerCase();
                
                jobCards.forEach(card => {
                    const title = card.querySelector('.job-title').textContent.toLowerCase();
                    const company = card.querySelector('.job-company').textContent.toLowerCase();
                    const location = card.querySelector('.job-location').textContent.toLowerCase();
                    
                    if (title.includes(searchTerm) || company.includes(searchTerm) || location.includes(searchTerm)) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        }
    }
    
    // 表单验证
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const inputs = this.querySelectorAll('input[required], select[required], textarea[required]');
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add('error');
                    
                    // 添加错误提示
                    if (!input.nextElementSibling || !input.nextElementSibling.classList.contains('error-text')) {
                        const errorText = document.createElement('div');
                        errorText.className = 'error-text';
                        errorText.textContent = '此字段为必填项';
                        errorText.style.color = 'var(--danger)';
                        errorText.style.fontSize = '12px';
                        errorText.style.marginTop = '5px';
                        input.parentNode.appendChild(errorText);
                    }
                } else {
                    input.classList.remove('error');
                    const errorText = input.nextElementSibling;
                    if (errorText && errorText.classList.contains('error-text')) {
                        errorText.remove();
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('请填写所有必填字段');
            }
        });
    });
});
