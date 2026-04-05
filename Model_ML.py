from sklearn.linear_model import LogisticRegression
import pandas as pd

def predict(df1):

    #On récupere le dataset et on y ajoute la colonne Liked (=1 par définition)

    df_User= df1[['danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','time_signature']]
    df_User["Liked"]=[1 for i in range(len(df_User))]

    #print(X_User) #test

    #On prend maintenant un dataset public de tout les sons sur spotify 

    df2=pd.read_csv("spotify-tracks-dataset.csv")

    df_Spotify=df2[['danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','time_signature']]
    df_Spotify["Liked"]=[0 for k in range(len(df_Spotify))]

    #print(X_Spotify) #test

    #On a donc les dataset de l'utilisateur et de spotify On va train le modele sur le dataset user et un echantillon aleatoire de meme taille 

    df_rand_spotify=df_Spotify.sample(n=len(df_User))

    df=pd.concat([df_User,df_rand_spotify])

    #X variable predictrice, y variable à predire

    X=df[['danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','time_signature']]
    Y=df["Liked"]

    # On scales les valeurs suite a des erreurs 

    from sklearn.preprocessing import StandardScaler #on importe le module 

    scaler = StandardScaler() # on crée l objet scaler

    X_scaled = scaler.fit_transform(X) #X le vecteur des variables predictrice et X_scaled le X scalé dcp  
    df_Spotify_scaled=scaler.transform(df_Spotify[['danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','time_signature']])
    #on train le modele 

    Cl=LogisticRegression(random_state=808).fit(X_scaled,Y)

    #Le modele calcule la proba pour chaque son du dataset

    Y_proba=Cl.predict_proba(df_Spotify_scaled)

    Y_proba = pd.DataFrame(Y_proba)

    Y_proba['Artists']=df2['Artists'].values
    Y_proba['Track_Name']=df2['Track_Name'].values
    Y_proba['track_id']=df2['track_id'].values

    #On fixe le seuil à 90% si le son à 90% de chance d'etre liké => 1 sinon 0

    Y_proba['Predict']=[0 if son<0.99 else 1 for son in Y_proba[1]]

    #On crée Y_Predict avec seulement les sons à recommander

    Y_Predict = Y_proba[Y_proba["Predict"] == 1][["Artists", "Track_Name","track_id"]]

    print(Y_Predict)

    return Y_Predict

def IdToURI(id):
    return "spotify:track:" + id