from typing import List
import model
import db

DATE_LIMIT = 12
TITLE_LIMIT = 21
TEXT_LIMIT = 61

class LogicException(Exception):
    pass

class CalendarLogic:
    def __init__(self):
        self._calendar_db = db.CalendarDB()


    @staticmethod
    def _validate_calendar(note: model.CalendarEvent):
        if note is None:
            raise LogicException('calendar is None')
        if note.date is None or len(note.date) > DATE_LIMIT:
            raise LogicException(f'date lenght > MAX: {DATE_LIMIT}')
        if note.title is None or len(note.title) > TITLE_LIMIT:
            raise LogicException(f'title lenht > MAX: {TITLE_LIMIT}')
        if note.text is None or len(note.text) > TEXT_LIMIT:
            raise LogicException(f'text lenght > MAX: {TEXT_LIMIT}')


    def create(self, note: model.CalendarEvent) -> str:
        self._validate_calendar(note)
        try:
            date_list = self._calendar_db.list()
            for date in date_list:
                if note.date == date:
                    raise LogicException(f'{note.date}: такая дата уже существует')
            return self._calendar_db.create(note)
        except Exception as ex:
            raise LogicException(f'failed CREATE operation with: {ex}')


    def list(self) -> List[model.CalendarEvent]:
        try:
            return self._calendar_db.list()
        except Exception as ex:
            raise LogicException(f'failed LIST operation with: {ex}')

    def read(self, _id: str) -> model.CalendarEvent:
        try:
            return self._calendar_db.read(_id)
        except Exception as ex:
            raise LogicException(f'failed READ operation with: {ex}')

    def update(self, _id: str, note: model.CalendarEvent):
        self._validate_calendar(note)
        try:
            date_list = self._calendar_db.list()
            for date in date_list:
                if note.date == date:
                    raise LogicException(f'такая дата уже существует')
            return self._calendar_db.update(_id, note)
        except Exception as ex:
            raise LogicException(f'failed UPDATE operation with: {ex}')

    def delete(self, _id: str):
        try:
            return self._calendar_db.delete(_id)
        except Exception as ex:
            raise LogicException(f'failed DELETE operation with: {ex}')
