from flask import Flask
from flask_restx import Api

from app.views.note_views import bday_ns
from default_config import Config
from setup_db import db


def create_app(config: Config) -> Flask:
    """
    Создает экземпляр Flask-приложения и применяет конфигурацию.

    Args:
        config: Объект класса Config с конфигурационными параметрами.

    Returns:
        Экземпляр Flask-приложения.

    """
    app = Flask(__name__)
    app.config.from_object(config)
    app.app_context().push()
    register_extensions(app)
    return app


def register_extensions(application: Flask) -> None:
    """
    Регистрирует расширения для Flask-приложения.

    Args:
        application: Экземпляр Flask-приложения.

    """
    db.init_app(application)
    api = Api(application)
    api.add_namespace(bday_ns)


# Создаем объект конфигурации приложения
app_config = Config()

# Создаем экземпляр Flask-приложения
app = create_app(app_config)

# Создаем все таблицы в базе данных
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
