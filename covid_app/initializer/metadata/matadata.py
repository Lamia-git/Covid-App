from models.models import *
from models.database import *
from sqlalchemy import inspect
from pprint import pprint

inspector = inspect(engine)

# Get table name's and column's information

for e in inspector.get_table_names():
    print("Table : ",e)
    print("columns :")
    pprint((inspector.get_columns(e)))
    print("Tuple indexes: ", inspector.get_indexes(e))
    print("_____________________________________")
