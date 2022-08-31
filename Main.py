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

book1 = Book(title='Изучаем Python', id_publisher=2)
book2 = Book(title='Python. К вершинам мастерства', id_publisher=3)
book3 = Book(title='Python. Книга рецептов', id_publisher=1)

stock1 = Stock(id_book=2, id_shop=3, count=100)
stock2 = Stock(id_book=1, id_shop=3, count=250)
stock3 = Stock(id_book=2, id_shop=1, count=1800)
stock4 = Stock(id_book=3, id_shop=2, count=57)

shop1 = Shop(name='ЧитайГород')
shop2 = Shop(name='Лабиринт')
shop3 = Shop(name='Глобус')

session.add_all([publisher1, publisher2, publisher3,
                 book1, book2, book3,
                 stock1, stock2, stock3, stock4,
                 shop1, shop2, shop3])
session.commit()

print('Все издатели:')
for p in session.query(Publisher).all():
    print(p)

target_publisher = input('Введите название издателя:')

subq1 = session.query(Book).join(Book.publisher).filter(Publisher.name == target_publisher).subquery()

subq2 = session.query(Stock).join(subq1, Stock.id_book == subq1.c.id_book).subquery()

print('Список магазинов продающих книги выбранного издателя:')

for join2 in session.query(Shop).join(subq2, Shop.id_shop == subq2.c.id_shop).all():
    print(join2.name)


session.close()
