from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

# Biến toàn cục để lưu thông tin đăng nhập
session_data = {}

# Login
def login(shopname, username, password):
    SHOPNAME_URL = f"https://{shopname}.pos365.vn"
    url = f"{SHOPNAME_URL}/api/auth/credentials?format=json&Username={username}&Password={password}"
    response = requests.get(url)
    if response.status_code == 200:
        session_id = response.json().get("SessionId")
        return SHOPNAME_URL, session_id
    return None, None

# Get branches
def get_branchs(SHOPNAME_URL, session_id):
    url = f"{SHOPNAME_URL}/api/branchs?format=json"
    headers = {"Cookie": f"ss-id={session_id}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("results")
    return []

# Get orders
def get_orders(SHOPNAME_URL, session_id, branch_id):
    list_orders = []
    page_size = 100
    skip = 0
    while True:
        url = f"{SHOPNAME_URL}/api/orders?format=json&$top={page_size}&$skip={skip}"
        headers = {"Cookie": f"ss-id={session_id}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            orders = response.json().get("results")
            for order in orders:
                if order["BranchId"] == branch_id:
                    list_orders.append(order["Id"])
            if len(orders) < page_size:
                break
            skip += page_size
        else:
            break
    return list_orders

# Delete order
def delete_order(SHOPNAME_URL, session_id, order_id):
    url = f"{SHOPNAME_URL}/api/orders/{order_id}/void"
    headers = {"Cookie": f"ss-id={session_id}"}
    requests.delete(url, headers=headers)
    url = f"{SHOPNAME_URL}/api/orders/{order_id}"
    response = requests.delete(url, headers=headers)
    return response.status_code == 200

# Các hàm khác (orderstocks, inventorycountings, accountingtransactions, products, customers, suppliers, categories)
# Tương tự như get_orders và delete_order, tôi sẽ thêm một ví dụ cho products:
def get_products(SHOPNAME_URL, session_id):
    list_products = []
    page_size = 100
    skip = 0
    while True:
        url = f"{SHOPNAME_URL}/api/products?format=json&$top={page_size}&$skip={skip}"
        headers = {"Cookie": f"ss-id={session_id}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            products = response.json().get("results")
            for product in products:
                list_products.append(product["Id"])
            if len(products) < page_size:
                break
            skip += page_size
        else:
            break
    return list_products

def delete_product(SHOPNAME_URL, session_id, product_id):
    url = f"{SHOPNAME_URL}/api/products/{product_id}"
    headers = {"Cookie": f"ss-id={session_id}"}
    response = requests.delete(url, headers=headers)
    return response.status_code == 200

# Routes
@app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        shopname = request.form['shopname']
        username = request.form['username']
        password = request.form['password']
        SHOPNAME_URL, session_id = login(shopname, username, password)
        if session_id:
            session_data['SHOPNAME_URL'] = SHOPNAME_URL
            session_data['session_id'] = session_id
            branches = get_branchs(SHOPNAME_URL, session_id)
            return render_template('menu.html', branches=branches)
        return "Login failed! Please try again."
    return render_template('login.html')

@app.route('/menu', methods=['POST'])
def menu_action():
    action = request.form['action']
    branch_id = request.form.get('branch_id')
    SHOPNAME_URL = session_data.get('SHOPNAME_URL')
    session_id = session_data.get('session_id')
    
    if action == "delete_orders" and branch_id:
        orders = get_orders(SHOPNAME_URL, session_id, int(branch_id))
        for order_id in orders:
            delete_order(SHOPNAME_URL, session_id, order_id)
        return jsonify({"message": f"Deleted {len(orders)} orders"})
    elif action == "delete_products":
        products = get_products(SHOPNAME_URL, session_id)
        for product_id in products:
            delete_product(SHOPNAME_URL, session_id, product_id)
        return jsonify({"message": f"Deleted {len(products)} products"})
    # Thêm các hành động khác tương tự (orderstocks, inventorycountings, v.v.)
    return jsonify({"message": "Action completed"})

if __name__ == '__main__':
    app.run(debug=True)
