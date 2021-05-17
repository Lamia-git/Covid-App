from initializer.services.service import *


if __name__ == "__main__":

    # Create Region Service Object.
    serviceRegion = RegionService()
    serviceRegion.create_regions()
    serviceRegion.add_region_population()


    # Create departement Service Object.
    serviceDepartement = DepartementService()
    serviceDepartement.create_departments()
    serviceDepartement.add_depart_population()

    # Create information Service Object
    serviceInformation = InformationService()
    data = serviceInformation.getData()
    serviceInformation.createInformation(data)

