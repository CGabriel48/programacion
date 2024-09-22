import network
import socket
from machine import Pin

# Configuración del LED en el pin 2 (puedes cambiar el pin según tu configuración)
led = Pin(2, Pin.OUT)

# Conexión a la red Wi-Fi
ssid = 'NombreDeRed'
password = 'ContraseñaDeRed'


def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        pass

    print('Conexión Wi-Fi establecida')
    print(wlan.ifconfig())  # Muestra la IP asignada por el router


conectar_wifi()


# Página web simple para controlar el LED
def pagina_web(led_state):
    html = """
    <!DOCTYPE html>
    <html>
        <head><title>Control de LED con ESP32</title></head>
        <body>
            <h1>Control de LED</h1>
            <p>LED está {}</p>
            <a href="/?led=on"><button>Encender</button></a>
            <a href="/?led=off"><button>Apagar</button></a>
        </body>
    </html>
    """.format(led_state)
    return html


# Iniciar servidor web
def iniciar_servidor():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))  # El servidor escucha en el puerto 80
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print('Conexión desde:', addr)
        request = conn.recv(1024)
        request = str(request)

        # Control del LED según la petición
        if '/?led=on' in request:
            led.value(1)
            led_state = "ENCENDIDO"
        elif '/?led=off' in request:
            led.value(0)
            led_state = "APAGADO"
        else:
            led_state = "APAGADO" if led.value() == 0 else "ENCENDIDO"

        # Enviar la respuesta de la página web
        response = pagina_web(led_state)
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()


# Iniciar el servidor web
iniciar_servidor()
