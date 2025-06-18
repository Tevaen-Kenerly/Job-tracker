import os

from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template, redirect, url_for, request, flash
from main import app, db, login_manager
from models import User, Job
from werkzeug.utils import secure_filename

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('register.html', error='Username already taken')
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template ('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        found_user = User.query.filter_by(username=request.form['username']).first()
        if found_user and found_user.password == request.form['password']:
            login_user(found_user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        company=request.form['company']
        role=request.form['role']
        status=request.form['status']
        notes=request.form['notes']
        file=request.files.get('resume')
        filename=None

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash ('Resume uploaded successfully!', 'success')
        else:
            flash('No file selected!', 'error')
        new_job = Job(
            company=company,
            role=role,
            status=status,
            notes=notes,
            resume=filename,
            user_id=current_user.id
    )
        db.session.add(new_job)
        db.session.commit()
        return redirect(url_for('index'))
    jobs = Job.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html',jobs=jobs)
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    job = Job.query.get(id)
    if job and job.user_id == current_user.id:
        db.session.delete(job)
        db.session.commit()
    return redirect(url_for('index'))
@app.route('/', methods=['GET'])
def filter():
    company_filter = request.args.get('company')
    status_filter = request.args.get('status')
    role_filter = request.args.get('role')

    jobs = Job.query
    if company_filter:
        jobs = jobs.filter(Job.company.ilike(f'%{company_filter}%'))
    if status_filter:
        jobs = jobs.filter(Job.status.ilike(f'%{status_filter}%'))
    if role_filter:
        jobs = jobs.filter(Job.role.ilike(f'%{role_filter}%'))
    jobs = jobs.all()
    return render_template('index.html',jobs=jobs)

@app.route('/dashboard')
@login_required
def dashboard():
    jobs = Job.query.filter_by(user_id=current_user.id).all()
    total_jobs = len(jobs)
    status_counts = {}
    for job in jobs:
        status_counts[job.status] = status_counts.get(job.status, 0) + 1
    return render_template('dashboard.html', total_jobs=total_jobs, status_counts=status_counts, jobs=jobs)


