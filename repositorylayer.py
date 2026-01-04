from .models.user_model import userverify
from sqlmodel import SQLModel, create_engine, Session, select


#Here we are trying to connect with database 
sqllite_url="mysql+pymysql://root:password@localhost/userverify"
engine=create_engine(sqllite_url,echo=False)

#creating the tables in the database if they dont exist
def create_db_and_tables():
    #Creates the tables if they don't exist.
    SQLModel.metadata.create_all(engine)

def get_user(name: str):
    #Fetches a user from MySQL by name.
    with Session(engine) as session:
        statement = select(userverify).where(userverify.name == name)
        return session.exec(statement).first()
