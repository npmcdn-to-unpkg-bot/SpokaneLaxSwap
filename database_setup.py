
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime

Base = declarative_base()


# class for user information
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    email = Column(String(40), nullable=False)

# class for post information
class Posting(Base):
    __tablename__ = 'posting'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("user.email"))
    title = Column(String(30), nullable=False)
    description = Column(String(400), nullable=False)
    price = Column(Integer)
    category = Column(String)
    picture = Column(String)

    @property
    def serialize(self):
        """ returns object data in easily serializable form """
        return { 
            'title' : self.title,
            'description' : self.description,
            'price' : self.price,
            'category' : self.category 
        }
    


engine = create_engine('sqlite:///database.db')

Base.metadata.create_all(engine)



