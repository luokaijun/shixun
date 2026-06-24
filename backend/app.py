from functools import wraps
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from uuid import uuid4
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB_PATH = 'shop_ecommerce.db'


def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"数据库连接错误: {e}")
        return None


def row_to_dict(row):
    return dict(row) if row else None


def get_token():
    auth = request.headers.get('Authorization', '')
    return auth[7:] if auth.startswith('Bearer ') else None


def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = get_token()
        if not token:
            return jsonify({'success': False, 'message': '未授权'}), 401

        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': '数据库连接失败'}), 500

        try:
            cursor = conn.cursor()
            cursor.execute('SELECT user_id FROM sessions WHERE token = ?', (token,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()

            if not row:
                return jsonify({'success': False, 'message': '未授权'}), 401
            return fn(user_id=row['user_id'], *args, **kwargs)
        except Exception as e:
            conn.close()
            return jsonify({'success': False, 'message': str(e)}), 500
    return wrapper


def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def create_token():
    return uuid4().hex


def init_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            parent_id INTEGER DEFAULT 0,
            icon VARCHAR(200),
            sort_order INTEGER DEFAULT 0,
            status TINYINT(1) DEFAULT 1,
            create_time TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS brands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            logo VARCHAR(200),
            sort_order INTEGER DEFAULT 0,
            status TINYINT(1) DEFAULT 1,
            create_time TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(200) NOT NULL,
            category_id INTEGER NOT NULL,
            brand_id INTEGER,
            price DECIMAL(10,2) NOT NULL,
            original_price DECIMAL(10,2),
            stock INTEGER DEFAULT 0,
            sales INTEGER DEFAULT 0,
            rating DECIMAL(3,1) DEFAULT 0,
            review_count INTEGER DEFAULT 0,
            is_hot TINYINT(1) DEFAULT 0,
            is_new TINYINT(1) DEFAULT 0,
            is_on_sale TINYINT(1) DEFAULT 1,
            description TEXT,
            specifications TEXT,
            create_time TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            image_url VARCHAR(500) NOT NULL,
            is_main TINYINT(1) DEFAULT 0,
            sort_order INTEGER DEFAULT 0,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE,
            nickname VARCHAR(50),
            status TINYINT(1) DEFAULT 1,
            register_time TEXT DEFAULT CURRENT_TIMESTAMP,
            last_login_time TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token VARCHAR(64) NOT NULL UNIQUE,
            user_id INTEGER NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS addresses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            consignee VARCHAR(50) NOT NULL,
            phone VARCHAR(20) NOT NULL,
            province VARCHAR(50) NOT NULL,
            city VARCHAR(50) NOT NULL,
            district VARCHAR(50),
            detail VARCHAR(500) NOT NULL,
            is_default TINYINT(1) DEFAULT 0,
            status TINYINT(1) DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS carts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            create_time TEXT DEFAULT CURRENT_TIMESTAMP,
            update_time TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id VARCHAR(50) PRIMARY KEY,
            user_id INTEGER NOT NULL,
            address_id INTEGER NOT NULL,
            total_amount DECIMAL(12,2) NOT NULL,
            pay_amount DECIMAL(12,2) NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            status_text VARCHAR(50) DEFAULT '待付款',
            remark TEXT,
            create_time TEXT DEFAULT CURRENT_TIMESTAMP,
            pay_time TEXT,
            ship_time TEXT,
            complete_time TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (address_id) REFERENCES addresses(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id VARCHAR(50) NOT NULL,
            product_id INTEGER NOT NULL,
            product_name VARCHAR(200) NOT NULL,
            product_image VARCHAR(500),
            price DECIMAL(10,2) NOT NULL,
            quantity INTEGER NOT NULL,
            subtotal DECIMAL(12,2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            rating DECIMAL(3,1) NOT NULL,
            content TEXT,
            is_anonymous TINYINT(1) DEFAULT 0,
            is_show TINYINT(1) DEFAULT 1,
            create_time TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    if cursor.execute('SELECT COUNT(*) FROM users').fetchone()[0] == 0:
        cursor.execute('INSERT INTO users (username, password, email, nickname) VALUES (?, ?, ?, ?)',
                      ('admin', '123456', 'admin@example.com', '管理员'))
        cursor.execute('INSERT INTO users (username, password, email, nickname) VALUES (?, ?, ?, ?)',
                      ('test', '123456', 'test@example.com', '测试用户'))

    if cursor.execute('SELECT COUNT(*) FROM categories').fetchone()[0] == 0:
        cursor.executemany('INSERT INTO categories (name, parent_id, icon) VALUES (?, ?, ?)',
                          [('数码', 0, '📱'), ('服饰', 0, '👕'), ('家居', 0, '🏠'), ('食品', 0, '🍎'), ('图书', 0, '📚')])

    if cursor.execute('SELECT COUNT(*) FROM brands').fetchone()[0] == 0:
        cursor.executemany('INSERT INTO brands (name, logo, sort_order) VALUES (?, ?, ?)',
                          [('小米', '', 1), ('华为', '', 2), ('苹果', '', 3), ('优衣库', '', 4), ('李宁', '', 5)])

    if cursor.execute('SELECT COUNT(*) FROM products').fetchone()[0] == 0:
        products = [
            ('无线蓝牙耳机', 1, 1, 199.00, 299.00, 320, 1580, 4.8, 256, 1, 1, '高品质无线蓝牙耳机，降噪效果出色，续航持久'),
            ('智能手表', 1, 2, 899.00, 1299.00, 180, 890, 4.6, 134, 1, 0, '运动健康监测智能手表，支持心率血氧检测'),
            ('纯棉T恤', 2, 4, 59.90, 99.00, 860, 3200, 4.7, 567, 1, 1, '100%纯棉透气T恤，舒适百搭'),
            ('运动跑鞋', 2, 5, 299.00, 499.00, 420, 2100, 4.9, 389, 1, 0, '专业运动跑鞋，缓震舒适，轻便透气'),
            ('保温杯', 3, 1, 89.00, 129.00, 510, 1800, 4.5, 213, 0, 0, '304不锈钢保温杯，保温12小时'),
            ('收纳箱', 3, 2, 45.00, 79.00, 680, 1200, 4.4, 156, 0, 0, '大容量塑料收纳箱，带滑轮方便移动'),
            ('坚果礼盒', 4, 3, 128.00, 198.00, 260, 980, 4.8, 178, 1, 0, '精选混合坚果礼盒，送礼佳品'),
            ('有机蜂蜜', 4, 1, 68.00, 99.00, 380, 720, 4.6, 89, 0, 1, '纯天然有机蜂蜜，口感醇厚'),
            ('Python编程入门', 5, 2, 59.00, 89.00, 500, 3500, 4.9, 892, 1, 0, '零基础Python编程入门教程'),
            ('设计心理学', 5, 3, 78.00, 118.00, 280, 1500, 4.7, 345, 0, 0, '经典设计心理学读物'),
            ('无线鼠标', 1, 1, 79.00, 129.00, 650, 2800, 4.5, 423, 0, 0, '人体工学无线鼠标，办公必备'),
            ('机械键盘', 1, 2, 249.00, 399.00, 180, 1200, 4.8, 267, 1, 1, 'RGB背光机械键盘，游戏利器'),
            ('休闲短裤', 2, 5, 49.00, 79.00, 520, 1800, 4.4, 198, 0, 0, '夏季休闲短裤，舒适透气'),
            ('防晒衣', 2, 4, 99.00, 159.00, 380, 1500, 4.6, 234, 1, 0, 'UPF50+防晒衣，轻薄透气'),
            ('台灯', 3, 1, 129.00, 199.00, 240, 900, 4.7, 167, 0, 1, '护眼台灯，无极调光'),
            ('数据线', 1, 2, 29.00, 49.00, 1200, 5600, 4.5, 890, 0, 0, 'Type-C快充数据线，1.5米'),
            ('巧克力礼盒', 4, 3, 68.00, 99.00, 420, 1800, 4.8, 321, 0, 0, '比利时进口巧克力礼盒'),
            ('儿童绘本', 5, 1, 45.00, 68.00, 380, 2100, 4.9, 456, 1, 0, '精选儿童绘本套装，适合3-6岁'),
            ('便携充电宝', 1, 1, 149.00, 199.00, 450, 2800, 4.6, 512, 1, 0, '20000mAh大容量充电宝，支持快充'),
            ('运动水壶', 3, 5, 59.00, 89.00, 620, 1500, 4.5, 267, 0, 0, '运动大容量水壶，防漏设计'),
        ]
        cursor.executemany('''
            INSERT INTO products (name, category_id, brand_id, price, original_price, stock, sales, rating, review_count, is_hot, is_new, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', products)

        for i, kw in enumerate([
            'headphone', 'smartwatch', 'tshirt', 'sneaker,running', 'thermos,bottle',
            'storage,box', 'nuts,gift', 'honey,jar', 'book,python', 'book,design',
            'mouse,computer', 'keyboard,mechanical', 'shorts,clothing', 'jacket,outdoor',
            'lamp,desk', 'usb,cable', 'chocolate,box', 'children,book',
            'powerbank,battery', 'water,bottle,sports'
        ], 1):
            cursor.execute('INSERT INTO product_images (product_id, image_url, is_main, sort_order) VALUES (?, ?, ?, ?)',
                          (i, f'https://loremflickr.com/600/600/{kw}?lock={i}', 1, 1))

    conn.commit()
    conn.close()


@app.route('/api/products', methods=['GET'])
def products():
    search = request.args.get('search', '').strip().lower()
    category_id = request.args.get('category_id', '')
    brand_id = request.args.get('brand_id', '')
    sort_by = request.args.get('sort', '')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    offset = (page - 1) * page_size

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'}), 500

    try:
        cursor = conn.cursor()
        sql = 'SELECT p.*, c.name as category_name, b.name as brand_name FROM products p LEFT JOIN categories c ON p.category_id = c.id LEFT JOIN brands b ON p.brand_id = b.id WHERE p.is_on_sale = 1'
        conditions = []
        params = []

        if search:
            conditions.append('(LOWER(p.name) LIKE ? OR LOWER(p.description) LIKE ?)')
            params.extend([f'%{search}%', f'%{search}%'])

        if category_id:
            conditions.append('p.category_id = ?')
            params.append(category_id)

        if brand_id:
            conditions.append('p.brand_id = ?')
            params.append(brand_id)

        if conditions:
            sql += ' AND ' + ' AND '.join(conditions)

        sql += {'price-asc': ' ORDER BY p.price ASC', 'price-desc': ' ORDER BY p.price DESC',
                'sales': ' ORDER BY p.sales DESC', 'rating': ' ORDER BY p.rating DESC'}.get(sort_by, ' ORDER BY p.create_time DESC')

        count_sql = sql.replace('SELECT p.*, c.name as category_name, b.name as brand_name', 'SELECT COUNT(*)')
        cursor.execute(count_sql, params)
        total = cursor.fetchone()[0]

        sql += ' LIMIT ? OFFSET ?'
        params.extend([page_size, offset])
        cursor.execute(sql, params)

        products = []
        for row in cursor.fetchall():
            product = row_to_dict(row)
            cursor.execute('SELECT image_url FROM product_images WHERE product_id = ? AND is_main = 1 LIMIT 1', (product['id'],))
            img = cursor.fetchone()
            product['main_image'] = img['image_url'] if img else ''
            products.append(product)

        cursor.close()
        conn.close()

        return jsonify({'success': True, 'data': products, 'total': total, 'page': page, 'page_size': page_size})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/products/<int:product_id>', methods=['GET'])
def product_detail(product_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.*, c.name as category_name, b.name as brand_name
            FROM products p LEFT JOIN categories c ON p.category_id = c.id LEFT JOIN brands b ON p.brand_id = b.id
            WHERE p.id = ? AND p.is_on_sale = 1
        ''', (product_id,))
        product = row_to_dict(cursor.fetchone())

        if not product:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': '商品不存在'}), 404

        cursor.execute('SELECT image_url, is_main FROM product_images WHERE product_id = ? ORDER BY sort_order', (product_id,))
        images = [row_to_dict(row) for row in cursor.fetchall()]
        product['images'] = images
        product['main_image'] = images[0]['image_url'] if images else ''

        cursor.execute('''
            SELECT r.*, u.nickname, u.avatar FROM reviews r LEFT JOIN users u ON r.user_id = u.id
            WHERE r.product_id = ? AND r.is_show = 1 ORDER BY r.create_time DESC LIMIT 20
        ''', (product_id,))
        product['reviews'] = [row_to_dict(row) for row in cursor.fetchall()]

        cursor.close()
        conn.close()
        return jsonify({'success': True, 'data': product})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/categories', methods=['GET'])
def categories():
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, parent_id, icon FROM categories WHERE status = 1 ORDER BY sort_order')
        categories = [row_to_dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'data': categories})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/brands', methods=['GET'])
def brands():
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, logo FROM brands WHERE status = 1 ORDER BY sort_order')
        brands = [row_to_dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'data': brands})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({'success': False, 'message': '请输入用户名和密码'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, username, email, nickname, avatar FROM users WHERE username = ? AND password = ? AND status = 1',
            (username, password)
        )
        user = row_to_dict(cursor.fetchone())

        if not user:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': '用户名或密码错误'}), 401

        token = create_token()
        cursor.execute('INSERT INTO sessions (token, user_id, created_at) VALUES (?, ?, ?)',
                      (token, user['id'], now()))
        cursor.execute('UPDATE users SET last_login_time = ? WHERE id = ?', (now(), user['id']))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'success': True, 'user': user, 'token': token})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json or {}
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    if not username or not email or not password:
        return jsonify({'success': False, 'message': '请填写完整注册信息'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': '用户名已存在'}), 400

        cursor.execute('SELECT 1 FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': '邮箱已被注册'}), 400

        cursor.execute(
            'INSERT INTO users (username, password, email, nickname, register_time) VALUES (?, ?, ?, ?, ?)',
            (username, password, email, username, now())
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'success': True, 'message': '注册成功，请登录'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/cart', methods=['GET'])
@auth_required
def get_cart(user_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.*, p.name, p.price, p.original_price,
                   (SELECT image_url FROM product_images WHERE product_id = p.id AND is_main = 1 LIMIT 1) as image
            FROM carts c LEFT JOIN products p ON c.product_id = p.id
            WHERE c.user_id = ? ORDER BY c.update_time DESC
        ''', (user_id,))
        rows = cursor.fetchall()
        cart_items = [row_to_dict(row) for row in rows]
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'data': cart_items})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/cart', methods=['POST'])
@auth_required
def add_cart(user_id):
    data = request.json or {}
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if not product_id or quantity <= 0:
        return jsonify({'success': False, 'message': '参数错误'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT stock FROM products WHERE id = ? AND is_on_sale = 1', (product_id,))
        product = cursor.fetchone()
        if not product:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': '商品不存在或已下架'}), 404

        cursor.execute('SELECT quantity FROM carts WHERE user_id = ? AND product_id = ?', (user_id, product_id))
        existing = cursor.fetchone()
        current_time = now()
        if existing:
            new_quantity = existing['quantity'] + quantity
            if new_quantity > product['stock']:
                cursor.close()
                conn.close()
                return jsonify({'success': False, 'message': '库存不足'}), 400
            cursor.execute('UPDATE carts SET quantity = ?, update_time = ? WHERE user_id = ? AND product_id = ?',
                          (new_quantity, current_time, user_id, product_id))
        else:
            if quantity > product['stock']:
                cursor.close()
                conn.close()
                return jsonify({'success': False, 'message': '库存不足'}), 400
            cursor.execute('INSERT INTO carts (user_id, product_id, quantity, create_time, update_time) VALUES (?, ?, ?, ?, ?)',
                          (user_id, product_id, quantity, current_time, current_time))

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': '添加购物车成功'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/cart/<int:cart_id>', methods=['PUT'])
@auth_required
def update_cart(user_id, cart_id):
    data = request.json or {}
    quantity = data.get('quantity')

    if quantity is None or quantity <= 0:
        return jsonify({'success': False, 'message': '参数错误'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT c.product_id, p.stock FROM carts c LEFT JOIN products p ON c.product_id = p.id WHERE c.id = ? AND c.user_id = ?',
                      (cart_id, user_id))
        cart = cursor.fetchone()
        if not cart:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': '购物车项不存在'}), 404

        if quantity > cart['stock']:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': '库存不足'}), 400

        cursor.execute('UPDATE carts SET quantity = ?, update_time = ? WHERE id = ?', (quantity, now(), cart_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': '更新成功'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/cart/<int:cart_id>', methods=['DELETE'])
@auth_required
def delete_cart(user_id, cart_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM carts WHERE id = ? AND user_id = ?', (cart_id, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': '删除成功'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/addresses', methods=['GET'])
@auth_required
def get_addresses(user_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM addresses WHERE user_id = ? AND status = 1 ORDER BY is_default DESC', (user_id,))
        addresses = [row_to_dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'data': addresses})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/addresses', methods=['POST'])
@auth_required
def add_address(user_id):
    data = request.json or {}
    required_fields = ['consignee', 'phone', 'province', 'city', 'detail']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'success': False, 'message': f'{field}不能为空'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'}), 500

    try:
        cursor = conn.cursor()
        is_default = data.get('is_default', 0)
        if is_default:
            cursor.execute('UPDATE addresses SET is_default = 0 WHERE user_id = ?', (user_id,))

        cursor.execute('''
            INSERT INTO addresses (user_id, consignee, phone, province, city, district, detail, is_default, create_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, data['consignee'], data['phone'], data['province'], data['city'],
              data.get('district', ''), data['detail'], is_default, now()))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': '添加地址成功'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/orders', methods=['GET'])
@auth_required
def list_orders(user_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT o.*, a.consignee, a.phone, a.province, a.city, a.district, a.detail
            FROM orders o LEFT JOIN addresses a ON o.address_id = a.id
            WHERE o.user_id = ? ORDER BY o.create_time DESC
        ''', (user_id,))
        orders = [row_to_dict(row) for row in cursor.fetchall()]

        for order in orders:
            cursor.execute('''
                SELECT oi.id, oi.product_id, oi.product_name, oi.product_image, oi.price, oi.quantity, oi.subtotal,
                       r.id as review_id
                FROM order_items oi LEFT JOIN reviews r ON oi.product_id = r.product_id AND r.user_id = ?
                WHERE oi.order_id = ?
            ''', (user_id, order['id']))
            items = []
            for row in cursor.fetchall():
                item = row_to_dict(row)
                item['reviewed'] = row['review_id'] is not None
                items.append(item)
            order['items'] = items

        cursor.close()
        conn.close()
        return jsonify({'success': True, 'data': orders})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/orders', methods=['POST'])
@auth_required
def create_order_route(user_id):
    data = request.json or {}
    address_id = data.get('address_id')
    items = data.get('items', [])
    remark = data.get('remark', '')

    if not address_id or not items:
        return jsonify({'success': False, 'message': '订单数据无效'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM addresses WHERE id = ? AND user_id = ? AND status = 1', (address_id, user_id))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': '收货地址无效'}), 400

        total_amount = 0
        order_items_data = []

        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)

            cursor.execute('SELECT price, stock, name FROM products WHERE id = ? AND is_on_sale = 1', (product_id,))
            product = cursor.fetchone()
            if not product:
                cursor.close()
                conn.close()
                return jsonify({'success': False, 'message': '商品不存在或已下架'}), 404

            if quantity > product['stock']:
                cursor.close()
                conn.close()
                return jsonify({'success': False, 'message': '库存不足'}), 400

            subtotal = product['price'] * quantity
            total_amount += subtotal

            cursor.execute('SELECT image_url FROM product_images WHERE product_id = ? AND is_main = 1 LIMIT 1', (product_id,))
            image = cursor.fetchone()
            order_items_data.append((product_id, product['name'], image['image_url'] if image else '',
                                     product['price'], quantity, subtotal, item.get('spec_info', '')))

        order_id = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid4().hex[:4].upper()}"
        create_time = now()

        cursor.execute('''
            INSERT INTO orders (id, user_id, address_id, total_amount, pay_amount, status, status_text, remark, create_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (order_id, user_id, address_id, total_amount, total_amount, 'pending', '待付款', remark, create_time))

        for item_data in order_items_data:
            cursor.execute('''
                INSERT INTO order_items (order_id, product_id, product_name, product_image, price, quantity, subtotal, spec_info)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (order_id,) + item_data)
            cursor.execute('UPDATE products SET stock = stock - ?, sales = sales + ? WHERE id = ?',
                          (item_data[4], item_data[4], item_data[0]))
            cursor.execute('DELETE FROM carts WHERE user_id = ? AND product_id = ?', (user_id, item_data[0]))

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': '下单成功', 'order_id': order_id})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/orders/<order_id>/cancel', methods=['POST'])
@auth_required
def cancel_order_route(user_id, order_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE id = ? AND user_id = ?', (order_id, user_id))
        order = row_to_dict(cursor.fetchone())
        if not order:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': '订单不存在'}), 404

        if order['status'] not in ['pending', 'paid']:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': '该状态的订单无法取消'}), 400

        cursor.execute('UPDATE orders SET status = ?, status_text = ? WHERE id = ?', ('canceled', '已取消', order_id))

        cursor.execute('SELECT product_id, quantity FROM order_items WHERE order_id = ?', (order_id,))
        for item in cursor.fetchall():
            cursor.execute('UPDATE products SET stock = stock + ? WHERE id = ?', (item['quantity'], item['product_id']))

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': '订单已取消'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500


def update_order_status(user_id, order_id, target_status, new_status, new_status_text, time_field):
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE id = ? AND user_id = ?', (order_id, user_id))
        order = row_to_dict(cursor.fetchone())
        if not order:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': '订单不存在'}), 404

        if order['status'] != target_status:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': '该状态的订单无法操作'}), 400

        cursor.execute(f'UPDATE orders SET status = ?, status_text = ?, {time_field} = ? WHERE id = ?',
                      (new_status, new_status_text, now(), order_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': f'{new_status_text}成功'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/orders/<order_id>/pay', methods=['POST'])
@auth_required
def pay_order_route(user_id, order_id):
    return update_order_status(user_id, order_id, 'pending', 'paid', '已付款', 'pay_time')


@app.route('/api/orders/<order_id>/receive', methods=['POST'])
@auth_required
def receive_order_route(user_id, order_id):
    return update_order_status(user_id, order_id, 'shipped', 'completed', '已完成', 'complete_time')


@app.route('/api/orders/<order_id>/ship', methods=['POST'])
@auth_required
def ship_order_route(user_id, order_id):
    return update_order_status(user_id, order_id, 'paid', 'shipped', '已发货', 'ship_time')


@app.route('/api/reviews', methods=['POST'])
@auth_required
def submit_review(user_id):
    data = request.json or {}
    product_id = data.get('product_id')
    rating = data.get('rating')
    content = data.get('content', '')

    if not product_id or not rating:
        return jsonify({'success': False, 'message': '参数错误'}), 400

    if rating < 1 or rating > 5:
        return jsonify({'success': False, 'message': '评分必须在1-5之间'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'}), 500

    try:
        cursor = conn.cursor()

        cursor.execute('SELECT 1 FROM orders o JOIN order_items oi ON o.id = oi.order_id WHERE o.id = ? AND o.user_id = ? AND oi.product_id = ? AND o.status = "completed"',
                      (data.get('order_id'), user_id, product_id))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': '无法评价该商品'}), 400

        cursor.execute('SELECT 1 FROM reviews WHERE product_id = ? AND user_id = ?', (product_id, user_id))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': '您已经评价过该商品'}), 400

        cursor.execute('''
            INSERT INTO reviews (product_id, user_id, rating, content, is_anonymous, is_show, create_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (product_id, user_id, rating, content, data.get('is_anonymous', 0), 1, now()))

        cursor.execute('''
            UPDATE products SET rating = (SELECT AVG(rating) FROM reviews WHERE product_id = ? AND is_show = 1),
                               review_count = (SELECT COUNT(*) FROM reviews WHERE product_id = ? AND is_show = 1)
            WHERE id = ?
        ''', (product_id, product_id, product_id))

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': '评价成功'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/reviews/<int:product_id>', methods=['GET'])
def get_reviews(product_id):
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    offset = (page - 1) * page_size

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.*, u.nickname, u.avatar FROM reviews r LEFT JOIN users u ON r.user_id = u.id
            WHERE r.product_id = ? AND r.is_show = 1 ORDER BY r.create_time DESC LIMIT ? OFFSET ?
        ''', (product_id, page_size, offset))
        reviews = [row_to_dict(row) for row in cursor.fetchall()]

        cursor.execute('SELECT COUNT(*) FROM reviews WHERE product_id = ? AND is_show = 1', (product_id,))
        total = cursor.fetchone()[0]

        cursor.close()
        conn.close()
        return jsonify({'success': True, 'data': reviews, 'total': total, 'page': page, 'page_size': page_size})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500


if __name__ == '__main__':
    init_database()
    print('Starting Flask app on http://0.0.0.0:5000')
    app.run(host='0.0.0.0', port=5000, debug=True)