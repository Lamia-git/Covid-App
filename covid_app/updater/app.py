from service import *
from backup import update_dataBase_backup
if __name__ == "__main__":
    # Create Region Service Object.
    apiService = InformationFromApi()
    apiService.saveDataInDb()

    # Update backup dataBase
    update_dataBase_backup()

