import tweepy
import networkx as nx
import webbrowser
import time
from tweepy.streaming import StreamListener
from json import dump,loads
from random import choices
from pathlib import Path

api_key= ""
api_secret= ""
token=""
token_secret=""
#uri='oob' #https:cfe.sh/twitter/callback
#auth= tweepy.OAuthHandler(api_key,api_secret,uri) # pour se connecter a twitter 
#-----------Pin et recuprer token et token sec-------------------
#redirect_url= auth.get_authorization_url()
#webbrowser.open(redirect_url)
#pin=input("what's the pin number? ")
#print(auth.get_access_token(pin))
#-------------------------------------
 
global filename,keyword,sensibilite,start_time,timer
filename=input("Entrer le nom de fichier :")
keyword=input("Entrer le mots cle:")
sensibilite=int(input("Entrer la sensibilité  du capture (%):"))
timer=float(input("Entrer le timer (days):"))*60*60*24
size=float(input("la taille maximal de stockage (MB):"))

start_time=time.time()
class listener(StreamListener): # capture des tweet en temps reel

    def on_data(self, data):
        try:
                 x=[0,1]
                 p=[sensibilite/100,1-(sensibilite/100)]
                 random=choices(x,p)
                 if (random[0]==0):
                     if (time.time()-start_time < timer):
                            print("Receive data...")
                            with open(f"{filename}.json", "a") as f:
                                if ((Path(f'{filename}.json').stat().st_size/10**6)<=size):

                                            f.write(data)
                                            return(True)
                                else:
                                     return False
                     
                 else:
                     print("Sleep 3 sec...")

                     if (time.time()-start_time < timer):
                         open(f"{filename}.json", "a")
                         time.sleep(2)
                         return(True)
                        
                     else :
                            return False
        except tweepy.TweepError:
                    print("vous avez atteint le maximum des requêtes...")
                    print("attendre 15 min...")
                    time.sleep(60 * 15)
                    return True     

#    def on_error(self, status):
#        if status == 420:
#            #returning False in on_error disconnects the stream
#            return False
                    
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(token, token_secret)

twitterStream = tweepy.Stream(auth, listener())
twitterStream.filter( track=[f"{keyword}"])
    
    
    