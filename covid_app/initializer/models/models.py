# Create and insert data in region table
from initializer.models.database import *
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class Region(Base):
    # Table name.
    __tablename__ = "region"
    # We always need an id
    code = Column(String, primary_key=True)
    name = Column(String(100), unique=True)
    departments = relationship("Department")

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __repr__(self):
        return "Region (code='%s', name='%s')" % (self.code, self.name)


class Department(Base):
    # Table name.
    __tablename__ = "departement"
    code = Column(String, primary_key=True)
    name = Column(String(100), unique=True)
    region = Column(String, ForeignKey('region.name'))
    information = relationship("Information")

    def __init__(self, code, name, region):
        self.code = code
        self.name = name
        self.region = region

    def __repr__(self):
        return "(code='%s', name='%s',region ='%s)" % (self.code, self.name, self.region)

class Information(Base):
    # Table name.
    __tablename__ = "information"
    # Column
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String, ForeignKey('departement.name'))
    date = Column(Date)
    hospitalises = Column(Integer)
    reanimation = Column(Integer)
    nouvellesHospitalisations = Column(Integer)
    nouvellesReanimations = Column(Integer)
    deces = Column(Integer)
    decesEhpad = Column(Integer)
    gueris = Column(Integer)
    casConfirmes = Column(Integer)
    sourceId = Column(Integer, ForeignKey('source.id'))
    source = relationship("Source")
    sourceType = Column(String)

    def __init__(self, nom, date, hospitalises, reanimation, nouvellesHospitalisations,
                 nouvellesReanimations, deces, decesEhpad, gueris, casConfirmes, sourceType):
        self.nom = nom
        self.date = date
        self.hospitalises = hospitalises
        self.reanimation = reanimation
        self.nouvellesHospitalisations = nouvellesHospitalisations
        self.nouvellesReanimations = nouvellesReanimations
        self.deces = deces
        self.decesEhpad = decesEhpad
        self.gueris = gueris
        self.casConfirmes = casConfirmes
        self.sourceType = sourceType

    def __repr__(self):
        return "Informations(nom='%s', date='%s', hospitalises ='%s', reanimation ='%s', " \
               "nouvellesReanimations ='%s', nouvellesHospitalisations ='%s'," \
               " deces ='%s', decesEhpad ='%s'," \
               " gueris ='%s',casConfirmes ='%s', sourceType ='%s')" \
               % (self.nom, self.date, self.hospitalises, self.reanimation, self.nouvellesReanimations,
                  self.nouvellesHospitalisations, self.deces, self.decesEhpad,
                  self.gueris, self.casConfirmes, self.sourceType)


class Source(Base):
    # Table name.
    __tablename__ = "source"
    # Column
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String)
    url = Column(String)
    archive = Column(String)


    def __repr__(self):
        return "Source(id='%s', nom='%s', url='%s',archive ='%s')" % (self.id, self.nom, self.url, self.archive)


association_table = Table('user_roles', Base.metadata,
                            Column('user_id', Integer, ForeignKey('users.id')),
                            Column('role_id', Integer, ForeignKey('roles.id'))
                             )


class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)  # primary keys are required
    email = Column(String(100), unique=True)
    password = Column(String(100))
    name = Column(String(1000))
    roles = relationship("Role", secondary=association_table)


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)  # primary keys are required
    libel = Column(String(100), unique=True)


if __name__ == "__main__":
    print("Creating region table...")
    print("Creating Department table...")
    print("Creating table information")
    print("creating table source")
    print("creating table user")
    print("creating table role")
    print("creating table user_role")
    Base.metadata.create_all(bind=engine)
    print("Done!, tables created")
