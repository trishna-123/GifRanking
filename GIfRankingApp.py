from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)


TENOR_API_KEY = 'AIzaSyDJ-ymkDjHS8zf8UTTK9okb4qHFDHLew9M'
TENOR_SEARCH_URL = 'https://tenor.googleapis.com/v2/search'

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>GIF Search</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        background-color: #f0f0f0;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
      }
      h1 {
        color: #333;
        margin-top: 20px;
      }
      form {
        margin: 20px 0;
        display: flex;
        align-items: center;
      }
      input[type="text"] {
        padding: 10px;
        width: 300px;
        border: 2px solid #ddd;
        border-radius: 5px;
        margin-right: 10px;
        font-size: 16px;
      }
      input[type="submit"] {
        padding: 10px 20px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
        transition: background-color 0.3s;
      }
      input[type="submit"]:hover {
        background-color: #0056b3;
      }
      hr {
        width: 80%;
        border: 1px solid #ddd;
      }
      .gif-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        margin-top: 20px;
      }
      .gif-container img {
        width: 200px;
        height: auto;
        margin: 10px;
        border-radius: 10px;
        transition: transform 0.3s, box-shadow 0.3s;
      }
      .gif-container img:hover {
        transform: scale(1.1);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
      }
    </style>
  </head>
  <body>
    <h1>Search for GIFs</h1>
    <form action="/" method="get">
      <input type="text" name="q" placeholder="Search for GIFs">
      <input type="submit" value="Search">
    </form>
    <hr>
    {% if gifs %}
      <h2>Top GIFs for "{{ query }}"</h2>
      <div class="gif-container">
        {% for gif in gifs %}
          <img src="{{ gif }}" alt="GIF">
        {% endfor %}
      </div>
    {% endif %}
  </body>
</html>
"""


@app.route('/', methods=['GET'])
def index():
    query = request.args.get('q')
    gifs = []
    if query:
        gifs = search_gifs(query)
    return render_template_string(HTML_TEMPLATE, gifs=gifs, query=query)

def search_gifs(query):
    """Search GIFs using Tenor API based on the given query."""
    params = {
        'q': query,
        'key': 'AIzaSyDJ-ymkDjHS8zf8UTTK9okb4qHFDHLew9M',
        'limit': 50,
        'media_filter': 'minimal',
    }
    response = requests.get(TENOR_SEARCH_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return [result['media_formats']['gif']['url'] for result in data['results']]
    return []

if __name__ == '__main__':
    app.run(debug=True)
