
from .board import ChessBoard
from .move import MoveValidator, MoveExecutor
from .check import GameChecker

class ChessGame:
    """象棋游戏管理类"""

    def __init__(self):
        self.board = ChessBoard()
        self.move_validator = MoveValidator(self.board)
        self.move_executor = MoveExecutor(self.board)
        self.game_checker = GameChecker(self.board)
        self.players = {}  # 存储玩家ID和颜色的映射
        self.turn = 'red'  # 当前轮次

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
            # 房间已满
            return None

    def remove_player(self, player_id):
        """从游戏中移除玩家"""
        if player_id in self.players:
            del self.players[player_id]

    def get_valid_moves(self, row, col):
        """获取棋子的有效移动"""
        return self.move_validator.get_valid_moves(row, col)

    def make_move(self, move, player_id):
        """执行移动"""
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

        # 切换回合
        self.turn = 'black' if self.turn == 'red' else 'red'

        return True, "移动成功"

    def check_game_status(self):
        """检查游戏状态"""
        return self.game_checker.check_game_over()

    def get_game_state(self):
        """获取游戏状态"""
        return {
            'players': self.players,
            'board': self.board.to_dict(),
            'turn': self.turn
        }

    def is_room_full(self):
        """检查房间是否已满"""
        return len(self.players) >= 2

    def is_empty(self):
        """检查房间是否为空"""
        return len(self.players) == 0
