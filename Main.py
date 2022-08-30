import sqlalchemy

from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Book, Stock, Shop, Sale


DSN = "postgresql://postgres:111@localhost:5432/orm_db"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)


Session = sessionmaker(bind=engine)
session = Session()

publisher1 = Publisher(name='ЛитРес')
publisher2 = Publisher(name='Эксмо')
publisher3 = Publisher(name='Алтапресс')

session.add_all([publisher1, publisher2, publisher3])
session.commit()

for p in session.query(Publisher).all():
    print(p)

target_publisher = input('Введите название издателя: ')

for p in session.query(Publisher).filter(Publisher.name == target_publisher).all():
    print(p)


session.close()
