from app.dao.note_dao import BdayDao


class BdayService:
    """
    Класс для предоставления сервисных операций связанных с моделью BdayModel.

    Args:
        dao: Объект класса BdayDao для доступа к данным.

    Attributes:
        dao: Объект класса BdayDao для доступа к данным.

    """

    def __init__(self, dao: BdayDao):
        """
        Инициализация объекта класса BdayService.

        Args:
            dao: Объект класса BdayDao для доступа к данным.

        """
        self.dao = dao

    def get_all(self):
        """
        Получает все объекты модели BdayModel.

        Returns:
            Список всех объектов модели BdayModel.

        """
        return self.dao.get_all()

    def get_by_id(self, id):
        """
        Получает объект модели BdayModel по его идентификатору.

        Args:
            id: Идентификатор объекта.

        Returns:
            Объект модели BdayModel или None, если объект не найден.

        """
        return self.dao.get_by_id(id)

    def create(self, data):
        """
        Создает новый объект модели BdayModel.

        Args:
            data: Словарь с данными для создания объекта.

        Returns:
            Созданный объект модели BdayModel.

        """
        return self.dao.create(data)

    def update(self, data, id):
        """
        Обновляет существующий объект модели BdayModel по его идентификатору.

        Args:
            data: Словарь с данными для обновления объекта.
            id: Идентификатор объекта для обновления.

        """
        bday = self.dao.get_by_id(id)

        bday.fio = data.get('fio')
        bday.bday = data.get('bday')
        bday.say = data.get('say')

        self.dao.update(bday)

    def update_partial(self, data, id):
        """
        Частично обновляет существующий объект модели BdayModel по его идентификатору.

        Args:
            data: Словарь с данными для обновления объекта.
            id: Идентификатор объекта для обновления.

        """
        bday = self.dao.get_by_id(id)
        if "fio" in data:
            bday.fio = data.get("fio")

        if "bday" in data:
            bday.bday = data.get("bday")

        if "say" in data:
            bday.text = data.get("say")

        self.dao.update(bday)

    def delete(self, id):
        """
        Удаляет объект модели BdayModel по его идентификатору.

        Args:
            id: Идентификатор объекта для удаления.

        """
        return self.dao.delete(id)

