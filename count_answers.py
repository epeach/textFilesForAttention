import csv
import os
import sys
import numpy as np
import matplotlib.pyplot as plt





try:
  fns = sys.argv[1:]
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
  try:
    care = int(row[careidx])
    selfr[gp].append(care)
    return care
  except:
    return 0

def add_answers(row):
  correct = 0.
  gp = int(row[gpidx])
  for i in quidx:
    if not i in anidx:
      print "formatting error, mismatched questions/answers"
    qnum = row[quidx[i]]
    if qnum.startswith("t"):
      age = 27
      try:
        age =int(row[ageidx])
      except:
        age = 27
      correct += checkans(qnum,int(row[anidx[i]]), age)
  answers[gp].append(correct)
  return correct

outputf = ["","","",""]
outw = [None,None,None,None]
for i in range(4):
  outputf[i] = open("output"+str(i)+".csv","w")
  outw[i] = csv.writer(outputf[i], delimiter=',', quotechar='"')
j=0
for fn in fns:
  with open(fn, 'rb') as csvfile:
    outputreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    header=True
    leng = 0
    for row in outputreader:
      if header:
        leng = len(row)
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

        if j ==0:
          for i in range(4):
            outw[i].writerow(row+["Correct","Self-rating"])
          j += 1
        if row[29] != "Answer.careful" or row[34] != "Answer.grouptype":
          print "formatting error"
        header= False
        continue
      ans = add_answers(row)
      sr = add_selfrating(row)
      while len(row) < leng:
        row.append("")
      outw[int(row[gpidx])].writerow(row+[ans,sr])
for i in range(4):
  outputf[i].close()
from scipy import stats
cond = ["IMC","Neutral","Financ","Positive"]
mean_ = [[],[]]
std_ = [[],[]]
for i in range(4):
    print str(i)+": "+cond[i]
    print "# of Responses:" +str(len(answers[i]))
    if len(answers[i]) > 0:
      print "Avg. Acc:"+str(sum(answers[i])/float(len(answers[i])))
      print "Avg. Self:"+str(sum(selfr[i])/float(len(selfr[i])))
      print "Stddev. Acc:"+str(np.asarray(answers[i]).std())
      print "Stddev. Self:"+str(np.asarray(selfr[i]).std())
      mean_[0].append(sum(answers[i])/float(len(answers[i])))
      #std_.append(stats.sem(np.asarray(answers[i])))
      std_[0].append(np.asarray(answers[i]).std()/float(len(answers[i])**.5))
      mean_[1].append(sum(selfr[i])/float(len(selfr[i])))
      std_[1].append(np.asarray(selfr[i]).std()/float(len(selfr[i])**.5))
      print "Complete Sheet"
      #for a in range(len(answers[i])):
      #  print str(answers[i][a])+"\t"+str(selfr[i][a])
    print "\n"
print stats.f_oneway(answers[0],answers[1],answers[2],answers[3])
print stats.f_oneway(selfr[0],selfr[1],selfr[2],selfr[3])

fig, ax = plt.subplots()
bar_width = 0.45

opacity = 0.6
error_config = {'ecolor': '0.1','elinewidth':2., 'capsize':5, 'capthick':2.}
index = np.arange(4)/2.#[0,1,2,3]
rects1 = plt.bar(index, mean_[0], bar_width,
                 alpha=opacity,
                 color='b',
                 yerr=std_[0],
                 error_kw=error_config)

ax.set_ylim([0,7.5])
plt.xlabel('Group')
plt.ylabel('# Correct')
plt.title('Average Score per Condition')
plt.xticks(index+.2, ('IMC', 'Neutral', 'Financial', 'Positive'))
#plt.legend()
#plt.tight_layout()
plt.show()

fig, ax = plt.subplots()
rects1 = plt.bar(index, mean_[1], bar_width,
                 alpha=opacity,
                 color='b',
                 yerr=std_[1],
                 error_kw=error_config)

ax.set_ylim([0,5.5])
plt.xlabel('Group')
plt.ylabel('Selfrating')
plt.title('User Self-Rating in Attentiveness')
plt.xticks(index+.2, ('IMC', 'Neutral', 'Financial', 'Positive'))
#plt.legend()
#plt.tight_layout()
plt.show()
