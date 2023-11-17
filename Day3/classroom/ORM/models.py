from sqlalchemy import create_engine, Integer, String, Column
from sqlalchemy.orm import declarative_base,sessionmaker

engine = create_engine("sqlite:///employees.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False,unique=True)
    address = Column(String, nullable=False)
    password = Column(String, nullable=False)
    pic_id = Column(String, default="default_pic")

    def __str__(self):
        return str({
            "id":self.id,
            "name":self.name,
            "address":self.address,
            "password":self.password
        })


Base.metadata.create_all(engine)
