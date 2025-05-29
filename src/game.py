from .board import ChessBoard
from .move import MoveValidator, MoveExecutor
from .check import GameChecker
import time
import threading

class ChessGame:
    """象棋游戏管理类"""

    def __init__(self):
        self.board = ChessBoard()
        self.move_validator = MoveValidator(self.board)
        self.move_executor = MoveExecutor(self.board)
        self.game_checker = GameChecker(self.board)
        self.players = {}  # 存储玩家ID和颜色的映射
        self.spectators = set()  # 存储观众ID
        self.turn = 'red'  # 当前轮次
        self.last_move = None  # 上一步移动
        self.check_status = None  # 将军状态
        self.confirm_status = {'red': False, 'black': False}  # 确认状态
        self.game_started = False  # 游戏是否已开始

        # 服务器端计时器
        self.timer_duration = 120  # 2分钟
        self.timer_remaining = 120
        self.timer_thread = None
        self.timer_active = False
        self.timer_callback = None  # 计时器回调函数

    def add_player(self, player_id):
        """添加玩家到游戏"""
        if len(self.players) == 0:
            # 第一个玩家是红方
            self.players[player_id] = 'red'
            return 'red'
        elif len(self.players) == 1:
            # 第二个玩家是黑方
            self.players[player_id] = 'black'
            return 'black'
        else:
            # 房间已满，成为观众
            self.spectators.add(player_id)
            return 'spectator'

    def remove_player(self, player_id):
        """从游戏中移除玩家"""
        if player_id in self.players:
            del self.players[player_id]
        elif player_id in self.spectators:
            self.spectators.remove(player_id)

    def get_valid_moves(self, row, col):
        """获取棋子的有效移动"""
        return self.move_validator.get_valid_moves(row, col)

    def make_move(self, move, player_id):
        """执行移动"""
        # 检查游戏是否已开始
        if not self.game_started:
            return False, "游戏尚未开始，请等待所有玩家确认"

        # 检查玩家是否有权限移动（只能在自己的回合移动自己的棋子）
        if player_id not in self.players:
            return False, "玩家不在游戏中"

        player_color = self.players[player_id]

        # 检查是否轮到该玩家
        if player_color != self.turn:
            return False, "不是您的回合"

        # 验证移动是否合法
        if not self.move_validator.validate_move(move, self.turn):
            return False, "无效的移动"

        # 执行移动
        self.move_executor.apply_move(move)

        # 记录上一步移动
        self.last_move = move

        # 切换回合
        self.turn = 'black' if self.turn == 'red' else 'red'

        # 检查将军状态
        self.check_status = self.game_checker.check_in_check(self.turn)

        return True, "移动成功"

    def check_game_status(self):
        """检查游戏状态"""
        return self.game_checker.check_game_over()

    def get_game_state(self):
        """获取游戏状态"""
        state = {
            'players': self.players,
            'board': self.board.to_dict(),
            'turn': self.turn
        }

        # 添加上一步移动信息
        if self.last_move:
            state['last_move'] = self.last_move

        # 添加将军状态信息
        if self.check_status:
            state['check_status'] = self.check_status

        return state

    def is_room_full(self):
        """检查房间是否已满"""
        return len(self.players) >= 2

    def is_empty(self):
        """检查房间是否为空"""
        return len(self.players) == 0 and len(self.spectators) == 0

    def player_confirm(self, player_id):
        """玩家确认准备"""
        print(f"player_confirm 被调用: player_id={player_id}")  # 调试信息
        print(f"当前玩家列表: {self.players}")  # 调试信息

        if player_id not in self.players:
            print(f"玩家不在游戏中: {player_id}")  # 调试信息
            return False, "玩家不在游戏中"

        player_color = self.players[player_id]
        print(f"玩家颜色: {player_color}")  # 调试信息
        print(f"当前确认状态: {self.confirm_status}")  # 调试信息

        if self.confirm_status[player_color]:
            print(f"玩家已经确认过了: {player_color}")  # 调试信息
            return False, "已经确认过了"

        self.confirm_status[player_color] = True
        print(f"更新后确认状态: {self.confirm_status}")  # 调试信息

        # 检查是否所有玩家都已确认
        if len(self.players) == 2 and all(self.confirm_status.values()):
            self.game_started = True
            print("游戏可以开始了!")  # 调试信息

        return True, f"{player_color}方已确认"

    def can_start_game(self):
        """检查游戏是否可以开始"""
        return len(self.players) == 2 and all(self.confirm_status.values())

    def reset_confirmations(self):
        """重置确认状态"""
        self.confirm_status = {'red': False, 'black': False}
        self.game_started = False

    def start_timer(self, callback=None):
        """启动服务器端计时器"""
        self.stop_timer()  # 停止之前的计时器

        self.timer_remaining = self.timer_duration
        self.timer_active = True
        self.timer_callback = callback

        def timer_worker():
            while self.timer_active and self.timer_remaining > 0:
                time.sleep(1)
                if self.timer_active:
                    self.timer_remaining -= 1

                    # 每秒发送计时器更新（通过回调）
                    if self.timer_callback:
                        self.timer_callback('timer_update', {
                            'time_remaining': self.timer_remaining,
                            'current_turn': self.turn
                        })

            # 时间耗尽
            if self.timer_active and self.timer_remaining <= 0:
                self.timer_active = False
                if self.timer_callback:
                    self.timer_callback('timer_timeout', {
                        'timeout_player': self.turn
                    })

        self.timer_thread = threading.Thread(target=timer_worker)
        self.timer_thread.daemon = True
        self.timer_thread.start()

    def stop_timer(self):
        """停止计时器"""
        self.timer_active = False
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join(timeout=1)

    def get_timer_status(self):
        """获取计时器状态"""
        return {
            'time_remaining': self.timer_remaining,
            'timer_active': self.timer_active,
            'current_turn': self.turn
        }
