from pyvis.network import Network
import networkx as nx
from json import dump,dumps,load,loads

i=0
net=Network('600px', '1340px',directed=True)
with open('TweetsSorDataTrump.json', 'r') as f:
	lines=f.readlines()
	for b in range(len(lines)):
		try:
			data=loads(lines[b])
			try:
				try: #si un tweet-retweer
					net.add_node(f"{data['retweeted_status']['user']['screen_name']}",size=25,color='#e75e5e')
					net.add_node(f"{data['user']['screen_name']}",size=23)
					net.add_edge(f"{data['retweeted_status']['user']['screen_name']}",f"{data['user']['screen_name']}", weight=5,title=str(f"{data['text']}"))
				except: #si un tweet origine   
					net.add_node(f"{data['user']['screen_name']}",size=20,color='#FFDC73',title=str(f"{data['text']}"))
			except:
				pass
		except:
			pass

list_int2 = net.get_nodes()



n=1690
small_net = Network('600px', '1340px',directed=True)

for l in list_int2:
	voisin = net.neighbors(l)
	if (len(voisin)>n):
		small_net.add_node(l,size=25,color='#FFDC73')
		with open('Retweet.txt','a') as f:
			f.write(l+" : "+ str(len(voisin)))
			f.write('\n')
		for v in voisin:
			list_int3 = small_net.get_nodes()
			if v not in list_int3:
				small_net.add_node(v,size=25,color='#e75e5e')
				small_net.add_edge(v,l,weight=5)

small_net.show_buttons(filter_=['physics','nodes', 'edges'])
small_net.save_graph('Condenser.html')