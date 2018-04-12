#!/usr/bin/python3

import subprocess;
import datetime;
import time;
import threading;
import argparse;

parser = argparse.ArgumentParser(description="sleep 3600 pour remise");
parser.add_argument("--destination", help='base dir destination');
parser.add_argument("--branch", help="branch to be checked out");

args = parser.parse_args();

BASE_DIR = "build";
BRANCH = "remise_1";
if args.destination is not None:
    BASE_DIR = args.destination;
if args.branch is not None:
    BRANCH = args.branch;

def preleve():
    subprocess.run(["python3", "remise.py", "--destination", BASE_DIR + "/" + timestamp, "--branch", BRANCH]);

for i in range (0,48):
    timestamp = datetime.datetime.now().strftime("%y-%m-%d_%H.%M");
    print(timestamp);
    threading.Thread(target=preleve).start();
    time.sleep(3600);
