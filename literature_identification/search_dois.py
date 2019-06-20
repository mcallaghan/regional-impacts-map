import django, sys, os
sys.path.append('/home/max/software/django-tmv/tmv_mcc-apsis/BasicBrowser')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BasicBrowser.settings")
django.setup()

from scoping.models import *
import bibtexparser
import json

with open("literature_identification/dois.json","r") as infile:
    bib = json.load(infile)

dois = [f'"{x["doi"].replace("Doi: ","")}"' for x in bib]

doi_wq = f'DO=({" OR ".join(dois)})'
doi_sq = f'DOI({" OR ".join(dois)})'

print(doi_wq)
print(doi_sq)

print(len(dois))
