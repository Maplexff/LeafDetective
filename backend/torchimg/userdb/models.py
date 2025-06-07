from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,BLOB,REAL,Double,TEXT,VARCHAR
from sqlalchemy.orm import relationship
# from .database import BASE
from config.database import Base
    
# class User(BASE):
#     __tablename__ = "user_password"
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, index=True)
#     password = Column(String)
#     items = relationship("History", back_populates="owner")


# class History(BASE):
#     __tablename__ = "history"
    
#     imageid = Column(Integer, primary_key=True, index=True)# autoincrement=True)
#     image = Column(BLOB)
#     time = Column(String)
#     location = Column(String)
#     lat = Column(REAL)
#     lng = Column(REAL)
#     reportid = Column(Integer, ForeignKey("user_password.id"))
#     predlabel = Column(String)
#     predclass = Column(String)
#     predscore = Column(REAL)
#     owner = relationship("User", back_populates="items")


# class User(Base):
#     __tablename__ = "user_password"
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(TEXT, unique=True, index=True)
#     password = Column(TEXT)
#     items = relationship("History", back_populates="owner")


# class History(Base):
#     __tablename__ = "history"
    
#     imageid = Column(Integer, primary_key=True, index=True)# autoincrement=True)
#     image = Column(BLOB)
#     time = Column(TEXT)
#     location = Column(TEXT)
#     lat = Column(Double)
#     lng = Column(Double)
#     reportid = Column(Integer, ForeignKey("user_password.id"))
#     predlabel = Column(TEXT)
#     predclass = Column(TEXT)
#     predscore = Column(Double)
#     owner = relationship("User", back_populates="items")





# class Item(BASE):
#     __tablename__ = "items"
    
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))
    
#     owner = relationship("User", back_populates="items")