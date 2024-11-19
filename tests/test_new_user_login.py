from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Настройки подключения к базе данных
DATABASE_URL = "postgresql+psycopg2://dev_user:123@localhost:5432/dev_db"

# Инициализация базы данных
Base = declarative_base()

# Определение модели пользователя
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Создание подключения к базе данных
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_user():
    # Создаем сессию
    session = SessionLocal()

    try:
        # Создаем нового пользователя
        new_user = User(name="Test User", email="test_user@example.com")
        session.add(new_user)

        # Сохраняем изменения
        session.commit()
        print(f"Пользователь {new_user.name} добавлен с ID {new_user.id}.")
    except Exception as e:
        session.rollback()
        print(f"Ошибка при добавлении пользователя: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    # Создаем таблицы, если их нет
    Base.metadata.create_all(bind=engine)
    # Добавляем пользователя
    add_user()