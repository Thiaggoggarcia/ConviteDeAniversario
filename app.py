from flask import Flask,render_template,request,jsonify, redirect, url_for, session
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


#Inicializa o cliente Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI,scope=SCOPE))

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')
  

@app.route('/login')
def login():
  # Redireciona o usuário para o login do Spotify
  auth_url = sp.get_authorize_url()
  print(f'Passe no login {auth_url}')
  return redirect(auth_url)

@app.route('/callback')
def callback():
  # Manipula o callback após o login do Spotify
  code = request.args.get('code')
  token_info = sp.get_access_token(code, as_dict=True)
  session['token_info'] = token_info
  print('Callback - Login realizado com sucesso!')

  return redirect(url_for('index'))

def get_spotify_client():
  token_info = session.get('token_info', None)
  if not token_info:
    return None

  if sp.is_token_expired(token_info):
    token_info = sp.refresh_access_token(token_info['refresh_token'])
    session['token_info'] = token_info

  access_token = token_info['access_token']
  return spotipy.Spotify(auth=access_token)

@app.route('/music', methods=['POST'])
def add_music():
  sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,client_secret=CLIENT_SECRET))
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
      "album": item['album']['name'],
      "artist": item['artists'][0]['name'],
      "image_url": item['album']['images'][1]['url'] if item['album']['images'] else None
    }
    tracks.append(track)

  return jsonify({"status": "success", "tracks": tracks}), 200

@app.route('/playlist', methods=['POST'])
def add_playlist():
  track_id = request.json.get('track_id')
  print(f'Estou na rota Playlist {track_id}')
  
  if not track_id:
    return jsonify({"status":"error"}),400

  try:
    sp.playlist_add_items(PLAYLIST_ID, [track_id])
    return jsonify({"status":"success"}),200
  except Exception as e:
    return jsonify({"status":"error", "message": str(e)}),500

if __name__ == "__main__":
    app.run(debug=True)
    

    