import psycopg2
from psycopg2 import sql
from time import sleep
import sys
from .process import CosmoCargoProcess
from .config import PostgresConfig
from .core.logger import logger


# check if database exist of not create database
def check_postgres_connection():
    """Check if PostgreSQL server is up and running."""
    try:
        # Connect to default postgres database
        conn = psycopg2.connect(
            host=PostgresConfig.DATABASE_HOSTNAME,
            user=PostgresConfig.DATABASE_USERNAME,
            password=PostgresConfig.DATABASE_PASSWORD,
            port=PostgresConfig.DATABASE_PORT,
            dbname="postgres"  # Connect to default database
        )
        conn.close()
        logger.info("PostgreSQL server is up and running")
        return True
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL server: {e}")
        return False

i=0
while i<5:
    if check_postgres_connection():
        break
    sleep(3)
    i+=1
else:
    logger.error("PostgreSQL server is not available. Exiting.")
    sys.exit(1)


# start process
cosmo_cargo_process = CosmoCargoProcess()
cosmo_cargo_process.start()
