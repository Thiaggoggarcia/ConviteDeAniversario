from flask import Flask,render_template,request, jsonify
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials


load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = os.getenv("SCOPE")
PLAYLIST_ID = os.getenv("PLAYLIST_ID")


# Inicializa o cliente Spotify
#sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI,scope=SCOPE))

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET))
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/music', methods=['POST'])
def add_music():
  music = request.form.get('input-text')
  # Pesquisa a música no Spotify
  result = sp.search(q=music, limit=5, type='track')
  
  if not result['tracks']['items']:
    return jsonify({"status":"error", "message": "Música não encontrada"}),404
  
  tracks = []
  for item in result['tracks']['items']:
    track = {
      "id": item['id'],
      "name": item['name'],
      "artist": item['artists'][0]['name'],
      "preview_url": item['preview_url'],
      "image_url": item['album']['images'][1]['url'] if item['album']['images'] else None
    }
    tracks.append(track)

  return jsonify({"status": "success", "tracks": tracks}), 200

if __name__ == "__main__":
    app.run(debug=True)
    

    