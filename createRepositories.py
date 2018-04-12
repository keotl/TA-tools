#!/usr/bin/python3
import requests;
import subprocess;
import json;

PRIVATE_TOKEN = "foobar";

def createRepository(name: str):
    url = "https://gitlab.com/api/v4/projects"
    querystring = {"name" : name, "merge_requests_enabled": True,
                   "wiki_enabled": True, "resolve_outdated_diff_discussions": True,
                   "visibility": "private"}
    headers = {
        'private-token': PRIVATE_TOKEN
    }
    response = requests.request("POST", url, headers=headers, params=querystring)
    return response.json()['ssh_url_to_repo'];

def clone(repoUrl, destinationDir, logFilePath):
    logFile = open(logFilePath, "w");
    try:
        subprocess.run(["git","clone",repoUrl,destinationDir], stdout=logFile, stderr=logFile);
        subprocess.run(["git", "-C", destinationDir, "checkout", BRANCH], stdout=logFile, stderr=logFile);
        writeBranch(destinationDir);
    except:
        pass
    print("Done cloning {}".format(repoUrl));

def initializeEmptyReadme(repoSshUrl: str):
    subprocess.run(["mkdir", "tmp"]);
    clone(repoSshUrl, "tmp", "log.txt");
    subprocess.run(["echo", """# Readme
    vide"""], stdout=open("tmp/README.md", 'w'));
    subprocess.run(["git", "-C", "tmp", "add", "-A"]);
    subprocess.run(["git", "-C", "tmp", "commit", "-m", 'Initial commit']);
    subprocess.run(["git", "-C", "tmp", "push", "-u", "origin", "master"]);
    subprocess.run(["rm", "-rf", "tmp"]);
    
    
if __name__ == "__main__":
    with open('mapping.json') as fd:
        mapping = json.loads(fd.read());
    for cours, repos in mapping.items():
        for repo in repos['repos']:
            print(repo['equipe']);
            url = createRepository(repo['equipe']);
            initializeEmptyReadme(url);
            repo['url'] = url;
    with open('mapping.json', 'w') as fd:
        json.dump(mapping,fd);
