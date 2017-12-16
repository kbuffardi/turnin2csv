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

def getElement(source):
  #non-greedy search for the NEXT element
  tag = elementType(source)
  regex = "<" + tag + ">" + ".*?" + "</" + tag + ">"
  return re.search(regex,source,re.S).group()

def getInnerHTML(element):
  tag = elementType(element)
  start = "<"+tag+".*?>"
  end = re.compile("</"+tag+">")
  return re.sub("<"+tag+"(.*?)>","",element).rstrip(tag+">").rstrip("</")

def elementType(tag):
  ex = "<.*?>" #minimal (non-greedy) tag
  tag = re.search(ex,tag)
  if tag:
    tag = tag.group()
  else:
    return ""
  if tag.startswith("<") and tag.endswith(">"):
    tag = tag[1:-1].strip() #remove first and last character and whitespace
    return tag.split()[0]
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
  
  if len(table) == 1:
    rows = getElementsByType("tr",table[0])
    
    if len(rows) > 1:
      print len(rows)-1, " students found"
      for i in range(1,len(rows)-1):
        student = getElement(rows[i])
        cells = getElementsByType("td",getInnerHTML(student))

        #columns: name, username, t(1), ...t(n), late, chars, lines
        tests = len(cells) - 5
        if tests < 1:
          print "No test results available for student. Quitting."
          sys.exit()
        else:
          name = getInnerHTML(cells[0])
          if elementType(name) == "a": #get name from within link
            name = getInnerHTML(name) 
          username = cells[1]
          late = cells[tests+2]
          results = cells[2:(tests+2)]
          passed = 0
          for result in results:
            outcome = getInnerHTML(result)
            if outcome == "1":
              passed += 1
          print name, "passed", passed, "of", tests
      
  else:
    print "No results table found in html"

  
  



