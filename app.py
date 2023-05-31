from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))

    def __init__(self, name, city, addr, pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin

class Teacher(db.Model):
    id = db.Column('teacher_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    subjects = db.Column(db.String(150))
    education = db.Column(db.String(100))
    hire_date = db.Column(db.String())

    def __init__(self, name, subjects, education, hire_date):
        self.name = name
        self.subjects = subjects
        self.education = education
        self.hire_date = hire_date

@app.route('/')
def show_all():
    students = Student.query.all()
    teachers = Teacher.query.all()
    return render_template('show_all.html', students=students, teachers=teachers)

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            student = Student(request.form['name'], request.form['city'],
                              request.form['addr'], request.form['pin'])

            db.session.add(student)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html')

@app.route('/newteachers', methods=['GET', 'POST'])
def new_teachers():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['subjects'] or not request.form['education'] or not request.form['hire_date']:
            flash('Please enter all the fields', 'error')
        else:
            teacher = Teacher(request.form['name'], request.form['subjects'],
                              request.form['education'], request.form['hire_date'])

            db.session.add(teacher)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('newteachers.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
