"""Seeded dataset generator. Usage: python3 gen_data.py [sqlite|postgres|mysql|all]. Output: data/<dialect>/<dataset>.sql"""
import random, sys, os
from datetime import date, timedelta
DIALECTS = {
 'sqlite':   dict(i='INTEGER', t='TEXT', r='REAL', pk='INTEGER PRIMARY KEY'),
 'postgres': dict(i='INTEGER', t='TEXT', r='NUMERIC(12,2)', pk='INTEGER PRIMARY KEY'),
 'mysql':    dict(i='INT', t='VARCHAR(100)', r='DECIMAL(12,2)', pk='INT PRIMARY KEY')}
def q(v):
    if v is None: return 'NULL'
    if isinstance(v, str): return "'" + v.replace("'", "''") + "'"
    return str(v)
def d(n, base=date(2023, 1, 1)): return (base + timedelta(days=n)).isoformat()
def build(dial):
    T = DIALECTS[dial]; R = random.Random(42)
    def tbl(name, cols, rows):
        s = "CREATE TABLE %s (\n  %s\n);\n" % (name, ",\n  ".join(cols).format(**T))
        for k in range(0, len(rows), 100):
            s += "INSERT INTO %s VALUES\n" % name + ",\n".join("(" + ",".join(q(x) for x in r) + ")" for r in rows[k:k+100]) + ";\n"
        return s
    first = ['Aarav','Priya','Rohan','Sana','Vikram','Neha','Arjun','Isha','Kabir','Meera','Zoya','Dev']
    last = ['Sharma','Khan','Patel','Iyer','Singh','Das','Mehta','Nair','Joshi','Shah']
    cities = ['Mumbai','Delhi','Pune','Chennai','Kolkata','Bengaluru','Hyderabad','Jaipur']
    out = {}
    # company
    emp = [(i, R.choice(first) + ' ' + R.choice(last), (i % 4) + 1, R.randint(30000, 99000), d(R.randint(0, 1500), date(2018, 1, 1))) for i in range(1, 301)]
    out['company'] = tbl('departments', ['dept_id {pk}', 'dept_name {t} NOT NULL'], [(1,'Sales'),(2,'Engineering'),(3,'HR'),(4,'Finance')]) + \
        tbl('employees', ['emp_id {pk}', 'name {t} NOT NULL', 'dept_id {i}', 'salary {r}', 'hire_date {t}', 'FOREIGN KEY (dept_id) REFERENCES departments(dept_id)'], emp)
    # ecommerce
    cats = ['Electronics','Books','Clothing','Home','Toys','Sports','Beauty','Grocery']
    prods = []
    for i in range(1, 61):
        p = round(R.uniform(99, 4999), 2); prods.append((i, 'Product %d' % i, (i % 8) + 1, (i % 15) + 1, p, round(p * R.uniform(.5, .85), 2)))
    custs = [(i, R.choice(first) + ' ' + R.choice(last), 'user%d@example.com' % i, R.choice(cities), d(R.randint(0, 700))) for i in range(1, 201)]
    orders, items, pays = [], [], []; iid = 0
    for o in range(1, 801):
        od = R.randint(0, 729); st = R.choices(['Delivered','Shipped','Cancelled','Pending'], [60, 15, 15, 10])[0]
        orders.append((o, R.randint(1, 200), d(od), st)); tot = 0
        for p in R.sample(prods, R.randint(1, 4)):
            iid += 1; qn = R.randint(1, 5); items.append((iid, o, p[0], qn, p[4])); tot += qn * p[4]
        if st in ('Delivered', 'Shipped'):
            pays.append((len(pays) + 1, o, round(tot, 2), R.choice(['UPI','Card','COD','NetBanking']), d(od + R.randint(0, 3))))
    ev = []
    for e in range(1, 1501):
        n = R.randint(0, 729)
        ev.append((e, None if R.random() < .2 else R.randint(1, 200), R.choice(['view','click','add_to_cart','checkout','purchase']),
                   '%s %02d:%02d:00' % (d(n), R.randint(0, 23), R.randint(0, 59)), R.choice(['/home','/search','/product','/cart','/checkout'])))
    out['ecommerce'] = tbl('categories', ['category_id {pk}', 'category_name {t} NOT NULL'], list(enumerate(cats, 1))) + \
        tbl('suppliers', ['supplier_id {pk}', 'supplier_name {t} NOT NULL', 'country {t}'], [(i, 'Supplier %d' % i, R.choice(['India','China','Germany','USA'])) for i in range(1, 16)]) + \
        tbl('products', ['product_id {pk}', 'name {t} NOT NULL', 'category_id {i}', 'supplier_id {i}', 'price {r}', 'cost {r}', 'FOREIGN KEY (category_id) REFERENCES categories(category_id)', 'FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)'], prods) + \
        tbl('customers', ['customer_id {pk}', 'name {t} NOT NULL', 'email {t}', 'city {t}', 'signup_date {t}'], custs) + \
        tbl('orders', ['order_id {pk}', 'customer_id {i}', 'order_date {t}', 'status {t}', 'FOREIGN KEY (customer_id) REFERENCES customers(customer_id)'], orders) + \
        tbl('order_items', ['order_item_id {pk}', 'order_id {i}', 'product_id {i}', 'quantity {i}', 'unit_price {r}', 'FOREIGN KEY (order_id) REFERENCES orders(order_id)', 'FOREIGN KEY (product_id) REFERENCES products(product_id)'], items) + \
        tbl('payments', ['payment_id {pk}', 'order_id {i}', 'amount {r}', 'method {t}', 'paid_date {t}', 'FOREIGN KEY (order_id) REFERENCES orders(order_id)'], pays) + \
        tbl('web_events', ['event_id {pk}', 'customer_id {i}', 'event_type {t}', 'event_time {t}', 'page {t}'], ev)
    # telecom
    subs, rech, ch = [], [], []
    for s in range(1, 301):
        act = R.randint(0, 600); gone = R.random() < .2
        subs.append((s, '98' + ''.join(str(R.randint(0, 9)) for _ in range(8)), R.choice(['Plan 149','Plan 249','Plan 399','Plan 599']), R.choice(['Mumbai','Delhi','Kolkata','Chennai','Pune']), d(act), 'Churned' if gone else 'Active'))
        if gone: ch.append((s, d(act + R.randint(30, 120)), R.choice(['Price','Network','Competitor','Relocated'])))
    for r in range(1, 1501): rech.append((r, R.randint(1, 300), d(R.randint(0, 729)), R.choice([49, 99, 149, 249, 399])))
    out['telecom'] = tbl('telecom_subscribers', ['sub_id {pk}', 'msisdn {t}', 'plan {t}', 'circle {t}', 'activation_date {t}', 'status {t}'], subs) + \
        tbl('recharges', ['recharge_id {pk}', 'sub_id {i}', 'recharge_date {t}', 'amount {i}', 'FOREIGN KEY (sub_id) REFERENCES telecom_subscribers(sub_id)'], rech) + \
        tbl('churn', ['sub_id {pk}', 'churn_date {t}', 'reason {t}', 'FOREIGN KEY (sub_id) REFERENCES telecom_subscribers(sub_id)'], ch)
    # dirty
    rows = []
    for i in range(1, 151):
        nm = R.choice(first) + ' ' + R.choice(last); nm = R.choice([nm, nm.lower(), nm.upper(), '  ' + nm + ' '])
        em = R.choice(['%s@Example.com' % nm.strip().split()[0].lower(), ' %s@example.com' % nm.strip().split()[0].lower(), '', None])
        ph = R.choice(['98%08d' % R.randint(0, 99999999), '+91-98%08d' % R.randint(0, 99999999), '98%d %d' % (R.randint(100, 999), R.randint(10000, 99999)), None])
        ct = R.choice(['Mumbai', 'mumbai', 'MUMBAI ', 'Bombay', 'Pune', 'pune', 'Delhi', ' delhi'])
        sd = R.choice([d(R.randint(0, 700)), '%02d/%02d/2024' % (R.randint(1, 28), R.randint(1, 12)), ''])
        ag = R.choice([str(R.randint(18, 70)), str(R.randint(18, 70)), 'N/A', None, '-1'])
        rows.append((i, nm, em, ph, ct, sd, ag))
        if i % 10 == 0: rows.append((i + 1000, nm, em, ph, ct, sd, ag))
    out['dirty'] = tbl('dirty_customers', ['id {pk}', 'name {t}', 'email {t}', 'phone {t}', 'city {t}', 'signup_date {t}', 'age {t}'], rows)
    return out
if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else 'all'
    for dial in (DIALECTS if arg == 'all' else [arg]):
        os.makedirs('data/' + dial, exist_ok=True)
        for k, v in build(dial).items(): open('data/%s/%s.sql' % (dial, k), 'w').write(v)
        print('generated', dial)
