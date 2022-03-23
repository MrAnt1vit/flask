from data import db_session
from data.users import User
from data.jobs import Jobs
from flask import Flask, redirect, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def distribution():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    leaders = []
    for job in jobs:
        leader = db_sess.query(User).filter(User.id == job.team_leader).first()
        leaders.append(leader.name + ' ' + leader.surname)
    return render_template('index.html', jobs=jobs, leaders=leaders)


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


def main():
    db_session.global_init("db/mars_explorer.db")
    # new_person('Scott', 'Ridley', 21, 'captain', 'research engineer', 'module_1', 'scott_chief@mars.org')
    # new_person('Mark', 'Hunter', 24, 'colonist', 'electrician', 'module_1', 'm_hunter@mars.org')
    # new_person('Thomas', 'Fisher', 27, 'colonist', 'cook', 'module_2', 't_fisher@mars.org')
    # new_person('Wiliam', 'Wilson', 22, 'colonist', 'mechanic', 'module_2', 'w_w_w@mars.org')
    # new_job(1, 'deployment of residential modules 1 and 2', 15, '2, 3', datetime.datetime.now(), False)
    # new_job(2, 'exploration of mineral resourses', 15, '4, 3', datetime.datetime.now(), False)
    # new_job(3, 'development of a management system', 25, '5', datetime.datetime.now(), False)
    app.run(port=8080, host='0.0.0.0')


if __name__ == '__main__':
    main()