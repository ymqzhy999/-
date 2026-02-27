from flask import session
import service.users_data as user_service
from flask import Flask, render_template
from flask import flash
from flask import request
from utils import dbUtil
import random
import os
from werkzeug.utils import secure_filename
from flask import jsonify


app = Flask(__name__)
app.secret_key = ' '

# 配置文件上传
UPLOAD_FOLDER = 'static/images/pic'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 系统默认路径前台跳转
@app.route('/')
def main_page():
    return render_template("login.html")

# 登录
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        account = request.form.get('account')
        print(account)
        password = request.form.get('password')
        print(password)
        role = request.form.get('role')
        print(f"收到前端: account={account}, password={password}, role={role}")
        if not all([account, password, role]):
            flash('参数不完整')
            return "300"
        res = user_service.get_user(account, password, role)
        if res and res[0][0] > 0:
            session['is_login'] = True
            session['role'] = res[0][2]
            session['type'] = res[0][1]
            session['name'] = res[0][2]
            session['account'] = account
            # 获取用户头像
            db = dbUtil()
            sql = "select avatar from user where account=%s"
            avatar = db.query(sql, account)
            db.close()
            session['avatar'] = avatar[0][0] if avatar and avatar[0][0] else '../../static/images/default-avatar.png'
            return "200"
        else:
            return "300"


# 登录页面跳转
@app.route('/admin')
def admin():
    if session.get("is_login"):
        if session.get('role') == 0:
            return render_template('index.html')
        else:
            return render_template('index.html')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    try:
        session.pop("is_login")
        return render_template('login.html')
    except Exception:
        return render_template('login.html')

# 后台注册跳转
@app.route('/html/reg')
def html_reg():
    return render_template('reg.html')

# -----------------用户管理模块START-----------------


# 注册用户数据
@app.route('/user/reg', methods=["POST"])
def user_reg():
    get_data = request.form.to_dict()
    name = str(get_data.get('username'))
    account = str(get_data.get('account'))
    password = str(get_data.get('password'))
    company = "平台注册"
    phone = " "
    mail = " "
    type = 1
    return user_service.add_user(name, account, password, company, phone, mail, type)

# 用户信息管理（仅管理员可访问）
@app.route('/user/list')
def user_list():
    if session.get('role') != '管理员':
        return '无权限访问', 403
    db = dbUtil()
    sql = "select id, name, account, company, phone, mail, type, status from user where name != '管理员'"
    users = db.query(sql)
    db.close()
    return render_template('html/user_list.html', users=users)

@app.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
def user_edit(user_id):
    if session.get('role') != '管理员':
        return '无权限访问', 403
    db = dbUtil()
    if request.method == 'POST':
        name = request.form.get('name')
        company = request.form.get('company')
        phone = request.form.get('phone')
        mail = request.form.get('mail')
        sql = "update user set name=%s, company=%s, phone=%s, mail=%s where id=%s"
        db.query(sql, name, company, phone, mail, user_id)
        db.close()
        return '修改成功'
    else:
        sql = "select id, name, account, company, phone, mail from user where id=%s"
        user = db.query(sql, user_id)
        db.close()
        if user:
            user = user[0]
        return render_template('html/user_edit.html', user=user)

@app.route('/user/profile', methods=['GET', 'POST'])
def user_profile():
    if not session.get('is_login'):
        return render_template('login.html')
    account = session.get('account')
    db = dbUtil()
    sql = "select account, avatar from user where account=%s"
    user = db.query(sql, account)
    db.close()
    if user:
        userinfo = {
            'account': user[0][0],
            'avatar': user[0][1] or '../../static/images/default-avatar.png'
        }
    else:
        userinfo = {
            'account': account,
            'avatar': '../../static/images/default-avatar.png'
        }
    if request.method == 'POST':
        # 处理表单数据
        new_account = request.form.get('account')
        new_password = request.form.get('password')
        db = dbUtil()
        # 只更新有变化的字段
        if new_password:
            sql = "update user set account=%s, password=%s where account=%s"
            db.query(sql, new_account, new_password, account)
        else:
            sql = "update user set account=%s where account=%s"
            db.query(sql, new_account, account)
        db.close()
        session['account'] = new_account  # 同步session
        return '修改成功'
    else:
        return render_template('html/profile.html', userinfo=userinfo)

