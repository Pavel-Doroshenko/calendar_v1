from flask import Flask
from flask import request
import model
#import storage
#import db
import logic

app = Flask(__name__)

#_storage = storage.LocalStorage()
#_calendar_db = db.CalendarDB()
_calendar_logic = logic.CalendarLogic()

class ApiException(Exception):
    pass

def _from_raw(raw_calendar: str) -> model.CalendarEvent:
    parts = raw_calendar.split('|')
    if len(parts) == 3:
        note = model.CalendarEvent()
        note.id = None
        note.date = parts[0]
        note.title = parts[1]
        note.text = parts[2]
        return note
    elif len(parts) == 4:
        note = model.CalendarEvent()
        note.id = parts[0]
        note.date = parts[1]
        note.title = parts[2]
        note.text = parts[3]
        return note
    else:
        raise ApiException(f'invalid RAW note date {raw_calendar}')

def _to_raw(note: model.CalendarEvent) -> str:
    if note.id is None:
        return f'{note.date}|{note.title}|{note.text}'
    else:
        return f'{note.id}|{note.date}|{note.title}|{note.text}'


API_ROOT = '/api/v1/'
CALENDAR_API_ROOT = API_ROOT + '/calendar'

@app.route(CALENDAR_API_ROOT + '/', methods=['POST'])
def create():
    try:
        data = str(request.get_data(as_text=True))
        note = _from_raw(data)
        _id = _calendar_logic.create(note)
        return f'new id: {_id}', 201
    except Exception as ex:
        return f'failed to CREATE with: {ex}', 404


@app.route(CALENDAR_API_ROOT + '/', methods=['GET'])
def list():
    try:
        notes = _calendar_logic.list()
        raw_notes = ''
        for note in notes:
            raw_notes += _to_raw(note) +'\n'
        return raw_notes, 200
    except Exception as ex:
        return f'failed to LIST with: {ex}', 404


@app.route(CALENDAR_API_ROOT + '/<_id>/', methods=['GET'])
def read(_id: str):
    try:
        note = _calendar_logic.read(_id)
        raw_note = _to_raw(note)
        return raw_note, 200
    except Exception as ex:
        return f'failed to READ with: {ex}', 404


@app.route(CALENDAR_API_ROOT + '/<_id>/', methods=['PUT'])
def update(_id: str):
    try:
        data = str(request.get_data(as_text=True))
        note = _from_raw(data)
        _calendar_logic.update(_id, note)
        return 'updated', 200
    except Exception as ex:
        return f'failed to UPDATE with: {ex}', 404



@app.route(CALENDAR_API_ROOT + '/<_id>/', methods=['DELETE'])
def delete(_id: str):
    try:
        _calendar_logic.delete(_id)
        return "delete", 200
    except Exception as ex:
        return f'failed to DELETE with: {ex}', 404


if __name__ =='__main__':
    app.run()