import pandas as pd
import os
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, create_tables, test_connection
from models import (
    DistributionCenter, Product, User, Order, OrderItem, InventoryItem
)

from sqlalchemy.exc import SQLAlchemyError

def parse_datetime(date_str):
    """Parse datetime string, return None if empty or invalid"""
    if pd.isna(date_str) or date_str == '' or date_str is None:
        return None
    try:
        return pd.to_datetime(date_str).to_pydatetime()
    except:
        return None

def load_distribution_centers(db: Session, csv_path: str):
    """Load distribution centers data"""
    print("📦 Loading distribution centers...")
    df = pd.read_csv(csv_path)
    
    centers = [
        DistributionCenter(
            id=int(row['id']),
            name=row['name'],
            latitude=float(row['latitude']) if pd.notna(row['latitude']) else None,
            longitude=float(row['longitude']) if pd.notna(row['longitude']) else None
        )
        for _, row in df.iterrows()
    ]
    try:
        db.bulk_save_objects(centers)
        db.commit()
        print(f"✅ Loaded {len(df)} distribution centers")
    except SQLAlchemyError as e:
        print(f"❌ Error loading distribution centers: {e}")
        db.rollback()

def load_products(db: Session, csv_path: str):
    """Load products data"""
    print("🛍️ Loading products...")
    df = pd.read_csv(csv_path)
    
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
        for _, row in df.iterrows()
    ]
    try:
        db.bulk_save_objects(products)
        db.commit()
        print(f"✅ Loaded {len(df)} products")
    except SQLAlchemyError as e:
        print(f"❌ Error loading products: {e}")
        db.rollback()

def load_users(db: Session, csv_path: str):
    """Load users data"""
    print("👥 Loading users...")
    df = pd.read_csv(csv_path)
    
    batch_size = 1000
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
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
            for _, row in batch.iterrows()
        ]
        try:
            db.bulk_save_objects(users)
            db.commit()
            print(f"✅ Loaded batch {i//batch_size + 1} ({min(i+batch_size, len(df))}/{len(df)} users)")
        except SQLAlchemyError as e:
            print(f"❌ Error loading users: {e}")
            db.rollback()
    
    print(f"✅ Loaded {len(df)} users")

def load_orders(db: Session, csv_path: str):
    """Load orders data, skipping orders with missing users for demo purposes."""
    print("📦 Loading orders...")
    df = pd.read_csv(csv_path)
    # Get all user IDs from the users table
    user_ids = set([u.id for u in db.query(User.id).all()])
    skipped = 0
    valid_orders = []
    for _, row in df.iterrows():
        if int(row['user_id']) not in user_ids:
            print(f"⚠️ Skipping order {row['order_id']} due to missing user_id {row['user_id']}")
            skipped += 1
            continue
        valid_orders.append(Order(
            order_id=int(row['order_id']),
            user_id=int(row['user_id']),
            status=row['status'],
            gender=row['gender'] if 'gender' in row else None,
            created_at=parse_datetime(row['created_at']),
            shipped_at=parse_datetime(row['shipped_at']),
            num_of_item=int(row['num_of_item']) if pd.notna(row['num_of_item']) else None
        ))
    try:
        db.bulk_save_objects(valid_orders)
        db.commit()
        print(f"✅ Loaded {len(valid_orders)} orders (skipped {skipped})")
    except SQLAlchemyError as e:
        print(f"❌ Error loading orders: {e}")
        db.rollback()

    """Load orders data"""
    print("📋 Loading orders...")
    df = pd.read_csv(csv_path)
    
    batch_size = 1000
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
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
            for _, row in batch.iterrows()
        ]
        try:
            db.bulk_save_objects(orders)
            db.commit()
            print(f"✅ Loaded batch {i//batch_size + 1} ({min(i+batch_size, len(df))}/{len(df)} orders)")
        except SQLAlchemyError as e:
            print(f"❌ Error loading orders: {e}")
            db.rollback()
    
    print(f"✅ Loaded {len(df)} orders")

