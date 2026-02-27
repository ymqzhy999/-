from utils import dbUtil
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


# 用户登录业务
def get_user(account, password, name):
    print(f"SQL参数: account={account}, password={password}, name={name}")
    sql = "select id, type, name from user where account=%s and password=%s and name=%s"
    db = dbUtil()
    res = db.query(sql, account, password, name)
    print(f"SQL结果: {res}")
    db.close()
    return res


# 用户注册业务
def add_user(name, account, password, company, phone, mail, type):
    db = dbUtil()
    # 判断账号是否存在
    exit_sql = "select count(id) from `user` where account=%s"
    exit_res = db.query(exit_sql, account)
    if exit_res[0][0] > 0:
        return "300"
    else:
        sql = """
        insert into `user`
        (id, name, account, password, company, phone, mail, type, status, avatar, favorites)
        VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, 1, NULL, NULL)
        """
        res = db.query(sql, name, account, password, company, phone, mail, type)
        db.close()
        return "200"

def record_user_behavior(user_id, item_id, behavior_type):
    """记录用户行为
    behavior_type: 1-浏览 2-收藏 3-购买
    """
    db = dbUtil()
    sql = """
    INSERT INTO user_behavior (user_id, item_id, behavior_type)
    VALUES (%s, %s, %s)
    """
    try:
        db.query(sql, user_id, item_id, behavior_type)
        db.close()
        return True
    except Exception as e:
        print(f"记录用户行为失败: {e}")
        db.close()
        return False

def get_user_recommendations(user_id, limit=5):
    """获取用户推荐
    基于协同过滤算法，推荐用户可能感兴趣的商品
    """
    db = dbUtil()
    
    # 1. 获取所有用户行为数据
    sql = """
    SELECT user_id, item_id, behavior_type, COUNT(*) as weight
    FROM user_behavior
    GROUP BY user_id, item_id, behavior_type
    """
    behaviors = db.query(sql)
    
    if not behaviors:
        return []
    
    # 2. 构建用户-物品矩阵
    df = pd.DataFrame(behaviors, columns=['user_id', 'item_id', 'behavior_type', 'weight'])
    
    # 行为权重：浏览=1，收藏=2，购买=3
    df['score'] = df['behavior_type'] * df['weight']
    
    # 构建用户-物品矩阵
    user_item_matrix = df.pivot_table(
        index='user_id',
        columns='item_id',
        values='score',
        fill_value=0
    )
    
    # 3. 计算用户相似度
    user_similarity = cosine_similarity(user_item_matrix)
    user_similarity_df = pd.DataFrame(
        user_similarity,
        index=user_item_matrix.index,
        columns=user_item_matrix.index
    )
    
    # 4. 获取目标用户的相似用户
    if user_id not in user_similarity_df.index:
        return []
    
    similar_users = user_similarity_df[user_id].sort_values(ascending=False)[1:6]
    
    # 5. 获取推荐物品
    user_items = user_item_matrix.loc[user_id]
    similar_user_items = user_item_matrix.loc[similar_users.index]
    
    # 计算推荐分数
    recommendations = []
    for item in user_item_matrix.columns:
        if user_items[item] == 0:  # 用户未交互过的物品
            score = 0
            for similar_user in similar_users.index:
                score += similar_users[similar_user] * similar_user_items.loc[similar_user, item]
            if score > 0:
                recommendations.append((item, score))
    
    # 6. 获取推荐物品的详细信息
    if not recommendations:
        return []
    
    recommendations.sort(key=lambda x: x[1], reverse=True)
    recommended_items = [item[0] for item in recommendations[:limit]]
    
    # 获取推荐美食/店铺的详细信息
    items_sql = """
    SELECT `index`, title, type, area, averge_price, comment_count, favorite_count
    FROM data
    WHERE `index` IN %s
    """
    items_info = db.query(items_sql, tuple(recommended_items))
    
    db.close()
    return items_info

def get_user_behavior_history(user_id):
    """获取用户行为历史"""
    db = dbUtil()
    sql = """
    SELECT b.item_id, b.behavior_type, b.behavior_time, d.title as item_name
    FROM user_behavior b
    JOIN data d ON b.item_id = d.`index`
    WHERE b.user_id = %s
    ORDER BY b.behavior_time DESC
    LIMIT 10
    """
    history = db.query(sql, user_id)
    db.close()
    return history
