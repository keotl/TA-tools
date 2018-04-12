import json;

with open('projects.json') as fd:
    projects = json.loads(fd.read());

for project in projects:
    print(project['ssh_url_to_repo']);
