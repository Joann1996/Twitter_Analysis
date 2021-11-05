from stream_graph import ITemporalNodeSetDF, ITemporalLinkSetDF, StreamGraph, Visualizer
import  pandas.io.json as pdd
import  pandas as pd
import json
from bokeh.io import output_notebook
from bokeh.plotting import figure, show
import datetime
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from bokeh.models import BasicTicker, ColorBar, LinearColorMapper, ColumnDataSource, PrintfTickFormatter
from bokeh.transform import transform
from bokeh.palettes import plasma

user=[]
retweet=[]
retweetTime=[]
tweettime=[]
with open('vaccin.json','r') as f:
    lines=f.readlines()
    print("max Tweet=",int((len(lines)-1)/2))
    s=int(input("Le numéro du Début des tweets a traité:"))
    e=int(input("Le numéro du fin des tweets a traité:"))
    for b in range(s,e):
        data = json.loads(lines[b])
        user.append(data["user"]["screen_name"])
        tTweet = datetime.datetime.strptime(data["created_at"],'%a %b %d %H:%M:%S +0000 %Y')
        tweettime.append(tTweet)
        if "retweeted_status" in data:
            retweet.append(data["retweeted_status"]["user"]["screen_name"])
            date=data['retweeted_status']['created_at']
            tRetweet = datetime.datetime.strptime(date,'%a %b %d %H:%M:%S +0000 %Y')
            retweetTime.append(tRetweet)

        

dfretweet=pd.DataFrame(user, columns = ["Retweet_user"])
dfretweeted=pd.DataFrame(retweet, columns = ["retweeted_user"])

dfTweetdate=pd.DataFrame(tweettime,columns=["created_at"])

tls_df=pd.concat([dfTweetdate,dfretweet],axis=1)
tls_df["OrgTweet_user"]=dfretweeted
tls_df.dropna(subset = ["OrgTweet_user"], inplace=True)
dfretweetTime=pd.DataFrame(retweetTime, columns = ["created_at"])
tls_df=tls_df.fillna("nothing")
tns_df=pd.concat([dfTweetdate,dfretweet],axis=1)
tns_df.columns = ['created_at', 'Node']
dfretweeted=pd.concat([dfretweetTime,dfretweeted],axis=1)
dfretweeted.columns = ['created_at','Node']

tns_df=tns_df.append(dfretweeted,ignore_index = True)



#
#
date_to_t = {date: i for i, date in enumerate(sorted(list(set(tns_df['created_at']))))}

t_to_date = {i: date  for date, i in date_to_t.items()}
def to_date(t):
    return pd.to_datetime(t_to_date[t], format='%Y-%m-%d')


#
tns_df['ts'] = tns_df['created_at'].map(date_to_t)
tls_df['ts'] = tls_df['created_at'].map(date_to_t)


tns_df.drop(columns=['created_at'], inplace=True)
tls_df.drop(columns=['created_at'], inplace=True)

tns_df=tns_df.sort_values(by=['ts'])
tns_df=tns_df.drop_duplicates(subset=["Node", "ts"])
tls_df=tls_df.sort_values(by=['ts'])


tns = ITemporalNodeSetDF(tns_df, discrete=True)
tls = ITemporalLinkSetDF(tls_df, discrete=True)


#
ns, ts = tns.nodeset, tls.timeset

sg = StreamGraph(ns, ts, tns, tls)


maxtimeset=print("Maximum timeset est: ",sg.timeset_.size)
limit=int(input("Entrez la limit de timeset affiche: "))
nsu, nsv = zip(*[u for u,d in ITemporalLinkSetDF(tls_df[tls_df.ts <= limit], discrete=True).duration_of() ])
sgv = sg.substream(nsu, nsv, [(0, limit)])
Visualizer(y_axis_label='#Retweet').fit(sgv).show()

print("################ Résultat #################")           
nnodes = sg.nodeset_.size  
print(" le nombre de différents tweets",nnodes)         
ntimes = sg.timeset_.size
print("le nombre des instants (ts): ",ntimes)
print("la somme de tous les tweets (retweet inclus): ",sg.temporal_nodeset_.size)
print("le nombre des noeuds à chaque instants: ",sg.n)
print("le couvrage de stream-graph: ",sg.coverage)  
print("le nombre des interactions: ",sg.temporal_linkset_.number_of_interactions)
print("le nombre des retweet à chaque instants",sg.m)
print("la densité: ",sg.density)
print("le nombre de couples Retweet distincts: ",sg.temporal_linkset_.m)  
print("##########################################")           


# WordCloud
wc = WordCloud(background_color="white", repeat=True)
wc.fit_words(dict(sg.node_contribution_of()))

# 
plt.rcParams["figure.figsize"] = (10, 10)
plt.axis("off")
plt.imshow(wc, interpolation="bilinear")
plt.show()

#top20 retweeted tweet
u, d = zip(*sg.temporal_linkset_.degree_of())
top_20 = pd.DataFrame({'retweet': u, 'degree': d}).sort_values(by=['degree'], ascending=False).head(20)
del u, d

p = figure(title="Top 20 Tweet Retweeteé (par username)",y_range=top_20['retweet'],plot_width=1300, plot_height=600)
p.hbar(y=top_20['retweet'], right=top_20['degree'], height=0.5)
show(p)

#les tweet en fonction de temps
tv = sg.temporal_nodeset_.n_at()
t, value = zip(*((to_date(t), v) for t, v in tv))
p = figure(title="Les tweets en fonction du temps (Retweet inclus)",x_axis_type="datetime",plot_width=1300, plot_height=600)
p.vbar(x=t, top=value, width=1, line_color="blue")
show(p)





# Le nombre des interaction en fonction de temps
tv = sg.temporal_linkset_.m_at()

t, value = zip(*((to_date(t), v) for t, v in tv))
p = figure(title="Le nombre des interaction en fonction de temps ",x_axis_type="datetime",plot_width=1300, plot_height=600)
p.vbar(x=t, top=value, width=1, line_color="green")
show(p)



# Le nombre des interaction en fonction de temps
tv = sg.density_at()
t, value = zip(*((to_date(t), v) for t, v in tv))
p = figure(title="La densité a un temps donnés",x_axis_type="datetime",plot_width=1300, plot_height=600)
p.vbar(x=t, top=value, width=1, line_color="#a23420")
show(p)


