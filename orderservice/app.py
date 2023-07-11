from flask import Flask, render_template, request
import csv
from collections import defaultdict

app = Flask(__name__)

def read_csv_file():
    orders = []
    with open('orders.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            orders.append(row)
    return orders

def compute_monthly_revenue(orders):
    monthly_revenue = defaultdict(float)
    for order in orders:
        order_date = order['order_date']
        revenue = float(order['product_price']) * int(order['quantity'])
        year_month = order_date[:7]
        monthly_revenue[year_month] += revenue
    return monthly_revenue

def compute_product_revenue(orders):
    product_revenue = defaultdict(float)
    for order in orders:
        revenue = float(order['product_price']) * int(order['quantity'])
        product_revenue[order['product_name']] += revenue
    return product_revenue

def compute_customer_revenue(orders):
    customer_revenue = defaultdict(float)
    for order in orders:
        revenue = float(order['product_price']) * int(order['quantity'])
        customer_revenue[order['customer_id']] += revenue
    return customer_revenue

def get_top_10_customers(customer_revenue):
    top_10_customers = sorted(customer_revenue.items(), key=lambda x: x[1], reverse=True)[:10]
    return top_10_customers

def test_revenue_calculations(orders):
    csv_file = 'orders.csv'

    # Test monthly revenue calculation
    monthly_revenue = compute_monthly_revenue(orders)
    assert monthly_revenue['2023-08'] == 157.87

    # Test product revenue calculation
    product_revenue = compute_product_revenue(orders)
    assert product_revenue['Product A'] == 296.73

    # Test customer revenue calculation
    customer_revenue = compute_customer_revenue(orders)
    assert customer_revenue['C101'] == 142.87


    return("All revenue calculations passed!")

@app.route('/orders', endpoint='orders', methods=["POST", "GET"])
@app.route('/test', endpoint='test', methods=["POST", "GET"])
def index():
    if request.endpoint == 'orders':
        orders = read_csv_file()
        monthly_revenue = compute_monthly_revenue(orders)
        product_revenue = compute_product_revenue(orders)
        customer_revenue = compute_customer_revenue(orders)
        top_10_customers = get_top_10_customers(customer_revenue)
        return render_template('index.html', monthly_revenue=monthly_revenue, product_revenue=product_revenue, customer_revenue=customer_revenue, top_10_customers=top_10_customers)
    elif request.endpoint == 'test':
         orders = read_csv_file()
         unit_tests = test_revenue_calculations(orders)
         return (unit_tests)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 83, debug=True)
