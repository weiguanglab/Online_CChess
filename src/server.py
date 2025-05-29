from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from .game import ChessGame

class ChessServer:
    """象棋游戏服务器类"""

    def __init__(self):
        self.app = Flask(__name__, template_folder='../templates')
        self.app.config['SECRET_KEY'] = 'your_secret_key'
        self.socketio = SocketIO(self.app)
        self.games = {}  # 存储游戏房间
        self._setup_routes()
        self._setup_socket_handlers()

    def _setup_routes(self):
        """设置HTTP路由"""
        @self.app.route('/')
        def index():
            return render_template('index.html')

    def _setup_socket_handlers(self):
        """设置Socket事件处理器"""

        @self.socketio.on('join_game')
        def on_join(data):
            room = data['room']
            join_room(room)
            print(f"玩家 {request.sid} 加入房间 {room}")  # 调试信息

            # 创建游戏房间（如果不存在）
            if room not in self.games:
                self.games[room] = ChessGame()
                print(f"创建新游戏房间: {room}")  # 调试信息

            game = self.games[room]

            # 添加玩家
            player_role = game.add_player(request.sid)
            print(f"玩家角色分配: {request.sid} -> {player_role}")  # 调试信息
            print(f"当前玩家列表: {game.players}")  # 调试信息

            # 发送游戏状态和玩家角色
            emit('game_state', game.get_game_state(), room=room)
            emit('player_role', {'role': player_role}, room=request.sid)

            # 发送确认状态
            emit('confirm_status', {
                'confirm_status': game.confirm_status,
                'game_started': game.game_started
            }, room=room)

        @self.socketio.on('get_valid_moves')
        def on_get_valid_moves(data):
            room = data['room']
            row = data['row']
            col = data['col']

            if room in self.games:
                game = self.games[room]
                valid_moves = game.get_valid_moves(row, col)
                emit('valid_moves', {'moves': valid_moves}, room=request.sid)

        @self.socketio.on('get_game_state')
        def on_get_game_state(data):
            room = data['room']
            if room in self.games:
                game = self.games[room]
                emit('game_state', game.get_game_state(), room=request.sid)

        @self.socketio.on('send_message')
        def on_send_message(data):
            room = data['room']
            message = data['message']
            sender_id = request.sid

            if room in self.games:
                game = self.games[room]
                # 确定发送者身份
                if sender_id in game.players:
                    sender_role = game.players[sender_id]
                elif sender_id in game.spectators:
                    sender_role = 'spectator'
                else:
                    return

                # 广播消息到房间内所有人
                emit('receive_message', {
                    'message': message,
                    'sender': sender_role,
                    'timestamp': data.get('timestamp', '')
                }, room=room)

        @self.socketio.on('player_confirm')
        def on_player_confirm(data):
            room = data['room']
            print(f"收到确认请求: room={room}, player_id={request.sid}")  # 调试信息

            if room not in self.games:
                print(f"房间不存在: {room}")  # 调试信息
                return

            game = self.games[room]
            print(f"玩家列表: {game.players}, 确认状态: {game.confirm_status}")  # 调试信息
            success, message = game.player_confirm(request.sid)
            print(f"确认结果: success={success}, message={message}")  # 调试信息

            if success:
                # 发送系统消息
                emit('receive_message', {
                    'message': message,
                    'sender': 'system',
                    'timestamp': ''
                }, room=room)

                # 广播确认状态更新
                emit('confirm_status', {
                    'confirm_status': game.confirm_status,
                    'game_started': game.game_started
                }, room=room)

                # 如果游戏可以开始，发送游戏开始消息并启动计时器
                if game.can_start_game():
                    emit('receive_message', {
                        'message': '双方已确认，游戏开始！',
                        'sender': 'system',
                        'timestamp': ''
                    }, room=room)

                    # 启动服务器端计时器
                    def timer_callback(event_type, data):
                        if event_type == 'timer_update':
                            self.socketio.emit('timer_update', data, room=room)
                        elif event_type == 'timer_timeout':
                            self.socketio.emit('timer_timeout', data, room=room)
                            # 发送游戏结束消息
                            winner = 'black' if data['timeout_player'] == 'red' else 'red'
                            self.socketio.emit('game_over', {
                                'winner': winner,
                                'reason': f"{data['timeout_player']}方超时"
                            }, room=room)

                    game.start_timer(timer_callback)

        @self.socketio.on('move')
        def on_move(data):
            room = data['room']
            move = data['move']

            if room not in self.games:
                emit('invalid_move', {}, room=request.sid)
                return

            game = self.games[room]

            # 执行移动
            success, message = game.make_move(move, request.sid)

            if success:
                # 重新启动计时器（移动后开始新的计时）
                def timer_callback(event_type, data):
                    if event_type == 'timer_update':
                        self.socketio.emit('timer_update', data, room=room)
                    elif event_type == 'timer_timeout':
                        self.socketio.emit('timer_timeout', data, room=room)
                        # 发送游戏结束消息
                        winner = 'black' if data['timeout_player'] == 'red' else 'red'
                        self.socketio.emit('game_over', {
                            'winner': winner,
                            'reason': f"{data['timeout_player']}方超时"
                        }, room=room)

                game.start_timer(timer_callback)

                # 检查游戏是否结束
                game_status = game.check_game_status()

                # 发送更新的游戏状态
                game_state = game.get_game_state()
                game_state.update(game_status)
                emit('game_state', game_state, room=room)

                # 如果游戏结束，发送游戏结束消息
                if game_status.get('game_over'):
                    game.stop_timer()  # 停止计时器
                    emit('game_over', {
                        'winner': game_status['winner'],
                        'reason': game_status['reason']
                    }, room=room)
            else:
                emit('invalid_move', {'message': message}, room=request.sid)

        @self.socketio.on('leave_game')
        def on_leave(data):
            room = data['room']
            leave_room(room)

            if room in self.games:
                game = self.games[room]
                game.remove_player(request.sid)

                # 如果房间为空，删除游戏
                if game.is_empty():
                    del self.games[room]

    def run(self, host='0.0.0.0', port=5000, debug=False):
        """启动服务器"""
        self.socketio.run(self.app, host=host, port=port, debug=debug)