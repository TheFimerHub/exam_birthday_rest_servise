from marshmallow import Schema, fields
from setup_db import db


class BdayModel(db.Model):
    '''
    Создаем модель с полями
    '''
    __tablename__ = 'bday'

    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String)
    bday = db.Column(db.String)
    say = db.Column(db.String)

class BdaySchema(Schema):
    '''
    Создаем схему с полями
    '''
    id = fields.Int(dump_only=True)
    fio = fields.Str()
    bday = fields.Str()
    say = fields.String()