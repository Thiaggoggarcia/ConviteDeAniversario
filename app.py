from flask import Flask,render_template,request, jsonify
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = os.getenv("SCOPE")
PLAYLIST_ID = os.getenv("PLAYLIST_ID")


# Inicializa o cliente Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE
                                               ))

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

#TODO: Implementar via JavaScript fetch para não recarregar a página
@app.route('/music', methods=['POST'])
def add_music():
    music = request.form.get('message-text')

    return f"<h1>Musica recebida: {music}</h1>"

if __name__ == "__main__":
    app.run(debug=True)
    

    