import pandas as pd
import argparse
import os
from collections import defaultdict
from hpotk.ontology import Ontology
from hpotk.ontology.load.obographs import load_ontology


class TermInfo:
    def __init__(self, ID, label, synonyms, parent_ids, parents, definition, comment) -> None:
        self._hpo_id = ID
        self._label = label
        self._synonyms = TermInfo.or_else_dash(synonyms)
        self._parents = TermInfo.or_else_dash(parents)
        self._parent_id_set = set(parent_ids)
        self._definition = TermInfo.or_else_dash(definition)
        self._comment = TermInfo.or_else_dash(comment)

    @staticmethod
    def or_else_dash(contents):
        if contents is None or len(contents) == 0:
            return "-"
        else:
            return contents

    def descends_from(self, id):
        return id in self._parent_id_set

    @property
    def hpo_id(self):
        return self._hpo_id

    @property
    def label(self):
        return self._label

    @property
    def synonyms(self):
        return self._synonyms

    @property
    def parents(self):
        return self._parents

    @property
    def definition(self):
        return self._definition

    @property
    def comment(self):
        return self._comment




parser = argparse.ArgumentParser()
parser.add_argument("--hpo", required=True, type=str)
parser.add_argument("--term", required=True, type=str)
parser.add_argument("--out", default="hpo_terms")
args = parser.parse_args()

hpo_path = args.hpo
if not os.path.isfile(hpo_path):
    print(f"[ERROR] could not find HPO file at {hpo_path}")
    exit(1)
hpo_term = args.term
out_prefix = args.out
out_filename = f"{out_prefix}.tsv"

print(f"[INFO] Will extract data for descendents of {hpo_term}")

hpo: Ontology = load_ontology(hpo_path)
if not hpo_term in hpo:
    print(f"[ERROR] Could not find {hpo_term} in ontology")
    exit(1)

terms =[hpo.get_term(t) for t in hpo.graph.get_descendants(hpo_term, include_source=True)]

term_i_list = list()

for t in terms:
    id = t.identifier
    label = t.name
    synonyms = ", ".join(list(s.name for s in t.synonyms)) if t.synonyms is not None else ""
    parent_ids = list(hpo.get_term(p).identifier for p in hpo.graph.get_parents(t))
    parents = ", ".join(list(hpo.get_term(p).name for p in hpo.graph.get_parents(t)))
    definition = t.definition
    comment = t.comment
    term_i_list.append(TermInfo(label=label, ID=id, synonyms=synonyms, parent_ids=parent_ids, parents=parents, definition=definition, comment=comment))

print(f"[INFO] extracted {len(term_i_list)} terms.")

## Get immediate descendants of target term
target_children = set()
child_d = defaultdict(list)
for t in term_i_list:
    if hpo.graph.is_child_of(t.hpo_id, hpo_term):
        target_children.add(t.hpo_id)
for t in term_i_list:
    t_id = t.hpo_id
    for s in target_children:
        if t_id == s:
            child_d[t_id].append(t) ## first entry in list
for t in term_i_list:
    for s in target_children:
        if hpo.graph.is_descendant_of(t.hpo_id, s):
            child_d[s].append(t)

d_list = list()
for hpo_lists in child_d.values():
    for t in hpo_lists:
        d = {"hpo_id":t._hpo_id, "hpo_label":t._label,
                "synonyms":t._synonyms,
                "parents":t._parents,
                "definition": t._definition,
                "comment":t._comment }
        d_list.append(d)
df = pd.DataFrame(d_list)
df.to_csv(out_filename, sep="\t", index=False)