// Add product row in invoice form
function addProductRow() {
    const container = document.getElementById('invoice-items');
    const rowCount = container.children.length;
    
    const newRow = document.createElement('div');
    newRow.className = 'row mb-2 invoice-item-row';
    newRow.innerHTML = `
        <div class="col-md-5">
            <select class="form-control item-product" name="item_product_id">
                <option value="">-- Select Product --</option>
            </select>
        </div>
        <div class="col-md-2">
            <input type="number" class="form-control" name="item_quantity" placeholder="Qty" min="1">
        </div>
        <div class="col-md-3">
            <input type="number" class="form-control" name="item_price" placeholder="Price" readonly>
        </div>
        <div class="col-md-2">
            <button type="button" class="btn btn-sm btn-danger" onclick="removeProductRow(this)">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `;
    
    container.appendChild(newRow);
}

function removeProductRow(btn) {
    btn.closest('.invoice-item-row').remove();
}

// Format currency
function formatCurrency(value) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(value);
}

// Calculate invoice total
function calculateInvoiceTotal() {
    let subtotal = 0;
    
    document.querySelectorAll('.invoice-item-row').forEach(row => {
        const quantity = parseFloat(row.querySelector('[name="item_quantity"]').value) || 0;
        const price = parseFloat(row.querySelector('[name="item_price"]').value) || 0;
        subtotal += quantity * price;
    });
    
    const taxPercent = parseFloat(document.querySelector('[name="tax_percent"]').value) || 0;
    const discountAmount = parseFloat(document.querySelector('[name="discount_amount"]').value) || 0;
    
    const tax = subtotal * (taxPercent / 100);
    const total = subtotal + tax - discountAmount;
    
    document.getElementById('subtotal').textContent = formatCurrency(subtotal);
    document.getElementById('tax-amount').textContent = formatCurrency(tax);
    document.getElementById('total-amount').textContent = formatCurrency(total);
}

// Search products
function searchProducts(query) {
    if (query.length < 2) return;
    
    fetch(`/api/search-products?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            const suggestions = document.getElementById('product-suggestions');
            suggestions.innerHTML = '';
            
            data.forEach(product => {
                const div = document.createElement('div');
                div.className = 'suggestion-item';
                div.textContent = `${product.name} (${product.sku})`;
                div.onclick = () => selectProduct(product);
                suggestions.appendChild(div);
            });
        });
}

// Debounce function
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

// Export to PDF
function exportToPDF(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    window.print();
}

// Date range picker
function initializeDateRanges() {
    const fromDateInput = document.querySelector('[name="from_date"]');
    const toDateInput = document.querySelector('[name="to_date"]');
    
    if (fromDateInput && toDateInput) {
        toDateInput.min = fromDateInput.value;
        
        fromDateInput.addEventListener('change', function() {
            toDateInput.min = this.value;
        });
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Initialize date ranges
    initializeDateRanges();
    
    // Add event listeners for dynamic calculations
    document.addEventListener('change', function(e) {
        if (e.target.matches('[name="item_quantity"], [name="item_price"], [name="tax_percent"], [name="discount_amount"]')) {
            calculateInvoiceTotal();
        }
    });
});

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    });
}

// Show notification
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.querySelector('.container-fluid').insertBefore(alertDiv, document.querySelector('.container-fluid').firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}
