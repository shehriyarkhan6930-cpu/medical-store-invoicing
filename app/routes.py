from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app import db, login_manager
from app.models import User, Product, Customer, Invoice, InvoiceItem, Transaction, StockAdjustment
from app.database import DatabaseManager
from datetime import datetime, timedelta
from sqlalchemy import func, and_, or_
import uuid

# Blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
invoice_bp = Blueprint('invoice', __name__, url_prefix='/invoice')
inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')
customer_bp = Blueprint('customer', __name__, url_prefix='/customer')
report_bp = Blueprint('report', __name__, url_prefix='/report')
main_bp = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# ==================== AUTH ROUTES ====================

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            login_user(user, remember=request.form.get('remember_me'))
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not current_user.check_password(old_password):
            flash('Old password is incorrect', 'danger')
        elif new_password != confirm_password:
            flash('New passwords do not match', 'danger')
        elif len(new_password) < 6:
            flash('Password must be at least 6 characters', 'danger')
        else:
            current_user.set_password(new_password)
            db.session.commit()
            flash('Password changed successfully', 'success')
            return redirect(url_for('main.dashboard'))
    
    return render_template('change_password.html')

# ==================== MAIN ROUTES ====================

@main_bp.route('/')
@main_bp.route('/dashboard')
@login_required
def dashboard():
    stats = DatabaseManager.get_dashboard_stats()
    return render_template('index.html', stats=stats)

# ==================== INVOICE ROUTES ====================

@invoice_bp.route('/list')
@login_required
def list_invoices():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Invoice.query
    if search:
        query = query.filter(
            or_(
                Invoice.invoice_number.ilike(f'%{search}%'),
                Invoice.customer_name.ilike(f'%{search}%')
            )
        )
    
    invoices = query.order_by(Invoice.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('invoices.html', invoices=invoices, search=search)

@invoice_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_invoice():
    if request.method == 'POST':
        try:
            customer_id = request.form.get('customer_id')
            customer_name = request.form.get('customer_name')
            payment_method = request.form.get('payment_method', 'cash')
            tax_percent = float(request.form.get('tax_percent', 0))
            discount_amount = float(request.form.get('discount_amount', 0))
            notes = request.form.get('notes', '')
            
            # Generate invoice number
            invoice_number = f"INV-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
            
            invoice = Invoice(
                invoice_number=invoice_number,
                customer_id=customer_id,
                customer_name=customer_name,
                payment_method=payment_method,
                tax_percent=tax_percent,
                discount_amount=discount_amount,
                notes=notes,
                created_by=current_user.id
            )
            
            # Get items from request
            items_data = request.form.getlist('item_product_id')
            quantities = request.form.getlist('item_quantity')
            
            subtotal = 0
            for product_id, quantity in zip(items_data, quantities):
                if not product_id or not quantity:
                    continue
                
                quantity = int(quantity)
                product = Product.query.get(product_id)
                
                if not product or quantity > product.quantity:
                    flash(f'Insufficient stock for {product.name}', 'danger')
                    return redirect(url_for('invoice.create_invoice'))
                
                item_price = product.selling_price
                item_discount = product.discount_percent
                item_total = quantity * item_price * (1 - item_discount/100)
                
                invoice_item = InvoiceItem(
                    product_id=product_id,
                    product_name=product.name,
                    quantity=quantity,
                    unit_price=item_price,
                    discount_percent=item_discount,
                    discount_amount=quantity * item_price * (item_discount/100),
                    total_amount=item_total
                )
                
                invoice.items.append(invoice_item)
                subtotal += item_total
                
                # Update product quantity
                product.quantity -= quantity
            
            # Calculate totals
            invoice.subtotal = subtotal
            invoice.tax_amount = subtotal * (tax_percent / 100)
            invoice.total_amount = subtotal + invoice.tax_amount - discount_amount
            
            db.session.add(invoice)
            db.session.commit()
            
            flash(f'Invoice {invoice_number} created successfully', 'success')
            return redirect(url_for('invoice.view_invoice', invoice_id=invoice.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating invoice: {str(e)}', 'danger')
    
    customers = Customer.query.filter_by(is_active=True).all()
    products = Product.query.filter_by(is_active=True).all()
    return render_template('create_invoice.html', customers=customers, products=products)

@invoice_bp.route('/view/<invoice_id>')
@login_required
def view_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    return render_template('view_invoice.html', invoice=invoice)

# ==================== INVENTORY ROUTES ====================

@inventory_bp.route('/list')
@login_required
def list_products():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    query = Product.query.filter_by(is_active=True)
    
    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f'%{search}%'),
                Product.sku.ilike(f'%{search}%')
            )
        )
    
    if category:
        query = query.filter_by(category=category)
    
    products = query.order_by(Product.name).paginate(page=page, per_page=20)
    categories = db.session.query(Product.category).distinct().all()
    
    return render_template('inventory.html', products=products, categories=categories, search=search, category=category)

