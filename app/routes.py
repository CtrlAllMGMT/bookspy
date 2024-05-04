from flask import render_template, redirect, url_for, flash, request, jsonify
from app import app, db
from app.models import Employee, Customer, Part, Car, Order, Invoice, InvoiceItem
from app.forms import EmployeeForm, CustomerForm, PartForm, CarForm, OrderForm

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/employees', methods=['GET', 'POST'])
def employees():
    form = EmployeeForm()
    if form.validate_on_submit():
        employee = Employee(name=form.name.data, email=form.email.data,
                            phone=form.phone.data, address=form.address.data)
        db.session.add(employee)
        db.session.commit()
        flash('Employee added successfully', 'success')
        return redirect(url_for('employees'))
    employees = Employee.query.all()
    return render_template('employees.html', form=form, employees=employees)

@app.route('/customers', methods=['GET', 'POST'])
def customers():
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customer(name=form.name.data, email=form.email.data,
                            phone=form.phone.data, address=form.address.data)
        db.session.add(customer)
        db.session.commit()
        flash('Customer added successfully', 'success')
        return redirect(url_for('customers'))
    customers = Customer.query.all()
    return render_template('customers.html', form=form, customers=customers)

@app.route('/parts', methods=['GET', 'POST'])
def parts():
    form = PartForm()
    if form.validate_on_submit():
        part = Part(name=form.name.data, description=form.description.data,
                    price=form.price.data, quantity=form.quantity.data)
        db.session.add(part)
        db.session.commit()
        flash('Part added successfully', 'success')
        return redirect(url_for('parts'))
    parts = Part.query.all()
    return render_template('parts.html', form=form, parts=parts)

@app.route('/cars', methods=['GET', 'POST'])
def cars():
    form = CarForm()
    if form.validate_on_submit():
        car = Car(make=form.make.data, model=form.model.data,
                  year=form.year.data, vin=form.vin.data)
        db.session.add(car)
        db.session.commit()
        flash('Car added successfully', 'success')
        return redirect(url_for('cars'))
    cars = Car.query.all()
    return render_template('cars.html', form=form, cars=cars)

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    form = OrderForm()
    form.customer_id.choices = [(c.id, c.name) for c in Customer.query.all()]
    form.car_id.choices = [(c.id, f"{c.make} {c.model}") for c in Car.query.all()]
    if form.validate_on_submit():
        order = Order(customer_id=form.customer_id.data, car_id=form.car_id.data)
        db.session.add(order)
        db.session.commit()
        flash('Order created successfully', 'success')
        return redirect(url_for('orders'))
    orders = Order.query.all()
    return render_template('orders.html', form=form, orders=orders)

@app.route('/invoices', methods=['GET', 'POST'])
def invoices():
    form = OrderForm()
    form.order_id.choices = [(o.id, str(o.id)) for o in Order.query.all()]
    parts = Part.query.all()
    invoices = Invoice.query.all()

    if form.validate_on_submit():
        order = Order.query.get(form.order_id.data)
        invoice = Invoice(order=order)
        db.session.add(invoice)
        db.session.flush()  # Flush to get the new invoice ID

        for part_id, quantity in zip(request.form.getlist('parts[]'), request.form.getlist('quantities[]')):
            part = Part.query.get(part_id)
            invoice_item = InvoiceItem(invoice=invoice, part=part, quantity=quantity, price=part.price)
            db.session.add(invoice_item)

        db.session.commit()
        flash('Invoice created successfully', 'success')
        return redirect(url_for('invoices'))

    return render_template('invoices.html', form=form, parts=parts, invoices=invoices)

@app.route('/sales', methods=['GET', 'POST'])
def sales():
    form = OrderForm()
    form.customer_id.choices = [(c.id, c.name) for c in Customer.query.all()]
    form.car_id.choices = [(c.id, f"{c.make} {c.model}") for c in Car.query.all()]
    parts = Part.query.all()
    sales = Order.query.filter(Order.invoices.any()).all()

    if form.validate_on_submit():
        customer = Customer.query.get(form.customer_id.data)
        car = Car.query.get(form.car_id.data)
        order = Order(customer=customer, car=car)
        db.session.add(order)
        db.session.flush()  # Flush to get the new order ID

        for part_id, quantity in zip(request.form.getlist('parts[]'), request.form.getlist('quantities[]')):
            part = Part.query.get(part_id)
            if part.quantity >= quantity:
                part.quantity -= quantity
                invoice_item = InvoiceItem(order=order, part=part, quantity=quantity, price=part.price)
                db.session.add(invoice_item)
            else:
                flash(f'Not enough stock for {part.name}', 'danger')

        db.session.commit()
        flash('Sale completed successfully', 'success')
        return redirect(url_for('sales'))

    return render_template('sales.html', form=form, parts=parts, sales=sales)

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    form = PartForm()
    if form.validate_on_submit():
        part = Part(name=form.name.data, description=form.description.data,
                    price=form.price.data, quantity=form.quantity.data)
        db.session.add(part)
        db.session.commit()
        flash('Part added successfully', 'success')
        return redirect(url_for('inventory'))
    parts = Part.query.all()
    return render_template('inventory.html', form=form, parts=parts)

@app.route('/parts/<int:part_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_part(part_id):
    part = Part.query.get_or_404(part_id)

    if request.method == 'GET':
        return jsonify({
            'id': part.id,
            'name': part.name,
            'description': part.description,
            'price': part.price,
            'quantity': part.quantity
        })

    if request.method == 'PUT':
        data = request.form
        part.name = data.get('name')
        part.description = data.get('description')
        part.price = data.get('price')
        part.quantity = data.get('quantity')
        db.session.commit()
        return jsonify({
            'id': part.id,
            'name': part.name,
            'description': part.description,
            'price': part.price,
            'quantity': part.quantity
        })

    if request.method == 'DELETE':
        db.session.delete(part)
        db.session.commit()
        return jsonify({'message': 'Part deleted successfully'})