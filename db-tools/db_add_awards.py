from time import time
from datetime import datetime
from sqlalchemy import Column, Text, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import app
from app.models import Award, User
import os
import csv

os.chdir('/home/eddie/pervade-coding/db-tools')
FILENAME = 'NSF_Funded_Pis_CISE-out.csv'
FIELDNAMES = (
    'pi_name',
    'contact',
    'pi_email',
    'organization',
    'program',
    'title',
    'abstract',
    'award_number',
    'id'
)



if __name__ == "__main__":
    t = time()

    Base = declarative_base()

    # Create the database
    engine = create_engine('postgres://mkfaygifhvukdz:4753f32b2ac2e2b7cf5ee67e4d871291b00eb06b03cd6027036ec0ae04902886@ec2-107-21-98-165.compute-1.amazonaws.com:5432/d1hvrpqqju1diu')

    # Create a configured "Session" class
    Session = sessionmaker(bind=engine)

    # Create a Session object
    session = Session()

    try:
        with open(FILENAME, 'r', encoding='UTF-8') as csvfile:
            reader = csv.DictReader(csvfile, FIELDNAMES)
            for i, row in enumerate(reader):
                record = Award(**{
                    'pi_name': row['pi_name'],
                    'contact': row['contact'],
                    'pi_email': row['pi_email'],
                    'organization': row['organization'],
                    'program': row['program'],
                    'title': row['title'],
                    'abstract': row['abstract'],
                    'award_number': row['award_number']
                })
                session.add(record)
                if i % 1000 == 0:
                    session.flush()
                    print('*flush*')
            session.commit() #Attempt to commit all the records
            print('we did it')
    except Exception as e:
        session.rollback() #Rollback the changes on error
        print(e)
    finally:
        session.close() #Close the connection
    print("Time elapsed: " + str(time() - t) + " s.")