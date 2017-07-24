from app import create_app
from flask_script import Manager,Shell,Server

from werkzeug.contrib.fixers import ProxyFix

app = create_app('dev')
app.wsgi_app = ProxyFix(app.wsgi_app)

# send email if error
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    handler = RotatingFileHandler('flask.log',maxBytes=1024 * 1024 * 100, backupCount=20)
    # 设置日志记录最低级别为DEBUG，低于DEBUG级别的日志记录会被忽略，不设置setLevel()则默认为NOTSET级别。
    handler.setLevel(logging.DEBUG)
    # 控制日志记录格式
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    # 将此handler加入到此app中
    app.logger.addHandler(handler)



manager = Manager(app)

def make_shell_context():
    return dict(app=app)

manager.add_command('shell',Shell(make_context=make_shell_context))
# DEBUG
manager.add_command("runserver", Server(use_debugger=True))


if __name__ == '__main__':
    # app.run()
    manager.run()