from database import engine,Base, db_session
from sqlalchemy import Table, MetaData,Column,Integer,Date, String, PrimaryKeyConstraint
from sqlalchemy.sql import text
from sqlalchemy_views import CreateView, DropView


metadata = MetaData(engine)
view = Table('CleanDataByDepartement', metadata)
definition = text('select i."date" as date,'
                  'i.nom as departement,'
                  'max(i.hospitalises) as hospitalises,'
                  'max(i.reanimation) as reanimation,'
                  'max(i."nouvellesHospitalisations") as "nouvellesHospitalisations",'
                  'max(i."nouvellesReanimations") as "nouvellesReanimations",'
                  'max(i.deces) as deces,'
                  'max(i."decesEhpad") as "decesEhpad",'
                  'max(i.gueris) as gueris,'
                  'max(i."casConfirmes") as "casConfirmes"'
                  'from information i '                
                  'group by date, departement '
                  'order by date desc')

# Info by department
create_view = CreateView(view, definition, or_replace=True)
engine.execute(create_view)
# Info by region
CleanDataByRegion = Table('CleanDataByRegion', metadata)
definition = text('select dp.date,d.region,r.code, '
                  'sum(dp.hospitalises) as hospitalises, '
                  'sum(dp.reanimation) as reanimation, '
                  'sum(dp."nouvellesHospitalisations") as "nouvellesHospitalisations", '
                  'sum(dp."nouvellesReanimations") as "nouvellesReanimations", '
                  'sum(dp.deces) as deces,'
                  'sum(dp."decesEhpad") as "decesEhpad",'
                  'sum(dp.gueris) as gueris,'
                  'sum(dp."casConfirmes") as "casConfirmes"'
                  'from public."CleanDataByDepartement" dp '
                  'join departement d '
                  'on dp.departement = d."name"'
                  'join region r on d.region = r."name"'
                  'group by date, d.region, r.code '
                  'order by date desc')
create_view = CreateView(CleanDataByRegion, definition, or_replace=True)
engine.execute(create_view)




