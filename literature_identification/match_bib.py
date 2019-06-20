import django, sys, os
sys.path.append('/home/max/software/django-tmv/tmv_mcc-apsis/BasicBrowser')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BasicBrowser.settings")
django.setup()

from scoping.models import *
import bibtexparser
import json

# Load the IPCC .bib database
with open('literature_identification/IPCC/AR5 Chapter.bib') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

# Set up a query in the project
p = Project.objects.get(pk=178)
u = User.objects.get(username="galm")
q, created = Query.objects.get_or_create(
    project=p,
    creator=u,
    title="IPCC bib in database",
    database="intern"
)

print(created)


print(len(bib_database.entries))

found = 0
notfound = 0

doi_list = []
no_doi_list = []

cat = Category.objects.get(pk=319)

for e in bib_database.entries:
    d = None
    if "doi" in e:
        try:
            d = Doc.objects.get(wosarticle__di__iexact=e['doi'])
        except:
            pass
    if d is None:
        try:
            d = Doc.objects.get(title__iexact=e['title'].strip('{} '), PY=e['year'])
        except:
            pass
    if d is not None:
        d.query.add(q)
        if "included" in e:
            d.category.add(cat)
    else:
        if "doi" in e:
            doi_list.append(e)
        else:
            no_doi_list.append(e)
        print(e)
        #break
        notfound+=1

q.r_count = q.doc_set.count()
q.save()
print(notfound)
print(len(doi_list))


with open("literature_identification/dois.json","w") as f:
    json.dump(doi_list, f)

with open("literature_identification/no_dois.json","w") as f:
    json.dump(no_doi_list, f)
