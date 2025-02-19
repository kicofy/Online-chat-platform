from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['DATA_FOLDER'] = 'chat_app/data'
socketio = SocketIO(app, async_mode='threading')

# 支持的语言
LANGUAGES = {
    'en': 'English',
    'zh': '中文'
}

# 数据文件路径
USERS_FILE = os.path.join(app.config['DATA_FOLDER'], 'users.json')
PRIVATE_MESSAGES_FILE = os.path.join(app.config['DATA_FOLDER'], 'private_messages.json')
GROUP_CHATS_FILE = os.path.join(app.config['DATA_FOLDER'], 'group_chats.json')

# 用户数据存储
def load_data():
    global users, private_messages, group_chats
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                users = json.load(f)
        if os.path.exists(PRIVATE_MESSAGES_FILE):
            with open(PRIVATE_MESSAGES_FILE, 'r', encoding='utf-8') as f:
                private_messages = json.load(f)
        if os.path.exists(GROUP_CHATS_FILE):
            with open(GROUP_CHATS_FILE, 'r', encoding='utf-8') as f:
                group_chats = json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")

def save_data():
    try:
        os.makedirs(app.config['DATA_FOLDER'], exist_ok=True)
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
        with open(PRIVATE_MESSAGES_FILE, 'w', encoding='utf-8') as f:
            json.dump(private_messages, f, ensure_ascii=False, indent=2)
        with open(GROUP_CHATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(group_chats, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving data: {e}")

# 初始化数据
users = {}
private_messages = {}
group_chats = {}
load_data()

@app.route('/')
def index():
    return render_template('index.html', languages=LANGUAGES)

@app.route('/login', methods=['POST'])
def login():
    nickname = request.form.get('nickname')
    language = request.form.get('language', 'en')
    if not nickname:
        return jsonify({'error': 'Nickname is required'}), 400
    
    session['nickname'] = nickname
    session['language'] = language
    if nickname not in users:
        users[nickname] = {'online': True, 'rooms': []}
        save_data()
    return redirect(url_for('chat'))

@app.route('/chat')
def chat():
    if 'nickname' not in session:
        return redirect(url_for('index'))
    return render_template('chat.html', 
                         nickname=session['nickname'],
                         users={},  # 不再直接传递所有用户
                         group_chats=group_chats)

@app.route('/get_chat_history', methods=['POST'])
def get_chat_history():
    if 'nickname' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    chat_type = request.json.get('type')
    target = request.json.get('target')
    
    if chat_type == 'private':
        chat_id = f"{min(session['nickname'], target)}_{max(session['nickname'], target)}"
        messages = private_messages.get(chat_id, [])
    elif chat_type == 'group':
        if target in group_chats:
            messages = group_chats[target]['messages']
        else:
            messages = []
    else:
        messages = []
    
    return jsonify({'messages': messages})

@app.route('/create_group', methods=['POST'])
def create_group():
    if 'nickname' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    group_name = request.json.get('group_name')
    members = request.json.get('members', [])
    
    if not group_name:
        return jsonify({'error': 'Group name is required'}), 400
    
    if group_name in group_chats:
        return jsonify({'error': 'Group already exists'}), 400
    
    creator = session['nickname']
    members.append(creator)
    members = list(set(members))  # 去重
    
    group_chats[group_name] = {
        'members': members,
        'messages': [],
        'created_by': creator,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    save_data()
    
    # 通知所有被邀请的成员
    notification = {
        'type': 'group_invitation',
        'group_name': group_name,
        'invited_by': creator,
        'members': members
    }
    
    for member in members:
        if member != creator:  # 不需要通知创建者自己
            emit('group_invitation', notification, room=member, namespace='/')
    
    return jsonify({'success': True, 'group': group_name})

@socketio.on('connect')
def handle_connect():
    if 'nickname' in session:
        current_user = session['nickname']
        join_room(current_user)
        users[current_user]['online'] = True
        
        # 广播当前用户的在线状态
        emit('user_status', {
            'nickname': current_user,
            'status': 'online'
        }, broadcast=True)
        
        # 向新连接的用户发送所有在线用户的状态
        online_users = [
            {'nickname': nickname, 'status': 'online'}
            for nickname, data in users.items()
            if data.get('online') and nickname != current_user
        ]
        emit('initial_users_status', {'users': online_users})
        
        save_data()

@socketio.on('disconnect')
def handle_disconnect():
    if 'nickname' in session:
        current_user = session['nickname']
        users[current_user]['online'] = False
        emit('user_status', {
            'nickname': current_user,
            'status': 'offline'
        }, broadcast=True)
        save_data()

@socketio.on('private_message')
def handle_private_message(data):
    recipient = data['recipient']
    message = data['message']
    sender = session['nickname']
    reply_to = data.get('reply_to')  # 回复消息的时间戳
    
    if recipient not in users:
        return
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message_data = {
        'sender': sender,
        'content': message,
        'timestamp': timestamp,
        'reply_to': reply_to,  # 添加回复引用
        'reactions': {},  # 添加表情回应
        'is_recalled': False  # 添加撤回标记
    }
    
    # 存储私聊消息
    chat_id = f"{min(sender, recipient)}_{max(sender, recipient)}"
    if chat_id not in private_messages:
        private_messages[chat_id] = []
    private_messages[chat_id].append(message_data)
    save_data()
    
    emit('new_private_message', message_data, room=recipient)
    emit('new_private_message', message_data, room=sender)

@socketio.on('group_message')
def handle_group_message(data):
    group_name = data['group']
    message = data['message']
    sender = session['nickname']
    reply_to = data.get('reply_to')  # 回复消息的时间戳
    
    if group_name not in group_chats:
        return
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message_data = {
        'sender': sender,
        'content': message,
        'timestamp': timestamp,
        'reply_to': reply_to,  # 添加回复引用
        'reactions': {},  # 添加表情回应
        'is_recalled': False  # 添加撤回标记
    }
    
    group_chats[group_name]['messages'].append(message_data)
    save_data()
    
    for member in group_chats[group_name]['members']:
        emit('new_group_message', {
            'group': group_name,
            'message': message_data
        }, room=member)

@socketio.on('recall_message')
def handle_recall_message(data):
    message_timestamp = data['message_id']  # 现在使用时间戳作为消息ID
    chat_type = data['type']
    target = data['target']
    sender = session['nickname']
    
    if chat_type == 'private':
        chat_id = f"{min(sender, target)}_{max(sender, target)}"
        messages = private_messages.get(chat_id, [])
    else:
        if target not in group_chats:
            return
        messages = group_chats[target]['messages']
    
    # 查找消息并标记为已撤回
    for msg in messages:
        if msg['timestamp'] == message_timestamp and msg['sender'] == sender:
            # 检查是否在2分钟内
            msg_time = datetime.strptime(msg['timestamp'], '%Y-%m-%d %H:%M:%S')
            if (datetime.now() - msg_time).total_seconds() <= 120:
                msg['is_recalled'] = True
                save_data()
                
                recall_data = {
                    'message_id': message_timestamp,
                    'chat_type': chat_type,
                    'target': target
                }
                
                if chat_type == 'private':
                    emit('message_recalled', recall_data, room=sender)
                    emit('message_recalled', recall_data, room=target)
                else:
                    for member in group_chats[target]['members']:
                        emit('message_recalled', recall_data, room=member)
            break

@socketio.on('add_reaction')
def handle_add_reaction(data):
    message_timestamp = data['message_id']  # 现在使用时间戳作为消息ID
    chat_type = data['type']
    target = data['target']
    emoji = data['emoji']
    sender = session['nickname']
    
    if chat_type == 'private':
        chat_id = f"{min(sender, target)}_{max(sender, target)}"
        messages = private_messages.get(chat_id, [])
    else:
        if target not in group_chats:
            return
        messages = group_chats[target]['messages']
    
    # 添加或移除表情回应
    for msg in messages:
        if msg['timestamp'] == message_timestamp:
            # 确保reactions字段存在
            if 'reactions' not in msg:
                msg['reactions'] = {}
            
            # 先移除用户之前的所有表情回应
            for existing_emoji in list(msg['reactions'].keys()):
                if sender in msg['reactions'][existing_emoji]:
                    msg['reactions'][existing_emoji].remove(sender)
                    if not msg['reactions'][existing_emoji]:
                        del msg['reactions'][existing_emoji]
            
            # 添加新的表情回应（如果不是取消操作）
            if data.get('action') != 'remove':
                if emoji not in msg['reactions']:
                    msg['reactions'][emoji] = []
                if sender not in msg['reactions'][emoji]:
                    msg['reactions'][emoji].append(sender)
            
            save_data()
            
            reaction_data = {
                'message_id': message_timestamp,
                'chat_type': chat_type,
                'target': target,
                'reactions': msg['reactions']
            }
            
            if chat_type == 'private':
                emit('reaction_updated', reaction_data, room=sender)
                emit('reaction_updated', reaction_data, room=target)
            else:
                for member in group_chats[target]['members']:
                    emit('reaction_updated', reaction_data, room=member)
            break

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({
            'success': True,
            'filename': filename,
            'url': f"/static/uploads/{filename}"
        })

@app.route('/get_active_contacts')
def get_active_contacts():
    if 'nickname' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    current_user = session['nickname']
    active_contacts = set()
    
    # 遍历所有私聊消息，找出与当前用户有过对话的用户
    for chat_id, messages in private_messages.items():
        if not messages:  # 如果没有消息，跳过
            continue
        users = chat_id.split('_')
        if current_user in users:
            other_user = users[0] if users[1] == current_user else users[1]
            active_contacts.add(other_user)
    
    # 将活跃联系人转换为列表并排序
    active_contacts = sorted(list(active_contacts))
    
    return jsonify({'contacts': active_contacts})

if __name__ == '__main__':
    socketio.run(app, debug=True) 