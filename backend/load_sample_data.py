import pandas as pd
import os
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, create_tables, test_connection
from models import (
    DistributionCenter, Product, User, Order, OrderItem, InventoryItem
)

def parse_datetime(date_str):
    """Parse datetime string, return None if empty or invalid"""
    if pd.isna(date_str) or date_str == '' or date_str is None:
        return None
    try:
        return pd.to_datetime(date_str).to_pydatetime()
    except:
        return None

def load_sample_data():
    """Load a sample of data to demonstrate functionality"""
    print("🚀 Loading sample data for demonstration...")
    
    # Test connection first
    if not test_connection():
        print("❌ Database connection failed. Please check your database configuration.")
        return
    
    # Create tables
    create_tables()
    
    # Data directory
    data_dir = os.path.join("..", "data")
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Load distribution centers (small file)
        print("📦 Loading distribution centers...")
        df = pd.read_csv(os.path.join(data_dir, "distribution_centers.csv"))
        centers = [
            DistributionCenter(
                id=int(row['id']),
                name=row['name'],
                latitude=float(row['latitude']) if pd.notna(row['latitude']) else None,
                longitude=float(row['longitude']) if pd.notna(row['longitude']) else None
            )
            for _, row in df.iterrows()
        ]
        db.bulk_save_objects(centers)
        db.commit()
        print(f"✅ Loaded {len(df)} distribution centers")

        # Load products (sample first 1000)
        print("🛍️ Loading sample products...")
        df = pd.read_csv(os.path.join(data_dir, "products.csv"))
        sample_df = df.head(1000)  # Take first 1000 products
        products = [
            Product(
                id=int(row['id']),
                cost=float(row['cost']) if pd.notna(row['cost']) else None,
                category=row['category'] if pd.notna(row['category']) else None,
                name=row['name'] if pd.notna(row['name']) else None,
                brand=row['brand'] if pd.notna(row['brand']) else None,
                retail_price=float(row['retail_price']) if pd.notna(row['retail_price']) else None,
                department=row['department'] if pd.notna(row['department']) else None,
                sku=row['sku'] if pd.notna(row['sku']) else None,
                distribution_center_id=int(row['distribution_center_id']) if pd.notna(row['distribution_center_id']) else None
            )
            for _, row in sample_df.iterrows()
        ]
        db.bulk_save_objects(products)
        db.commit()
        print(f"✅ Loaded {len(sample_df)} sample products")

        # Load users (sample first 1000)
        print("👥 Loading sample users...")
        df = pd.read_csv(os.path.join(data_dir, "users.csv"))
        sample_df = df.head(1000)  # Take first 1000 users
        users = [
            User(
                id=int(row['id']),
                first_name=row['first_name'] if pd.notna(row['first_name']) else None,
                last_name=row['last_name'] if pd.notna(row['last_name']) else None,
                email=row['email'] if pd.notna(row['email']) else None,
                age=int(row['age']) if pd.notna(row['age']) else None,
                gender=row['gender'] if pd.notna(row['gender']) else None,
                state=row['state'] if pd.notna(row['state']) else None,
                street_address=row['street_address'] if pd.notna(row['street_address']) else None,
                postal_code=row['postal_code'] if pd.notna(row['postal_code']) else None,
                city=row['city'] if pd.notna(row['city']) else None,
                country=row['country'] if pd.notna(row['country']) else None,
                latitude=float(row['latitude']) if pd.notna(row['latitude']) else None,
                longitude=float(row['longitude']) if pd.notna(row['longitude']) else None,
                traffic_source=row['traffic_source'] if pd.notna(row['traffic_source']) else None,
                created_at=parse_datetime(row['created_at'])
            )
            for _, row in sample_df.iterrows()
        ]
        db.bulk_save_objects(users)
        db.commit()
        print(f"✅ Loaded {len(sample_df)} sample users")

        # Load orders (sample first 1000)
        print("📋 Loading sample orders...")
        df = pd.read_csv(os.path.join(data_dir, "orders.csv"))
        sample_df = df.head(1000)  # Take first 1000 orders
        orders = [
            Order(
                order_id=int(row['order_id']),
                user_id=int(row['user_id']) if pd.notna(row['user_id']) else None,
                status=row['status'] if pd.notna(row['status']) else None,
                gender=row['gender'] if pd.notna(row['gender']) else None,
                created_at=parse_datetime(row['created_at']),
                returned_at=parse_datetime(row['returned_at']),
                shipped_at=parse_datetime(row['shipped_at']),
                delivered_at=parse_datetime(row['delivered_at']),
                num_of_item=int(row['num_of_item']) if pd.notna(row['num_of_item']) else None
            )
            for _, row in sample_df.iterrows()
        ]
        db.bulk_save_objects(orders)
        db.commit()
        print(f"✅ Loaded {len(sample_df)} sample orders")

        print("🎉 Sample data loading completed successfully!")
        print("\n📊 Database Summary:")
        print(f"  - Distribution Centers: {db.query(DistributionCenter).count()}")
        print(f"  - Products: {db.query(Product).count()}")
        print(f"  - Users: {db.query(User).count()}")
        print(f"  - Orders: {db.query(Order).count()}")
        
    except Exception as e:
        print(f"❌ Error during data loading: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    load_sample_data()
