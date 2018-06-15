from flask_script import Manager

from utils.function import create_app

app = create_app()
manage = Manager(app=app)


if __name__ == '__main__':
    manage.run()
