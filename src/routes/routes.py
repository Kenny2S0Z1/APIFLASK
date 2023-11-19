from app import app
from flask_cors import CORS,cross_origin
from flask import jsonify
import requests
from src.functions import obtener_lista_de_corte,agregar_ip_a_lista_corte




CORS(app)
@app.route('/')
def index():
    return '¡API FLASK MIKROTIK'

@app.route('/list_c')
@cross_origin()
def route_ver_lista_de_corte():
    try:
        resultado = obtener_lista_de_corte()
        return jsonify(resultado)
    except Exception as e:
        print(f"Error al obtener la lista de cortes: {str(e)}")
        return jsonify({"error": "Error al obtener la lista de cortes"}), 500
        
@app.route('/agregar_ip', methods=['POST'])
@cross_origin()
def route_agregar_ip():
    data = requests.get_json()
    ip_a_agregar = data.get('ip')

    if not ip_a_agregar:
        return jsonify({"error": "Se requiere la dirección IP para agregar a la lista de cortes"}), 400

    if agregar_ip_a_lista_corte(ip_a_agregar):
        return jsonify({"mensaje": f"La IP {ip_a_agregar} se ha agregado correctamente a la lista de cortes"})
    else:
        return jsonify({"error": f"No se pudo agregar la IP {ip_a_agregar} a la lista de cortes"}), 500