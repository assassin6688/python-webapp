from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

# Biến toàn cục để lưu thông tin đăng nhập
session_data = {}

# Hàm login
def login(shopname, username, password):
    SHOPNAME_URL = f"https://{shopname}.pos365.vn"
    url = f"{SHOPNAME_URL}/api/auth/credentials?format=json&Username={username}&Password={password}"
    response = requests.get(url)
    if response.status_code == 200:
        session_id = response.json().get("SessionId")
        return SHOPNAME_URL, session_id
    return None, None

# Hàm get branches
def get_branchs(SHOPNAME_URL, session_id):
    url = f"{SHOPNAME_URL}/api/branchs?format=json"
    headers = {"Cookie": f"ss-id={session_id}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("results")
    return []

# Hàm get và delete cho từng loại dữ liệu
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

def delete_order(SHOPNAME_URL, session_id, order_id):
    url = f"{SHOPNAME_URL}/api/orders/{order_id}/void"
    headers = {"Cookie": f"ss-id={session_id}"}
    requests.delete(url, headers=headers)
    url = f"{SHOPNAME_URL}/api/orders/{order_id}"
    response = requests.delete(url, headers=headers)
    return response.status_code == 200

def get_orderstocks(SHOPNAME_URL, session_id, branch_id):
    list_orderstocks = []
    page_size = 100
    skip = 0
    while True:
        url = f"{SHOPNAME_URL}/api/orderstock?format=json&$top={page_size}&$skip={skip}"
        headers = {"Cookie": f"ss-id={session_id}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            orderstocks = response.json().get("results")
            for orderstock in orderstocks:
                if orderstock["BranchId"] == branch_id:
                    list_orderstocks.append(orderstock["Id"])
            if len(orderstocks) < page_size:
                break
            skip += page_size
        else:
            break
    return list_orderstocks

def delete_orderstock(SHOPNAME_URL, session_id, orderstock_id):
    url = f"{SHOPNAME_URL}/api/orderstock/{orderstock_id}/void"
    headers = {"Cookie": f"ss-id={session_id}"}
    requests.delete(url, headers=headers)
    url = f"{SHOPNAME_URL}/api/orderstock/{orderstock_id}"
    response = requests.delete(url, headers=headers)
    return response.status_code == 200

def get_inventorycountings(SHOPNAME_URL, session_id, branch_id):
    list_inventorycountings = []
    page_size = 100
    skip = 0
    while True:
        url = f"{SHOPNAME_URL}/api/inventorycount?format=json&$top={page_size}&$skip={skip}"
        headers = {"Cookie": f"ss-id={session_id}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            inventorycountings = response.json().get("results")
            for inventorycounting in inventorycountings:
                if inventorycounting["BranchId"] == branch_id:
                    list_inventorycountings.append(inventorycounting["Id"])
            if len(inventorycountings) < page_size:
                break
            skip += page_size
        else:
            break
    return list_inventorycountings

def delete_inventorycounting(SHOPNAME_URL, session_id, inventorycounting_id):
    url = f"{SHOPNAME_URL}/api/inventorycount/{inventorycounting_id}/void"
    headers = {"Cookie": f"ss-id={session_id}"}
    requests.delete(url, headers=headers)
    url = f"{SHOPNAME_URL}/api/inventorycount/{inventorycounting_id}"
    response = requests.delete(url, headers=headers)
    return response.status_code == 200

def get_accountingtransactions(SHOPNAME_URL, session_id):
    list_accountingtransactions = []
    page_size = 100
    skip = 0
    while True:
        url = f"{SHOPNAME_URL}/api/accountingtransaction?format=json&$top={page_size}&$skip={skip}"
        headers = {"Cookie": f"ss-id={session_id}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            accountingtransactions = response.json().get("results")
            for accountingtransaction in accountingtransactions:
                list_accountingtransactions.append(accountingtransaction["Id"])
            if len(accountingtransactions) < page_size:
                break
            skip += page_size
        else:
            break
    return list_accountingtransactions

def delete_accountingtransaction(SHOPNAME_URL, session_id, accountingtransaction_id):
    url = f"{SHOPNAME_URL}/api/accountingtransaction/{accountingtransaction_id}/void"
    headers = {"Cookie": f"ss-id={session_id}"}
    response = requests.delete(url, headers=headers)
    return response.status_code == 200

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

def get_customers(SHOPNAME_URL, session_id):
    list_customers = []
    page_size = 100
    skip = 0
    while True:
        url = f"{SHOPNAME_URL}/api/partners?format=json&Type=1&$top={page_size}&$skip={skip}"
        headers = {"Cookie": f"ss-id={session_id}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            customers = response.json().get("results")
            for customer in customers:
                list_customers.append(customer["Id"])
            if len(customers) < page_size:
                break
            skip += page_size
        else:
            break
    return list_customers

def delete_customer(SHOPNAME_URL, session_id, customer_id):
    url = f"{SHOPNAME_URL}/api/partners/{customer_id}?format=json&Type=1"
    headers = {"Cookie": f"ss-id={session_id}"}
    response = requests.delete(url, headers=headers)
    return response.status_code == 200

def get_suppliers(SHOPNAME_URL, session_id):
    list_suppliers = []
    page_size = 100
    skip = 0
    while True:
        url = f"{SHOPNAME_URL}/api/partners?format=json&Type=2&$top={page_size}&$skip={skip}"
        headers = {"Cookie": f"ss-id={session_id}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            suppliers = response.json().get("results")
            for supplier in suppliers:
                list_suppliers.append(supplier["Id"])
            if len(suppliers) < page_size:
                break
            skip += page_size
        else:
            break
    return list_suppliers

def delete_supplier(SHOPNAME_URL, session_id, supplier_id):
    url = f"{SHOPNAME_URL}/api/partners/{supplier_id}?format=json&Type=2"
    headers = {"Cookie": f"ss-id={session_id}"}
    response = requests.delete(url, headers=headers)
    return response.status_code == 200

def get_categories(SHOPNAME_URL, session_id):
    list_categories = []
    page_size = 100
    skip = 0
    while True:
        url = f"{SHOPNAME_URL}/api/categories?format=json&$top={page_size}&$skip={skip}"
        headers = {"Cookie": f"ss-id={session_id}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            categories = response.json().get("results")
            for category in categories:
                list_categories.append(category["Id"])
            if len(categories) < page_size:
                break
            skip += page_size
        else:
            break
    return list_categories

def delete_category(SHOPNAME_URL, session_id, category_id):
    url = f"{SHOPNAME_URL}/api/categories/{category_id}"
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
        items = get_orders(SHOPNAME_URL, session_id, int(branch_id))
        for item_id in items:
            delete_order(SHOPNAME_URL, session_id, item_id)
        return jsonify({"message": f"Deleted {len(items)} orders"})
    elif action == "delete_orderstocks" and branch_id:
        items = get_orderstocks(SHOPNAME_URL, session_id, int(branch_id))
        for item_id in items:
            delete_orderstock(SHOPNAME_URL, session_id, item_id)
        return jsonify({"message": f"Deleted {len(items)} orderstocks"})
    elif action == "delete_inventorycountings" and branch_id:
        items = get_inventorycountings(SHOPNAME_URL, session_id, int(branch_id))
        for item_id in items:
            delete_inventorycounting(SHOPNAME_URL, session_id, item_id)
        return jsonify({"message": f"Deleted {len(items)} inventorycountings"})
    elif action == "delete_accountingtransactions":
        items = get_accountingtransactions(SHOPNAME_URL, session_id)
        for item_id in items:
            delete_accountingtransaction(SHOPNAME_URL, session_id, item_id)
        return jsonify({"message": f"Deleted {len(items)} accountingtransactions"})
    elif action == "delete_products":
        items = get_products(SHOPNAME_URL, session_id)
        for item_id in items:
            delete_product(SHOPNAME_URL, session_id, item_id)
        return jsonify({"message": f"Deleted {len(items)} products"})
    elif action == "delete_customers":
        items = get_customers(SHOPNAME_URL, session_id)
        for item_id in items:
            delete_customer(SHOPNAME_URL, session_id, item_id)
        return jsonify({"message": f"Deleted {len(items)} customers"})
    elif action == "delete_suppliers":
        items = get_suppliers(SHOPNAME_URL, session_id)
        for item_id in items:
            delete_supplier(SHOPNAME_URL, session_id, item_id)
        return jsonify({"message": f"Deleted {len(items)} suppliers"})
    elif action == "delete_categories":
        items = get_categories(SHOPNAME_URL, session_id)
        for item_id in items:
            delete_category(SHOPNAME_URL, session_id, item_id)
        return jsonify({"message": f"Deleted {len(items)} categories"})
    return jsonify({"message": "Invalid action or missing branch_id"})

if __name__ == '__main__':
    app.run(debug=True)
