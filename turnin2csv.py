#! /usr/bin/python
# python 2.7

import sys
import re

###############################################################################
# FUNCTIONS


def getElementsByType(tag,source):
  #non-greedy search for all tags of that type
  regex = "<" + tag + ">" + ".*?" + "</" + tag + ">"
  return re.findall(regex,source,re.S)

def getInnerHTML(element):
  tag = elementType(element)
  return element.lstrip("<"+tag+".*?>").rstrip(tag+">").rstrip("</")

def elementType(tag):
  ex = "<.*?>" #minimal (non-greedy) tag
  tag = re.search(ex,tag).group()
  if tag.startswith("<") and tag.endswith(">"):
    return tag[1:-1].strip() #remove first and last character and whitespace
  else:
    return ""

###############################################################################
# Get file name and open it
if len(sys.argv) != 2:
  print "Usage:\n python turnin2csv.py <filename.html>"
  sys.exit()

htmlfile = sys.argv[1]
print "Processing ", htmlfile, "..."

with open(htmlfile, 'r') as infile:
  html = infile.read()
  infile.close()
  table = getElementsByType("table",html)
  print len(table), " tables"
  if table:
    rows = getElementsByType("tr",table[0])
    print len(rows), " rows"
  else:
    print "No results table found in html"

  print 
  



