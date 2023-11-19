import routeros_api
from dotenv import load_dotenv
import os

load_dotenv()
MIKROTIK_IP = os.environ.get('MIKROTIK_IP')
MIKROTIK_API_USER = os.environ.get('MIKROTIK_API_USER')
MIKROTIK_PORT=os.environ.get('MIKROTIK_PORT')
MIKROTIK_API_PASSWORD = os.environ.get('MIKROTIK_API_PASSWORD')
MIKROTIK_LIST  = os.environ.get('MIKROTIK_LIST')


def establecer_conexion():
    global global_connection
    try:
        global_connection = routeros_api.RouterOsApiPool(
            MIKROTIK_IP, username=MIKROTIK_API_USER,
            password=MIKROTIK_API_PASSWORD, port=MIKROTIK_PORT,
        )
        api = global_connection.get_api()
        print('Conexión establecida')
        return api
    except Exception as e:
        print(f"Error al establecer la conexión: {str(e)}")
        return None

def agregar_ip_a_lista_corte(ip):
    global global_connection
  

    try:
        if not global_connection:
            # Si no hay conexión, intenta establecerla
            establecer_conexion()

        if global_connection:
            # Agrega la IP a la lista de cortes
            resource = global_connection.get_api().get_resource('/ip/firewall/address-list/add')
            result = resource.get(list=MIKROTIK_LIST, address=ip)

            # Si la respuesta es en formato JSON y contiene un elemento 'trap'
            try:
                result_json = result.json()
                if 'trap' in result_json:
                    print(f"IP {ip} agregada correctamente a la lista de cortes.")
                    return True
                else:
                    print(f"Error al agregar la IP {ip} a la lista de cortes.")
                    return False

            except ValueError:
                print("La respuesta no es un JSON válido.")
                return False

        else:
            print('No hay conexión para agregar la IP a la lista de cortes')
            return False

    except Exception as e:
        print(f"Error al agregar la IP a la lista de cortes: {str(e)}")
        return False

def obtener_lista_de_corte():
    global global_connection
    try:
        if not global_connection:
            # Si no hay conexión, intenta establecerla
            establecer_conexion()

        if global_connection:
            # Obtén la lista de direcciones desde la lista 'no-corte'
            result = global_connection.get_api().get_resource('/ip/firewall/address-list').get(where={'list': MIKROTIK_LIST})
            return result

        else:
            print('No hay conexión para obtener la lista de cortes')
            return None
    except Exception as e:
        print(f"Error al obtener la lista de cortes: {str(e)}")
        return None