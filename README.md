# recruitment-platform
基于Web设计的网站招聘系统
# 更新系统
sudo yum update -y

# 安装 Python 3 和 pip
sudo yum install -y python3 python3-pip

# 安装 Git
sudo yum install -y git

# 安装 SQLite（通常已预装）
sudo yum install -y sqlite

# 克隆项目（假设项目在 GitHub 上）
git clone https://github.com/Ly-yang/recruitment-platform.git
cd recruitment-platform

# 或者手动创建项目结构
mkdir -p recruitment-platform/{static/{css,js},templates,database}
touch recruitment-platform/app.py
touch recruitment-platform/static/css/style.css
touch recruitment-platform/static/js/main.js
touch recruitment-platform/templates/index.html

# 安装 Python 依赖
pip3 install flask flask-sqlalchemy werkzeug

# 创建数据库目录
mkdir database

# 初始化数据库
python3 -c "from app import db; db.create_all()"

# 启动 Flask 应用
python3 app.py

用户注册测试：

访问 http://your-server-ip:5000/register/candidate

填写求职者注册表单

验证是否成功创建账户并登录

企业注册测试：

访问 http://your-server-ip:5000/register/employer

填写企业注册表单

验证是否成功创建企业账户

职位发布测试：

以企业身份登录

访问 http://your-server-ip:5000/post_job

发布新职位

验证职位是否显示在首页和职位列表页

职位申请测试：

以求职者身份登录

浏览职位列表

申请一个职位

验证申请是否出现在个人仪表盘

搜索功能测试：

在首页或职位列表页使用搜索框

验证搜索结果是否符合预期

系统功能特点
多角色系统：

求职者：浏览职位、申请职位、管理申请

企业：发布职位、管理职位、查看申请

管理员：管理用户和内容

完整用户认证：

安全密码存储（使用 werkzeug 的密码哈希）

会话管理

注册表单验证

职位管理系统：

职位发布与编辑

职位搜索与筛选

职位申请与状态跟踪

响应式设计：

适配桌面、平板和手机

移动端优化导航

自适应布局

交互体验优化：

实时搜索反馈

表单验证与错误提示

悬停效果与视觉反馈

这个动态招聘网站系统提供了完整的交互体验，采用了现代化的布局设计，并针对 CentOS 7 环境进行了优化。系统包含了用户认证、职位管理、申请流程等核心功能，可以满足基本的招聘网站需求。

