from flask import Blueprint, render_template, request, redirect, url_for, session

from App.model import db, Students, Grades, is_login, Users

school = Blueprint('school', __name__)
user = Blueprint('user', __name__)


@school.route('/create_table/')
def create_table():
    db.create_all()
    return '创建成功'


@school.route('/')
@is_login
def index():
    return render_template('index.html')


@school.route('/select_student/', methods=['GET'])
def select_student():
    if request.method == 'GET':
        page = request.args.get('page', 1)
        paginate = Students.query.paginate(page, 5)
        students = paginate.items
        if students == []:
            return '暂无学生信息'
        return render_template('student.html', students=students, paginate=paginate)


@school.route('/select_grade/')
def select_grade():
    page = request.args.get('page', 1)
    paginate = Grades.query.paginate(page, 5)
    grades = paginate.items
    if grades == []:
        return '暂无班级信息'
    return render_template('grade.html', students=grades, paginate=paginate)


@user.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if not all([username, password1, password2]):
            return render_template('register.html', msg='请输入完整信息')
        if password1 != password2:
            return render_template('register.html', msg='两次密码不一致')
        user = Users(u_name=username, u_password=password1)
        user.save()
        return redirect(url_for('user.login'))


@user.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.query.filter_by(u_name=username, u_password=password).first()
        if not user:
            return render_template('login.html', msg='用户名或密码错误')
        session['u_id'] = user.u_id
        return redirect(url_for('school.index'))



