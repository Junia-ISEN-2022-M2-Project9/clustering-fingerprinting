class NoEntrySpecified(Exception):
    def __str__(self):
        return "You have to specify at least a pcap file or a fingerprints file"
