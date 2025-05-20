class CalendarEvent:
    id: str
    date: str
    title: str
    text: str

    def __eq__(self, other):
        return self.date == other