from app.dao.note_dao import BdayDao
from app.services.note_servise import BdayService
from setup_db import db

# Создаем объект BdayDao, передавая ему сессию базы данных
bday_dao = BdayDao(db.session)

# Создаем объект BdayService, передавая ему объект BdayDao
bday_service = BdayService(dao=bday_dao)

