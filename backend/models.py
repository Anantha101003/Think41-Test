from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class DistributionCenter(Base):
    __tablename__ = "distribution_centers"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Relationships
    products = relationship("Product", back_populates="distribution_center")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    cost = Column(Float)
    category = Column(String(255))
    name = Column(String(255))
    brand = Column(String(255))
    retail_price = Column(Float)
    department = Column(String(255))
    sku = Column(String(255), unique=True)
    distribution_center_id = Column(Integer, ForeignKey('distribution_centers.id'))
    
    # Relationships
    distribution_center = relationship("DistributionCenter", back_populates="products")
    inventory_items = relationship("InventoryItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), unique=True)
    age = Column(Integer)
    gender = Column(String(50))
    state = Column(String(255))
    street_address = Column(String(500))
    postal_code = Column(String(50))
    city = Column(String(255))
    country = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    traffic_source = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = relationship("Order", back_populates="user")
    order_items = relationship("OrderItem", back_populates="user")

class Order(Base):
    __tablename__ = "orders"
    
    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String(255))
    gender = Column(String(50))
    created_at = Column(DateTime)
    returned_at = Column(DateTime)
    shipped_at = Column(DateTime)
    delivered_at = Column(DateTime)
    num_of_item = Column(Integer)
    
    # Relationships
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    inventory_item_id = Column(Integer, ForeignKey('inventory_items.id'))
    status = Column(String(255))
    created_at = Column(DateTime)
    shipped_at = Column(DateTime)
    delivered_at = Column(DateTime)
    returned_at = Column(DateTime)
    
    # Relationships
    order = relationship("Order", back_populates="order_items")
    user = relationship("User", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
    inventory_item = relationship("InventoryItem", back_populates="order_items")

class InventoryItem(Base):
    __tablename__ = "inventory_items"
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    created_at = Column(DateTime)
    sold_at = Column(DateTime)
    cost = Column(Float)
    product_category = Column(String(255))
    product_name = Column(String(255))
    product_brand = Column(String(255))
    product_retail_price = Column(Float)
    product_department = Column(String(255))
    product_sku = Column(String(255))
    product_distribution_center_id = Column(Integer)
    
    # Relationships
    product = relationship("Product", back_populates="inventory_items")
    order_items = relationship("OrderItem", back_populates="inventory_item")

# Models for conversation history
class ConversationSession(Base):
    __tablename__ = "conversation_sessions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), nullable=False)  # Can be a session ID or user identifier
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    messages = relationship("ConversationMessage", back_populates="session", cascade="all, delete-orphan")

class ConversationMessage(Base):
    __tablename__ = "conversation_messages"
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('conversation_sessions.id'), nullable=False)
    role = Column(String(50), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship("ConversationSession", back_populates="messages")