# 上传头像
@app.route('/user/avatar', methods=['POST'])
def upload_avatar():
    if not session.get('is_login'):
        return '请先登录', 401
    if 'avatar' not in request.files:
        return '没有文件', 400
    file = request.files['avatar']
    if file.filename == '':
        return '没有选择文件', 400
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{session.get('account')}_{file.filename}")
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # 存储相对路径
        avatar_path = f"images/pic/{filename}"
        db = dbUtil()
        sql = "update user set avatar=%s where account=%s"
        db.query(sql, avatar_path, session.get('account'))
        db.close()
        session['avatar'] = avatar_path
        return 'success'
    return '文件类型不允许', 400

# 获取收藏列表
@app.route('/user/favorites')
def favorites_page():
    return render_template('html/favorites.html')

# 添加收藏
@app.route('/user/favorite/add', methods=['POST'])
def add_favorite():
    if not session.get('is_login'):
        return '请先登录', 401
    
    food_id = request.form.get('id')
    if not food_id:
        return '参数错误', 400
    
    account = session.get('account')
    db = dbUtil()
    
    # 获取用户当前收藏
    sql = "select favorites from user where account=%s"
    result = db.query(sql, account)
    current_favorites = result[0][0].split(',') if result and result[0][0] else []
    
    # 检查是否已收藏
    if food_id in current_favorites:
        db.close()
        return '已经收藏过了', 400
    
    # 更新用户收藏
    current_favorites.append(food_id)
    new_favorites = ','.join(current_favorites)
    sql = "update user set favorites=%s where account=%s"
    db.query(sql, new_favorites, account)
    
    # 更新美食收藏数
    sql = "update data set favorite_count=favorite_count+1 where `index`=%s"
    db.query(sql, food_id)
    
    db.close()
    return 'success'

# 取消收藏
@app.route('/user/favorite/remove', methods=['POST'])
def remove_favorite():
    if not session.get('is_login'):
        return '请先登录', 401
    
    food_id = request.form.get('id')
    if not food_id:
        return '参数错误', 400
    
    account = session.get('account')
    db = dbUtil()
    
    # 获取用户当前收藏
    sql = "select favorites from user where account=%s"
    result = db.query(sql, account)
    current_favorites = result[0][0].split(',') if result and result[0][0] else []
    
    # 检查是否已收藏
    if food_id not in current_favorites:
        db.close()
        return '未收藏该美食', 400
    
    # 更新用户收藏
    current_favorites.remove(food_id)
    new_favorites = ','.join(current_favorites)
    sql = "update user set favorites=%s where account=%s"
    db.query(sql, new_favorites, account)
    
    # 更新美食收藏数
    sql = "update data set favorite_count=favorite_count-1 where `index`=%s"
    db.query(sql, food_id)
    
    db.close()
    return 'success'

# 获取收藏列表数据
@app.route('/user/favorites/data')
def favorites_data():
    if not session.get('is_login'):
        return jsonify([])

    account = session.get('account')
    db = dbUtil()
    # 获取用户收藏的美食ID
    sql = "select favorites from user where account=%s"
    result = db.query(sql, account)
    favorite_ids = result[0][0].split(',') if result and result[0][0] else []
    if not favorite_ids or favorite_ids == ['']:
        db.close()
        return jsonify([])

    # 查询收藏美食详情
    format_strings = ','.join(['%s'] * len(favorite_ids))
    sql = f"select `index`, title, comment_count, averge_price, type, area, recommend, group_purchase, preferential, favorite_count from data where `index` in ({format_strings})"
    foods = db.query(sql, *favorite_ids)
    db.close()
    foods_list = []
    for f in foods:
        foods_list.append({
            'id': f[0],
            'title': f[1],
            'comment_count': f[2],
            'averge_price': f[3],
            'type': f[4],
            'area': f[5],
            'recommend': f[6],
            'group_purchase': f[7],
            'preferential': f[8],
            'favorite_count': f[9],
            'is_favorited': str(f[0]) in favorite_ids
        })
    return jsonify(foods_list)

