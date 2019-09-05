
"""
    Import this file to get an sqlalchemy session object throughout the program.
"""


def create_session():
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine
    global session
    global engine
    en_flag = 0
    ses_flag = 0
    try:
        engine = create_engine(connection_url)
        en_flag = 1
        Session = sessionmaker(bind=engine)
        session = Session()
        ses_flag = 1
    except Exception as e:
        if en_flag == 1:
            engine.dispose()
        if ses_flag == 1:
            session.close()
        raise e


create_session()
