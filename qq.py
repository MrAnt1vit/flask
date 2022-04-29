import chief as chief
from flask import Flask, redirect, render_template, request
from flask_login import logout_user, login_required, login_user, LoginManager

from data import db_session
from data.jobs import Jobs
from data.user_form import RegisterForm
from data.users import User
from data.login_form import LoginForm
from data.jobs_form import JobsForm
from data.department import Department
from data.department_form import DepartmentsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)
    else:
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', form=form, message="Пароли не совпадают")
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', form=form,
                                       message="Такой пользователь уже есть")
            user = User(
                surname=form.surname.data,
                name=form.name.data,
                age=form.age.data,
                position=form.position.data,
                speciality=form.speciality.data,
                address=form.address.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
        return render_template('register.html', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
def new_job():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        Job = Jobs(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data,
        )
        db_sess.add(Job)
        db_sess.commit()
        return redirect('/')
    return render_template('addjob.html', form=form)


@app.route('/adddepartment', methods=['GET', 'POST'])
def new_department():
    form = DepartmentsForm()
    if request.method == 'GET':
        return render_template('adddepartment.html', form=form)
    else:
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            department = Department(
                title=form.title.data,
                chief=form.chief.data,
                members=form.members.data,
                email=form.email.data,
            )
            db_sess.add(department)
            db_sess.commit()
            return redirect('/departments')
        return render_template('adddepartment.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
@app.route('/jobs')
def jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    leaders = []
    for job in jobs:
        leader = db_sess.query(User).filter(User.id == job.team_leader).first()
        leaders.append(leader.name + ' ' + leader.surname)
    return render_template('index.html', jobs=jobs, leaders=leaders)


@app.route('/departments')
def departments():
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).all()
    leaders = []
    for department in departments:
        leader = db_sess.query(User).filter(User.id == department.chief).first()
        leaders.append(leader.name + ' ' + leader.surname)
    return render_template('departments.html', departments=departments, leaders=leaders)


def new_person(surname, name, age, position, speciality, adress, email):
    user = User()
    user.surname = surname
    user.name = name
    user.age = age
    user.position = position
    user.speciality = speciality
    user.adress = adress
    user.email = email

    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


def new_job(team_leader, job, work_size, collaborators, start_date, is_finished):
    jobs = Jobs()
    jobs.team_leader = team_leader
    jobs.job = job
    jobs.work_size = work_size
    jobs.collaborators = collaborators
    jobs.start_date = start_date
    jobs.is_finished = is_finished

    db_sess = db_session.create_session()
    db_sess.add(jobs)
    db_sess.commit()


def new_department(team_leader, job, work_size, collaborators, start_date, is_finished):
    jobs = Jobs()
    jobs.team_leader = team_leader
    jobs.job = job
    jobs.work_size = work_size
    jobs.collaborators = collaborators
    jobs.start_date = start_date
    jobs.is_finished = is_finished

    db_sess = db_session.create_session()
    db_sess.add(jobs)
    db_sess.commit()


def main():
    db_session.global_init("db/mars_explorer.db")
    # db_session.create_session().commit()
    # new_person('Scott', 'Ridley', 21, 'captain', 'research engineer', 'module_1', 'scott_chief@mars.org') / пароль - aboba
    # new_person('Mark', 'Hunter', 24, 'colonist', 'electrician', 'module_1', 'm_hunter@mars.org')
    # new_person('Thomas', 'Fisher', 27, 'colonist', 'cook', 'module_2', 't_fisher@mars.org')
    # new_person('Wiliam', 'Wilson', 22, 'colonist', 'mechanic', 'module_2', 'w_w_w@mars.org')
    # new_job(1, 'deployment of residential modules 1 and 2', 15, '2, 3', datetime.datetime.now(), False)
    # new_job(2, 'exploration of mineral resourses', 15, '4, 3', datetime.datetime.now(), False)
    # new_job(3, 'development of a management system', 25, '5', datetime.datetime.now(), False)
    app.run(port=8080, host='0.0.0.0')


@app.route('/edit_jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        form.team_leader.data = job.team_leader
        form.job.data = job.job
        form.work_size.data = job.work_size
        form.collaborators.data = job.collaborators
        form.is_finished.data = job.is_finished
        return render_template('addjob.html', form=form)
    else:
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            job = db_sess.query(Jobs).filter(Jobs.id == id).first()
            job.team_leader = form.team_leader.data
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            return render_template('addjob.html', form=form)


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id).first()
    db_sess.delete(job)
    db_sess.commit()
    return redirect('/')


@app.route('/edit_department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = DepartmentsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        department = db_sess.query(Department).filter(Department.id == id).first()
        form.title.data = department.title
        form.chief.data = department.chief
        form.members.data = department.members
        form.email.data = department.email
        return render_template('adddepartment.html', form=form)
    else:
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            department = db_sess.query(Department).filter(Department.id == id).first()
            department.title = form.title.data
            department.chief = form.chief.data
            department.members = form.members.data
            department.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
        else:
            return render_template('adddepartment.html', form=form)


@app.route('/department_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def department_delete(id):
    db_sess = db_session.create_session()
    department = db_sess.query(Department).filter(Department.id == id).first()
    db_sess.delete(department)
    db_sess.commit()
    return redirect('/')


if __name__ == '__main__':
    main()