# 获取用户收藏的美食列表
@app.route('/user/<int:user_id>/favorites')
def admin_user_favorites(user_id):
    if session.get('role') != '管理员':
        return '无权限访问', 403
    db = dbUtil()
    # 获取用户账号
    sql = "select account, name from user where id=%s"
    user = db.query(sql, user_id)
    if not user:
        db.close()
        return '用户不存在', 404
    account, name = user[0][0], user[0][1]
    # 获取收藏的美食ID
    sql = "select favorites from user where id=%s"
    result = db.query(sql, user_id)
    favorite_ids = result[0][0].split(',') if result and result[0][0] else []
    foods = []
    if favorite_ids and favorite_ids != ['']:
        format_strings = ','.join(['%s'] * len(favorite_ids))
        sql = f"select `index`, title, comment_count, averge_price, type, area, recommend, group_purchase, preferential, favorite_count from data where `index` in ({format_strings})"
        foods = db.query(sql, *favorite_ids)
    db.close()
    foods_list = []
    for f in foods:
        foods_list.append({
            'id': f[0],
            'title': f[1],
            'comment_count': f[2],
            'averge_price': f[3],
            'type': f[4],
            'area': f[5],
            'recommend': f[6],
            'group_purchase': f[7],
            'preferential': f[8],
            'favorite_count': f[9],
            'is_favorited': str(f[0]) in favorite_ids
        })
    return render_template('html/admin_favorites.html', user_name=name, user_account=account, foods=foods_list)

# -----------------用户管理模块END-----------------

@app.route("/index")
def root():
    return render_template("index.html")

@app.route("/店铺有无优惠占比")
def shop_discount_ratio():
    return render_template('店铺有无优惠占比.html')

@app.route("/美食排行榜前20")
def food_top20():
    db = dbUtil()
    # 按评论数排序，取前20
    sql = """
        SELECT `index`, title, comment_count, averge_price, type, area, recommend, favorite_count
        FROM data
        ORDER BY comment_count DESC
        LIMIT 20
    """
    results = db.query(sql)
    db.close()
    foods = []
    for f in results:
        foods.append({
            'id': f[0],
            'title': f[1],
            'comment_count': f[2],
            'averge_price': f[3],
            'type': f[4],
            'area': f[5],
            'recommend': f[6],
            'favorite_count': f[7],
            'is_favorited': False  # 如果有登录用户可以再判断
        })
    return render_template('美食排行榜前20.html', foods=foods)

@app.route("/a")
def a():
    return render_template("店铺有无优惠占比.html")

@app.route("/平均消费价格区间柱状图")
def price_bar():
    return render_template("平均消费价格区间柱状图.html")

@app.route("/店铺类型占比饼图")
def pie_chart():
    return render_template("店铺类型占比饼图.html")

@app.route("/美食店铺评论人数top10")
def comment_top10():
    return render_template("美食店铺评论人数top10.html")

@app.route("/推荐菜品词云图")
def wordcloud():
    return render_template("推荐菜品词云图.html")

@app.route("/e")
def e():
    return render_template("美食店铺人均消费top10.html")

@app.route("/f")
def f():
    return render_template("美食店铺评论人数top10.html")

# 后台首页面跳转
@app.route('/html/welcome')
def welcome():
    account = session.get('account')
    if not account:
        return render_template('login.html')
    # 针对特定账号固定个人信息
    if account == '123456':
        userinfo = {
            'company': '经济管理系',
            'major': '金融学',
            'name': '李明',
            'student_id': '2023123456'
        }
    elif account == 'admin':
        userinfo = {
            'company': '计算机工程系',
            'major': '大数据',
            'name': '王康佳',
            'student_id': '23050803058'
        }
    else:
        # 其他账号用账号做种子保证一致
        colleges = ['计算机工程系', '信息管理系', '经济管理系', '外国语学院', '数学与统计学院']
        majors = ['大数据', '人工智能', '软件工程', '网络安全', '金融学']
        names = ['王康佳', '李明', '张伟', '赵丽', '孙强', '周婷', '钱坤', '吴昊', '郑爽', '冯晨']
        random.seed(account)
        userinfo = {
            'company': random.choice(colleges),
            'major': random.choice(majors),
            'name': random.choice(names),
            'student_id': str(random.randint(2000000000, 2999999999))
        }
    return render_template('html/welcome.html', userinfo=userinfo)

