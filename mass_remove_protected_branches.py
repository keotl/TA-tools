import json

with open('mapping.json', 'r') as f:
    mapping = json.loads("".join(f.readlines()))

def delete_protected_branch(repo_name: str):
    import requests

    url = f"https://gitlab.com/api/v4/projects/glo2004-ift2007%2F{repo_name}/protected_branches/master"

    headers = {
        'private-token': "teAZauX_VTg7NyPoQFsu",
    }

    response = requests.request("DELETE", url, headers=headers)

    print(response.text)


for cours, liste_equipes in mapping.items():
    for equipe in liste_equipes['repos']:
        delete_protected_branch(equipe['equipe'])

