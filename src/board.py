
class ChessBoard:
    """中国象棋棋盘类"""

    def __init__(self):
        self.board = self._initialize_board()

    def _initialize_board(self):
        """初始化棋盘"""
        # 使用汉字表示棋子，黑棋在上（0-4行），红棋在下（5-9行）
        return [
            ['車', '馬', '象', '士', '將', '士', '象', '馬', '車'],  # 黑方后排
            ['', '', '', '', '', '', '', '', ''],                    # 空行
            ['', '砲', '', '', '', '', '', '砲', ''],                # 黑砲
            ['卒', '', '卒', '', '卒', '', '卒', '', '卒'],           # 黑卒
            ['', '', '', '', '', '', '', '', ''],                    # 楚河汉界
            ['', '', '', '', '', '', '', '', ''],                    # 楚河汉界
            ['兵', '', '兵', '', '兵', '', '兵', '', '兵'],           # 红兵
            ['', '炮', '', '', '', '', '', '炮', ''],                # 红炮
            ['', '', '', '', '', '', '', '', ''],                    # 空行
            ['俥', '傌', '相', '仕', '帥', '仕', '相', '傌', '俥']    # 红方后排
        ]

    def get_piece(self, row, col):
        """获取指定位置的棋子"""
        if 0 <= row < 10 and 0 <= col < 9:
            return self.board[row][col]
        return None

    def set_piece(self, row, col, piece):
        """设置指定位置的棋子"""
        if 0 <= row < 10 and 0 <= col < 9:
            self.board[row][col] = piece

    def is_empty(self, row, col):
        """检查指定位置是否为空"""
        return self.get_piece(row, col) == ''

    def is_red_piece(self, piece):
        """判断是否为红方棋子"""
        red_pieces = ['兵', '炮', '俥', '傌', '相', '仕', '帥']
        return piece in red_pieces

    def is_black_piece(self, piece):
        """判断是否为黑方棋子"""
        black_pieces = ['卒', '砲', '車', '馬', '象', '士', '將']
        return piece in black_pieces

    def find_king(self, is_red):
        """查找将/帅的位置"""
        king_piece = '帥' if is_red else '將'
        for row in range(10):
            for col in range(9):
                if self.board[row][col] == king_piece:
                    return row, col
        return None, None

    def find_piece(self, piece):
        """查找指定棋子的位置"""
        for row in range(10):
            for col in range(9):
                if self.board[row][col] == piece:
                    return row, col
        return None, None

    def copy(self):
        """创建棋盘的深拷贝"""
        new_board = ChessBoard()
        new_board.board = [row[:] for row in self.board]
        return new_board

    def to_dict(self):
        """将棋盘转换为字典格式，用于网络传输"""
        return self.board