from sqlalchemy import create_engine, MetaData, Table
from .config import DATABASE_URI

def create_database(dataframes):
    engine = create_engine(DATABASE_URI)
    for table_name, dataframe in dataframes.items():
        dataframe.to_sql(table_name, engine, if_exists="replace")
    return engine

def get_tables(engine):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    tables = {table.name: table for table in metadata.tables.values()}
    return tables
