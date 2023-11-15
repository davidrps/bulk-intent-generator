import csv, json
from copy import deepcopy
import codecs

# Open the template JSON files for intents and user responses 
with open(r'templates/template.json') as f:
    template_question=json.loads(f.read())
with open(r'templates/template_usersays.json') as f:
    template_userSays=json.loads(f.read())

# Set the language of the Agent
language = 'es'

# Set the filename with the intents data
filename = 'intents.csv'

def to_utf(filename):
    #read input file
    with codecs.open(filename, 'r', encoding = 'mbcs') as file:
        lines = file.read()

    #write output file
    with codecs.open(filename, 'w', encoding = 'utf8') as file:
        file.write(lines)

# Open the CSV file with the intents information
with open(filename, encoding='utf-8') as intents:
    csv_reader = csv.reader(intents, delimiter=',')
    row_count = 0
    for row in csv_reader:
        if row_count!=0:
            # Extract intent information from row
            intentName = row[0]
            trainingPhrases = row[1].split('|')
            responses = row[2].split('|')
            action = row[3].split('|')
            contexts = row[4].split('|')
            affectedContexts = row[5].split('|')
            lifespan = row[6].split('|')
            affectedContextsList = []
            # Copy structure json from template
            q_copy=deepcopy(template_question)
            u_copy=deepcopy(template_userSays)
            i = 0
            # Set json values
            while i < len(affectedContexts):
                affectedContextsList.append({"name": affectedContexts[i],"lifespan": lifespan[i]})
                i+=1
            q_copy['responses'][0]['affectedContexts'] = affectedContextsList
            q_copy['name'] = intentName
            q_copy['contexts'] = contexts
            q_copy['responses'][0]['action'] = action
            q_copy['responses'][0]['messages'][0]['speech'] = responses
            q_copy['responses'][0]['messages'][0]['lang'] = language
            i = 0
            while i < len(trainingPhrases):
                if i!=0:
                    training = deepcopy(u_copy[0])
                    u_copy.append(training)
                u_copy[i]['data'][0]['text'] = trainingPhrases[i]
                u_copy[i]['lang'] = language
                i+=1

            # Save json file
            with open(f'intents/{intentName}.json','w') as f:
                f.write(json.dumps(q_copy, ensure_ascii=False))
            with open(f'intents/{intentName}_usersays_'+language+'.json','w') as f:
                f.write(json.dumps(u_copy, ensure_ascii=False))
            
            # Set UTF8 encode to json file
            to_utf('intents/'+intentName+'.json')
            to_utf('intents/'+intentName+'_usersays_'+language+'.json')

        row_count+=1
