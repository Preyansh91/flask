from sqlalchemy import *
from sqlalchemy import create_engine, Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://root:root@localhost/flask')
Base = declarative_base()

class UsersDb(Base):
    __tablename__ = "usersTable"
    userid = Column(Integer, primary_key=True)
    username = Column(String(32))
    password = Column(String(32))
    email = Column(String(50))
#    results = relationship('ResultsDb', backref='user')

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

class BigipDb(Base):
    __tablename__ = "bigipTable"
    bigipid = Column(Integer, primary_key=True)
    bigip_name = Column(String(32))

    def __init__(self, bigip_name):
        self.bigip_name = bigip_name

class ReleaseDb(Base):
    __tablename__ = "releaseTable"
    releaseid = Column(Integer, primary_key=True)
    release_name = Column(String(32))

    def __init__(self, release_name):
        self.release_name = release_name

class ProjectDb(Base):
    __tablename__ = "projectTable"
    projectid = Column(Integer, primary_key=True)
    project_name = Column(String(32))

    def __init__(self, project_name):
        self.project_name = project_name

class ResultsDb(Base):
    __tablename__ = "resultsTable"
    testid = Column(Integer, primary_key=True)
    description = Column(String(60))
    user_id = Column(Integer, ForeignKey('usersTable.userid', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    bigip_id = Column(Integer, ForeignKey('bigipTable.bigipid', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    release_id = Column(Integer, ForeignKey('releaseTable.releaseid', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    project_id = Column(Integer, ForeignKey('projectTable.projectid', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
#    stats = relationship('StatsDb', backref='test')

    def __init__(self, description, user_id, bigip_id, release_id, project_id):
        self.description = description
        self.user_id = user_id
        self.bigip_id = bigip_id
        self.release_id = release_id
        self.project_id = project_id

class StatsDb(Base):
    __tablename__ = "statsTable"
    statsid = Column(Integer, primary_key=True)
    testname = Column(String(200))
    tps = Column(Integer)
    cpu = Column(Integer)
    degradation = Column(Integer)
    comments = Column(String(300))
    test_id = Column(Integer, ForeignKey('resultsTable.testid', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)

    def __init__(self, testname, tps, cpu, degradation, comments, test_id):
        self.testname = testname
        self.tps = tps
        self.cpu = cpu
        self.degradation = degradation
        self.comments = comments
        self.test_id = test_id

if __name__ == "__main__":
    Base.metadata.create_all(engine)
