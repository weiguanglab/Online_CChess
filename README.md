# 中国象棋在线对战游戏 🏁

一个基于 Flask-SocketIO 的中国象棋在线对战游戏，支持多人实时对战。

## 📋 功能特性

- 🎮 完整的中国象棋规则实现
- 🌐 在线实时对战
- 👥 多房间支持
- 🎯 移动验证和提示
- 🏆 游戏状态检测
- 📱 响应式网页界面

## 🛠️ 技术栈

- **后端**: Python Flask + Flask-SocketIO
- **前端**: HTML + CSS + JavaScript + Socket.IO
- **实时通信**: WebSocket
- **架构**: 面向对象设计，模块化开发

## 📦 项目结构

```
CChess/
├── main.py              # 主程序入口
├── requirements.txt     # 依赖包列表
├── README.md           # 项目说明
├── .gitignore          # Git忽略文件
├── src/                # 源代码目录
│   ├── __init__.py     # 包初始化
│   ├── board.py        # 棋盘类
│   ├── move.py         # 移动验证和执行
│   ├── check.py        # 游戏状态检查
│   ├── game.py         # 游戏管理
│   └── server.py       # 服务器和路由
└── templates/          # HTML模板
    └── index.html      # 游戏界面
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <your-repo-url>
   cd CChess
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **启动服务器**
   ```bash
   python main.py
   ```

4. **开始游戏**
   打开浏览器访问: `http://localhost:5000`

## 🎯 游戏规则

### 基本规则
- 红方先行，双方轮流移动
- 将死对方获胜
- 飞将（将帅照面）可直接吃掉对方

### 棋子移动规则
- **将/帅**: 只能在九宫格内移动一格
- **士/仕**: 只能在九宫格内斜走
- **象/相**: 走田字，不能过河，不能塞象眼
- **马/傌**: 走日字，不能蹩马腿
- **车/俥**: 横竖直线移动
- **炮/砲**: 移动时同车，吃子时需隔一子
- **兵/卒**: 只能向前，过河后可左右移动

## 🏗️ 架构设计

### 核心类

1. **ChessBoard**: 棋盘管理
   - 棋盘初始化
   - 棋子位置管理
   - 棋子类型判断

2. **MoveValidator**: 移动验证
   - 各种棋子的移动规则
   - 移动合法性检查

3. **MoveExecutor**: 移动执行
   - 执行合法移动
   - 更新棋盘状态

4. **GameChecker**: 游戏状态检查
   - 检查游戏是否结束
   - 判断胜负条件

5. **ChessGame**: 游戏管理
   - 玩家管理
   - 回合控制
   - 游戏流程

6. **ChessServer**: 服务器管理
   - WebSocket事件处理
   - 房间管理
   - 客户端通信

## 🔧 开发说明

### 添加新功能

1. 在相应的模块中添加功能
2. 更新 `__init__.py` 中的导出
3. 在服务器类中添加对应的事件处理

### 自定义规则

可以在 `MoveValidator` 类中修改各种棋子的移动规则。

## 🐛 常见问题

**Q: 无法连接到服务器？**
A: 检查防火墙设置，确保 5000 端口可访问。

**Q: 移动无效？**
A: 检查是否轮到你的回合，移动是否符合象棋规则。

**Q: 房间已满？**
A: 每个房间只支持两名玩家，请尝试其他房间。

## 📝 更新日志

### v1.0.0 (2025-05-27)
- ✨ 初始版本发布
- 🎮 完整的象棋规则实现
- 🌐 在线对战功能
- 📱 Web界面

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 👨‍💻 作者

- **Ethan** - *Initial work*

## 🙏 致谢

- 感谢所有贡献者
- 感谢开源社区的支持
