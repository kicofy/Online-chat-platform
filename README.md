# 实时聊天室应用 | Real-time Chat Room Application

一个基于 Flask 和 Socket.IO 的实时聊天应用，支持私聊、群聊、表情回应和文件共享。

A real-time chat application based on Flask and Socket.IO, supporting private chat, group chat, emoji reactions, and file sharing.

## 功能特点 | Features

### 基础功能 | Basic Features
- 📝 无需密码的昵称登录系统 | Nickname-based login without password
- 💬 支持私聊和群聊 | Private and group chat support
- ⚡ 实时消息推送 | Real-time message delivery
- 🌓 深色/浅色主题切换 | Dark/Light theme support
- 📱 响应式布局，支持移动端 | Responsive layout for mobile devices

### 聊天功能 | Chat Features
- 😊 支持表情回应 | Emoji reactions support
- 📎 文件上传和分享 | File upload and sharing
- ↩️ 支持回复特定消息 | Reply to specific messages
- ⏪ 2分钟内可撤回消息 | Message recall within 2 minutes
- 👥 联系人管理 | Contact management

### 群聊功能 | Group Features
- 👑 群组创建与管理 | Group creation and management
- 📢 群组公告 | Group announcements
- 👥 成员管理 | Member management
- 🔄 群组重命名 | Group renaming

## 技术栈 | Tech Stack

### 后端 | Backend
- Flask 3.0.2
- Flask-SocketIO 5.3.6
- Python-SocketIO 5.11.1
- Flask-Babel 3.1.0
- Eventlet 0.35.2

### 前端 | Frontend
- HTML5
- JavaScript (原生 | Vanilla)
- TailwindCSS
- DaisyUI
- Socket.IO Client

## 安装步骤 | Installation

1. **克隆项目 | Clone the repository**
```bash
git clone [repository-url]
cd chat-app
```

2. **创建虚拟环境（可选）| Create virtual environment (optional)**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. **安装依赖 | Install dependencies**
```bash
pip install -r requirements.txt
```

4. **运行应用 | Run the application**
```bash
python chat_app/app.py
```

5. **访问应用 | Access the application**
```
http://localhost:5000
```

## 使用说明 | Usage Guide

### 登录 | Login
1. 输入昵称 | Enter your nickname
2. 选择语言（中文/English）| Select language
3. 点击"进入聊天室" | Click "Enter Chat Room"

### 私聊 | Private Chat
1. 在联系人列表中点击用户 | Click a user in the contacts list
2. 通过昵称添加新联系人 | Add new contacts by nickname
3. 发送文本消息、表情或文件 | Send text messages, emojis, or files

### 群聊 | Group Chat
1. 创建新群组 | Create new group
2. 添加群组成员 | Add group members
3. 管理群组设置 | Manage group settings
   - 修改群名 | Rename group
   - 更新公告 | Update announcement
   - 管理成员 | Manage members

### 消息功能 | Message Features
1. 回复消息：点击消息的回复按钮 | Reply: Click the reply button on a message
2. 表情回应：点击消息的表情按钮 | React: Click the emoji button on a message
3. 撤回消息：2分钟内点击撤回按钮 | Recall: Click recall button within 2 minutes
4. 文件分享：点击文件按钮上传 | Share files: Click the file button to upload

## 注意事项 | Notes

- 数据存储在本地文件中，重启服务不会丢失 | Data is stored in local files, persists after restart
- 上传的文件保存在 `static/uploads` 目录 | Uploaded files are saved in `static/uploads` directory
- 支持中英文双语界面 | Bilingual interface (Chinese/English)
- 建议使用现代浏览器访问 | Recommended to use modern browsers

## 开发说明 | Development Notes

### 目录结构 | Directory Structure
```
chat-app/
├── chat_app/
│   ├── static/
│   │   └── uploads/    # 文件上传目录
│   ├── templates/      # HTML模板
│   ├── translations/   # 多语言翻译
│   ├── data/          # 数据存储
│   └── app.py         # 主应用文件
├── requirements.txt    # 项目依赖
└── README.md          # 项目说明
```

### 数据存储 | Data Storage
- users.json: 用户数据 | User data
- private_messages.json: 私聊消息 | Private messages
- group_chats.json: 群聊数据 | Group chat data

## 贡献 | Contributing

欢迎提交 Issue 和 Pull Request | Welcome to submit issues and pull requests

## 许可证 | License

MIT License 