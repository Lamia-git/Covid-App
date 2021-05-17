# Alimentation des tables Region et Departement.
import pandas as pd
from models.utils import *
from models.models import *
import json
from services.dtos import *
import os

class RegionService:
    racine_path = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(racine_path, "data", "regions-france.csv")
    path_population = os.path.join(racine_path, "data", "populationRegion.xlsx")
    # Create Region
    def create_regions(self):
        region = pd.read_csv(self.path, delimiter=",")
        region = region.rename(columns={"nom_region": "name",
                                        "code_region": "code"
                                        })
        lists = region.to_dict(orient='records')
        create(lists, "region")

    def add_region_population(self):
        population = pd.read_excel(self.path_population)
        # Add population column
        add_population_column_Region("region")
        # Insert population
        list = population.to_dict(orient='records')
        for e in list:

            insert_region_population("region",e)
            pass


class DepartementService:
    racine_path = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(racine_path, "data", "departments-region.csv")
    path_population = os.path.join(racine_path, "data", "population.xlsx")

    # Create Departement
    def create_departments(self):
        department = pd.read_csv(self.path, delimiter=",")
        department = department.rename(columns={"num_dep": "code",
                                                "dep_name": "name",
                                                "region_name": "region"
                                                })
        lists = department.to_dict(orient='records')
        print(lists)
        create(lists, "departement")

    def add_depart_population(self):
        population = pd.read_excel(self.path_population)
        # Add population column
        add_population_column("departement")
        # Insert population
        list = population.to_dict(orient='records')
        for e in list:

            insert_population("departement",e)


class InformationService:
    # Store oldest information data,
    racine_path = os.path.dirname(os.path.dirname(__file__))
    file = os.path.join(racine_path, "data", "chiffres-cles.json")

    def getData(self):
        with open(self.file, encoding='utf-8') as json_data:
            data_dict = json.load(json_data)
            data = []
            # print(data_dict)
        """ To optimize my database I eliminate data by region and country, because it is calculable """
        for d in data_dict:
            if (d["code"].startswith('DEP')):
                data.append(d)
        return data

    def _ToSource(self, sourceDto):
        return(Source(nom=sourceDto.nom,
                      archive=sourceDto.archive,
                      url=sourceDto.url))

    def _ToInformation(self, informatioDto):
        return Information(
            nom=informatioDto.nom,
            date=informatioDto.date,
            hospitalises=informatioDto.hospitalises,
            reanimation=informatioDto.reanimation,
            nouvellesHospitalisations=informatioDto.nouvellesHospitalisations,
            nouvellesReanimations=informatioDto.nouvellesReanimations,
            deces=informatioDto.deces,
            decesEhpad=informatioDto.decesEhpad,
            gueris=informatioDto.gueris,
            casConfirmes=informatioDto.casConfirmes,
            sourceType=informatioDto.sourceType,
        )

    def createInformation(self, allData):

        for data in allData:
            informationDto, sourceDto = InformationDto.fromJson(data)
            infoEntity = self._ToInformation(informationDto)

            try:
                result = None
                if sourceDto:
                    source = self._ToSource(sourceDto)
                    result = db_session.query(Source).filter(Source.nom == source.nom,
                                                         Source.url == source.url).first()
                    if bool(result) == False:
                        db_session.add(source)
                        db_session.flush()
                        result = source

                infoEntity.source = result
                db_session.add(infoEntity)
                db_session.flush()
                db_session.commit()
            except:
                print("error during insert")

                db_session.close()


