from .board import ChessBoard

class MoveValidator:
    """移动验证器"""

    def __init__(self, board: ChessBoard):
        self.board = board

    def get_valid_moves(self, row, col):
        """获取棋子可移动的位置"""
        piece = self.board.get_piece(row, col)
        if piece == '':
            return []

        moves = []

        # 兵/卒的移动规则
        if piece == '兵':  # 红兵
            moves.extend(self._get_soldier_moves(row, col, True))
        elif piece == '卒':  # 黑卒
            moves.extend(self._get_soldier_moves(row, col, False))

        # 车/俥的移动规则
        elif piece in ['車', '俥']:
            moves.extend(self._get_rook_moves(row, col, piece))

        # 马/傌的移动规则
        elif piece in ['馬', '傌']:
            moves.extend(self._get_horse_moves(row, col, piece))

        # 象/相的移动规则
        elif piece in ['象', '相']:
            moves.extend(self._get_elephant_moves(row, col, piece))

        # 士/仕的移动规则
        elif piece in ['士', '仕']:
            moves.extend(self._get_guard_moves(row, col, piece))

        # 将/帅的移动规则
        elif piece in ['將', '帥']:
            moves.extend(self._get_king_moves(row, col, piece))

        # 炮/砲的移动规则
        elif piece in ['炮', '砲']:
            moves.extend(self._get_cannon_moves(row, col, piece))

        return moves

    def _get_soldier_moves(self, row, col, is_red):
        """获取兵/卒的移动"""
        moves = []
        if is_red:  # 红兵
            if row > 0:  # 向前移动
                target = self.board.get_piece(row-1, col)
                if target == '' or self.board.is_black_piece(target):
                    moves.append((row-1, col))
            if row <= 4:  # 过河后可以左右移动
                if col > 0:
                    target = self.board.get_piece(row, col-1)
                    if target == '' or self.board.is_black_piece(target):
                        moves.append((row, col-1))
                if col < 8:
                    target = self.board.get_piece(row, col+1)
                    if target == '' or self.board.is_black_piece(target):
                        moves.append((row, col+1))
        else:  # 黑卒
            if row < 9:  # 向前移动
                target = self.board.get_piece(row+1, col)
                if target == '' or self.board.is_red_piece(target):
                    moves.append((row+1, col))
            if row >= 5:  # 过河后可以左右移动
                if col > 0:
                    target = self.board.get_piece(row, col-1)
                    if target == '' or self.board.is_red_piece(target):
                        moves.append((row, col-1))
                if col < 8:
                    target = self.board.get_piece(row, col+1)
                    if target == '' or self.board.is_red_piece(target):
                        moves.append((row, col+1))
        return moves

    def _get_rook_moves(self, row, col, piece):
        """获取车/俥的移动"""
        moves = []
        # 横向移动
        for direction in [-1, 1]:
            for c in range(col + direction, 9 if direction > 0 else -1, direction):
                target = self.board.get_piece(row, c)
                if target == '':
                    moves.append((row, c))
                else:
                    if ((piece == '車' and self.board.is_red_piece(target)) or
                        (piece == '俥' and self.board.is_black_piece(target))):
                        moves.append((row, c))
                    break
        # 纵向移动
        for direction in [-1, 1]:
            for r in range(row + direction, 10 if direction > 0 else -1, direction):
                target = self.board.get_piece(r, col)
                if target == '':
                    moves.append((r, col))
                else:
                    if ((piece == '車' and self.board.is_red_piece(target)) or
                        (piece == '俥' and self.board.is_black_piece(target))):
                        moves.append((r, col))
                    break
        return moves

    def _get_horse_moves(self, row, col, piece):
        """获取马/傌的移动"""
        moves = []
        # 马走日字，8个可能的位置
        horse_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in horse_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 10 and 0 <= new_col < 9:
                # 检查蹩马腿
                if dr == -2 and self.board.get_piece(row-1, col) != '':  # 向上走日
                    continue
                if dr == 2 and self.board.get_piece(row+1, col) != '':   # 向下走日
                    continue
                if dc == -2 and self.board.get_piece(row, col-1) != '':  # 向左走日
                    continue
                if dc == 2 and self.board.get_piece(row, col+1) != '':   # 向右走日
                    continue

                target = self.board.get_piece(new_row, new_col)
                if target == '' or ((piece == '馬' and self.board.is_red_piece(target)) or
                                   (piece == '傌' and self.board.is_black_piece(target))):
                    moves.append((new_row, new_col))
        return moves

    def _get_elephant_moves(self, row, col, piece):
        """获取象/相的移动"""
        moves = []
        # 象走田字，4个可能的位置
        elephant_moves = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
        for dr, dc in elephant_moves:
            new_row, new_col = row + dr, col + dc
            # 象不能过河
            if piece == '象' and new_row > 4:  # 黑象不能过河
                continue
            if piece == '相' and new_row < 5:  # 红相不能过河
                continue

            if 0 <= new_row < 10 and 0 <= new_col < 9:
                # 检查塞象眼
                if self.board.get_piece(row + dr//2, col + dc//2) != '':
                    continue

                target = self.board.get_piece(new_row, new_col)
                if target == '' or ((piece == '象' and self.board.is_red_piece(target)) or
                                   (piece == '相' and self.board.is_black_piece(target))):
                    moves.append((new_row, new_col))
        return moves

    def _get_guard_moves(self, row, col, piece):
        """获取士/仕的移动"""
        moves = []
        # 士只能在九宫格内斜着走
        guard_moves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in guard_moves:
            new_row, new_col = row + dr, col + dc
            # 限制在九宫格内
            if piece == '士':  # 黑士
                if not (0 <= new_row <= 2 and 3 <= new_col <= 5):
                    continue
            else:  # 红仕
                if not (7 <= new_row <= 9 and 3 <= new_col <= 5):
                    continue

            if 0 <= new_row < 10 and 0 <= new_col < 9:
                target = self.board.get_piece(new_row, new_col)
                if target == '' or ((piece == '士' and self.board.is_red_piece(target)) or
                                   (piece == '仕' and self.board.is_black_piece(target))):
                    moves.append((new_row, new_col))
        return moves

    def _get_king_moves(self, row, col, piece):
        """获取将/帅的移动"""
        moves = []
        # 将帅只能在九宫格内走一格
        king_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in king_moves:
            new_row, new_col = row + dr, col + dc
            # 限制在九宫格内
            if piece == '將':  # 黑将
                if not (0 <= new_row <= 2 and 3 <= new_col <= 5):
                    continue
            else:  # 红帅
                if not (7 <= new_row <= 9 and 3 <= new_col <= 5):
                    continue

            if 0 <= new_row < 10 and 0 <= new_col < 9:
                target = self.board.get_piece(new_row, new_col)
                if target == '' or ((piece == '將' and self.board.is_red_piece(target)) or
                                   (piece == '帥' and self.board.is_black_piece(target))):
                    moves.append((new_row, new_col))

        # 添加飞将移动：将/帅可以移动到与对方将/帅同列且中间无子的任意位置
        enemy_king = '帥' if piece == '將' else '將'
        enemy_row, enemy_col = self.board.find_piece(enemy_king)

        if enemy_row is not None and enemy_col == col:  # 同列
            # 检查中间是否有其他棋子
            start_check = min(row, enemy_row) + 1
            end_check = max(row, enemy_row)
            has_pieces_between = False

            for check_row in range(start_check, end_check):
                if self.board.get_piece(check_row, col) != '':
                    has_pieces_between = True
                    break

            if not has_pieces_between:
                # 可以飞将，将对方将/帅的位置加入可移动位置
                moves.append((enemy_row, enemy_col))

        return moves

    def _get_cannon_moves(self, row, col, piece):
        """获取炮/砲的移动"""
        moves = []
        # 横向移动
        for direction in [-1, 1]:
            cannon_found = False
            for c in range(col + direction, 9 if direction > 0 else -1, direction):
                target = self.board.get_piece(row, c)
                if not cannon_found:
                    if target == '':
                        moves.append((row, c))
                    else:
                        cannon_found = True
                else:
                    if target != '':
                        if ((piece == '炮' and self.board.is_black_piece(target)) or
                            (piece == '砲' and self.board.is_red_piece(target))):
                            moves.append((row, c))
                        break

        # 纵向移动
        for direction in [-1, 1]:
            cannon_found = False
            for r in range(row + direction, 10 if direction > 0 else -1, direction):
                target = self.board.get_piece(r, col)
                if not cannon_found:
                    if target == '':
                        moves.append((r, col))
                    else:
                        cannon_found = True
                else:
                    if target != '':
                        if ((piece == '炮' and self.board.is_black_piece(target)) or
                            (piece == '砲' and self.board.is_red_piece(target))):
                            moves.append((r, col))
                        break
        return moves

    def validate_move(self, move, turn):
        """验证移动是否合法"""
        start_row, start_col, end_row, end_col = move
        piece = self.board.get_piece(start_row, start_col)

        if piece == '':
            return False

        # 检查是否轮到该玩家
        if (turn == 'red' and self.board.is_black_piece(piece)) or (turn == 'black' and self.board.is_red_piece(piece)):
            return False

        # 检查目标位置是否在可移动范围内
        valid_moves = self.get_valid_moves(start_row, start_col)
        if (end_row, end_col) not in valid_moves:
            return False

        return True


class MoveExecutor:
    """移动执行器"""

    def __init__(self, board: ChessBoard):
        self.board = board

    def apply_move(self, move):
        """执行移动"""
        start_row, start_col, end_row, end_col = move
        piece = self.board.get_piece(start_row, start_col)
        self.board.set_piece(end_row, end_col, piece)  # 移动棋子
        self.board.set_piece(start_row, start_col, '')  # 清空起始位置