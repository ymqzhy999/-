-- 创建用户行为记录表
CREATE TABLE IF NOT EXISTS user_behavior (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    item_id INT NOT NULL,
    behavior_type INT NOT NULL COMMENT '1:浏览 2:收藏 3:购买',
    behavior_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户行为记录表';

-- 添加索引
CREATE INDEX idx_user_behavior ON user_behavior(user_id, item_id, behavior_type);
CREATE INDEX idx_behavior_time ON user_behavior(behavior_time); 