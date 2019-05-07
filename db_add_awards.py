import csv
import os
from time import time

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Award



FILENAME = '/home/eddie/Projects/infost_785/pervade-coding/CISE_filtered_no_dupes.csv'
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
    basedir = os.path.abspath(os.path.dirname(__file__))
    engine = create_engine('sqlite:///' + os.path.join(basedir, 'app.db'))
    # engine = create_engine('postgres://mkfaygifhvukdz:4753f32b2ac2e2b7cf5ee67e4d871291b00eb06b03cd6027036ec0ae04902886@ec2-107-21-98-165.compute-1.amazonaws.com:5432/d1hvrpqqju1diu')


    Session = sessionmaker(bind=engine)
    session = Session()
    
    Base.metadata.create_all(bind=engine)

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
                    'award_id': row['award_number']
                    })
                session.add(record)
                if i % 1000 == 0:
                    session.flush()
                    print('*flush*')
            session.commit()
            print('we did it')
    except Exception as e:
        session.rollback()
        print(e)
    finally:
        session.close()
    print("Time elapsed: " + str(time() - t) + " s.")
