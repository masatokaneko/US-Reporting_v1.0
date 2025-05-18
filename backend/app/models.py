from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    department = Column(String)
    position = Column(String)
    phone = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    create_quote_permission = Column(Boolean, default=False)
    approve_quote_permission = Column(Boolean, default=False)
    manage_order_permission = Column(Boolean, default=False)
    create_invoice_permission = Column(Boolean, default=False)
    approve_invoice_permission = Column(Boolean, default=False)
    manage_revenue_permission = Column(Boolean, default=False)
    admin_permission = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Customer(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True, index=True)
    company_name = Column(String, index=True)
    contact_name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(JSON)
    billing_address = Column(JSON)
    payment_terms = Column(String)
    tax_id = Column(String)
    status = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, ForeignKey("users.id"))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, ForeignKey("users.id"))

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True)
    product_code = Column(String, unique=True, index=True)
    product_name = Column(String)
    description = Column(Text)
    category = Column(String)
    unit_price = Column(Float)
    tax_rate = Column(Float)
    unit = Column(String)
    minimum_quantity = Column(Integer)
    status = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, ForeignKey("users.id"))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, ForeignKey("users.id"))

class Quotation(Base):
    __tablename__ = "quotations"

    id = Column(String, primary_key=True, index=True)
    quotation_number = Column(String, unique=True, index=True)
    quotation_date = Column(DateTime)
    expiration_date = Column(DateTime)
    customer_id = Column(String, ForeignKey("customers.id"))
    subtotal = Column(Float)
    tax_amount = Column(Float)
    total_amount = Column(Float)
    status = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, ForeignKey("users.id"))
    approver_id = Column(String, ForeignKey("users.id"))
    approved_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, ForeignKey("users.id"))

    customer = relationship("Customer")
    items = relationship("QuotationItem", back_populates="quotation")

class QuotationItem(Base):
    __tablename__ = "quotation_items"

    id = Column(String, primary_key=True, index=True)
    quotation_id = Column(String, ForeignKey("quotations.id"))
    product_id = Column(String, ForeignKey("products.id"))
    quantity = Column(Integer)
    unit_price = Column(Float)
    subtotal = Column(Float)
    tax_rate = Column(Float)
    tax_amount = Column(Float)
    total_amount = Column(Float)
    description = Column(Text)
    sort_order = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    quotation = relationship("Quotation", back_populates="items")
    product = relationship("Product")

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(String, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, index=True)
    invoice_date = Column(DateTime)
    due_date = Column(DateTime)
    customer_id = Column(String, ForeignKey("customers.id"))
    subtotal = Column(Float)
    tax_amount = Column(Float)
    total_amount = Column(Float)
    status = Column(String)
    payment_status = Column(String)
    payment_terms = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, ForeignKey("users.id"))
    approver_id = Column(String, ForeignKey("users.id"))
    approved_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, ForeignKey("users.id"))

    customer = relationship("Customer")
    items = relationship("InvoiceItem", back_populates="invoice")
    payments = relationship("Payment", back_populates="invoice")

class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(String, primary_key=True, index=True)
    invoice_id = Column(String, ForeignKey("invoices.id"))
    product_id = Column(String, ForeignKey("products.id"))
    quantity = Column(Integer)
    unit_price = Column(Float)
    subtotal = Column(Float)
    tax_rate = Column(Float)
    tax_amount = Column(Float)
    total_amount = Column(Float)
    description = Column(Text)
    sort_order = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    invoice = relationship("Invoice", back_populates="items")
    product = relationship("Product")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, index=True)
    invoice_id = Column(String, ForeignKey("invoices.id"))
    payment_date = Column(DateTime)
    payment_amount = Column(Float)
    payment_method = Column(String)
    reference_number = Column(String)
    notes = Column(Text)
    payment_status = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, ForeignKey("users.id"))

    invoice = relationship("Invoice", back_populates="payments")

class TaxRate(Base):
    __tablename__ = "tax_rates"

    id = Column(String, primary_key=True, index=True)
    rate = Column(Float)
    name = Column(String)
    description = Column(Text)
    is_default = Column(Boolean, default=False)
    effective_from = Column(DateTime)
    effective_to = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, ForeignKey("users.id"))

class PaymentTerm(Base):
    __tablename__ = "payment_terms"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    days = Column(Integer)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, ForeignKey("users.id"))

class EmailTemplate(Base):
    __tablename__ = "email_templates"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)
    subject = Column(String)
    body = Column(Text)
    variables = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, ForeignKey("users.id"))

class SystemSetting(Base):
    __tablename__ = "system_settings"

    id = Column(String, primary_key=True, index=True)
    company = Column(JSON)
    invoice = Column(JSON)
    quotation = Column(JSON)
    email = Column(JSON)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, ForeignKey("users.id")) 