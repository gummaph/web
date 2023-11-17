import sqlalchemy as db
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

engine=db.create_engine("sqlite:///employees.sqlite")
conn=engine.connect()

metadata=db.MetaData()
employee=db.Table('Employee',metadata,
                  db.Column('id',db.Integer(),primary_key=True),
                  db.Column('name',db.String(255),nullable=False),
                  db.Column('address',db.String(1024),default='Earth'),
                  db.Column('pic_id',db.String(1024),default='default'))
metadata.create_all(engine)
Base = declarative_base()
session = sessionmaker(bind=engine)()

class Employee(Base):
    __tableme__="Employee"
    id=Column(Integer,primary_key=True)
    name=Column(String)
    address=Column(String)
    pic_id=Column(String)
    def __init__(self,id,name,address,pic_id='default'):
        super().__init__()

        self.id=id
        self.name=name
        self.address=address
        self.pic_id=pic_id
    def add_Employee(self):
        session.add(self)
        session.commit()