# 数据可视化大屏页面跳转
@app.route('/page')
def page():
    return render_template('page.html')

# 美食详情页面
@app.route('/food/<int:food_id>')
def food_detail(food_id):
    if not session.get('is_login'):
        return render_template('login.html')
    
    db = dbUtil()
    # 正确的字段名
    sql = """
    SELECT `index`, title, comment_count, averge_price, type, area, recommend, group_purchase, preferential, favorite_count
    FROM data
    WHERE `index`=%s
    """
    food = db.query(sql, food_id)
    
    if not food:
        db.close()
        return '美食不存在', 404
    
    food = {
        'id': food[0][0],
        'name': food[0][1],  # title
        'comment_count': food[0][2],
        'price': food[0][3],  # averge_price
        'type': food[0][4],
        'area': food[0][5],
        'recommend': food[0][6],
        'group_purchase': food[0][7],
        'preferential': food[0][8],
        'favorite_count': food[0][9]
    }
    
    # 检查是否已收藏
    account = session.get('account')
    sql = "select favorites from user where account=%s"
    result = db.query(sql, account)
    favorites = result[0][0].split(',') if result and result[0][0] else []
    is_favorited = str(food_id) in favorites
    
    db.close()
    return render_template('html/food_detail.html', food=food, is_favorited=is_favorited)

@app.route('/recommendations')
def recommendations():
    if not session.get('is_login'):
        return redirect('/login')
    
    # 使用account而不是user_id
    account = session.get('account')
    if not account:
        return redirect('/login')
    
    db = dbUtil()
    # 获取用户ID
    sql = "SELECT id FROM user WHERE account=%s"
    result = db.query(sql, account)
    if not result:
        db.close()
        return redirect('/login')
    
    user_id = result[0][0]
    recommendations = user_service.get_user_recommendations(user_id)
    history = user_service.get_user_behavior_history(user_id)
    db.close()
    
    return render_template('recommendations.html', 
                         recommendations=recommendations,
                         history=history)

@app.route('/api/record_behavior', methods=['POST'])
def record_behavior():
    if not session.get('is_login'):
        return jsonify({'status': 'error', 'message': '请先登录'})
    
    account = session.get('account')
    if not account:
        return jsonify({'status': 'error', 'message': '请先登录'})
    
    data = request.get_json()
    item_id = data.get('item_id')
    behavior_type = data.get('behavior_type')  # 1:浏览 2:收藏 3:购买
    
    if not all([item_id, behavior_type]):
        return jsonify({'status': 'error', 'message': '参数不完整'})
    
    # 获取用户ID
    db = dbUtil()
    sql = "SELECT id FROM user WHERE account=%s"
    result = db.query(sql, account)
    if not result:
        db.close()
        return jsonify({'status': 'error', 'message': '用户不存在'})
    
    user_id = result[0][0]
    db.close()
    
    success = user_service.record_user_behavior(user_id, item_id, behavior_type)
    return jsonify({
        'status': 'success' if success else 'error',
        'message': '记录成功' if success else '记录失败'
    })

@app.route('/api/ai_recommend', methods=['POST'])
def ai_recommend():
    data = request.get_json()
    keyword = data.get('keyword', '').strip()
    if not keyword:
        return jsonify({'recommendations': []})
    # 简单分词和模糊查询
    db = dbUtil()
    sql = """
    SELECT `index`, title, type, area, averge_price, comment_count, favorite_count
    FROM data
    WHERE title LIKE %s OR type LIKE %s OR area LIKE %s OR averge_price LIKE %s
    LIMIT 10
    """
    like_kw = f'%{keyword}%'
    results = db.query(sql, like_kw, like_kw, like_kw, like_kw)
    db.close()
    return jsonify({'recommendations': results})

