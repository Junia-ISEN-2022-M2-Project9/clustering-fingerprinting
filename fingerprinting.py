from hfingerprinter.analysis import hfinger_analyze
from exceptions.mainExceptions import (NoEntrySpecified)

def formatFpFile(fingerprintFile):
    with open(fingerprintFile, "r") as file:
        listOfFingerprintsInFile = [line.replace('\n', '') for line in file]
        listOfFingerprintsInFile = sorted(set(listOfFingerprintsInFile), key = listOfFingerprintsInFile.index)  # Retire les doublons ET prévserve l'ordre
        listOfFingerprintsInFile = [stringLine for stringLine in listOfFingerprintsInFile if stringLine != ""] #Supprime les lignes vides
    return listOfFingerprintsInFile


def createFingerprint(inputFiles, format, reportingMode):
    if inputFiles == None:
        raise NoEntrySpecified

    dictOfFingerprints = {}

    if format == "pcap":
        dictOfFingerprints.update({pcap : hfinger_analyze(pcap, reportingMode) for pcap in inputFiles})
        for (key, value) in dictOfFingerprints.items():
             listOfFingerprints = [fp.get("fingerprint") for fp in value]
             dictOfFingerprints[key] = sorted(set(listOfFingerprints), key = listOfFingerprints.index)
    elif format == "fingerprint":
        dictOfFingerprints.update({file : formatFpFile(file) for file in inputFiles})

    return dictOfFingerprints
