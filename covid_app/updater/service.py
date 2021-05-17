import requests
from datetime import date, timedelta
from services.service import InformationService


class InformationFromApi:
    today = date.today()
    yesterday = today - timedelta(days = 1)
    urlbydate = f"https://coronavirusapi-france.now.sh/AllDataByDate?date=2021-05-07"
    url = "https://coronavirusapi-france.now.sh/AllLiveData"

    def getLiveInformation(self):
        # Get today information's covid from APi
        response = requests.request("GET", self.url)
        return response.json()["allLiveFranceData"]

    def getInformationByDate(self):
        # Get today information's covid from APi
        response = requests.request("GET", self.urlbydate)
        return response.json()["allFranceDataByDate"]

    def checkDate(self):
        # Check that the data retrieved by API is that of today.
        data = self.getLiveInformation()
        date_ = data[0]["date"]
        today = str(self.today)
        return date_ == today


    def saveDataInDb(self):
        #if self.checkDate():
        """ Save today's data
        insert information
        if new source, insert source """
        # Information By date
        #data = self.getInformationByDate()

        # Live data
        data = self.getLiveInformation()
        informationService = InformationService()
        informationService.createInformation(data)
        print(data)

    def automatisation(self):
        pass

