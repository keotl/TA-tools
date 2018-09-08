les_cours = ['glo-2004', 'ift-2007']

mapping = {}

for cours in les_cours:
    equipes_pour_cours = []
    for i in range(1,41):
        equipes_pour_cours.append({"equipe": f"A18-{'GLO' if 'glo' in cours else 'IFT'}-Equipe{i}"})

    mapping[cours] = {"repos": equipes_pour_cours}

import json
print(json.dumps(mapping))
