class Config:
    """
    Создание конфигурации приложения
    """
    DEBUG = True # Включаем режим отладки (Debug mode)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db' # URI для подключения к базе данных
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Отключить отслеживание изменений моделей SQLAlchemy

