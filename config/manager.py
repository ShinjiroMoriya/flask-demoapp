from app import app

from flask_migrate import MigrateCommand
from flask_script import Manager, Server

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command(
    'server',
    Server(
        use_debugger=True,
        use_reloader=True,
        host='127.0.0.1',
        port='80'
    )
)
