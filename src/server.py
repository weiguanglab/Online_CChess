
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

            # 创建游戏房间（如果不存在）
            if room not in self.games:
                self.games[room] = ChessGame()

            game = self.games[room]

            # 添加玩家
            player_color = game.add_player(request.sid)

            if player_color is None:
                # 房间已满
                emit('room_full', {}, room=request.sid)
                return

            # 发送游戏状态和玩家颜色
            emit('game_state', game.get_game_state(), room=room)
            emit('player_color', {'color': player_color}, room=request.sid)

        @self.socketio.on('get_valid_moves')
        def on_get_valid_moves(data):
            room = data['room']
            row = data['row']
            col = data['col']

            if room in self.games:
                game = self.games[room]
                valid_moves = game.get_valid_moves(row, col)
                emit('valid_moves', {'moves': valid_moves}, room=request.sid)

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
                # 检查游戏是否结束
                game_status = game.check_game_status()

                # 发送更新的游戏状态
                game_state = game.get_game_state()
                game_state.update(game_status)
                emit('game_state', game_state, room=room)

                # 如果游戏结束，发送游戏结束消息
                if game_status.get('game_over'):
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