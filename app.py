from flask import Flask,render_template,request,jsonify, redirect, url_for
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

app = Flask(__name__)

# Função auxiliar que sempre obtém o token válido do .cache
def get_user_spotify():
  #Inicializa o cliente Spotify
  sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI,scope=SCOPE,cache_path=".cache-user")
  
  token_info = sp_oauth.get_cached_token()
  if not token_info:
      raise Exception("❌ Nenhum token encontrado. Autentique com /login primeiro.")
  if sp_oauth.is_token_expired(token_info):
      token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
  return spotipy.Spotify(auth=token_info['access_token'])
 
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/login')
def login():
  # Redireciona o usuário para o login do Spotify
  sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI,scope=SCOPE,cache_path=".cache-user")
  auth_url = sp_oauth.get_authorize_url()
  return redirect(auth_url)

@app.route('/callback')
def callback():
  sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI,scope=SCOPE,cache_path=".cache-user")
  # Manipula o callback após o login do Spotify
  code = request.args.get('code')
  token_info = sp_oauth.get_access_token(code)
  print('Callback - Login realizado com sucesso!')

  return redirect(url_for('index'))

@app.route('/music', methods=['POST'])
def add_music():
  music = request.form.get('input-text')
  sp_app = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,client_secret=CLIENT_SECRET))
  # Pesquisa a música no Spotify
  result = sp_app.search(q=music, limit=10, type='track')
  
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
  data = request.get_json()
  track_id = data.get('track_id')
  
  if not track_id:
    return jsonify({"status":"error"}),400

  try:
    get_user_spotify().playlist_add_items(PLAYLIST_ID, [track_id])
    return jsonify({"status":"success"}),200
  except Exception as e:
    return jsonify({"status":"error", "message": str(e)}),500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    

    