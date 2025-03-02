from src.core.connection.postgres import Session


def init_session(func):
    def wraper(self, *args, **kwargs):
        session = Session()
        try:
            resutl = func(self, session, *args, **kwargs)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close() 
        return resutl       
    return wraper
