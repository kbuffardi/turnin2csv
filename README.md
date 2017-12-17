# turnin2csv

This script parses an html results page from the instructor's view of a [Turnin](https://turnin.ecst.csuchico.edu) assignment and creates a comma separated value (.csv) file with students' calculated grades.

Using **python 2.7**

## Getting Started

1. Log into Turnin as an instructor and 
2. Click on the name of an assignment to see a summary of all the students' results
3. In your web browser, choose to "Save as..." and save that page as "HTML only"
4. Name the file what you want the assignment to be called (e.g. "project1.html")
5. Copy the turnin2csv.py file into the same directory as the html file you saved
6. Run the script:

`python turnin2csv.py <filename.html>`

Each test is calculated as equal value and only a passed test earns points. In other words, if a student passes 3 of 4 tests, they are graded 75%.

Each test is calculated as equal value and only a passed test earns points. In other words, if a student passes 3 of 4 tests, they are graded 75%.

By default, a penalty of 20 points per day late is imposed when calculating the grades. If you want to change that value, edit the script and change the value that `LATE_PENALTY_PER_DAY()` returns.
