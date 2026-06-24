SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

CREATE DATABASE IF NOT EXISTS shop_ecommerce DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE shop_ecommerce;

-- 1. 用户表
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '用户主键ID',
  `username` VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
  `password` VARCHAR(255) NOT NULL COMMENT '密码(加密)',
  `email` VARCHAR(100) NOT NULL UNIQUE COMMENT '邮箱',
  `phone` VARCHAR(20) COMMENT '手机号',
  `avatar` VARCHAR(255) COMMENT '头像URL',
  `nickname` VARCHAR(50) COMMENT '昵称',
  `gender` TINYINT(1) DEFAULT 0 COMMENT '性别: 0未知, 1男, 2女',
  `birth_date` DATE COMMENT '出生日期',
  `register_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
  `last_login_time` DATETIME COMMENT '最后登录时间',
  `status` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '状态: 0禁用, 1启用',
  `level` INT(11) DEFAULT 1 COMMENT '用户等级',
  `points` INT(11) DEFAULT 0 COMMENT '积分',
  PRIMARY KEY (`id`),
  INDEX `idx_username` (`username`),
  INDEX `idx_email` (`email`),
  INDEX `idx_phone` (`phone`)
) ENGINE = InnoDB AUTO_INCREMENT = 10001 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '用户信息表';

-- 2. 商品分类表
DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '分类主键ID',
  `name` VARCHAR(50) NOT NULL COMMENT '分类名称',
  `parent_id` INT(11) DEFAULT 0 COMMENT '父分类ID',
  `icon` VARCHAR(255) COMMENT '分类图标',
  `sort_order` INT(11) DEFAULT 0 COMMENT '排序号',
  `status` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '状态: 0禁用, 1启用',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` DATETIME ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  INDEX `idx_parent_id` (`parent_id`),
  INDEX `idx_sort_order` (`sort_order`)
) ENGINE = InnoDB AUTO_INCREMENT = 101 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '商品分类表';

-- 3. 商品品牌表
DROP TABLE IF EXISTS `brands`;
CREATE TABLE `brands` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '品牌主键ID',
  `name` VARCHAR(100) NOT NULL COMMENT '品牌名称',
  `logo` VARCHAR(255) COMMENT '品牌Logo',
  `description` TEXT COMMENT '品牌描述',
  `sort_order` INT(11) DEFAULT 0 COMMENT '排序号',
  `status` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '状态: 0禁用, 1启用',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  INDEX `idx_name` (`name`)
) ENGINE = InnoDB AUTO_INCREMENT = 101 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '商品品牌表';

-- 4. 商品表
DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '商品主键ID',
  `name` VARCHAR(200) NOT NULL COMMENT '商品名称',
  `category_id` INT(11) NOT NULL COMMENT '分类ID',
  `brand_id` INT(11) COMMENT '品牌ID',
  `price` DECIMAL(10,2) NOT NULL COMMENT '售价',
  `original_price` DECIMAL(10,2) COMMENT '原价',
  `cost_price` DECIMAL(10,2) COMMENT '成本价',
  `stock` INT(11) NOT NULL DEFAULT 0 COMMENT '库存数量',
  `sales` INT(11) NOT NULL DEFAULT 0 COMMENT '销量',
  `rating` DECIMAL(3,1) DEFAULT 0 COMMENT '评分(0-5)',
  `review_count` INT(11) DEFAULT 0 COMMENT '评价数量',
  `weight` DECIMAL(6,2) COMMENT '重量(kg)',
  `is_hot` TINYINT(1) DEFAULT 0 COMMENT '是否热销: 0否, 1是',
  `is_new` TINYINT(1) DEFAULT 0 COMMENT '是否新品: 0否, 1是',
  `is_on_sale` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否上架: 0下架, 1在售',
  `description` LONGTEXT COMMENT '商品详情(富文本)',
  `specifications` TEXT COMMENT '规格参数(JSON)',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` DATETIME ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  INDEX `idx_category_id` (`category_id`),
  INDEX `idx_brand_id` (`brand_id`),
  INDEX `idx_price` (`price`),
  INDEX `idx_sales` (`sales`),
  INDEX `idx_is_on_sale` (`is_on_sale`),
  FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`),
  FOREIGN KEY (`brand_id`) REFERENCES `brands` (`id`)
) ENGINE = InnoDB AUTO_INCREMENT = 10001 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '商品信息表';

-- 5. 商品图片表
DROP TABLE IF EXISTS `product_images`;
CREATE TABLE `product_images` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '图片主键ID',
  `product_id` BIGINT UNSIGNED NOT NULL COMMENT '商品ID',
  `image_url` VARCHAR(500) NOT NULL COMMENT '图片URL',
  `is_main` TINYINT(1) DEFAULT 0 COMMENT '是否主图: 0否, 1是',
  `sort_order` INT(11) DEFAULT 0 COMMENT '排序号',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  INDEX `idx_product_id` (`product_id`),
  INDEX `idx_is_main` (`is_main`),
  FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 10001 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '商品图片表';

