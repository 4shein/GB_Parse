from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import joinedload

from models import BASE, Post, Tag, Writer


class GBBlogDB:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        BASE.metadata.create_all(engine)
        self.session_db = sessionmaker(bind=engine)

    def create_post(self, post_obj: Post):
        session = self.session_db()
        post_obj.writer = self.__create_or_update(session, post_obj.writer)
        post_obj.tags = [self.__create_or_update(session, tag) for tag in post_obj.tags]
        session.add(post_obj)
        try:
            session.commit()
        except Exception:
            session.rollback()
        finally:
            session.close()

    def __create_or_update(self, session, model_obj):
        try:
            session.add(model_obj)
            session.commit()
        except Exception:
            session.rollback()
            model_obj = session.query(type(model_obj)).filter(type(model_obj).url == model_obj.url).first()
        return model_obj


if __name__ == '__main__':
    db = GBBlogDB('sqlite:///gb_blog.db')
    print(1)
