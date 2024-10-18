from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from decimal import Decimal
import os

app = Flask(__name__)
app.secret_key = 'secreto'

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        if 'total' in request.form:  # Se está agregando un nuevo sueldo mensual
            total = Decimal(request.form['total'])
            ahorro = total * Decimal(0.2)
            restante = total - ahorro
            semanal = restante / Decimal(4)

            cursor.execute('INSERT INTO sueldo_mensual (total, ahorro, restante, fecha) VALUES (%s, %s, %s, NOW())', 
                            (total, ahorro, restante))
            sueldo_mensual_id = cursor.lastrowid

            # Insertar las 4 semanas con su monto asignado
            for semana in range(1, 5):
                cursor.execute('INSERT INTO semanas (sueldo_mensual_id, semana, monto_asignado, gasto, sobrante) VALUES (%s, %s, %s, %s, %s)', 
                                (sueldo_mensual_id, semana, semanal, Decimal(0), semanal))
            mysql.connection.commit()

        elif 'gasto' in request.form:  # Se está registrando un gasto semanal
            semana_id = int(request.form['semana_id'])
            gasto = Decimal(request.form['gasto'])

            cursor.execute('SELECT monto_asignado, gasto FROM semanas WHERE id = %s', (semana_id,))
            semana = cursor.fetchone()
            if semana:
                nuevo_gasto = Decimal(semana[1]) + gasto
                sobrante = Decimal(semana[0]) - nuevo_gasto

                cursor.execute('UPDATE semanas SET gasto = %s, sobrante = %s WHERE id = %s', 
                                (nuevo_gasto, sobrante, semana_id))

                # Si hay sobrante, se suma al ahorro
                if sobrante > 0:
                    cursor.execute('SELECT sueldo_mensual_id FROM semanas WHERE id = %s', (semana_id,))
                    sueldo_mensual_id = cursor.fetchone()[0]
                    cursor.execute('UPDATE sueldo_mensual SET ahorro = ahorro + %s WHERE id = %s', 
                                    (sobrante, sueldo_mensual_id))

                mysql.connection.commit()

    # Obtener el sueldo mensual más reciente
    cursor.execute('SELECT * FROM sueldo_mensual ORDER BY fecha DESC LIMIT 1')
    sueldo = cursor.fetchone()

    semanas = []
    if sueldo:
        cursor.execute('SELECT * FROM semanas WHERE sueldo_mensual_id = %s', (sueldo[0],))
        semanas = cursor.fetchall()

    # Calcular el ahorro total acumulado
    cursor.execute('SELECT SUM(ahorro) FROM sueldo_mensual')
    total_ahorro = cursor.fetchone()[0] or Decimal(0)

    cursor.close()

    return render_template('index.html', sueldo=sueldo, semanas=semanas, total_ahorro=total_ahorro)

@app.route('/borrar', methods=['POST'])
def borrar_datos():
    cursor = mysql.connection.cursor()
    
    # Eliminar todos los datos de la tabla semanas y sueldo_mensual
    cursor.execute('DELETE FROM semanas')
    cursor.execute('DELETE FROM sueldo_mensual')
    mysql.connection.commit()
    
    cursor.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
