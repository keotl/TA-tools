import json
import random

FILL_SEQUENTIALLY = True
SHUFFLE_SUBMITTED_FORMS = True

plages = {
    "Samedi 15 septembre": 20,
    "Lundi 17 septembre (soir)": 20,
    "Mardi 18 septembre (soir)": 10,
    "Mercredi 19 septembre (soir)": 10,
    "Samedi 22 septembre": 10
}

all_teams = [str(x) for x in range(1, 41)]
random.shuffle(all_teams)

submitted_forms = []
with open("form.csv", 'r') as f:
    lines = f.readlines()
    header = lines[0]
    for line in lines[1::]:
        row = dict(zip(header.replace('"', '').replace("\n", '').split(","),
                       line.replace('"', '').replace("\n", '').split(",")))
        submitted_forms.append(row)

if SHUFFLE_SUBMITTED_FORMS:
    random.shuffle(submitted_forms)

equipes_placees = {key: [] for key in plages.keys()}

jubilant_teams = []
happy_teams = []
unhappy_teams = []
indifferent_teams = []


def schedule_anywhere(team_number):
    order_of_iteration = [x for x in plages.keys()]
    if not FILL_SEQUENTIALLY:
        random.shuffle(order_of_iteration)
    for potential_choice in order_of_iteration:
        if len(equipes_placees[potential_choice]) < plages[potential_choice]:
            equipes_placees[potential_choice].append(team_number)
            break


for row in submitted_forms:
    team_number = row["Numéro d'équipe"]
    if len(equipes_placees[row['Préférence 1']]) < plages[row['Préférence 1']]:
        equipes_placees[row['Préférence 1']].append(team_number)
        jubilant_teams.append(team_number)
    elif len(equipes_placees[row['Préférence 2']]) < plages[row['Préférence 2']]:
        equipes_placees[row['Préférence 2']].append(team_number)
        happy_teams.append(team_number)
    else:
        schedule_anywhere(team_number)
        unhappy_teams.append(team_number)

for team_number in all_teams:
    if team_number not in jubilant_teams + happy_teams + unhappy_teams:
        schedule_anywhere(team_number)
        indifferent_teams.append(team_number)

print(json.dumps(equipes_placees))
print(f"Jubilant teams: {len(jubilant_teams)}")
print(f"Happy teams: {len(happy_teams)}")
print(f"Unhappy teams: {len(unhappy_teams)}")
print(f"Indifferent teams: {len(indifferent_teams)}")
