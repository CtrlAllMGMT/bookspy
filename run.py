from app import app, db
from app.models import Employee, Customer, Part, Car, Order, Invoice, InvoiceItem

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Employee': Employee, 'Customer': Customer,
            'Part': Part, 'Car': Car, 'Order': Order, 'Invoice': Invoice,
            'InvoiceItem': InvoiceItem}

if __name__ == '__main__':
    app.run(debug=True)