-- 6. 收货地址表
DROP TABLE IF EXISTS `addresses`;
CREATE TABLE `addresses` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '地址主键ID',
  `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
  `consignee` VARCHAR(50) NOT NULL COMMENT '收货人',
  `phone` VARCHAR(20) NOT NULL COMMENT '手机号',
  `province` VARCHAR(50) NOT NULL COMMENT '省份',
  `city` VARCHAR(50) NOT NULL COMMENT '城市',
  `district` VARCHAR(50) COMMENT '区县',
  `detail` VARCHAR(500) NOT NULL COMMENT '详细地址',
  `is_default` TINYINT(1) DEFAULT 0 COMMENT '是否默认: 0否, 1是',
  `status` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '状态: 0删除, 1有效',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` DATETIME ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  INDEX `idx_user_id` (`user_id`),
  INDEX `idx_is_default` (`is_default`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 10001 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '收货地址表';

-- 7. 订单表
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `id` VARCHAR(32) NOT NULL COMMENT '订单编号',
  `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
  `address_id` BIGINT UNSIGNED NOT NULL COMMENT '收货地址ID',
  `total_amount` DECIMAL(12,2) NOT NULL COMMENT '订单总金额',
  `discount_amount` DECIMAL(12,2) DEFAULT 0 COMMENT '优惠金额',
  `pay_amount` DECIMAL(12,2) NOT NULL COMMENT '实付金额',
  `pay_method` VARCHAR(20) COMMENT '支付方式: wechat, alipay, bank',
  `pay_time` DATETIME COMMENT '支付时间',
  `status` VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT '订单状态: pending待付款, paid待发货, shipped待收货, completed已完成, canceled已取消',
  `status_text` VARCHAR(50) NOT NULL DEFAULT '待付款' COMMENT '状态文本',
  `remark` TEXT COMMENT '订单备注',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` DATETIME ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  INDEX `idx_user_id` (`user_id`),
  INDEX `idx_address_id` (`address_id`),
  INDEX `idx_status` (`status`),
  INDEX `idx_create_time` (`create_time`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  FOREIGN KEY (`address_id`) REFERENCES `addresses` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '订单表';

-- 8. 订单明细表
DROP TABLE IF EXISTS `order_items`;
CREATE TABLE `order_items` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '明细主键ID',
  `order_id` VARCHAR(32) NOT NULL COMMENT '订单编号',
  `product_id` BIGINT UNSIGNED NOT NULL COMMENT '商品ID',
  `product_name` VARCHAR(200) NOT NULL COMMENT '商品名称',
  `product_image` VARCHAR(500) COMMENT '商品图片',
  `price` DECIMAL(10,2) NOT NULL COMMENT '购买单价',
  `quantity` INT(11) NOT NULL DEFAULT 1 COMMENT '购买数量',
  `subtotal` DECIMAL(12,2) NOT NULL COMMENT '小计金额',
  `spec_info` VARCHAR(200) COMMENT '规格信息',
  PRIMARY KEY (`id`),
  INDEX `idx_order_id` (`order_id`),
  INDEX `idx_product_id` (`product_id`),
  FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE = InnoDB AUTO_INCREMENT = 10001 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '订单明细表';

-- 9. 购物车表
DROP TABLE IF EXISTS `carts`;
CREATE TABLE `carts` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '购物车主键ID',
  `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
  `product_id` BIGINT UNSIGNED NOT NULL COMMENT '商品ID',
  `quantity` INT(11) NOT NULL DEFAULT 1 COMMENT '数量',
  `selected` TINYINT(1) DEFAULT 1 COMMENT '是否选中: 0否, 1是',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` DATETIME ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  INDEX `idx_user_id` (`user_id`),
  INDEX `idx_product_id` (`product_id`),
  UNIQUE INDEX `uk_user_product` (`user_id`, `product_id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 10001 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '购物车表';

-- 10. 商品评价表
DROP TABLE IF EXISTS `reviews`;
CREATE TABLE `reviews` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '评价主键ID',
  `order_id` VARCHAR(32) COMMENT '订单编号',
  `product_id` BIGINT UNSIGNED NOT NULL COMMENT '商品ID',
  `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
  `rating` TINYINT(1) NOT NULL COMMENT '评分(1-5)',
  `content` TEXT COMMENT '评价内容',
  `images` TEXT COMMENT '评价图片(JSON数组)',
  `is_anonymous` TINYINT(1) DEFAULT 0 COMMENT '是否匿名: 0否, 1是',
  `is_show` TINYINT(1) DEFAULT 1 COMMENT '是否显示: 0隐藏, 1显示',
  `reply` TEXT COMMENT '商家回复',
  `reply_time` DATETIME COMMENT '回复时间',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  INDEX `idx_order_id` (`order_id`),
  INDEX `idx_product_id` (`product_id`),
  INDEX `idx_user_id` (`user_id`),
  INDEX `idx_rating` (`rating`),
  FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
  FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE = InnoDB AUTO_INCREMENT = 10001 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '商品评价表';

SET FOREIGN_KEY_CHECKS = 1;