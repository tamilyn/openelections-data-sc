
from patch import *
import csv
import re

def buildLine(county,r):
  district = ""
  precinct = r.jurisdiction

  total_votes = 0
  party = "unknown party"
  candidate = "unknown candidate"
  office = r.contest.text
  office = office.replace('  ', ' ')
  parts = office.split(",")

  if len(parts) == 2:
    house = office.find( "House")
    senate = office.find( "Senate")
    if house >= 0 or senate >= 0:
      office = parts[0].strip()
      district = parts[1].strip()
   
  if r.jurisdiction is not None:
    precinct = r.jurisdiction.name

  if r.choice is not None:
    total_votes = r.choice.total_votes
    votes = r.votes
    party = r.choice.party
    candidate = r.choice.text
    candidate = candidate.replace('  ', ' ')

  if precinct is None:
    return None
  else:
    return([county, precinct, office, district, party, candidate, votes])

def output_file(outfile,items):
  with open(outfile, "wb") as csv_outfile:
    outfile = csv.writer(csv_outfile)
    outfile.writerow(['county', 'precinct', 'office', 'district', 'party', 'candidate', 'votes'])
    outfile.writerows(items)


def go(filename):

  items = []
  p = MyParser()
  p.parse(filename)
  print "Processing ", filename, p.election_name, p.region
  county = p.region 

  for r in p.results:
     if r.votes > 0:
       if r.choice is not None:
         item = buildLine(county, r)
         if item is not None:
           items.append( item )

  return(items)

def processCounties(counties,outfile):
  allitems = []
  for c in counties:
    print "Processing county: ", c

    infile = c + ".xml"
    items = go(infile)
    allitems = allitems + items
    print "Num items in ", c, " = ", len(items)


  print "processed ", len(counties), " counties"
  print "total items ", len(allitems)
  output_file(outfile, allitems)



counties = [ "abbeville", "aiken", "allendale", "anderson",
  "bamberg", "barnwell", "beaufort", "berkeley", "calhoun",
  "charleston", "cherokee", "chester", "chesterfield",
  "clarendon", "colleton", "darlington", "dillon",
  "dorchester", "edgefield", "fairfield", "florence",
  "georgetown", "greenville", "greenwood", "hampton",
  "horry", "jasper", "kershaw", "lancaster",
  "laurens", "lee", "lexington", "marion", "marlboro",
  "mccormick", "newberry", "oconee", "orangeburg",
  "pickens", "richland", "saluda", "spartanburg",
  "sumter", "union", "williamsburg", "york"
 ]

outfile = '20161108__sc__general__precinct.csv'
processCounties(counties, outfile)

#counties = ["abbeville"]
#processCounties(counties, "gen_abbeville.csv")




