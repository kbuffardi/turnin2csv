#! /usr/bin/python
# python 2.7

import sys
import re
import os

###############################################################################
# PSEUDO-CONSTANTS

# penalty (value subtracted) for each day late. Change to calculate grade
# according to your late policy or change to 0 to disregard from calculation 
def LATE_PENALTY_PER_DAY():
  return 20

# should the script be quiet (no standard output, only file out)
def QUIET():
  return False
###############################################################################
# FUNCTIONS
def stdout(message):
  if not QUIET():
    print message

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
  #parameters without a tag return empty string
  if tag:
    tag = tag.group()
  else:
    return ""
  # #remove first and last character and whitespace
  if tag.startswith("<") and tag.endswith(">"):
    tag = tag[1:-1].strip() 
    return tag.split()[0]
  else:
    return ""

def newCSVFile(name):
  pwd = os.getcwd()
  file = pwd+"/"+name
  suffix = ""
  while os.path.isfile(file+str(suffix)+".csv"):
    if suffix == "":
      suffix = -1
    else:
      suffix = int(suffix)-1
  file = file + str(suffix) + ".csv"
  stdout("Creating file " + file)
  return open(file, "a") #opened file for appending

###############################################################################
# Get file name and open it
if len(sys.argv) != 2:
  stdout("Usage:\n python turnin2csv.py <filename.html>")
  sys.exit()

htmlfile = sys.argv[1]
stdout("Processing "+ htmlfile + "...")

with open(htmlfile, 'r') as infile:
  html = infile.read()
  infile.close()
  table = getElementsByType("table",html)
  
  if len(table) == 1:
    rows = getElementsByType("tr",table[0])
    
    if len(rows) > 1:
      stdout(str(len(rows)) + " students found")
      column_name = os.path.splitext(htmlfile)[0]
      csv = newCSVFile(column_name)
      #write row for column headers
      csv.write("Username,"+column_name+"\n")
      for i in range(1,len(rows)):
        student = getElement(rows[i])
        cells = getElementsByType("td",getInnerHTML(student))

        #columns: name, username, t(1), ...t(n), late, chars, lines
        tests = len(cells) - 5
        
        if tests >= 1:
          name = getInnerHTML(cells[0])
          if elementType(name) == "a": #get name from within link
            name = getInnerHTML(name) 
          username = getInnerHTML(cells[1])
          late = getInnerHTML(cells[tests+2])
          if late == '-':
            late = 0
          results = cells[2:(tests+2)]
          passed = 0
          for result in results:
            outcome = getInnerHTML(result)
            if outcome == "1":
              passed += 1
          stdout(name + " passed " + str(passed) + " of " + str(tests))
          grade_str = str(float(passed)/tests*100-(LATE_PENALTY_PER_DAY()*int(late)))
          csv.write(username + "," + grade_str + "\n")
        else:
          stdout("No test results available for student. Quitting.")
          sys.exit()
      csv.close()
      stdout("Done reading results. Saved to CSV." )
    else:
      stdout("No student results found. Quitting.")
      sys.exit() 
  else:
    stdout("No results table found in html")