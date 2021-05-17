from models.database import engine
import pandas as pd

# Get departement list.
departements = """select distinct(departement) from "CleanDataByDepartement"  """

# Get covid information by departement from database covid.
allData = """select * from "CleanDataByDepartement"  """

# Get covid information by departement from database covid.( divided on population)

allDataDividedPopulation = """
  select
	c.departement, 
	(sum(c.deces) ::decimal/ d.population) as deces_population, 
	(sum(c."nouvellesHospitalisations") ::decimal/ d.population) as nouvellesHospitalisationsp,
	(sum(c."nouvellesReanimations") ::decimal / d.population) as nouvellesReanimationp,
	(sum(c.hospitalises) ::decimal / d.population) as hospitalisesp,
	(sum(c."reanimation") ::decimal / d.population) as reanimationp,
	(sum(c."gueris") ::decimal / d.population) as guerisp	
    from
	"CleanDataByDepartement" c
    join departement d on
	c.departement = d."name"
	group by c.departement,d.population 
"""

# Get region list.
regions = """select distinct(region) from "CleanDataByRegion"  """

# Get covid information by region from database covid.
allDataRegion = """select * from "CleanDataByRegion"  """

# Get covid information by region from database covid.( divided on population)

DividedPopRegion = """
    select
	c.region ,c.date,
	(c.deces ::decimal/ r.population) as deces, 
	(c."nouvellesHospitalisations" ::decimal/r.population) as nouvellesHospitalisations,
	(c."nouvellesReanimations" ::decimal / r.population) as nouvellesReanimation,
	(c.hospitalises ::decimal / r.population) as hospitalises,
	(c."reanimation" ::decimal / r.population) as reanimation,
	(c."gueris" ::decimal / r.population) as gueris	
    from
	"CleanDataByRegion" c
    join region r on
	c.region = r."name"
"""
# Get covid info by date

infoDepartDate = """ select c.date, c.hospitalises,c."nouvellesHospitalisations",
c.departement,c.deces,lag(deces) over (order by date ) as previous_deces,
                    lag(deces) over (order by date desc) - deces as nouveau_deces 
                    from "CleanDataByDepartement" c
                    where 
                    departement = 'Territoire de Belfort'
                    order by date desc """
# Get covid information by region during confinement
CovidRegionCon = """select * from "CleanDataByRegion"  """

# Get covid information by region out of confinement

CovidRegionHorsCon = """select * from "CleanDataByRegion"  """


def expDataDepartment():
    df_depart = pd.read_sql_query(departements, engine)
    allDataDepartment = pd.read_sql_query(allData, engine)
    dfDepDate = pd.read_sql_query(infoDepartDate, engine)
    return df_depart, allDataDepartment, dfDepDate  # Return list of department, and covid result by department


def GetInfoPopulation():
    df_depart_pop = pd.read_sql_query(allDataDividedPopulation, engine)
    df_region_pop = pd.read_sql_query(DividedPopRegion, engine)

    return df_depart_pop, df_region_pop


def expDataRegion():
    df_regions = pd.read_sql_query(regions, engine)
    df_allDataRegion = pd.read_sql_query(allDataRegion, engine)
    return df_regions, df_allDataRegion  # Return list of regions, and covid result by region
