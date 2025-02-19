# Chat Room Application | 聊天室应用

A real-time chat application based on Flask and Socket.IO, supporting private chat, group chat, emoji reactions, and file sharing.

基于 Flask 和 Socket.IO 的实时聊天应用，支持私聊、群聊、表情回应和文件共享。

## Features | 功能特点

- Nickname-based login without password | 无需密码的昵称登录系统
- Private and group chat support | 支持私聊和群聊
- Real-time message delivery | 实时消息推送
- Emoji reactions and file sharing | 支持表情回应和文件分享
- Message recall within 2 minutes | 2分钟内可撤回消息
- Reply to specific messages | 支持回复特定消息
- Beautiful UI design (based on DaisyUI) | 美观的界面设计（基于 DaisyUI）
- Responsive layout for mobile devices | 响应式布局，支持移动端
- Dark/Light theme support | 支持深色/浅色主题切换

## Installation | 安装步骤

1. Clone the repository | 克隆项目到本地:
```bash
git clone [repository-url]
cd chat-app
```

2. Create and activate virtual environment (optional) | 创建并激活虚拟环境（可选）:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies | 安装依赖:
```bash
pip install -r requirements.txt
```

4. Run the application | 运行应用:
```bash
python chat_app/app.py
```

5. Access in browser | 在浏览器中访问:
```
http://localhost:5000
```

## Usage Guide | 使用说明

1. Login | 登录
   - Enter your nickname | 输入你的昵称
   - Click "Enter Chat Room" | 点击"进入聊天室"

2. Chat Features | 聊天功能
   - Click a contact to start private chat | 点击联系人开始私聊
   - Create groups and add members | 创建群聊并添加成员
   - Send text messages, emojis, and files | 发送文本消息、表情和文件
   - React to messages with emojis | 对消息添加表情回应
   - Reply to specific messages | 回复特定消息
   - Recall messages within 2 minutes | 在2分钟内撤回消息

3. UI Features | 界面功能
   - Switch between dark/light themes | 切换深色/浅色主题
   - Responsive design for all devices | 适配所有设备的响应式设计
   - Swipe gestures on mobile | 移动端滑动手势支持

## Technical Stack | 技术栈

- Backend | 后端:
  - Flask
  - Flask-SocketIO
  - Python-SocketIO
  - Flask-Babel

- Frontend | 前端:
  - HTML5
  - JavaScript
  - DaisyUI
  - TailwindCSS
  - Socket.IO Client

## Notes | 注意事项

- Data is stored in memory and will be lost after restart | 数据存储在内存中，重启后会丢失
- Uploaded files are saved in static/uploads directory | 上传的文件保存在 static/uploads 目录下
- The application runs in debug mode by default | 应用默认以调试模式运行 