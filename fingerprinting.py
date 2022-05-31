from hfingerprinter.analysis import hfinger_analyze
from exceptions.mainExceptions import (NoEntrySpecified)

def formatFpFile(fingerprintFile):
    with open(fingerprintFile, "r") as file:
        listOfFingerprintsInFile = [line.replace('\n', '') for line in file]
        listOfFingerprintsInFile = sorted(set(listOfFingerprintsInFile), key = listOfFingerprintsInFile.index)  # Retire les doublons ET prévserve l'ordre
        listOfFingerprintsInFile = [stringLine for stringLine in listOfFingerprintsInFile if stringLine != ""] #Supprime les lignes vides
    return listOfFingerprintsInFile


def createFingerprint(pcapFiles, fpFiles, reportingMode):
    dictOfFingerprints = {}

    if pcapFiles != None:
        dictOfFingerprints.update({pcap : hfinger_analyze(pcap, reportingMode) for pcap in pcapFiles})
        for (key, value) in dictOfFingerprints.items():
             listOfFingerprints = [fp.get("fingerprint") for fp in value]
             dictOfFingerprints[key] = sorted(set(listOfFingerprints), key = listOfFingerprints.index)
    if fpFiles != None:
        dictOfFingerprints.update({file : formatFpFile(file) for file in fpFiles})
    if pcapFiles == None and fpFiles == None:
        raise NoEntrySpecified

    return dictOfFingerprints
