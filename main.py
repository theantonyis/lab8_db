import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP, select
from sqlalchemy.orm import declarative_base, Session

# Підключення до бази даних
engine = create_engine('sqlite:///notes.db', echo=False)
Base = declarative_base()

# Оголошення класів моделей
class Notes(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now())


# Створення таблиць
Base.metadata.create_all(engine)

# Створення сесії
def create_session():
    return Session(engine)

# Функція для створення нової замітки
def create_note(session, title, content):
    new_note = Notes(title=title, content=content)
    session.add(new_note)
    session.commit()


# Функція для отримання всіх заміток
def get_all_notes(session):
    all_notes = session.query(Notes).all()
    print("Всі замітки:")
    for note in all_notes:
        print(note.id, '\t', note.title, '\t', note.content, '\t', note.created_at)

# Функція для оновлення замітки
def update_note(session, id, new_title, new_content):
    notes_to_update = session.query(Notes).filter_by(id=id).first()
    if notes_to_update:
        notes_to_update.title = new_title
        notes_to_update.content = new_content
        session.commit()

# Функція для видалення замітки
def delete_note(session, id):
    note_to_delete = session.query(Notes).filter_by(id=id).first()
    if note_to_delete:
        session.delete(note_to_delete)
        session.commit()

def search_note (session, id):
    note_to_search = session.get(Notes, id)
    if note_to_search is not None:
        print(note_to_search.id, '\t', note_to_search.title, '\t', note_to_search.content, '\t', note_to_search.created_at)
    else:
        print("Така замітка не знайдена.")


# Закриття сесії
def close_session(session):
    session.close()

# Приклад використання:
session = create_session()

# CRUD операції

with session:
    notes_to_add = [['Note 1', 'Products list: milk, bread, chocolate'],
                    ['Note 2', "Don't forget to order the present!"],
                    ['Note 3', 'Olivia birthday - 25 November']]
    for item in notes_to_add:
        create_note(session, item[0], item[1])

    update_note(session, 102, "New title", "Don't forget to write a title!")

    delete_note(session, 104)

    # Вивід всіх заміток
    get_all_notes(session)

    print("Знайдена замітка: ")
    search_note(session, 100)


# Закриття сесії
close_session(session)
