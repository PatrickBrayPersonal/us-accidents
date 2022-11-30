import sqlite3
from sqlite3 import Error
import csv
import pandas as pd
import dask.dataframe as dd

COLS = [
    "ID",
    "Severity",
    "Start_Time",
    "Start_Lat",
    "Start_Lng",
    "Precipitation(in)",
    "Weather_Condition",
]


class Driver:
    ############### DO NOT MODIFY THIS SECTION ###########################
    ######################################################################
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))

        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.execute(query)
                connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)

    def create_table(self, connection):
        connection.execute("DROP TABLE IF EXISTS accidents;")
        sql = """
        CREATE TABLE accidents (
            ID TEXT PRIMARY KEY,
            Severity INTEGER,
            Start_Time DATETIME,
            Start_Lat FLOAT,
            Start_Lng FLOAT,
            Precipitation FLOAT,
            Weather_Condition TEXT
        )
        """
        return self.execute_query(connection, sql)

    def import_data(self, connection, path):
        df = pd.read_parquet(path, columns=COLS)
        df = df.rename(
            columns={"Start_Time": "Time", "Precipitation(in)": "Precipitation"}
        )

        def _insert(row, cols):
            columns = tuple(cols)
            row = row.fillna(0.0)
            vals = tuple(row.values)
            sql = f"""
            INSERT INTO accidents {columns}
            VALUES {vals}
            """
            self.execute_query(connection, sql)

        df.apply(lambda x: _insert(x, df.columns), axis=1)

    def import_bulk(self, connection, path):
        df = (
            pd.read_parquet(path, columns=COLS)
            .rename(columns={"Precipitation(in)": "Precipitation"})
            .fillna(0.0)
        )
        df["Start_Time"] = df["Start_Time"].astype(str)
        columns = tuple(df.columns)
        vals = ",\n".join([str(tuple(row)) for row in df.values])
        sql = f"""
        INSERT INTO accidents {columns}
        VALUES {vals}
        """
        return self.execute_query(connection, sql)


if __name__ == "__main__":
    db = Driver()
    connection = db.create_connection("data/accidents.db")
    # Sample Drop table
    connection.execute("DROP TABLE IF EXISTS sample;")
    # Sample Create
    connection.execute("CREATE TABLE sample(id integer, name text);")
    connection.execute("DROP TABLE IF EXISTS sample;")
    print(db.create_table(connection))
    print(db.import_bulk(connection, "data/processed/us-accidents.parquet"))