@inventory_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            sku = request.form.get('sku')
            category = request.form.get('category')
            quantity = int(request.form.get('quantity', 0))
            cost_price = float(request.form.get('cost_price', 0))
            selling_price = float(request.form.get('selling_price', 0))
            
            # Check if SKU already exists
            if Product.query.filter_by(sku=sku).first():
                flash('SKU already exists', 'danger')
                return redirect(url_for('inventory.add_product'))
            
            product = Product(
                name=name,
                sku=sku,
                category=category,
                quantity=quantity,
                cost_price=cost_price,
                selling_price=selling_price,
                unit=request.form.get('unit', 'pieces'),
                description=request.form.get('description', ''),
                manufacturer=request.form.get('manufacturer', ''),
                batch_number=request.form.get('batch_number', '')
            )
            
            if request.form.get('expiry_date'):
                product.expiry_date = datetime.strptime(request.form.get('expiry_date'), '%Y-%m-%d')
            
            db.session.add(product)
            db.session.commit()
            
            flash(f'Product {name} added successfully', 'success')
            return redirect(url_for('inventory.list_products'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding product: {str(e)}', 'danger')
    
    return render_template('add_product.html')

# ==================== CUSTOMER ROUTES ====================

@customer_bp.route('/list')
@login_required
def list_customers():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Customer.query.filter_by(is_active=True)
    
    if search:
        query = query.filter(
            or_(
                Customer.name.ilike(f'%{search}%'),
                Customer.phone.ilike(f'%{search}%'),
                Customer.email.ilike(f'%{search}%')
            )
        )
    
    customers = query.order_by(Customer.name).paginate(page=page, per_page=20)
    return render_template('customers.html', customers=customers, search=search)

@customer_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            phone = request.form.get('phone')
            email = request.form.get('email')
            
            customer = Customer(
                name=name,
                phone=phone,
                email=email,
                address=request.form.get('address', ''),
                city=request.form.get('city', ''),
                state=request.form.get('state', ''),
                pincode=request.form.get('pincode', ''),
                gstin=request.form.get('gstin', ''),
                customer_type=request.form.get('customer_type', 'retail'),
                credit_limit=float(request.form.get('credit_limit', 0))
            )
            
            db.session.add(customer)
            db.session.commit()
            
            flash(f'Customer {name} added successfully', 'success')
            return redirect(url_for('customer.list_customers'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding customer: {str(e)}', 'danger')
    
    return render_template('add_customer.html')

# ==================== REPORT ROUTES ====================

@report_bp.route('/sales')
@login_required
def sales_report():
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    
    query = Invoice.query
    
    if from_date:
        from_date_obj = datetime.strptime(from_date, '%Y-%m-%d')
        query = query.filter(Invoice.created_at >= from_date_obj)
    
    if to_date:
        to_date_obj = datetime.strptime(to_date, '%Y-%m-%d') + timedelta(days=1)
        query = query.filter(Invoice.created_at < to_date_obj)
    
    invoices = query.order_by(Invoice.created_at.desc()).all()
    
    total_sales = sum(inv.total_amount for inv in invoices)
    total_items = sum(len(inv.items) for inv in invoices)
    
    return render_template('sales_report.html', invoices=invoices, total_sales=total_sales, total_items=total_items)

@report_bp.route('/inventory')
@login_required
def inventory_report():
    products = Product.query.all()
    
    low_stock = [p for p in products if p.is_low_stock()]
    expiring = [p for p in products if p.is_expired()]
    expiring_soon = [p for p in products if p.expiry_date and datetime.utcnow() < p.expiry_date < datetime.utcnow() + timedelta(days=30)]
    
    total_inventory_value = sum(p.quantity * p.cost_price for p in products)
    
    return render_template('inventory_report.html', 
                         products=products, 
                         low_stock=low_stock, 
                         expiring=expiring,
                         expiring_soon=expiring_soon,
                         total_value=total_inventory_value)
