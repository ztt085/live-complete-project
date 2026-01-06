# 导入所有必要依赖（确保已通过PyCharm安装，无缺失）
from flask import Flask, jsonify, request
from faker import Faker
from flask_cors import CORS
import random
from datetime import datetime, timedelta

# ---------------------- 初始化配置（核心：Flask应用 + 跨域配置，适配PyCharm调试） ----------------------
# 初始化Flask应用，PyCharm 2.9.1可识别app实例，提供代码提示
app = Flask(__name__)

# 配置跨域：支持所有来源，适配本地前端/网关联调，无CORS报错
# PyCharm 2.9.1可识别flask-cors配置，无语法警告
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

# 初始化Faker：生成中文模拟数据，避免乱码，贴合业务场景
fake = Faker(locale="zh_CN")


# ---------------------- 核心Mock接口实现（覆盖前端主要业务，返回标准JSON，可直接运行） ----------------------
# 接口1：健康检查（验证后端服务，PyCharm调试时可快速验证）
@app.route("/api/health", methods=["GET"])
def health_check():
    """后端服务健康检查接口（PyCharm 2.9.1可识别文档字符串，鼠标悬浮显示说明）"""
    response = {
        "code": 200,  # 业务状态码（200=成功，500=失败）
        "message": "success",  # 业务提示信息
        "data": {  # 业务数据体
            "service": "live-backend",
            "status": "running",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }
    return jsonify(response)


# 接口2：获取当前登录用户信息（前端个人中心场景）
@app.route("/api/user/info", methods=["GET"])
def get_user_info():
    """获取用户基本信息接口"""
    # 生成Mock用户数据（Faker+固定结构，格式统一）
    user_data = {
        "userId": fake.uuid4(),  # 唯一用户ID
        "username": fake.user_name(),  # 登录用户名
        "nickname": fake.name(),  # 用户昵称
        "avatar": fake.image_url(200, 200),  # 用户头像（有效图片链接）
        "email": fake.email(),  # 邮箱
        "phone": fake.phone_number(),  # 手机号码
        "gender": random.choice([0, 1, 2]),  # 性别（0=未知，1=男，2=女）
        "level": random.randint(1, 10),  # 用户等级
        "createTime": fake.date_time_this_year().strftime("%Y-%m-%d %H:%M:%S")
    }

    # 构造标准JSON返回结果
    response = {
        "code": 200,
        "message": "获取用户信息成功",
        "data": user_data
    }
    return jsonify(response)


# 接口3：获取直播列表（分页功能，前端核心场景）
@app.route("/api/live/list", methods=["GET"])
def get_live_list():
    """获取直播列表接口（支持page/size分页参数）"""
    # 接收前端分页参数（默认值：第1页，每页10条）
    page = request.args.get("page", 1, type=int)
    size = request.args.get("size", 10, type=int)

    # 生成批量Mock直播数据
    live_records = []
    for _ in range(size):
        # 随机生成直播状态（0=未开始，1=直播中，2=已结束）
        live_status = random.choice([0, 1, 2])

        # 生成合理的直播时间
        start_time = fake.date_time_this_week()
        end_time = start_time + timedelta(hours=random.randint(1, 6)) if live_status == 2 else None

        # 单条直播数据结构
        live_item = {
            "liveId": fake.uuid4(),  # 唯一直播ID
            "title": fake.sentence(nb_words=5),  # 直播标题
            "anchorName": fake.name(),  # 主播昵称
            "anchorAvatar": fake.image_url(100, 100),  # 主播头像
            "coverImage": fake.image_url(640, 360),  # 直播封面图
            "viewCount": random.randint(100, 100000),  # 观看人数
            "likeCount": random.randint(50, 50000),  # 点赞人数
            "commentCount": random.randint(10, 10000),  # 评论数
            "status": live_status,  # 直播状态
            "startTime": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "endTime": end_time.strftime("%Y-%m-%d %H:%M:%S") if end_time else None,
            "category": random.choice(["游戏", "娱乐", "教育", "美食", "户外"])
        }
        live_records.append(live_item)

    # 构造分页返回结果
    total_records = 100
    total_pages = (total_records + size - 1) // size  # 向上取整计算总页数

    response = {
        "code": 200,
        "message": "获取直播列表成功",
        "data": {
            "records": live_records,
            "total": total_records,
            "page": page,
            "size": size,
            "pages": total_pages
        }
    }
    return jsonify(response)


# 接口4：创建直播（POST请求，接收前端JSON参数）
@app.route("/api/live/create", methods=["POST"])
def create_live():
    """创建直播接口（接收前端提交的标题/分类参数）"""
    # 接收前端JSON数据（兜底空字典，避免PyCharm调试时报错）
    req_json = request.get_json() or {}

    # 提取前端参数（无参数时用Mock数据兜底）
    live_title = req_json.get("title", fake.sentence(nb_words=5))
    live_category = req_json.get("category", random.choice(["游戏", "娱乐", "教育", "美食", "户外"]))

    # 构造创建成功结果
    create_result = {
        "liveId": fake.uuid4(),
        "title": live_title,
        "category": live_category,
        "createTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": 0  # 未开始状态
    }

    response = {
        "code": 200,
        "message": "直播创建成功",
        "data": create_result
    }
    return jsonify(response)


# 接口5：获取单场直播详情（路径参数传递直播ID）
@app.route("/api/live/detail/<live_id>", methods=["GET"])
def get_live_detail(live_id):
    """获取单场直播详情接口（根据直播ID返回数据）"""
    # 生成直播详情数据（与请求ID保持一致）
    live_detail = {
        "liveId": live_id,
        "title": fake.sentence(nb_words=5),
        "anchorName": fake.name(),
        "anchorAvatar": fake.image_url(100, 100),
        "anchorId": fake.uuid4(),
        "coverImage": fake.image_url(640, 360),
        "viewCount": random.randint(100, 100000),
        "likeCount": random.randint(50, 50000),
        "commentCount": random.randint(10, 10000),
        "status": random.choice([0, 1, 2]),
        "startTime": fake.date_time_this_week().strftime("%Y-%m-%d %H:%M:%S"),
        "endTime": fake.date_time_this_week().strftime("%Y-%m-%d %H:%M:%S") if random.choice([True, False]) else None,
        "category": random.choice(["游戏", "娱乐", "教育", "美食", "户外"]),
        "description": fake.paragraph(nb_sentences=3),
        "tags": [fake.word() for _ in range(random.randint(2, 5))]
    }

    response = {
        "code": 200,
        "message": "获取直播详情成功",
        "data": live_detail
    }
    return jsonify(response)


# ---------------------- 启动配置（适配PyCharm 2.9.1调试，可直接运行） ----------------------
if __name__ == "__main__":
    # 本地调试模式：监听所有网卡，端口5000，开启自动重启
    app.run(
        host="0.0.0.0",  # 允许局域网访问，方便前端联调
        port=5000,  # 固定端口，PyCharm调试时可快速访问
        debug=True  # 调试模式：修改代码后PyCharm可自动重启服务（适配2.9.1）
    )