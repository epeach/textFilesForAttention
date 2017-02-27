import csv
import os
import sys

try:
  fn = sys.argv[1]
except:
  print "usage='python count_answers.py <amt_output_file>'"
  exit(1)

answers = [[],[],[],[]]
selfr = [[],[],[],[]]
gpidx = 34
careidx = 29
ageidx = 28
quidx = dict()
anidx = dict()

def checkans(tqid, answer, age):
  if tqid == "tqu1":
    if age >= 27 and answer == 5:
      return 1
    if age <= 27 and answer == 1:
      return 1
  if tqid=="tqu2" and answer == 1:
    return 1
  if tqid=="tqu3" and answer == 1:
    return 1
  if tqid=="tqu4" and answer == 1:
    return 1
  if tqid=="tqu5" and answer == 5:
    return 1
  if tqid=="tqu6" and answer == 1:
    return 1
  if tqid=="tqu7" and answer == 1:
    return 1
  return 0

def add_selfrating(row):
	gp = int(row[gpidx])
	care = int(row[careidx])
	selfr[gp].append(care)

def add_answers(row):
	correct = 0.
	gp = int(row[gpidx])
	for i in quidx:
		if not i in anidx:
			print "formatting error, mismatched questions/answers"
		qnum = row[quidx[i]]
		if qnum.startswith("t"):
			correct += checkans(qnum,int(row[anidx[i]]), int(row[ageidx]))
	answers[gp].append(correct)


with open(fn, 'rb') as csvfile:
  outputreader = csv.reader(csvfile, delimiter=',', quotechar='"')
  header=True
  for row in outputreader:

    if header:
      for idx in range(len(row)):
      	if row[idx] == "Answer.careful":
      		careidx = idx
      	elif row[idx] == "Answer.grouptype":
      		gpidx = idx
        elif row[idx] == "Answer.age":
          ageidx = idx
      	elif row[idx].startswith("Answer.qNum"):
      		quidx[int(row[idx].split("m")[1])] = idx
      	elif row[idx].startswith("Answer.q"):
      		anidx[int(row[idx].split("q")[1])] = idx

      if row[29] != "Answer.careful" or row[34] != "Answer.grouptype":
      	print "formatting error"
      header= False
      continue
    add_answers(row)
    add_selfrating(row)

cond = ["IMC","Neutral","Financ","Positive"]
for i in range(4):
    print str(i)+": "+cond[i]
    print "# of Responses:" +str(len(answers[i]))
    if len(answers[i]) > 0:
      print "Avg. Acc:"+str(sum(answers[i])/float(len(answers[i])))
      print "Avg. Self:"+str(sum(selfr[i])/float(len(answers[i])))
    print "\n"