def load_order_items(db: Session, csv_path: str):
    """Load order items data"""
    print("📦 Loading order items...")
    df = pd.read_csv(csv_path)
    
    batch_size = 1000
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        order_items = [
            OrderItem(
                id=int(row['id']),
                order_id=int(row['order_id']) if pd.notna(row['order_id']) else None,
                user_id=int(row['user_id']) if pd.notna(row['user_id']) else None,
                product_id=int(row['product_id']) if pd.notna(row['product_id']) else None,
                inventory_item_id=int(row['inventory_item_id']) if pd.notna(row['inventory_item_id']) else None,
                status=row['status'] if pd.notna(row['status']) else None,
                created_at=parse_datetime(row['created_at']),
                shipped_at=parse_datetime(row['shipped_at']),
                delivered_at=parse_datetime(row['delivered_at']),
                returned_at=parse_datetime(row['returned_at'])
            )
            for _, row in batch.iterrows()
        ]
        try:
            db.bulk_save_objects(order_items)
            db.commit()
            print(f"✅ Loaded batch {i//batch_size + 1} ({min(i+batch_size, len(df))}/{len(df)} order items)")
        except SQLAlchemyError as e:
            print(f"❌ Error loading order items: {e}")
            db.rollback()
    
    print(f"✅ Loaded {len(df)} order items")

def load_inventory_items(db: Session, csv_path: str):
    """Load inventory items data"""
    print("📊 Loading inventory items...")
    df = pd.read_csv(csv_path)
    
    batch_size = 1000
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        inventory_items = [
            InventoryItem(
                id=int(row['id']),
                product_id=int(row['product_id']) if pd.notna(row['product_id']) else None,
                created_at=parse_datetime(row['created_at']),
                sold_at=parse_datetime(row['sold_at']),
                cost=float(row['cost']) if pd.notna(row['cost']) else None,
                product_category=row['product_category'] if pd.notna(row['product_category']) else None,
                product_name=row['product_name'] if pd.notna(row['product_name']) else None,
                product_brand=row['product_brand'] if pd.notna(row['product_brand']) else None,
                product_retail_price=float(row['product_retail_price']) if pd.notna(row['product_retail_price']) else None,
                product_department=row['product_department'] if pd.notna(row['product_department']) else None,
                product_sku=row['product_sku'] if pd.notna(row['product_sku']) else None,
                product_distribution_center_id=int(row['product_distribution_center_id']) if pd.notna(row['product_distribution_center_id']) else None
            )
            for _, row in batch.iterrows()
        ]
        try:
            db.bulk_save_objects(inventory_items)
            db.commit()
            print(f"✅ Loaded batch {i//batch_size + 1} ({min(i+batch_size, len(df))}/{len(df)} inventory items)")
        except SQLAlchemyError as e:
            print(f"❌ Error loading inventory items: {e}")
            db.rollback()
    
    print(f"✅ Loaded {len(df)} inventory items")

def main():
    """Main function to load all data"""
    print("🚀 Starting data ingestion process...")
    
    # Test connection first
    if not test_connection():
        print("❌ Database connection failed. Please check your database configuration.")
        return
    
    # Drop all tables for a clean demo DB load
    from database import Base, engine
    Base.metadata.drop_all(bind=engine)
    create_tables()
    
    # Data directory
    # Use /data if running in Docker, else ../data for local
    if os.path.exists("/data"):
        data_dir = "/data"
    else:
        data_dir = os.path.join("..", "data")
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Load data in dependency order
        load_distribution_centers(db, os.path.join(data_dir, "distribution_centers.csv"))
        load_products(db, os.path.join(data_dir, "products.csv"))
        load_users(db, os.path.join(data_dir, "users.csv"))
        load_orders(db, os.path.join(data_dir, "orders.csv"))
        load_inventory_items(db, os.path.join(data_dir, "inventory_items.csv"))
        load_order_items(db, os.path.join(data_dir, "order_items.csv"))
        
        print("🎉 Data ingestion completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during data ingestion: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
