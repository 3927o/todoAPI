from flask import url_for, request, render_template
from flask_restful import Api, Resource, reqparse
from database import db, app, Task, User
from flask_login import login_required, login_user, logout_user, LoginManager, current_user
import logging

api = Api(app)
post_reqparse = reqparse.RequestParser()
post_reqparse.add_argument('title', type=str, required=True, location='json')
post_reqparse.add_argument('content', type=str, location='json')
post_reqparse.add_argument('timeend', type=str, required=True, location='json')

put_reqparse = reqparse.RequestParser()
put_reqparse.add_argument('title', type=str, location='json')
put_reqparse.add_argument('content', type=str, location='json')
put_reqparse.add_argument('finished', type=int, location='json')
put_reqparse.add_argument('timeend', type=str, location='json')

user_post_reqparse = reqparse.RequestParser()
user_post_reqparse.add_argument('action', type=str, required=True, location='json')
user_reqparse = reqparse.RequestParser()
user_reqparse.add_argument('username', type=str, required=True, location='json')
user_reqparse.add_argument('password', type=str, required=True, location='json')

user_put_reqparse = reqparse.RequestParser()
user_put_reqparse.add_argument('username', type=str, location='json')
user_put_reqparse.add_argument('password', type=str, location='json')


# class Name(fields.Raw):
#     def format(self, value):
#         return str(User.query.get(value).username)
#
#
# class Finish(fields.Raw):
#     def format(self, value):
#         return "finished" if value == 1 else "unfinished"
#
#
# class Time(fields.Raw):
#     def format(self, value):
#         return str(value)
#
#
# task_fields = {
#     'uri': fields.Url('task', absolute=True),
#     'username': Name(attribute='uid'),
#     'title': fields.String,
#     'content': fields.String,
#     'finished': Finish,
#     'timestart': fields.DateTime,
#     'timeend': Time,
# }

lm = LoginManager()
lm.init_app(app)
lm.login_message = 'please login'
lm.login_view = 'login'
@lm.user_loader
def load_user(id):
    return User.query.get(id)


@app.route('/')
def index():
    return "hello world"


@app.route('/login')  # 跟UserAPI资源的post方法合在一起，添加一个action参数
def login():
    return {'status': 1, 'message': 'login please', 'data': {}}
#     else:
#         status = 0
#         message = ""
#         user = User.query.filter_by(username=request.form['username']).first()
#         if user is not None:
#             if user.verify_password(request.form['password']):
#                 login_user(user, remember=request.form['remember'])
#                 data = {'uid': user.id, 'username': user.username}
#             else:
#                 status = 1
#                 message = 'wrong password'
#                 data = {}
#         else:
#             status = 1
#             message = 'user do not exit'
#             data = {}
#         return {'status': status, 'message': message, 'data': data}
#
#
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return {'status': 0, 'message': 'success', 'data': {}}


class TaskListAPI(Resource):
    decorators = [login_required]

    def get(self):
        state = 0
        message = "succeed"
        status = int(request.args.get('status', -1))
        tasks = current_user.getTasks(status)
        tasks = get_tasks(tasks)
        return {'status': state, 'message': message, 'data': tasks}

    def post(self):
        state = 0
        message = "succeed"
        args = post_reqparse.parse_args()
        new_task = Task(title=args['title'], timeend=args['timeend'], uid=current_user.id)
        if 'content' in args:
            new_task.content = args['content']
        db.session.add(new_task)
        db.session.commit()
        return {'status': state, 'message': message, 'data': make_public_task(new_task)}

    def put(self):
        state = 0
        message = "succeed"
        status = int(request.args.get('status', -1))
        tasks = current_user.getTasks(status)
        args = put_reqparse.parse_args()
        update(args, tasks)
        tasks = get_tasks(tasks)
        return {'status': state, 'message': message, 'data': tasks}

    def delete(self):
        status = int(request.args.get('status', -1))
        tasks = current_user.getTasks(status)
        for task in tasks:
            db.session.delete(task)
        db.session.commit()
        return {'status': 0, 'message': "succeed", 'data': {}}


class TaskAPI(Resource):
    decorators = [login_required]

    # @marshal_with(task_fields)
    def get(self, id):
        if not verify_task(id):
            return {"status": 1, "message": "该事项不存在或无权限查看", "data": {}}
        state = 0
        message = "succeed"
        task = get_task(id)
        # task = Task.query.get(id)
        return {'status': state, 'message': message, 'data': task}

    def put(self, id):
        if not verify_task(id):
            return {"status": 1, "message": "该事项不存在或无权限查看", "data": {}}
        state = 0
        message = "succeed"
        task = Task.query.filter_by(id=id).all()
        args = dict(put_reqparse.parse_args())
        update(args, task)
        task = make_public_task(task[0])
        return {'status': state, 'message': message, 'data': task}

    def delete(self, id):
        if not verify_task(id):
            return {"status": 1, "message": "该事项不存在或无权限查看", "data": {}}
        task = Task.query.get(id)
        db.session.delete(task)
        db.session.commit()
        return {'status': 0, 'message': 'succeed', 'data': {}}


