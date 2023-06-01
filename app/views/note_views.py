from flask import request
from flask_restx import Namespace, Resource
from ..dao.models.bday_model import BdaySchema
from ..implemented import bday_service

bday_ns = Namespace("bdays")


@bday_ns.route("/")
class BdaysView(Resource):
    """
    Класс представления для работы с коллекцией BdayModel.

    """

    def get(self):
        """
        Получает все объекты модели BdayModel.

        Returns:
            Список всех объектов модели BdayModel.

        """
        bdays = bday_service.get_all()
        return BdaySchema(many=True).dump(bdays), 200

    def post(self):
        """
        Создает новый объект модели BdayModel.

        Returns:
            Созданный объект модели BdayModel.

        """
        data = request.json
        new_bday = bday_service.create(data)
        return BdaySchema().dump(new_bday), 201


@bday_ns.route("/<int:id>")
class BdayView(Resource):
    """
    Класс представления для работы с отдельным объектом BdayModel.

    """

    def get(self, id):
        """
        Получает объект модели BdayModel по его идентификатору.

        Args:
            id: Идентификатор объекта.

        Returns:
            Объект модели BdayModel.

        """
        bday = bday_service.get_by_id(id)
        return BdaySchema().dump(bday), 200

    def put(self, id):
        """
        Обновляет существующий объект модели BdayModel по его идентификатору.

        Args:
            id: Идентификатор объекта для обновления.

        Returns:
            Обновленный объект модели BdayModel.

        """
        data = request.json
        bday_service.update(data, id)

        bday = bday_service.get_by_id(id)
        return BdaySchema().dump(bday), 202

    def patch(self, id):
        """
        Частично обновляет существующий объект модели BdayModel по его идентификатору.

        Args:
            id: Идентификатор объекта для обновления.

        Returns:
            Частично обновленный объект модели BdayModel.

        """
        data = request.json
        bday_service.update_partial(data, id)

        bday = bday_service.get_by_id(id)
        return BdaySchema().dump(bday), 202

    def delete(self, id):
        """
        Удаляет объект модели BdayModel по его идентификатору.

        Args:
            id: Идентификатор объекта для удаления.

        Returns:
            Сообщение об успешном удалении объекта.

        """
        bday_service.delete(id)
        response = {"message": "Note has deleted successfully"}

        return response, 200

