from .board import ChessBoard

class GameChecker:
    """游戏状态检查器"""

    def __init__(self, board: ChessBoard):
        self.board = board

    def check_in_check(self, current_turn):
        """
        检查当前轮次的玩家是否被将军
        返回将军状态信息，包括威胁棋子和被威胁的将/帅的位置
        """
        # 找到当前轮次玩家的将/帅位置
        king_piece = '帥' if current_turn == 'red' else '將'
        king_pos = None

        for row in range(10):
            for col in range(9):
                if self.board.get_piece(row, col) == king_piece:
                    king_pos = (row, col)
                    break
            if king_pos:
                break

        if not king_pos:
            return None

        # 检查飞将（两个将/帅在同一列且中间无棋子）
        opponent_king_piece = '將' if current_turn == 'red' else '帥'
        opponent_king_pos = None

        for row in range(10):
            for col in range(9):
                if self.board.get_piece(row, col) == opponent_king_piece:
                    opponent_king_pos = (row, col)
                    break
            if opponent_king_pos:
                break

        threatening_pieces = []

        # 检查飞将
        if (opponent_king_pos and
            king_pos[1] == opponent_king_pos[1]):  # 同一列
            # 检查中间是否有棋子
            min_row = min(king_pos[0], opponent_king_pos[0])
            max_row = max(king_pos[0], opponent_king_pos[0])
            pieces_between = 0
            for row in range(min_row + 1, max_row):
                if self.board.get_piece(row, king_pos[1]):
                    pieces_between += 1

            if pieces_between == 0:  # 飞将
                threatening_pieces.append(opponent_king_pos)

        # 检查是否有对方棋子可以攻击到将/帅
        opponent_color = 'black' if current_turn == 'red' else 'red'

        for row in range(10):
            for col in range(9):
                piece = self.board.get_piece(row, col)
                if piece and self._get_piece_color(piece) == opponent_color:
                    # 排除对方的将/帅（飞将已经单独处理）
                    if piece != opponent_king_piece:
                        # 检查这个棋子是否可以攻击到将/帅
                        if self._can_attack(row, col, king_pos[0], king_pos[1]):
                            threatening_pieces.append((row, col))

        if threatening_pieces:
            positions = threatening_pieces + [king_pos]
            return {
                'in_check': True,
                'positions': positions
            }

        return None

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

    def _get_piece_color(self, piece):
        """获取棋子颜色"""
        red_pieces = ['兵', '炮', '俥', '傌', '相', '仕', '帥']
        return 'red' if piece in red_pieces else 'black'

    def _can_attack(self, from_row, from_col, to_row, to_col):
        """简化的攻击检查（这里只做基本的直线攻击检查）"""
        piece = self.board.get_piece(from_row, from_col)

        # 炮的攻击逻辑
        if piece in ['炮', '砲']:
            return self._check_cannon_attack(from_row, from_col, to_row, to_col)

        # 车的攻击逻辑
        if piece in ['俥', '車']:
            return self._check_rook_attack(from_row, from_col, to_row, to_col)

        # 马的攻击逻辑
        if piece in ['傌', '馬']:
            return self._check_horse_attack(from_row, from_col, to_row, to_col)

        # 兵/卒的攻击逻辑
        if piece in ['兵', '卒']:
            return self._check_pawn_attack(from_row, from_col, to_row, to_col, piece)

        # 相/象的攻击逻辑
        if piece in ['相', '象']:
            return self._check_elephant_attack(from_row, from_col, to_row, to_col)

        # 仕/士的攻击逻辑
        if piece in ['仕', '士']:
            return self._check_advisor_attack(from_row, from_col, to_row, to_col)

        return False

    def _check_cannon_attack(self, from_row, from_col, to_row, to_col):
        """检查炮的攻击"""
        if from_row != to_row and from_col != to_col:
            return False

        # 计算中间有多少个棋子
        pieces_between = 0
        if from_row == to_row:
            start_col = min(from_col, to_col) + 1
            end_col = max(from_col, to_col)
            for col in range(start_col, end_col):
                if self.board.get_piece(from_row, col):
                    pieces_between += 1
        else:
            start_row = min(from_row, to_row) + 1
            end_row = max(from_row, to_row)
            for row in range(start_row, end_row):
                if self.board.get_piece(row, from_col):
                    pieces_between += 1

        return pieces_between == 1

    def _check_rook_attack(self, from_row, from_col, to_row, to_col):
        """检查车的攻击"""
        if from_row != to_row and from_col != to_col:
            return False

        # 检查路径是否畅通
        if from_row == to_row:
            start_col = min(from_col, to_col) + 1
            end_col = max(from_col, to_col)
            for col in range(start_col, end_col):
                if self.board.get_piece(from_row, col):
                    return False
        else:
            start_row = min(from_row, to_row) + 1
            end_row = max(from_row, to_row)
            for row in range(start_row, end_row):
                if self.board.get_piece(row, from_col):
                    return False

        return True

    def _check_horse_attack(self, from_row, from_col, to_row, to_col):
        """检查马的攻击"""
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)

        if not ((row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)):
            return False

        # 检查马脚
        if row_diff == 2:
            blocking_row = from_row + (1 if to_row > from_row else -1)
            if self.board.get_piece(blocking_row, from_col):
                return False
        else:
            blocking_col = from_col + (1 if to_col > from_col else -1)
            if self.board.get_piece(from_row, blocking_col):
                return False

        return True

    def _check_pawn_attack(self, from_row, from_col, to_row, to_col, piece):
        """检查兵/卒的攻击"""
        row_diff = to_row - from_row
        col_diff = abs(to_col - from_col)

        if piece == '兵':  # 红兵
            if from_row <= 4:  # 未过河
                return row_diff == -1 and col_diff == 0
            else:  # 已过河
                return (row_diff == -1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)
        else:  # 黑卒
            if from_row >= 5:  # 未过河
                return row_diff == 1 and col_diff == 0
            else:  # 已过河
                return (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)

    def _check_elephant_attack(self, from_row, from_col, to_row, to_col):
        """检查相/象的攻击"""
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)

        if row_diff != 2 or col_diff != 2:
            return False

        # 检查象眼
        blocking_row = from_row + (1 if to_row > from_row else -1)
        blocking_col = from_col + (1 if to_col > from_col else -1)
        if self.board.get_piece(blocking_row, blocking_col):
            return False

        return True

    def _check_advisor_attack(self, from_row, from_col, to_row, to_col):
        """检查仕/士的攻击"""
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)

        return row_diff == 1 and col_diff == 1