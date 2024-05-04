from app import db
from datetime import datetime

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))

    def __repr__(self):
        return f'<Employee {self.name}>'

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    orders = db.relationship('Order', backref='customer', lazy='dynamic')

    def __repr__(self):
        return f'<Customer {self.name}>'

class Part(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    def __repr__(self):
        return f'<Part {self.name}>'

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(64), index=True)
    model = db.Column(db.String(64), index=True)
    year = db.Column(db.Integer)
    vin = db.Column(db.String(17), unique=True)
    orders = db.relationship('Order', backref='car', lazy='dynamic')

    def __repr__(self):
        return f'<Car {self.make} {self.model}>'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    invoices = db.relationship('Invoice', backref='order', lazy='dynamic')

    def __repr__(self):
        return f'<Order {self.id}>'

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float)
    items = db.relationship('InvoiceItem', backref='invoice', lazy='dynamic')

    def __repr__(self):
        return f'<Invoice {self.id}>'

class InvoiceItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
    part_id = db.Column(db.Integer, db.ForeignKey('part.id'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)

    def __repr__(self):
        return f'<InvoiceItem {self.id}>'