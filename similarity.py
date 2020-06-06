
import math
import string
import re
from flask import Flask, jsonify, render_template, request



def readfile(n1, n2):

	""" This function reads the file from the local directory"""

	file1 = open(n1,"r")
	file2 = open(n2,"r")
	return file1.read(), file2.read()
	
def bucket_creation(n1,n2):

	""" This function creates a bucket that 
	contains all the words from all the documents"""
	
	file1, file2 =  readfile(n1,n2)
		
	file2 = file2.replace("you'll","you will")
	file1 = file1.replace("you'll","you will")
	file2 = file2.replace("don't","do not")
	file1 = file1.replace("don't","do not")	
	file2 = file2.replace("\n"," ")
	file1 = file1.replace("\n"," ")
	
	exclude = set(string.punctuation)
	
	file2 = "".join([x.lower() for x in file2 if x not in exclude])
	file1 = "".join([x.lower() for x in file1 if x not in exclude])
		
	bucket = file1.split()	+ file2.split()
	
	file1 = file1.split()
	file2 = file2.split()
	return file1, file2, bucket
		
	
def	vector_formation(n1,n2):
	
	"""This function converts the two documnts 
	into a vector form using tf-idf method"""

	file1, file2, bucket = bucket_creation(n1,n2)
	count1 = []
	count2 = []
	
	for i in bucket:
		count1.append(file1.count(i))
		count2.append(file2.count(i))

	vector1 = dict( [ (a,b) for a,b in zip(bucket,count1)  ] )
	vector2 = dict( [ (a,b) for a,b in zip(bucket,count2)  ] )
	
	vector1 = dict( [ (key, round(value/len(file1), 2))  for key,value in vector1.items() ] )
	vector2 = dict( [ (key, round(value/len(file2), 2))  for key,value in vector2.items() ] )
	
	return vector1, vector2

def cosine_operation(n1,n2):

	"""This function finds the similarity between two vectors 
	using cosine formula. The result determines how similar two documents are
	based on their vector orientation"""
	
	vector1, vector2 = vector_formation(n1,n2)
	file1, file2, bucket = bucket_creation(n1,n2)
	
	idf = []
	doc_count = 2
	
	for i in bucket:
		if i in (file1 and file2):
			idf.append(2)
		else:
			idf.append(1)

	idf = [ math.log((doc_count)/x)  for x in idf ]
			
	for key, logs in zip(vector1,idf):
		vector1[key]  = logs * vector1[key]
		
	for key, logs in zip(vector2,idf):
		vector2[key]  = logs * vector2[key]

	numerator = sum([ vector1[key]*vector2[key] for key in vector1 ])
	denomenator = math.sqrt(sum([ (vector1[key]*vector1[key]) for key in vector1 ]) ) * math.sqrt(sum([ (vector2[key]*vector2[key]) for key in vector2 ]) )
	try:
		simalirity = numerator/denomenator	
		return simalirity
	except:
		return 1
	
app = Flask(__name__)

@app.route('/')
def student():
	""" This functions provides a form to input documents names"""

	return render_template('student.html')
   
	
@app.route('/result',methods = ['POST', 'GET'])
def result():

	""" this function renders the result 
	using the Post request from """
	
	n1 = request.form.get('n1')
	n1 = n1+".txt"
	n2 = request.form.get('n2')
	n2 = n2+'.txt'
			
		
	if not (n1 and n2) in ('sample1.txt','sample2.txt','sample3.txt'):
		return jsonify("Exception: Please input correct file names")

	s = cosine_operation(n1,n2) * 100
	answer = "The Similarity between two documents is = " + str(round(s,3)) + "%"
	if request.method == 'POST':
		return jsonify(answer)
	


if __name__=="__main__":
	app.run()
	
	