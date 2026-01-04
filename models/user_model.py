from sqlalchemy import table
from sqlmodel import SQLModel,Session, create_engine,select,Field
from typing import Optional

class userverify(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    name: str
    phonenumber: str
    address:  str
    dob:  str