import pandas as pd
import ontobio as ob
from ontobio import OntologyFactory
import networkx as nx


ofa = OntologyFactory()
ont = ofa.create('hp')


## The OWL version of HPO (used here) has many interesting relationship types;
## for now we just care about is-a (subClassOf between named classes)
ont = ont.subontology(relations='subClassOf')
G = ont.get_graph()

## Get all descendents of some term

[myterm] = ont.search('Abnormality of the nervous system')
print("Got my term {}".format(myterm))

desc = nx.descendants(G, myterm)

items = []
for n in desc:
    items.append({'id':n, 'label': ont.label(n)})

## Output using pandas
df = pd.DataFrame(items)
print(df.head())

outfilename = "descendenat.tsv"
df.to_csv(outfilename, sep="\t")


