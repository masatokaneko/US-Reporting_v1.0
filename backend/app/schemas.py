from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# Base schemas
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    department: Optional[str] = None
    position: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = True
    create_quote_permission: bool = False
    approve_quote_permission: bool = False
    manage_order_permission: bool = False
    create_invoice_permission: bool = False
    approve_invoice_permission: bool = False
    manage_revenue_permission: bool = False
    admin_permission: bool = False

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None
    create_quote_permission: Optional[bool] = None
    approve_quote_permission: Optional[bool] = None
    manage_order_permission: Optional[bool] = None
    create_invoice_permission: Optional[bool] = None
    approve_invoice_permission: Optional[bool] = None
    manage_revenue_permission: Optional[bool] = None
    admin_permission: Optional[bool] = None

class User(UserBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Customer schemas
class Address(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: str

class CustomerBase(BaseModel):
    company_name: str
    contact_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[Address] = None
    billing_address: Optional[Address] = None
    payment_terms: Optional[str] = None
    tax_id: Optional[str] = None
    status: str = "active"
    notes: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    company_name: Optional[str] = None
    contact_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[Address] = None
    billing_address: Optional[Address] = None
    payment_terms: Optional[str] = None
    tax_id: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class Customer(CustomerBase):
    id: str
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None

    class Config:
        orm_mode = True

# Product schemas
class ProductBase(BaseModel):
    product_code: str
    product_name: str
    description: Optional[str] = None
    category: Optional[str] = None
    unit_price: float
    tax_rate: float
    unit: str
    minimum_quantity: int = 1
    status: str = "active"
    notes: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    product_code: Optional[str] = None
    product_name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    unit_price: Optional[float] = None
    tax_rate: Optional[float] = None
    unit: Optional[str] = None
    minimum_quantity: Optional[int] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class Product(ProductBase):
    id: str
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None

    class Config:
        orm_mode = True

# Quotation schemas
class QuotationItemBase(BaseModel):
    product_id: str
    quantity: int
    unit_price: float
    description: Optional[str] = None
    sort_order: int = 0

class QuotationItemCreate(QuotationItemBase):
    pass

class QuotationItem(QuotationItemBase):
    id: str
    quotation_id: str
    subtotal: float
    tax_rate: float
    tax_amount: float
    total_amount: float
    created_at: datetime

    class Config:
        orm_mode = True

class QuotationBase(BaseModel):
    quotation_date: datetime
    expiration_date: datetime
    customer_id: str
    notes: Optional[str] = None

class QuotationCreate(QuotationBase):
    items: List[QuotationItemCreate]

class QuotationUpdate(BaseModel):
    quotation_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    customer_id: Optional[str] = None
    notes: Optional[str] = None
    items: Optional[List[QuotationItemCreate]] = None

class Quotation(QuotationBase):
    id: str
    quotation_number: str
    subtotal: float
    tax_amount: float
    total_amount: float
    status: str
    created_at: datetime
    created_by: str
    approver_id: Optional[str] = None
    approved_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None
    items: List[QuotationItem]
    customer: Customer

    class Config:
        orm_mode = True

# Invoice schemas
class InvoiceItemBase(BaseModel):
    product_id: str
    quantity: int
    unit_price: float
    description: Optional[str] = None
    sort_order: int = 0

class InvoiceItemCreate(InvoiceItemBase):
    pass

class InvoiceItem(InvoiceItemBase):
    id: str
    invoice_id: str
    subtotal: float
    tax_rate: float
    tax_amount: float
    total_amount: float
    created_at: datetime

    class Config:
        orm_mode = True

class PaymentBase(BaseModel):
    payment_date: datetime
    payment_amount: float
    payment_method: str
    reference_number: Optional[str] = None
    notes: Optional[str] = None

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: str
    invoice_id: str
    payment_status: str
    created_at: datetime
    created_by: str

    class Config:
        orm_mode = True

class InvoiceBase(BaseModel):
    invoice_date: datetime
    due_date: datetime
    customer_id: str
    payment_terms: Optional[str] = None
    notes: Optional[str] = None

class InvoiceCreate(InvoiceBase):
    items: List[InvoiceItemCreate]

class InvoiceUpdate(BaseModel):
    invoice_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    customer_id: Optional[str] = None
    payment_terms: Optional[str] = None
    notes: Optional[str] = None
    items: Optional[List[InvoiceItemCreate]] = None

class Invoice(InvoiceBase):
    id: str
    invoice_number: str
    subtotal: float
    tax_amount: float
    total_amount: float
    status: str
    payment_status: str
    created_at: datetime
    created_by: str
    approver_id: Optional[str] = None
    approved_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None
    items: List[InvoiceItem]
    payments: List[Payment]
    customer: Customer

    class Config:
        orm_mode = True

# Tax Rate schemas
class TaxRateBase(BaseModel):
    rate: float
    name: str
    description: Optional[str] = None
    is_default: bool = False
    effective_from: datetime
    effective_to: Optional[datetime] = None

class TaxRateCreate(TaxRateBase):
    pass

class TaxRateUpdate(BaseModel):
    rate: Optional[float] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_default: Optional[bool] = None
    effective_from: Optional[datetime] = None
    effective_to: Optional[datetime] = None

class TaxRate(TaxRateBase):
    id: str
    created_at: datetime
    created_by: str

    class Config:
        orm_mode = True

# Payment Term schemas
class PaymentTermBase(BaseModel):
    name: str
    description: Optional[str] = None
    days: int
    is_default: bool = False

class PaymentTermCreate(PaymentTermBase):
    pass

class PaymentTermUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    days: Optional[int] = None
    is_default: Optional[bool] = None

class PaymentTerm(PaymentTermBase):
    id: str
    created_at: datetime
    created_by: str

    class Config:
        orm_mode = True

# Email Template schemas
class EmailTemplateBase(BaseModel):
    name: str
    type: str
    subject: str
    body: str
    variables: Optional[Dict[str, Any]] = None

class EmailTemplateCreate(EmailTemplateBase):
    pass

class EmailTemplateUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    variables: Optional[Dict[str, Any]] = None

class EmailTemplate(EmailTemplateBase):
    id: str
    created_at: datetime
    created_by: str

    class Config:
        orm_mode = True

# System Setting schemas
class CompanySettings(BaseModel):
    name: str
    address: Address
    phone: str
    email: EmailStr
    website: Optional[str] = None
    tax_id: Optional[str] = None
    logo_url: Optional[str] = None

class InvoiceSettings(BaseModel):
    prefix: str
    next_number: int
    default_payment_terms: str
    default_tax_rate: float
    notes_template: Optional[str] = None

class QuotationSettings(BaseModel):
    prefix: str
    next_number: int
    default_expiration_days: int
    default_tax_rate: float
    notes_template: Optional[str] = None

class EmailSettings(BaseModel):
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    from_email: EmailStr
    from_name: str
    use_ssl: bool = True

class SystemSettingBase(BaseModel):
    company: CompanySettings
    invoice: InvoiceSettings
    quotation: QuotationSettings
    email: EmailSettings

class SystemSettingCreate(SystemSettingBase):
    pass

class SystemSettingUpdate(BaseModel):
    company: Optional[CompanySettings] = None
    invoice: Optional[InvoiceSettings] = None
    quotation: Optional[QuotationSettings] = None
    email: Optional[EmailSettings] = None

class SystemSetting(SystemSettingBase):
    id: str
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None

    class Config:
        orm_mode = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None 