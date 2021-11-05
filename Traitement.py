from json import dump,dumps,load,loads

with open('Retweet.txt', 'r') as g:
	lines=g.readlines()
	for l in lines:
		nom = l.split(':')[0]
		nb_retweet = l.split(':')[1]
		#print(nom)
		#print(int(nb_retweet))
		with open('TweetsSorDataTrump.json', 'r') as f:
			lines=f.readlines()
			list_int = []
			for b in range(len(lines)):
				data=loads(lines[b])
				try:	
					if (nom.rstrip() == data['retweeted_status']['user']['screen_name']):
						list_int.append(int(data['retweeted_status']['retweet_count']))
				except:
					pass
		if(len(list_int)>0):
			with open('Tweet_total.txt','a') as h:
					h.write(nom.rstrip() +" , " +nb_retweet.rstrip()+" , "+str(max(list_int)))
					h.write('\n')
