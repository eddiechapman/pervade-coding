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

os.chdir('/home/eddie/pervade-coding-db-tools')
FILENAME = '180806-db-update-awards.csv'
FIELDNAMES = (
    'pi_last_name',
    'pi_first_name',
    'contact',
    'pi_email',
    'organization',
    'program',
    'title',
    'abstract',
    'award_number'
)



if __name__ == "__main__":
    t = time()

    Base = declarative_base()

    # Create the database

    engine = create_engine('postgres://eaillotiydvbpd:56985558ef52045d8a3ab27b743eea27fda35d3337e3bc1909775177c6fae735@ec2-54-221-210-97.compute-1.amazonaws.com:5432/d95184iqlcre2g')

    # Create a configured "Session" class
    Session = sessionmaker(bind=engine)

    # Create a Session object
    session = Session()

    try:
        with open(FILENAME, 'r', encoding='UTF-8') as csvfile:
            reader = csv.DictReader(csvfile, FIELDNAMES)
            for row in reader:
                record = Award(**{
                    'pi_last_name': row['pi_last_name'],
                    'pi_first_name': row['pi_first_name'],
                    'contact': row['contact'],
                    'pi_email': row['pi_email'],
                    'organization': row['organization'],
                    'program': row['program'],
                    'title': row['title'],
                    'abstract': row['abstract'],
                    'award_number': row['award_number'],
                    # 'pervasive_data': None,
                    # 'data_science': None,
                    # 'big_data': None,
                    # 'case_study': None,
                    # 'data_synonyms': None,
                    # 'not_relevant': None,
                    # 'timestamp': None,
                    # 'user_id': None,
                })
                print(record)
                session.add(record)
            session.commit() #Attempt to commit all the records
            print('we did it')
    except Exception as e:
        session.rollback() #Rollback the changes on error
        print(e)
    finally:
        session.close() #Close the connection
    print("Time elapsed: " + str(time() - t) + " s.")