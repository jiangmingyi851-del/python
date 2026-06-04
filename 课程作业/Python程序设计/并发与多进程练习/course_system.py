# 将上面的 course_system.py 完整代码粘贴到此处（注意缩进）
"""
课程选课系统 - 整合版
支持通过命令行参数选择运行服务端或客户端
"""

import sys
import time
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor

# 服务端依赖
try:
    from flask import Flask, request, jsonify
except ImportError:
    print("服务端需要 Flask 库，请执行：pip install flask")
    sys.exit(1)

# 客户端依赖
try:
    import httpx
except ImportError:
    print("客户端需要 httpx 库，请执行：pip install httpx")
    sys.exit(1)

# ==================== 服务端代码 ====================
app = Flask(__name__)

# 模拟数据库
courses = {
    "C01": {"name": "Python并发编程", "capacity": 3, "current": 0, "credits": 2},
    "C02": {"name": "微服务架构", "capacity": 2, "current": 0, "credits": 3},
    "C03": {"name": "大学物理", "capacity": 10, "current": 0, "credits": 4}
}

students = {
    "S001": {"name": "小明", "selected": [], "credits_left": 5}
}

data_lock = threading.Lock()
executor = ThreadPoolExecutor(max_workers=5)


@app.route('/status', methods=['GET'])
def get_status():
    """查询所有课程现有人数"""
    return jsonify({"courses": courses})


@app.route('/my_info', methods=['GET'])
def get_my_info():
    """查询个人已选课程和剩余学分"""
    sid = request.args.get("sid")
    student = students.get(sid)
    if not student:
        return jsonify({"error": "学生不存在"}), 404
    return jsonify(student)


def process_add(sid, cid):
    with data_lock:
        student = students.get(sid)
        course = courses.get(cid)

        if not student or not course:
            return {"status": "失败", "msg": "学生或课程ID无效"}
        if cid in student['selected']:
            return {"status": "失败", "msg": "已选过该课程"}
        if course['current'] >= course['capacity']:
            return {"status": "失败", "msg": "课程名额已满"}
        if student['credits_left'] < course['credits']:
            return {"status": "失败", "msg": "学分不足，无法补选"}

        # 模拟处理延迟
        time.sleep(0.5)

        course['current'] += 1
        student['selected'].append(cid)
        student['credits_left'] -= course['credits']
        return {"status": "成功", "msg": f"补选 {course['name']} 成功"}


def process_drop(sid, cid):
    with data_lock:
        student = students.get(sid)
        course = courses.get(cid)

        if not student or cid not in student['selected']:
            return {"status": "失败", "msg": "未选修此课程，无法退选"}

        time.sleep(0.3)

        course['current'] -= 1
        student['selected'].remove(cid)
        student['credits_left'] += course['credits']
        return {"status": "成功", "msg": f"退选 {course['name']} 成功"}


@app.route('/add', methods=['POST'])
def add_course():
    data = request.json
    future = executor.submit(process_add, data['sid'], data['cid'])
    return jsonify(future.result())


@app.route('/drop', methods=['POST'])
def drop_course():
    data = request.json
    future = executor.submit(process_drop, data['sid'], data['cid'])
    return jsonify(future.result())


def run_server():
    """启动服务端"""
    print("服务器启动：处理选课线程池已就绪...")
    app.run(port=5000)


# ==================== 客户端代码 ====================
SERVER_URL = "http://127.0.0.1:5000"
STUDENT_ID = "S001"


async def fetch_status(client):
    """协程：查询课程现状"""
    resp = await client.get(f"{SERVER_URL}/status")
    data = resp.json()
    print("\n--- 课程当前状态 ---")
    for cid, info in data['courses'].items():
        print(f"ID:{cid} | {info['name']} | 人数:{info['current']}/{info['capacity']} | 学分:{info['credits']}")


async def fetch_my_info(client):
    """协程：查询个人信息"""
    resp = await client.get(f"{SERVER_URL}/my_info", params={"sid": STUDENT_ID})
    data = resp.json()
    print(f"\n[我的信息] 已选代码: {data['selected']} | 剩余学分: {data['credits_left']}")


async def operate_course(client, action, cid):
    """协程：执行补/退选动作"""
    url = f"{SERVER_URL}/{action}"
    payload = {"sid": STUDENT_ID, "cid": cid}
    resp = await client.post(url, json=payload)
    result = resp.json()
    print(f"\n>>> 操作结果 [{action}]: {result['status']} - {result['msg']}")


async def main_client():
    """客户端主协程"""
    async with httpx.AsyncClient() as client:
        while True:
            print("\n========== 学生选课系统 (协程客户端) ==========")
            print("1. 查看课程表  2. 补选课程  3. 退选课程  4. 查看我的课表  5. 退出")
            choice = input("请输入操作编号: ")

            if choice == '1':
                await fetch_status(client)
            elif choice == '2':
                cid = input("输入要补选的课程ID: ")
                await operate_course(client, "add", cid)
            elif choice == '3':
                cid = input("输入要退选的课程ID: ")
                await operate_course(client, "drop", cid)
            elif choice == '4':
                await fetch_my_info(client)
            elif choice == '5':
                break
            else:
                print("无效输入")


def run_client():
    """启动客户端"""
    try:
        asyncio.run(main_client())
    except KeyboardInterrupt:
        print("\n客户端退出")


# ==================== 主入口 ====================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("请指定运行模式：server 或 client")
        print("示例：")
        print("  python course_system.py server   # 启动服务端")
        print("  python course_system.py client   # 启动客户端")
        sys.exit(1)

    mode = sys.argv[1].lower()
    if mode == "server":
        run_server()
    elif mode == "client":
        run_client()
    else:
        print("无效模式，请使用 server 或 client")
        run_server()
        sys.exit(1)
