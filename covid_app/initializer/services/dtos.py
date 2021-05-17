class InformationDto:
    nom = None
    date = None
    hospitalises = None
    reanimation = None
    nouvellesHospitalisations = None
    nouvellesReanimations = None
    deces = None
    decesEhpad = None
    gueris = None
    casConfirmes = None
    sourceType = None

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

    @staticmethod
    def fromJson(jsonObject):
        nom = jsonObject["nom"] if "nom" in jsonObject else None
        date = jsonObject["date"] if "date" in jsonObject else None
        hospitalises = jsonObject["hospitalises"] if "hospitalises" in jsonObject else None
        reanimation = jsonObject["reanimation"] if "reanimation" in jsonObject else None
        nouvellesHospitalisations = jsonObject[
            "nouvellesHospitalisations"] if "nouvellesHospitalisations" in jsonObject else None
        nouvellesReanimations = jsonObject["nouvellesReanimations"] if "nouvellesReanimations" in jsonObject else None
        deces = jsonObject["deces"] if "deces" in jsonObject else None
        decesEhpad = jsonObject["decesEhpad"] if "decesEhpad" in jsonObject else None
        gueris = jsonObject["gueris"] if "gueris" in jsonObject else None
        casConfirmes = jsonObject["casConfirmes"] if "casConfirmes" in jsonObject else None
        sourceJson = jsonObject["source"] if "source" in jsonObject else None
        sourceType = jsonObject["sourceType"] if "sourceType" in jsonObject else None

        # Create source object foreach information.
        if sourceJson:
            nom_source = sourceJson["nom"] if "nom" in sourceJson else None
            url = sourceJson["url"] if "url" in sourceJson else None
            archive = sourceJson["archive"] if "archive" in sourceJson else None
            source = SourceDto()
            source.nom = nom_source
            source.url = url
            source.archive = archive

        else:
            source = None
        # Create information object foreach information.
        information = InformationDto(nom, date, hospitalises, reanimation, nouvellesHospitalisations,
                                     nouvellesReanimations, deces, decesEhpad, gueris, casConfirmes, sourceType)

        return information, source

    # @staticmethod
    """def fromJsonList(list):
        listObjectInformation = []
        ListObjectSource = []

        for e in list:
            information, source = InformationDto.fromJson(e)
            listObjectInformation.append(information)
            listObjectSource.append(source)

        return listObjectInformation"""


class SourceDto:
    nom = None
    url = None
    archive = None
