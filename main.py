from src import start_qdrant as sq
from src.ETL import Etl


etl = Etl()
etl.run()
sq.up_banco()