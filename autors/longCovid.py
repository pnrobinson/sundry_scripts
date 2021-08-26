import csv
from collections import defaultdict

fname = 'autors/data/LongCovidAuthor.tsv'


class Author:
    def __init__(self, row:list):
        order = row['Order']
        if order == 'A':
            self._alphabetical = True
            self._order = -1
        else:
            self._alphabetical = False
            self._order = int(order)
        self._completeName = row['CompleteName']
        self._surname = row['Surname']
        self._firstName = row['First name']
        self._middleInitial = row['Middle Initial']
        self._email = row['Email']
        self._institution1 = row['Institution 1']
        self._institution2 = row['Institution 2']
        self._institution3 = row['Institution 3']

    def is_alphabetical(self):
        return self._alphabetical

    @property
    def name(self):
        return self._completeName

    def get_non_empty_institutions(self):
        if self._institution1 is None:
            raise ValueError("Bad inst 1")
        inslist = []
        inslist.append(self._institution1)
        if len(self._institution2) > 5:
            inslist.append(self._institution2)
        if len(self._institution3) > 5:
            inslist.append(self._institution3)
        return inslist


class Institution:
    def __init__(self, name:str, order:int):
        self._name = name
        self._order = order

    @property
    def name(self):
        return self._name

    @property
    def order(self):
        return self._order


alphabetical_authors = []
ordered_authors = []



with open(fname) as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        author = Author(row=row)
        if author.is_alphabetical():
            alphabetical_authors.append(author)
        else:
            ordered_authors.append(author)

n_alph = len(alphabetical_authors)
n_ord = len(ordered_authors)
print("Got {} ordered and {} alphabetical authors (total {})".format(n_alph, n_ord, n_alph + n_ord))

ordered_authors.sort(key=lambda x:x._order)
alphabetical_authors.sort(key=lambda x:x._surname)

# first five ordered authors in front, rest in back
authors = ordered_authors[0:5]
authors.extend(alphabetical_authors)
authors.extend(ordered_authors[5:])

# collect the institutions in the order they are used.

seen_institutions = set()
institution_list = []
order = 0
for a in authors:
    i1 = a._institution1
    i2 = a._institution2
    i3 = a._institution3
    if i1 is None or len(i1) < 5:
        raise ValueError("Bad i1 {}".format(i1))
    elif i1 not in seen_institutions:
        seen_institutions.add(i1)
        order += 1
        institution = Institution(name=i1, order=order)
        institution_list.append(institution)
    if len(i2) > 5 and i2 not in seen_institutions:
        seen_institutions.add(i2)
        order += 1
        institution = Institution(name=i2, order=order)
        institution_list.append(institution)
    if len(i3) > 5 and i3 not in seen_institutions:
        seen_institutions.add(i3)
        order += 1
        institution = Institution(name=i3, order=order)
        institution_list.append(institution)

institution_to_order = defaultdict(int)
inst_lst = []
for i in institution_list:
    institution_to_order[i.name] = i.order
    s = "{}. {}".format(i.order, i.name)
    inst_lst.append(s)

authorlist = []

for a in authors:
    institution_list = a.get_non_empty_institutions()
    name = a.name
    nmbrs = []
    for i in institution_list:
        n = institution_to_order.get(i)
        nmbrs.append(n)
        nmbrs.sort()
        string_ints = [str(int) for int in nmbrs] 
    atr = "{},{}".format(name, ",".join(string_ints))
    authorlist.append(atr)

al = " ".join(authorlist)
print(al)
print()

   
print(" ".join(inst_lst))




            


