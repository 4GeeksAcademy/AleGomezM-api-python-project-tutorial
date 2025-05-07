import os
import pandas as pd
import seaborn as sns
from dotenv import load_dotenv
import spotipy
import matplotlib.pyplot as plt
from spotipy.oauth2 import SpotifyClientCredentials

# load the .env file variables
load_dotenv()

# Get credential values
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")


# Gestion del proceso de autenticacion a la API de spotify
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
spotify = spotipy.Spotify(auth_manager=auth_manager)

# Solicitudes a la API
oasis_id = '2DaxqgrOhkeH0fpeiQq2f4'
canciones_top=spotify.artist_top_tracks(oasis_id, country='US')

#Creamos un ciclo para obtener las 10 canciones top del artista en forma de diccionario
data = []

for track in canciones_top['tracks']:

    data.append({
        'track': track['name'],
        'duration_ms': track['duration_ms'],
        'popularity': track['popularity']
    })


# A partir del diccionario data creamos un dataframe 
top_data = pd.DataFrame(data)

#Creamos una fila llamada duracion_m para tener el tiempo en minutos e interpretarlo mas facil en el siguiente punto
duracion_m=round(top_data['duration_ms']/60000, 2)
top_data.insert(1, 'duracion_m', duracion_m)
print(top_data)

# crear un dataframe con las canciones ordenadas por popularidad y mostramos las 3 primeras
top_ordenda=top_data.sort_values("popularity", ascending=False)
top_ordenda.head(3)

# Se crea la gráfica con seaborn
sns.scatterplot(x='duracion_m', y='popularity', data=top_data)
plt.title("Popularidad vs duración de la canción")
plt.show()

# Se concluye que no hay una relación directa o indirecta entre la duracion de la cancion y su popularidad,
#  pues la cancion más popular no es la más larga, ya que las dos canciones mas populares duran un poco 
# mas de 4 minutos lo cual es un tiempo aceptable, y la tercera dura mas de 7 minutos, lo cual es bastante
# atipico. Las demas canciones se encuentran en todo el rango, sin tener un comportamiento que siga un 
# patron. Tambien hay que resaltar que las canciones top de Oasis tienen la mayoria una duración mas alta 
# de lo normal y que problamente una muestra de 10 canciones es talvez muy pequeña para concluir esta 
# relación de manera generalizada.