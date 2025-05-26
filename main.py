"""
中国象棋游戏主程序
使用Flask-SocketIO实现在线对战
"""

from src import ChessServer

def main():
    """主函数"""
    # 创建象棋服务器实例
    server = ChessServer()

    # 启动服务器
    print("正在启动中国象棋游戏服务器...")
    print("访问 http://localhost:5000 开始游戏")

    try:
        server.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"服务器启动失败: {e}")

if __name__ == '__main__':
    main()