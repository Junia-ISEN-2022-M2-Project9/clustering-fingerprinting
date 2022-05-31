# clustering-fingerprinting

## Option descriptions
**-h** : Display the help 

**--pcap** : add the pcap files to be analyzed.

**--fp** : add the fingerprint files to analyze after this flag

**--clusters** : number of cluster to create (this option or --threshold needs to be set)

**--mode**: type int.
    default = 2,
    choices = [0, 1, 2, 3, 4].
    "0 - similar number of collisions and fingerprints as mode 2, but using fewer features, "
    "1 - representation of all designed features, but a little more collisions than modes 0, 2, and 4, "
    "2 - optimal (the default mode), "
    "3 - the lowest number of generated fingerprints, but the highest number of collisions, "
    "4 - the highest fingerprint entropy, but slightly more fingerprints than modes 0-2",

**--threshold** : maximum distance inside a cluster

**--distance-algorithm** : select a distance type between ( _sequencematcher_(default), _levenstein_, _jaro_)
    
**--stats** : print the output in the terminal with full verbosity

**--json** : output to json to be reused

## Global descriptions
Several steps are required in order to anaylze a pcap file containing HTTP requests.


**Create clusters from several pcap files**

In order to compare pcap files you need you need to use the --pcap flag.**The program will automatically extract the HTTP fingerprints from the pcap and remove the duplicated ones when the fingerprint file is given to the clustering program.**


The goal is to create clusters from those files, you can add directly files containing the fingerprints with the --files flag. Then the --stats flag to get the printed results with many details. Finaly you need to set the -t (threshold) or -c (cluster),the cluster option indicates how many cluster you want, the threshold option indicates the size of the clusters to create. **Careful, on and exactly one of the options -t and -c must be specified in order to work.** 


**Determine if a pcap contains malicious requests.**

There are several ways to determine if a pcap is malicious or not. First you can use the method described above, create clusters based on a threshold and see if some requests of the analyzed pcap are in the same cluster than known malicious requests. (First usage exemple) 

The other way is to do it graphicaly using the graphical module. 


## Usage example
The following line is running the program asking for a stat output (all the clusters with the file from the fingerprints and their numbers), the files to analyze are given after the _--files_ flag, so it is fingerprints files, with the following format:

![Pyplot graph](fingerprintFileFormat.png)

The clusters are set to have a maximum distance of 3. 
> python3 main.py --fp pcap/xss pcap/sqlmap pcap/maliciousUser pcap/burp_bruteforce pcap/legitime -t 3 --stats

![Pyplot graph](result_exemple.png)


The following line asks for a json output. The Json file can then be used as a reference of malicious request in order to be compared to unknown pcap files. 
> python3 main.py --fp pcap/xss pcap/xxe pcap/ffuf pcap/sqlmap pcap/nmapScriptMethods pcap/burp_bruteforce -j superJson.json -t 3

## How does it works ? 

We modified the hfinger library to create fingerprint from HTTP requests and convert PCAP files to text files containing fingerprints. 

The difflib and jellyfish libraries are used to calculate distances between two fingerprints. 

The AgglomerativeClustering function from the sklearn.cluster library is used to create the clusters. 

## Development

- clustering
    - [x] Manage pcap and fingerprint files
    - [x] Create clusters from fingerprint files and print an output with statistic details of the clusters
    - [x] Change the distance type using a flag
    - [ ] Real time clustering 
- output
    - [x] Propose a Json output to avoid the recalculation of the clusters
