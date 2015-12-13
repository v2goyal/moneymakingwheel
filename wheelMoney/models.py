from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
	__tablename__ = 'users'

	Username = Column(String, primary_key=True)
	Password = Column(String)
	firstName = Column(String)
	lastName = Column(String)
	Spinsleft = Column(Integer)
	Balance = Column(Float)
	Cookie = Column(String)
	Email = Column(String)
	TimeLeft = Column(DateTime)
	AdIndex = Column(Integer)

	def __repr__(self):
		return "<User(Username='%s', Email='%s', firstName='%s', lastName='%s', Password='%s', TimeLeft='%d', AdIndex='%d', SpinsLeft='%d', Balance='%f', Cookie='%s')>" % (self.Username, self.Email, self.firstName, self.lastName, self.Password, self.TimeLeft, self.AdIndex, self.Spinsleft, self.Balance, self.Cookie)