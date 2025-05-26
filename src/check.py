
from .board import ChessBoard

class GameChecker:
    """游戏状态检查器"""

    def __init__(self, board: ChessBoard):
        self.board = board

    def check_game_over(self):
        """
        检查游戏是否结束
        只检查哪方的将/帅被吃掉了
        """
        # 检查是否还有帅/将
        red_king_exists = False
        black_king_exists = False

        for row in range(10):
            for col in range(9):
                piece = self.board.get_piece(row, col)
                if piece == '帥':
                    red_king_exists = True
                elif piece == '將':
                    black_king_exists = True

        # 如果某方的帅/将被吃掉，对方获胜
        if not red_king_exists:
            return {'game_over': True, 'winner': 'black', 'reason': 'king_captured'}
        if not black_king_exists:
            return {'game_over': True, 'winner': 'red', 'reason': 'king_captured'}

        return {'game_over': False}