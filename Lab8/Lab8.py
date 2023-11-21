from sqlalchemy import create_engine, Column, Integer, String, Date, func
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime

# Підключення до бази даних
engine = create_engine('sqlite:///income_orm.db', echo=False)
Base = declarative_base()

# Оголошення класів моделей
class Income(Base):
    __tablename__ = 'income'

    id = Column(Integer, primary_key=True)
    source = Column(String)
    amount = Column(Integer)
    date = Column(Date)

# Створення таблиць
Base.metadata.create_all(engine)

# Створення сесії
def create_session():
    return Session(engine)

# Функція для додавання нового запису про дохід
def add_income(session, source, amount, date):
    # Перетворення рядка у форматі '07-11-2023' в об'єкт datetime.date
    date_object = datetime.strptime(date, '%d-%m-%Y').date()
    
    new_income = Income(source=source, amount=amount, date=date_object)
    session.add(new_income)
    session.commit()

# Функція для отримання всіх записів про дохід
def get_all_income(session):
    return session.query(Income).all()

# Функція для отримання загальної суми доходів за певний період
def get_total_income(session, start_date, end_date):
    return session.query(func.sum(Income.amount).label('total_income')).\
        filter(Income.date.between(start_date, end_date)).scalar()

# Функція для видалення запису про дохід за його ідентифікатором
def delete_income(session, income_id):
    income_to_delete = session.query(Income).filter_by(id=income_id).first()
    if income_to_delete:
        session.delete(income_to_delete)
        session.commit()


income_session = create_session()

# Додавання записів про дохід                 
add_income(income_session, 'стипендія', 1500, '07-11-2023')
add_income(income_session, 'Фріланс', 1000, '16-11-2023')
add_income(income_session, 'Підробіток', 2000, '18-11-2023')

# Отримання всіх записів про дохід
all_income = get_all_income(income_session)
print("Всі записи про дохід:")
for income in all_income:
    print(income.id, income.source, income.amount, income.date.strftime('%d-%m-%Y'))

# Видалення запису про дохід за його ідентифікатором
delete_income(income_session, 2)

# Отримання загальної суми та середнього доходу за певний період
start_date = '01-11-2023'
end_date = '31-11-2023'
total_income = get_total_income(income_session, start_date, end_date)


print("\nЗагальний дохід за період:", total_income)

# Закриття сесії
income_session.close()
