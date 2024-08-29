from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def get_bac_results():
    nom = request.args.get('nom')
    if not nom:
        return jsonify({"error": "No name provided"}), 400
    
    # Étape 1: Rechercher la clé dynamique associée au nom
    base_url = "https://mahajanga-api.bacc.digital.gov.mg/api/search"
    params = {
        'nom': nom
    }
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch dynamic key"}), 500
    
    # Extraction de la clé à partir de la réponse HTML (ou JSON selon le site)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Remplacez cette ligne avec la méthode correcte pour extraire la clé
    key = extract_key(soup)  # Cette fonction est un exemple à implémenter
    
    if not key:
        return jsonify({"error": "Failed to extract key"}), 500
    
    # Étape 2: Effectuer la recherche des résultats avec la clé
    search_url = f"https://mahajanga-api.bacc.digital.gov.mg/api/search"
    search_params = {
        'nom': nom,
        'key': key
    }
    final_response = requests.get(search_url, params=search_params)
    
    if final_response.status_code != 200:
        return jsonify({"error": "Failed to fetch search results"}), 500
    
    # Étape 3: Parser les résultats et les retourner sous forme JSON
    results = parse_results(final_response.text)
    
    return jsonify(results)

def extract_key(soup):
    # Exemple d'extraction de clé: cela doit être adapté en fonction de la structure du site
    # key = soup.find('input', {'name': 'key'})['value']
    key = "386d6ff3cba30a4f92f02e67e3a5ed22"  # Remplacer par la logique d'extraction réelle
    return key

def parse_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    
    # Extraction des résultats en fonction de la structure du HTML
    rows = soup.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 0:
            result = {
                "numero_inscription": cols[0].text.strip(),
                "nom_prenoms": cols[1].text.strip(),
                "serie": cols[2].text.strip(),
                "centre": cols[3].text.strip(),
                "mention": cols[4].text.strip(),
                "observation": cols[5].text.strip()
            }
            results.append(result)
    
    return results

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
