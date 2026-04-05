from flask import Flask,render_template,redirect,request,session
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from sklearn.linear_model import LogisticRegression
import pandas as pd
from Model_ML import predict,IdToURI
import os
from dotenv import load_dotenv

## --------------- WEB APP -------------------------------


load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

REDIRECT_URI = "http://127.0.0.1:5000/callback"

app=Flask(__name__)
app.secret_key = "forshure"

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login-spotify")
def login_spotify():

    #creer une instance 0auth qui est un objet qui va prendre nos infos et etre la boite a outils pour utiliser l API ca s appelle un SDK

    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-library-read playlist-modify-public playlist-modify-private"  # Permissions
    )

    # Redirige vers la page d'auth Spotify
    auth_url = sp_oauth.get_authorize_url() # get_authorize_url() : methode qui construit l'url qui renvoie a la page de connexion


    return redirect(auth_url) # redirect(lien) envoie l utilisateur a un lien


# Route ou Spotify redirige après connexion
@app.route("/callback")
def callback():
    #Quand Spotify a fini l'authentification, il renvoie l'utilisateur vers MON site, à l'adresse que j'ai mise dans REDIRECT_URI Et il ajoute des informations dans l'URL dont un code
    # Spotify renvoie un code temporaire
    code = request.args.get('code') #va chercher dans l url le code crée , request.args cherche dans une url
    
    # Échange le code contre un token d'accès
    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-library-read playlist-modify-public playlist-modify-private"
    )
    token_info = sp_oauth.get_access_token(code)
    
    #token = sert à Prouver à Spotify qui tu es
    #session = sert à stocker des infos sur mon site 

    #on va donc stocker ce token dans une session a moi pour plus tard

    session['spotify_token'] = token_info
    
    return redirect("/final")


@app.route("/final")
def final():
    # Récupère le token Spotify
    token_info = session.get('spotify_token')
    if not token_info:
        return redirect("/login-spotify")
    
    # Crée l'objet Spotify
    sp = spotipy.Spotify(auth=token_info['access_token'])

    #sp.current_user_playlist_create("MakeMeAPlaylist!")

    #On recupere chaque musique qui est un dictionnaire contenant toute les infos 

    TrackLiked=(sp.current_user_saved_tracks())

    TLsize=TrackLiked['total']

##-------------------- DATA PIPELINE -------------------------------------------------


    #On récupere les infos interessante et le transforme en dataframe

    UserLiked=pd.DataFrame()

    id=[]
    name=[]

    #Les requete spotify sont limitées donc suite à une erruer 50 requette de 20 sons donne 1000 sons c'est une bonne base de travail 

    for i in range(50):

        TrackLiked=(sp.current_user_saved_tracks(20,i*20))

        for music in TrackLiked['items']:
            id.append(music['track']['id'])
            name.append(music['track']['name'])
        print(i)
    
    UserLiked['id']=pd.Series(id)
    UserLiked['name']=pd.Series(name)

    #print(UserLiked)

    # on a donc UserLiked un df avec les id et le nom des 1000 dernieres tracs likée par l'Utilisateur 

    features=['danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','time_signature']

    songFeature=sp.audio_features(UserLiked['id'])

    for feature in features:
        f=[]
        for music in songFeature:
            f.append(music[feature])
        UserLiked[feature]=pd.Series(f)
    
    #On a donc UserLiked['id','name','danceability','dnergy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','time signature']


##--------------- ML ------------------------------------------------------------

    recommendation=predict(UserLiked)

    ##Création de la playlist

    playlist=sp.current_user_playlist_create('Make Me a Playllist !')
    playlist_id = playlist['id']

    URI_list=[IdToURI(song) for song in recommendation["track_id"]]

    sp.playlist_add_items(playlist_id,URI_list)

    return render_template("final.html")






if __name__ == "__main__":
    app.run(debug=True)



