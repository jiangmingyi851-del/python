import requests
import time
import logging
import json
import threading
from urllib.parse import urljoin
from datetime import datetime
import curses
import sys
import re

class PKUCourseSelector:
    def __init__(self, username, password):
        self.username = 'username'
        self.password = 'password'
        self.session = requests.Session()
        self.base_url = "https://elective"  # 假设的选课系统地址
        self.is_logged_in = False
        self.refresh_interval = 5  # 默认5秒刷新一次
        self.course_targets = []  # 要抢的课程列表，包含优先级信息
        self.is_running = False
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.status_messages = []
        self.successful_selections = []
        self.captcha_count = 0
        
        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("course_selector.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def add_status_message(self, message):
        """添加状态消息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_messages.append(f"[{timestamp}] {message}")
        # 只保留最近20条消息
        if len(self.status_messages) > 20:
            self.status_messages = self.status_messages[-20:]
        self.logger.info(message)
    
    def login(self):
        """登录选课系统"""
        login_url = urljoin(self.base_url, "/login")
        login_data = {
            'username': self.username,
            'password': self.password
        }
        
        try:
            self.add_status_message("尝试登录选课系统...")
            response = self.session.post(login_url, data=login_data, headers=self.headers)
            if "登录成功" in response.text or response.status_code == 200:
                self.is_logged_in = True
                self.add_status_message("登录成功")
                return True
            else:
                self.add_status_message("登录失败，请检查用户名和密码")
                return False
        except Exception as e:
            self.add_status_message(f"登录过程中发生错误: {str(e)}")
            return False
    
    def load_course_targets(self, course_list):
        """加载目标课程列表，课程列表应包含优先级"""
        # 按优先级排序（数字越小优先级越高）
        self.course_targets = sorted(course_list, key=lambda x: x['priority'])
        self.add_status_message(f"已加载 {len(course_list)} 门目标课程，按优先级排序")
    
    def get_course_list(self):
        """获取可选课程列表（模拟函数）"""
        # 这里应该是从选课系统获取真实课程列表的代码
        # 为了演示，我们返回一个模拟的课程列表
        return [
            {"id": "CS101", "name": "计算机科学导论", "teachers": ["张老师", "李老师"], "available": True},
            {"id": "MATH202", "name": "高等数学", "teachers": ["王老师", "赵老师"], "available": False},
            {"id": "PHYS301", "name": "大学物理", "teachers": ["刘老师", "陈老师"], "available": True},
            {"id": "ENG401", "name": "学术英语", "teachers": ["周老师", "钱老师"], "available": True}
        ]
    
    def check_course_availability(self, course_id, teacher=None):
        """检查课程是否有空位，可以指定教师"""
        check_url = urljoin(self.base_url, f"/course/{course_id}/status")
        try:
            response = self.session.get(check_url, headers=self.headers)
            data = response.json()
            
            # 如果有指定教师，检查该教师的课程是否可用
            if teacher and 'classes' in data:
                for class_info in data['classes']:
                    if class_info['teacher'] == teacher and class_info['available']:
                        return True
                return False
            
            return data.get('available', False)
        except Exception as e:
            self.add_status_message(f"检查课程 {course_id} 时发生错误: {str(e)}")
            return False
    
    def pre_select_course(self, course_id, teacher=None):
        """预选课程，可以指定教师"""
        select_url = urljoin(self.base_url, f"/course/{course_id}/preselect")
        select_data = {}
        
        if teacher:
            select_data['teacher'] = teacher
        
        try:
            response = self.session.post(select_url, data=select_data, headers=self.headers)
            if "预选成功" in response.text:
                self.add_status_message(f"成功预选课程 {course_id}{f'（{teacher}）' if teacher else ''}!")
                self.successful_selections.append({
                    'course_id': course_id,
                    'teacher': teacher,
                    'time': datetime.now().strftime("%H:%M:%S")
                })
                return True
            else:
                # 尝试解析错误信息
                error_match = re.search(r'错误原因：(.*?)<', response.text)
                error_msg = error_match.group(1) if error_match else "未知错误"
                self.add_status_message(f"预选课程 {course_id} 失败: {error_msg}")
                return False
        except Exception as e:
            self.add_status_message(f"预选过程中发生错误: {str(e)}")
            return False
    
    def start_monitoring(self, stdscr):
        """开始监控课程"""
        if not self.is_logged_in:
            self.add_status_message("请先登录!")
            return
        
        self.is_running = True
        self.add_status_message("开始监控课程...")
        
        # 创建刷新计数
        refresh_count = 0
        
        while self.is_running:
            refresh_count += 1
            self.add_status_message(f"第 {refresh_count} 次刷新课程列表")
            
            # 获取当前课程列表
            # 在实际应用中，这里应该调用选课系统的API
            # current_courses = self.get_course_list()
            
            # 按优先级检查所有目标课程
            for course_info in self.course_targets:
                if not self.is_running:
                    break
                
                course_id = course_info['id']
                teacher = course_info.get('teacher')
                priority = course_info.get('priority', 99)
                
                self.add_status_message(f"检查课程 {course_id} (优先级: {priority}) 的空位情况...")
                
                if self.check_course_availability(course_id, teacher):
                    self.add_status_message(f"课程 {course_id}{f'（{teacher}）' if teacher else ''} 有空位，尝试预选...")
                    if self.pre_select_course(course_id, teacher):
                        # 选课成功，从目标列表中移除
                        self.course_targets.remove(course_info)
                        if not self.course_targets:
                            self.add_status_message("所有目标课程已选完，停止监控")
                            self.stop_monitoring()
                            return
                
                # 更新显示
                self.display_status(stdscr)
                
                # 等待下一次检查
                for i in range(self.refresh_interval):
                    if not self.is_running:
                        break
                    time.sleep(1)
                    # 每秒更新一次倒计时显示
                    self.display_status(stdscr, countdown=self.refresh_interval - i)
    
    def stop_monitoring(self):
        """停止监控"""
        self.is_running = False
        self.add_status_message("已停止监控")
    
    def set_refresh_interval(self, interval):
        """设置刷新间隔"""
        self.refresh_interval = interval
        self.add_status_message(f"刷新间隔设置为 {interval} 秒")
    
    def display_status(self, stdscr, countdown=None):
        """在终端显示当前状态"""
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # 显示标题
        title = "北京大学选课助手"
        stdscr.addstr(0, (width - len(title)) // 2, title, curses.A_BOLD)
        
        # 显示刷新间隔和倒计时
        refresh_info = f"刷新间隔: {self.refresh_interval} 秒"
        if countdown is not None:
            refresh_info += f" | 下次刷新: {countdown} 秒"
        stdscr.addstr(2, 2, refresh_info)
        
        # 显示登录状态
        login_status = "已登录" if self.is_logged_in else "未登录"
        stdscr.addstr(2, width - len(login_status) - 2, login_status)
        
        # 显示监控状态
        monitor_status = "监控中..." if self.is_running else "已停止"
        stdscr.addstr(3, 2, f"状态: {monitor_status}")
        
        # 显示剩余目标课程
        stdscr.addstr(5, 2, "目标课程 (按优先级排序):")
        for i, course in enumerate(self.course_targets, 1):
            course_info = f"{i}. {course['id']}"
            if 'name' in course:
                course_info += f" - {course['name']}"
            if 'teacher' in course:
                course_info += f" ({course['teacher']})"
            course_info += f" [优先级: {course.get('priority', 99)}]"
            
            if i + 6 < height:
                stdscr.addstr(5 + i, 4, course_info)
        
        # 显示成功选中的课程
        if self.successful_selections:
            stdscr.addstr(5 + len(self.course_targets) + 2, 2, "成功选中的课程:")
            for i, selection in enumerate(self.successful_selections, 1):
                selection_info = f"{i}. {selection['course_id']}"
                if selection['teacher']:
                    selection_info += f" ({selection['teacher']})"
                selection_info += f" - {selection['time']}"
                
                if 5 + len(self.course_targets) + 3 + i < height:
                    stdscr.addstr(5 + len(self.course_targets) + 3 + i, 4, selection_info)
        
        # 显示状态消息
        msg_start_line = max(5 + len(self.course_targets) + len(self.successful_selections) + 5, 10)
        stdscr.addstr(msg_start_line, 2, "最近状态:")
        
        for i, msg in enumerate(self.status_messages[-min(10, height - msg_start_line - 2):]):
            if msg_start_line + i + 1 < height:
                # 根据消息类型使用不同的颜色
                if "成功" in msg or "选完" in msg:
                    stdscr.addstr(msg_start_line + i + 1, 4, msg, curses.COLOR_GREEN)
                elif "错误" in msg or "失败" in msg:
                    stdscr.addstr(msg_start_line + i + 1, 4, msg, curses.COLOR_RED)
                else:
                    stdscr.addstr(msg_start_line + i + 1, 4, msg)
        
        # 显示操作提示
        if height > 2:
            help_text = "按 'q' 停止监控并退出"
            stdscr.addstr(height - 1, 2, help_text)
        
        stdscr.refresh()

def main(stdscr):
    # 初始化颜色
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    
    # 创建选课助手实例
    selector = PKUCourseSelector("你的学号", "你的密码")
    
    # 登录
    if selector.login():
        # 设置要抢的课程列表（包含优先级和可选教师）
        target_courses = [
            {"id": "CS101", "name": "计算机科学导论", "teacher": "张老师", "priority": 1},
            {"id": "MATH202", "name": "高等数学", "teacher": "王老师", "priority": 2},
            {"id": "PHYS301", "name": "大学物理", "teacher": "刘老师", "priority": 3},
            {"id": "ENG401", "name": "学术英语", "priority": 4}  # 不指定教师
        ]
        selector.load_course_targets(target_courses)
        
        # 设置刷新频率（秒）
        selector.set_refresh_interval(10)
        
        # 创建监控线程
        monitor_thread = threading.Thread(target=selector.start_monitoring, args=(stdscr,))
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # 显示初始状态
        selector.display_status(stdscr)
        
        # 主循环处理键盘输入
        while selector.is_running:
            # 检查键盘输入
            key = stdscr.getch()
            if key == ord('q'):
                selector.stop_monitoring()
                break
            
            # 更新显示
            selector.display_status(stdscr)
            time.sleep(0.1)
        
        # 等待监控线程结束
        monitor_thread.join(timeout=1.0)
    
    # 显示最终状态
    selector.add_status_message("程序结束")
    selector.display_status(stdscr)
    stdscr.getch()  # 等待用户按键退出

if __name__ == "__main__":
    # 使用curses包装main函数
    curses.wrapper(main)
