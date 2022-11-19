from google.cloud import bigquery
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

client = bigquery.Client()


def get_accidents(lat, lng, box_sz) -> float:
    query = f"""
        SELECT Start_Lat, Start_Lng, Start_DOW
        FROM `dvahw3-365900.us_accidents.accidents` 
        WHERE Start_Lat BETWEEN {lat - box_sz/2} AND {lat + box_sz/2} AND Start_Lng BETWEEN {lng - box_sz/2} AND {lng + box_sz/2}
    """
    df = client.query(query).to_dataframe()
    return df


if __name__ == "__main__":
    get_accidents(40, -70, 10)