@app.route('/api/price_predict', methods=['POST'])
def price_predict():
    data = request.get_json()
    food_type = data.get('type', '').strip()
    if not food_type:
        return jsonify({'bins': [], 'counts': [], 'mean': 0, 'min': 0, 'max': 0, 'median': 0, 'q1': 0, 'q3': 0})
    db = dbUtil()
    sql = "SELECT averge_price FROM data WHERE type LIKE %s"
    results = db.query(sql, f'%{food_type}%')
    db.close()
    # 数据清洗
    prices = []
    for row in results:
        price_str = row[0]
        if price_str:
            price_str = price_str.replace('￥', '').replace('元', '').strip()
            try:
                price = float(price_str)
                prices.append(price)
            except:
                continue
    if not prices:
        return jsonify({'bins': [], 'counts': [], 'mean': 0, 'min': 0, 'max': 0, 'median': 0, 'q1': 0, 'q3': 0})
    import numpy as np
    prices_np = np.array(prices)
    mean = float(np.mean(prices_np))
    min_ = float(np.min(prices_np))
    max_ = float(np.max(prices_np))
    median = float(np.median(prices_np))
    q1 = float(np.percentile(prices_np, 25))
    q3 = float(np.percentile(prices_np, 75))
    # 箱线图数据
    return jsonify({
        'mean': mean,
        'min': min_,
        'max': max_,
        'median': median,
        'q1': q1,
        'q3': q3,
        'prices': prices  # 可用于前端画KDE或箱线图
    })

@app.route('/api/shop_search', methods=['POST'])
def shop_search():
    data = request.get_json()
    keyword = data.get('keyword', '').strip()
    min_price = data.get('min_price')
    max_price = data.get('max_price')
    db = dbUtil()
    sql = """
    SELECT `index`, title, type, area, averge_price, comment_count, favorite_count
    FROM data
    WHERE 1=1
    """
    params = []
    if keyword:
        sql += " AND (title LIKE %s OR type LIKE %s OR area LIKE %s)"
        like_kw = f'%{keyword}%'
        params += [like_kw, like_kw, like_kw]
    if min_price:
        sql += " AND CAST(REPLACE(REPLACE(averge_price, '￥', ''), '元', '') AS DECIMAL) >= %s"
        params.append(min_price)
    if max_price:
        sql += " AND CAST(REPLACE(REPLACE(averge_price, '￥', ''), '元', '') AS DECIMAL) <= %s"
        params.append(max_price)
    sql += " LIMIT 30"
    shops = db.query(sql, *params)
    db.close()
    # 转为字典列表
    shop_list = []
    for s in shops:
        shop_list.append({
            'index': s[0],
            'title': s[1],
            'type': s[2],
            'area': s[3],
            'averge_price': s[4],
            'comment_count': s[5],
            'favorite_count': s[6]
        })
    return jsonify({'shops': shop_list})

@app.route('/api/food_detail', methods=['POST'])
def api_food_detail():
    data = request.get_json()
    food_id = data.get('food_id')
    db = dbUtil()
    sql = """
    SELECT `index`, title, comment_count, averge_price, type, area, recommend, group_purchase, preferential, favorite_count
    FROM data
    WHERE `index`=%s
    """
    food = db.query(sql, food_id)
    db.close()
    if not food:
        return jsonify({'success': False, 'msg': '美食不存在'})
    food = food[0]
    return jsonify({
        'success': True,
        'food': {
            'id': food[0],
            'name': food[1],
            'comment_count': food[2],
            'price': food[3],
            'type': food[4],
            'area': food[5],
            'recommend': food[6],
            'group_purchase': food[7],
            'preferential': food[8],
            'favorite_count': food[9]
        }
    })

@app.route('/api/all_shops')
def all_shops():
    db = dbUtil()
    sql = "SELECT `index`, title FROM data"
    shops = db.query(sql)
    db.close()
    return jsonify([{'id': s[0], 'title': s[1]} for s in shops])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

