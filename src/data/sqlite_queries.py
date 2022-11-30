from src.data.sqlite_driver import Driver
import pandas as pd


def get_accidents(coords, box_sz) -> float:
    db = Driver()
    connection = db.create_connection("data/accidents.db")
    query = f"""
        SELECT Start_Time, Start_Lat, Start_Lng
        FROM accidents 
        WHERE Start_Lat BETWEEN {coords['lat'] - box_sz/2} AND {coords['lat'] + box_sz/2} AND Start_Lng BETWEEN {coords["lng"] - box_sz/2} AND {coords["lng"] + box_sz/2}
    """
    cursor = connection.execute(query)
    df = pd.DataFrame(
        cursor.fetchall(), columns=["Start_Time", "Start_Lat", "Start_Lng"]
    )
    df["Start_Time"] = pd.to_datetime(df["Start_Time"])
    return df


if __name__ == "__main__":
    df = get_accidents({"lat": 38, "lng": -77}, 1)
    pass
