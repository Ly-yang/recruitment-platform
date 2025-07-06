from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/recruitment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 数据库模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # candidate, employer
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 求职者专属字段
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100))
    
    # 企业专属字段
    company_name = db.Column(db.String(100))
    company_description = db.Column(db.Text))

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text), nullable=False)
    requirements = db.Column(db.Text), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(50))
    job_type = db.Column(db.String(50))  # Full-time, Part-time, Contract
    employer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    employer = db.relationship('User', backref=db.backref('jobs', lazy=True))

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, reviewed, rejected, hired
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    cover_letter = db.Column(db.Text))
    
    job = db.relationship('Job', backref=db.backref('applications', lazy=True))
    candidate = db.relationship('User', backref=db.backref('applications', lazy=True))

# 创建数据库
@app.before_first_request
def create_tables():
    db.create_all()
    # 添加初始数据
    if not User.query.first():
        # 添加管理员用户
        admin = User(
            username='admin',
            email='admin@recruitment.com',
            password=generate_password_hash('admin123'),
            user_type='admin',
            full_name='系统管理员'
        )
        db.session.add(admin)
        db.session.commit()

# 路由定义
@app.route('/')
def index():
    jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).limit(6).all()
    companies = User.query.filter_by(user_type='employer').limit(6).all()
    return render_template('index.html', jobs=jobs, companies=companies)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['user_type'] = user.user_type
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='用户名或密码错误')
    
    return render_template('login.html')

@app.route('/register/candidate', methods=['GET', 'POST'])
def register_candidate():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        phone = request.form['phone']
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            return render_template('register_candidate.html', error='用户名已存在')
        
        # 创建新用户
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            user_type='candidate',
            full_name=full_name,
            phone=phone
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        session['user_type'] = new_user.user_type
        
        return redirect(url_for('dashboard'))
    
    return render_template('register_candidate.html')

@app.route('/register/employer', methods=['GET', 'POST'])
def register_employer():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        company_name = request.form['company_name']
        contact_person = request.form['contact_person']
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            return render_template('register_employer.html', error='用户名已存在')
        
        # 创建新用户
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            user_type='employer',
            full_name=contact_person,
            company_name=company_name
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        session['user_type'] = new_user.user_type
        
        return redirect(url_for('dashboard'))
    
    return render_template('register_employer.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    if user.user_type == 'candidate':
        # 求职者仪表盘
        applied_jobs = Application.query.filter_by(candidate_id=user.id).all()
        return render_template('candidate_dashboard.html', user=user, applied_jobs=applied_jobs)
    
    elif user.user_type == 'employer':
        # 企业仪表盘
        company_jobs = Job.query.filter_by(employer_id=user.id).all()
        return render_template('employer_dashboard.html', user=user, jobs=company_jobs)
    
    return redirect(url_for('index'))

@app.route('/jobs')
def job_list():
    jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).all()
    return render_template('job_list.html', jobs=jobs)

@app.route('/job/<int:job_id>')
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job_detail.html', job=job)

@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply_job(job_id):
    if 'user_id' not in session or session['user_type'] != 'candidate':
        return redirect(url_for('login'))
    
    job = Job.query.get_or_404(job_id)
    candidate = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        cover_letter = request.form['cover_letter']
        
        # 检查是否已申请
        existing_application = Application.query.filter_by(
            job_id=job_id, 
            candidate_id=candidate.id
        ).first()
        
        if existing_application:
            return render_template('apply_job.html', job=job, error='您已经申请过该职位')
        
        # 创建新申请
        new_application = Application(
            job_id=job_id,
            candidate_id=candidate.id,
            cover_letter=cover_letter
        )
        
        db.session.add(new_application)
        db.session.commit()
        
        return render_template('application_success.html', job=job)
    
    return render_template('apply_job.html', job=job)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if 'user_id' not in session or session['user_type'] != 'employer':
        return redirect(url_for('login'))
    
    employer = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        requirements = request.form['requirements']
        location = request.form['location']
        salary = request.form['salary']
        job_type = request.form['job_type']
        
        new_job = Job(
            title=title,
            description=description,
            requirements=requirements,
            location=location,
            salary=salary,
            job_type=job_type,
            employer_id=employer.id
        )
        
        db.session.add(new_job)
        db.session.commit()
        
        return redirect(url_for('dashboard'))
    
    return render_template('post_job.html', employer=employer)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# API 接口
@app.route('/api/jobs', methods=['GET'])
def api_jobs():
    jobs = Job.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': job.id,
        'title': job.title,
        'company': job.employer.company_name,
        'location': job.location,
        'salary': job.salary,
        'created_at': job.created_at.strftime('%Y-%m-%d')
    } for job in jobs])

if __name__ == '__main__':
    if not os.path.exists('database'):
        os.makedirs('database')
    app.run(host='0.0.0.0', port=5000, debug=True)
