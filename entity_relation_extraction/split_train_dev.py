import json
import numpy as np
import math
#with open('/home1/wlw2020/head_motion/SpERT/spert-master/scripts/data/datasets/conll04/conll04_types.json', 'r') as f:
 #   document=json.load(f)
with open('./documents_example_v3.json', 'r') as f:
    documents = json.load(f)
entities_set = set()
relations_set = set()
for document in documents:
    temp_entities = document['entities']
    if len(temp_entities)>=1 :
        for temp_entity in temp_entities:
            entities_set.add(temp_entity['type'])
    temp_relations = document['relations']
    if len(temp_relations)>=1:
        for temp_relation in temp_relations:
            relations_set.add(temp_relation['type'])
document_entities = {}
for entity in entities_set:
    document_entities[entity] = {'short':entity, 'verbose': entity}
document_relations = {}
for relation in relations_set:
    document_relations[relation] = {'short':relation, 'verbose': relation, 'symmetric': False}
document_type = {}
document_type['entities'] = document_entities
document_type['relations'] = document_relations
with open('./msp_type_example_v3.json', 'w') as f1:
    json.dump(document_type, f1)
for i in documents:
    for j in i['entities']:
        if (len(j)) < 3:
            j['start'] = j['end'] - 1
seed = np.arange(len(documents))
np.random.shuffle(seed)
train_documents = []
train_index = seed[0:math.floor(0.8*len(seed))]
for i in train_index:
    train_documents.append(documents[i])
dev_documents = []
dev_index = seed[math.floor(0.8*len(seed)):]
for i in dev_index:
    dev_documents.append(documents[i])
with open('./msp_train_example_v3.json', 'w') as f2:
    json.dump(train_documents, f2)
with open('./msp_dev_example_v3.json', 'w') as f3:
    json.dump(dev_documents, f3)
print('bupt')