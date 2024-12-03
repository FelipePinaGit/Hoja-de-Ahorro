# Administración de Sueldos

Esta aplicación permite administrar un sueldo mensual dividiéndolo en partes semanales, calculando el ahorro y registrando los gastos realizados cada semana. Está construida con **Flask**, utiliza **MySQL** como base de datos, y sigue buenas prácticas como la carga de variables de entorno con **python-dotenv**.


## Funcionalidades

### 1. Registro del Sueldo Mensual
- El usuario ingresa el total de su sueldo mensual.
- El sistema calcula:
  - **Ahorro**: 20% del total.
  - **Monto restante**: Total menos el ahorro.
  - **Asignación semanal**: El restante se divide en 4 partes iguales.
- Los datos se almacenan en las tablas `sueldo_mensual` y `semanas`.

### 2. Registro de Gastos Semanales
- El usuario puede registrar los gastos realizados en una semana específica.
- El sistema actualiza:
  - **Gasto acumulado** para la semana.
  - **Sobrante**, que se recalcula como la diferencia entre el monto asignado y los gastos.
- Si queda sobrante, se suma automáticamente al ahorro total del mes.

### 3. Visualización de Datos
- Muestra el sueldo mensual más reciente, incluyendo:
  - Total ingresado, ahorro, y restante.
  - Información detallada de cada semana: monto asignado, gasto y sobrante.
- Calcula y muestra el **ahorro total acumulado** de todos los meses.

### 4. Eliminación de Datos
- Permite borrar todos los registros de sueldos y semanas, restableciendo el sistema.


