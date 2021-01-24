import json
import requests
import datetime
import pandas as pd
import pprint
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
import sys

class readTweets:	
	def __init__(self):	
		self.data = []
		self.id = None
		self.rule_set = False
		self.links = []
		self.domains = {}
		self.words = []

	def set_rule(self, keyword, bearer_token):	
		rule = {
				"add": [
					{"value": keyword, "tag": "tweets with "+keyword}
				       ]
			    }
		rule_object = requests.post(
			      url='https://api.twitter.com/2/tweets/search/stream/rules',
			      json=rule,
			      headers={
					"Content-type":"application/json",
					"Authorization":"Bearer "+bearer_token
				      })
		if rule_object.status_code == 201:	
			self.id = json.loads(rule_object.text)['data'][0]['id']
			self.rule_set = True

	def unset_rule(self, keyword, bearer_token):	
		rule = {
				"delete": {
					    "ids": [self.id]
				          }
		       }
		rule_object = requests.post(
			      url='https://api.twitter.com/2/tweets/search/stream/rules',
			      json=rule,
			      headers={
					"Content-type":"application/json",
					"Authorization":"Bearer "+bearer_token
				      })
		if rule_object.status_code == 200:	
			self.rule_set = False

	def get_data(self, keyword, bearer_token, span):	
		if self.rule_set:	
			self.data = []
			data = requests.get(
						url='https://api.twitter.com/2/tweets/search/stream?expansions=author_id&user.fields=username&tweet.fields=entities',
						headers={"Authorization":"Bearer "+bearer_token},
						stream=True
					   )
			start = datetime.datetime.now()
			for line in data.iter_lines():	
				if line:	
					decoded_data = json.loads(line.decode('utf-8'))
					decoded_data['data']['users'] = decoded_data['includes']
					self.data.append(decoded_data['data'])
				end = datetime.datetime.now()
				if (end-start).seconds > span:	
					break
			if len(self.data) > 0:	
				self.data = pd.DataFrame(self.data)

	def process_links(self,decoded):	
		if decoded is not np.nan:	
			if 'urls' in decoded.keys():	
				for url in decoded['urls']:	
					self.links.append(url['expanded_url'])
					domain = url['expanded_url'].split("//")[1].split("/")[0]
					if domain not in self.domains:	
						self.domains[domain] = 1
					else:	
						self.domains[domain] = self.domains[domain] + 1

	def process_tweets(self, text):	
		for word in text.split(" "):	
			word = word.replace(r'(\\n|\\t|\\x|[^a-zA-Z0-9])',"")
			if len(re.findall(r'(https|http)',word))==0 and len(word)!=0 and word.lower() not in stopwords.words('english') and word.lower() not in ["a","an","the"]:	
				self.words.append(word)

	def generate_reports(self):	
		if len(self.data) > 0:	

			print()

			#User Report
			print("Usernames with Tweet Counts")
			self.data['username'] = self.data['users'].apply(lambda x: x['users'][0]['username'])
			print(self.data[['username','text']].groupby(['username'],as_index=False).count())

			print()

			#Link Report
			print("Domains with their Frequency")
			self.data['entities'].apply(lambda x: self.process_links(x))
			print(pd.DataFrame(data=sorted(self.domains.items(), key=lambda item:item[1], reverse=True),columns=["Domain","Frequency"]))

			print()

			#Unique Words and their occurences
			print("Words and their Occurences")
			self.data['text'].apply(lambda x: self.process_tweets(x))
			print(pd.value_counts(self.words)[0:10])

			print()


if len(sys.argv) < 5:	
	print("Invalid argument(s) passed")
	print("Format: <keyword> <span> <bearer_token> <mode>")
else:	
	mode = int(sys.argv[4])
	rt = readTweets()
	rt.set_rule(sys.argv[1], sys.argv[3])
	if mode == 0:	
		rt.get_data(
				keyword=sys.argv[1],
				span=int(sys.argv[2]),
				bearer_token=sys.argv[3]
	   		    )

		rt.generate_reports()
		rt.unset_rule(sys.argv[1], sys.argv[3])
	elif mode == 1:	
		i = 1
		while i >= 1:	
			print("RUN: "+str(i))
			rt.get_data(
				keyword=sys.argv[1],
				span=int(sys.argv[2]),
				bearer_token=sys.argv[3]
	   		    )
			rt.generate_reports()
			i=i+1
			ans = input("Press 1 to continue, 0 to Exit..")
			if ans == '0':	
				break
		rt.unset_rule(sys.argv[1], sys.argv[3])
	else:	
		i = 60
		while i >= 60:	
			print("RUN: "+str(i))
			rt.get_data(
				keyword=sys.argv[1],
				span=i,
				bearer_token=sys.argv[3]
	   		    )
			rt.generate_reports()
			i = i+60
			ans = input("Press 1 to continue, 0 to Exit..")
			if ans == '0':	
				break
		rt.unset_rule(sys.argv[1], sys.argv[3])
