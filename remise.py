#!/usr/bin/python3

import json;
import subprocess;
# import dummy_threading as threading;
import threading;
import argparse;

parser = argparse.ArgumentParser(description="git repo fetcher");
parser.add_argument("--destination", help='base dir destination');
parser.add_argument("--branch", help="branch to be checked out");

args = parser.parse_args();

BASE_DIR = "build";
BRANCH = "remise_4";
if args.destination is not None:
    BASE_DIR = args.destination;
if args.branch is not None:
    BRANCH = args.branch;

LOG_DIR = "log";

with open('mapping.json') as fd:
    mapping = json.loads(fd.read());

def writeBranch(destinationDir):
    logFile = open(destinationDir + "/BRANCH.txt", 'w');
    subprocess.run(["git", "-C", destinationDir, "rev-parse", "--abbrev-ref", "HEAD"], stdout=logFile, stderr=logFile);

def clone(repoUrl, destinationDir, logFilePath):
    logFile = open(logFilePath, "w");
    try:
        subprocess.run(["git","clone",repoUrl,destinationDir], stdout=logFile, stderr=logFile);
        subprocess.run(["git", "-C", destinationDir, "checkout", "--track", "origin/{}".format(BRANCH)], stdout=logFile, stderr=logFile);
        writeBranch(destinationDir);
    except:
        pass
    print("Done cloning {}".format(repoUrl));

threads = [];
    
for cours, repos in mapping.items():
    subprocess.run(["mkdir", "-p", BASE_DIR + "/" + LOG_DIR + "/" + cours]);
    for repo in repos['repos']:
        cloneDir = BASE_DIR + "/" + cours + "/" + repo['equipe'];
        logFilePath = BASE_DIR + "/" + LOG_DIR + "/" + cours + "/" + repo['equipe'] + ".txt";
        thread = threading.Thread(target=clone, args=(repo['url'], cloneDir, logFilePath));
        threads.append(thread);

        
for thread in threads:
    thread.start();

for thread in threads:
    thread.join();
