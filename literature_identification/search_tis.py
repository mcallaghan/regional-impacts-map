import django, sys, os
sys.path.append('/home/max/software/django-tmv/tmv_mcc-apsis/BasicBrowser')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BasicBrowser.settings")
django.setup()

from scoping.models import *
import bibtexparser
import json
import re

with open("literature_identification/no_dois.json","r") as infile:
    entries = json.load(infile)

qs = []
p = Project.objects.get(pk=178)
u = User.objects.get(username="galm")

for e in entries:
    if len(qs) == 25:
        text = " OR ".join([x for x in qs if '""' not in x])
        print(text)
        q, created = Query.objects.get_or_create(
                project = p,
                text = text,
                title = text,
                database = "WoS",
                creator = u,
                credentials = True
        )
        q.save()
        qs = []
    if "author" in e and "title" in e and "year" in e:
        a = e['author'].strip('{} ').replace('\\','').replace('{','').replace('\'','').replace('}','')
        a1 = re.split('\W', a)[0]
        ti = e['title'].strip('{} ').replace('\\','').replace('{','').replace('}','').replace('\'','').replace('"','')
        py = e['year']
        qs.append(f'(TI="{ti}" AND AU={a1} AND PY={py})')


if len(qs) > 0:
    text = " OR ".join([x for x in qs if '""' not in x])
    print(text)
    q, created = Query.objects.get_or_create(
            project = p,
            text = text,
            title = text,
            database = "WoS",
            creator = u,
            credentials = True
    )
    q.save()
