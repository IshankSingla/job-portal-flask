# app.py
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm
import os, secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobportal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    location = db.Column(db.String(100))
    company = db.Column(db.String(100))
    salary = db.Column(db.String(100))
    description = db.Column(db.Text)
    employer_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    seeker_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if current_user.role == 'admin':
        return render_template('admin_dashboard.html', users=User.query.all(), jobs=Job.query.all(), applications=Application.query.all())
    elif current_user.role == 'employer':
        return render_template('employer_dashboard.html', jobs=Job.query.filter_by(employer_id=current_user.id).all())
    else:
        keyword = request.args.get('keyword')
        location = request.args.get('location')
        company = request.args.get('company')

        query = Job.query
        if keyword:
            query = query.filter(Job.title.ilike(f"%{keyword}%"))
        if location:
            query = query.filter(Job.location.ilike(f"%{location}%"))
        if company:
            query = query.filter(Job.company.ilike(f"%{company}%"))

        jobs = query.all()
        applied = Application.query.filter_by(seeker_id=current_user.id).all()
        applied_jobs = [a.job_id for a in applied]
        return render_template('seeker_dashboard.html', jobs=jobs, applied_jobs=applied_jobs)

@app.route('/post-job', methods=['GET', 'POST'])
@login_required
def post_job():
    if current_user.role != 'employer':
        flash('Only employers can post jobs.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        job = Job(
            title=request.form['title'],
            location=request.form['location'],
            company=request.form['company'],
            salary=request.form['salary'],
            description=request.form['description'],
            employer_id=current_user.id
        )
        db.session.add(job)
        db.session.commit()
        flash('Job posted successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('post_job.html')

@app.route('/apply/<int:job_id>')
@login_required
def apply(job_id):
    if current_user.role != 'jobseeker':
        flash('Only job seekers can apply.', 'danger')
        return redirect(url_for('dashboard'))

    existing = Application.query.filter_by(job_id=job_id, seeker_id=current_user.id).first()
    if existing:
        flash('You already applied for this job.', 'info')
    else:
        application = Application(job_id=job_id, seeker_id=current_user.id)
        db.session.add(application)
        db.session.commit()
        flash('Applied successfully!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/api-jobs')
def api_jobs():
    import requests
    try:
        response = requests.get("https://remotive.io/api/remote-jobs")
        data = response.json()
        jobs = data.get("jobs", [])[:10]  # Display top 10 jobs
    except Exception as e:
        jobs = []
        flash(f"Failed to fetch API jobs: {str(e)}", "danger")
    return render_template('api_jobs.html', jobs=jobs)


@app.route('/delete-job/<int:job_id>')
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    if current_user.role != 'employer' or job.employer_id != current_user.id:
        flash('Unauthorized!', 'danger')
        return redirect(url_for('dashboard'))
    db.session.delete(job)
    db.session.commit()
    flash('Job deleted.', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
