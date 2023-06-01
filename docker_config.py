class Config:
    """
    Создание конфигурации приложения
    """
    DEBUG = True # Включаем режим отладки (Debug mode)
    SQLALCHEMY_DATABASE_URI = 'postgresql://flask_app:flask_app_password@pg/flask_app' # URI для подключения к базе данных
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Отключить отслеживание изменений моделей SQLAlchemy

