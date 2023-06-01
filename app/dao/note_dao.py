from app.dao.models.bday_model import BdayModel


class BdayDao:
    """
    Класс для взаимодействия с моделью BdayModel в базе данных.

    Args:
        session: Сессия базы данных.

    Attributes:
        session: Сессия базы данных.

    """

    def __init__(self, session):
        """
        Инициализация объекта класса BdayDao.

        Args:
            session: Сессия базы данных.

        """
        self.session = session

    def get_all(self):
        """
        Получает все объекты модели BdayModel из базы данных.

        Returns:
            Список всех объектов модели BdayModel.

        """
        return self.session.query(BdayModel).all()

    def get_by_id(self, id):
        """
        Получает объект модели BdayModel по его идентификатору.

        Args:
            id: Идентификатор объекта.

        Returns:
            Объект модели BdayModel или None, если объект не найден.

        """
        return self.session.query(BdayModel).get(id)

    def create(self, data):
        """
        Создает новый объект модели BdayModel в базе данных.

        Args:
            data: Словарь с данными для создания объекта.

        """
        bday = BdayModel(**data)

        self.session.add(bday)
        self.session.commit()

    def update(self, bday):
        """
        Обновляет существующий объект модели BdayModel в базе данных.

        Args:
            bday: Объект модели BdayModel для обновления.

        """
        self.session.add(bday)
        self.session.commit()

    def delete(self, id):
        """
        Удаляет объект модели BdayModel из базы данных по его идентификатору.

        Args:
            id: Идентификатор объекта для удаления.

        """
        bday = self.get_by_id(id)

        self.session.delete(bday)
        self.session.commit()