# class UserListAPI(Resource):
#     def get(self):
#         users = User.query.all()
#         Users = []
#         for user in users:
#             Users.append({'uid': user.id, 'name': user.username})
#         return {'status': 0, 'message': 'succeed', 'data': Users}
#
#     def post(self):
#         data = user_post_reqparse.parse_args()
#         new_user = User(data['username'])
#         new_user.hash_password(data['password'])
#         db.session.add(new_user)
#         db.session.commit()
#         return {'status': 0, 'message': 'succeed', 'data': {'uid': new_user.id, 'username': new_user.username}}


class UserAPI(Resource):
    @login_required
    def get(self):
        return {'status': 0, 'message': 'succeed', 'data': {'uid': current_user.id, 'username': current_user.username}}

    def post(self):
        data = user_post_reqparse.parse_args()
        if data['action'] == "signin":
            data = user_reqparse.parse_args()
            data = Signin(data)
        elif data['action'] == "login":
            data = user_reqparse.parse_args()
            data = Login(data)
        elif data['action'] == "logout":
            data = Logout()
        else:
            return {"status": 1, "message": "unknown param"}
        return data

    @login_required
    def put(self):
        args = user_put_reqparse.parse_args()
        if args['username'] is not None:
            current_user.username = args['username']
        if args['password'] is not None:
            current_user.hash_password(args['password'])
        db.session.commit()
        return {'status': 0, 'message': 'succeed', 'data': {'uid': current_user.id, 'username': current_user.username}}

    @login_required
    def delete(self):
        id = current_user.id
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        logout_user()
        return {'status': 0, 'message': 'succeed', 'data': {}}


class Data(Resource):
    def get(self):
        status = int(request.args.get('status', -1))
        tasks = get_Tasks(status)
        return {'status': 0, 'message': 'succeed', 'data': len(tasks)}


api.add_resource(TaskListAPI, '/api/tasks/', endpoint='tasks')
api.add_resource(TaskAPI, '/api/tasks/<int:id>', endpoint='task')
api.add_resource(Data, '/api/data/', endpoint='data')
# api.add_resource(UserListAPI, '/api/users/', endpoint='users')
api.add_resource(UserAPI, '/api/user/', endpoint='user')


def get_tasks(tasks):  # 返回字典
    Tasks = []
    for task in tasks:
        Tasks.append(make_public_task(task))
    return Tasks


@login_required
def get_Tasks(status):  # 返回Task类
    if status == -1:
        tasks = current_user.tasks
    elif status == 0:
        tasks = Task.query.filter_by(finished=0).all()
    else:
        tasks = Task.query.filter_by(finished=1).all()
    return tasks


def get_task(id):
    task = Task.query.filter_by(id=id).first()
    return make_public_task(task)


def make_public_task(task):
    task_ = dict()
    task_['uri'] = url_for(endpoint='task', id=task.id)  # 争取用filed
    task_['uid'] = task.uid
    task_['title'] = task.title
    task_['content'] = task.content
    task_['finished'] = task.finished
    task_['timestart'] = str(task.timeStart)
    task_['timeend'] = str(task.timeEnd)
    return task_


def exit_task(id):
    task = Task.query.filter_by(id=id).first()
    if task is not None:
        return True
    else:
        return False


def update(args, tasks):
    for task in tasks:
        if args['title'] is not None:
            task.title = args['title']
        if args['finished'] is not None:
            task.finished = args['finished']
        if args['content'] is not None:
            task.content = args['content']
        if args['timeend'] is not None:
            task.timeEnd = args['timeend']
        db.session.commit()


def verify_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        # abort(404)
        # return {"message": 'task do not exit'}
        return 0
    if current_user.id != task.uid:
        # abort(404)
        # return {"message": '无权限'}
        return 0
    return 1


def Signin(data):
    status = 0
    message = "succeed"
    user = User.query.filter_by(username=data['username']).first()
    if user is not None:
        status = 1
        message = "username already exits"
        data = {}
    else:
        new_user = User(data['username'])
        new_user.hash_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        data = {'uid': new_user.id, 'username': new_user.username}
    return {'status': status, 'message': message, 'data': data}


def Login(data):
    status = 0
    message = "succeed"
    user = User.query.filter_by(username=data['username']).first()
    if "remember" not in data:
        data["remember"] = 0
    if user is not None:
        if user.verify_password(data['password']):
            login_user(user, remember=data['remember'])
            data = {'uid': user.id, 'username': user.username}
        else:
            status = 1
            message = 'wrong password'
            data = {}
    else:
        status = 1
        message = 'user do not exit'
        data = {}
    return {'status': status, 'message': message, 'data': data}


@login_required
def Logout():
    logout_user()
    return {'status': 0, 'message': 'success', 'data': {}}


if __name__ == '__main__':
    app.run(debug=False)
