#!/bin/env python

from pymongo import MongoClient

connection = MongoClient("mongodb://allion:allion123@ds029821.mongolab.com:29821/twitter")

print connection

# connect to the students database and the ctec121 collection
db = connection.twitter.tweets
print db
# create a dictionary to hold student documents

# create dictionary
student_record = {}

# set flag variable
flag = True

# loop for data input
while (flag):
   # ask for input
   student_name = raw_input("Enter student name: ")
   print student_name
   student_grade = raw_input("Enter student grade: ")
   # place values in dictionary
   student_record = {'name':student_name,'grade':student_grade}
   # insert the record
   db.insert(student_record)
   # should we continue?
   flag = raw_input('Enter another record? ')
   if (flag[0].upper() == 'N'):
      flag = False

# find all documents
results = db.find()

print()
print('+-+-+-+-+-+-+-+-+-+-+-+-+-+-')

# display documents from collection
for record in results:
	# print out the document
	print(record['name'] + ',',record['grade'])

print()

# close the connection to MongoDB
connection.close()