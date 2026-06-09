from app import db
from app.models import User, Product, Customer, Invoice, InvoiceItem, Transaction, StockAdjustment
from datetime import datetime
import shutil
import os

class DatabaseManager:
    
    @staticmethod
    def initialize_database():
        """Initialize database with default data"""
        try:
            # Create tables
            db.create_all()
            
            # Check if admin user exists
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@medicalstore.com',
                    role='admin',
                    is_active=True
                )
                admin.set_password('admin')
                db.session.add(admin)
            
            db.session.commit()
            return True
        except Exception as e:
            print(f"Database initialization error: {str(e)}")
            return False
    
    @staticmethod
    def backup_database(backup_path=None):
        """Create a backup of the database"""
        try:
            if backup_path is None:
                backup_path = f'backups/medical_store_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
            
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            shutil.copy('instance/medical_store.db', backup_path)
            return True, backup_path
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def restore_database(backup_path):
        """Restore database from backup"""
        try:
            shutil.copy(backup_path, 'instance/medical_store.db')
            return True, "Database restored successfully"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_dashboard_stats():
        """Get dashboard statistics"""
        try:
            total_products = Product.query.count()
            total_customers = Customer.query.count()
            total_invoices = Invoice.query.count()
            
            # Today's sales
            from sqlalchemy import func, and_
            today = datetime.utcnow().date()
            today_sales = db.session.query(func.sum(Invoice.total_amount)).filter(
                func.date(Invoice.created_at) == today
            ).scalar() or 0
            
            # Low stock items
            low_stock = Product.query.filter(Product.quantity <= 10, Product.is_active == True).count()
            
            # Expiring items (next 30 days)
            from datetime import timedelta
            expiry_date_limit = datetime.utcnow() + timedelta(days=30)
            expiring = Product.query.filter(
                and_(
                    Product.expiry_date <= expiry_date_limit,
                    Product.expiry_date >= datetime.utcnow(),
                    Product.is_active == True
                )
            ).count()
            
            return {
                'total_products': total_products,
                'total_customers': total_customers,
                'total_invoices': total_invoices,
                'today_sales': today_sales,
                'low_stock_items': low_stock,
                'expiring_items': expiring
            }
        except Exception as e:
            print(f"Error getting dashboard stats: {str(e)}")
            return {}
    
    @staticmethod
    def export_to_csv(model, filename):
        """Export data to CSV"""
        try:
            import csv
            from datetime import datetime
            
            filename = f"exports/{model.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            os.makedirs('exports', exist_ok=True)
            
            data = model.query.all()
            if not data:
                return False, "No data to export"
            
            # Get column names
            columns = [col.name for col in model.__table__.columns]
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                
                for row in data:
                    writer.writerow([getattr(row, col) for col in columns])
            
            return True, filename
        except Exception as e:
            return False, str(e)
