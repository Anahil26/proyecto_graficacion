# Importar las bibliotecas necesarias
import pandas as pd                    # Para el manejo de datos
import matplotlib.pyplot as plt        # Para la generación de gráficos
import tkinter as tk                   # Para la creación de la interfaz gráfica
from PIL import Image, ImageTk         # Para trabajar con imágenes

# Crear la interfaz gráfica
root = tk.Tk()                         # Crear una instancia de la clase Tk de tkinter
root.title('gráficos de las ventas')# Establecer el título de la ventana

# Cargar el archivo CSV que contiene los datos de ventas
df = pd.read_csv('time-series.csv')

# Convertir la columna 'Fecha' a tipo datetime
df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d-%m-%Y')

# Extraer el mes y el año de la columna 'Fecha'
df['Mes'] = df['Fecha'].dt.month
df['Año'] = df['Fecha'].dt.year

# Agrupar por mes y año, y sumar las ventas
ventas_por_mes = df.groupby(['Año', 'Mes'])['Ventas'].sum().reset_index()

# Separar los datos por año
ventas_2017 = ventas_por_mes[ventas_por_mes['Año'] == 2017]
ventas_2018 = ventas_por_mes[ventas_por_mes['Año'] == 2018]

# Calcular el promedio de ventas para cada mes
ventas_promedio = ventas_por_mes.groupby('Mes')['Ventas'].mean().reset_index()

# Preparar datos para el gráfico de dispersión
meses = range(1, 13)
ventas_2017_totales = ventas_2017['Ventas']

# Ajustar la longitud de los datos de ventas de 2018 para que coincida con los meses disponibles
ventas_2018_totales = ventas_2018['Ventas']
if len(ventas_2018_totales) < 12:
    ventas_2018_totales = list(ventas_2018_totales) + [0] * (12 - len(ventas_2018_totales))

ventas_promedio_totales = ventas_promedio['Ventas']

# Función para mostrar el primer gráfico
def mostrar_grafico1():
    """
    Esta función genera y muestra un gráfico de dispersión para representar las ventas totales
    y el promedio mensual de ventas para los años 2017 y 2018.
    """
    plt.figure(figsize=(10, 6))    # Crear una nueva figura para el gráfico
    # Graficar el promedio de ventas mensuales
    plt.scatter(meses, ventas_promedio_totales, color='blue', label='Promedio')
    # Graficar las ventas totales de 2017
    plt.scatter(meses, ventas_2017_totales, color='red', label='Ventas 2017')
    # Graficar las ventas totales de 2018
    plt.scatter(meses, ventas_2018_totales, color='green', label='Ventas 2018')
    plt.title('Ventas totales y promedio por mes (2017 vs 2018)')   # Establecer el título del gráfico
    plt.xlabel('Mes')
    plt.ylabel('Ventas totales')
    plt.xticks(meses)
    plt.legend()
    plt.grid(True)
    plt.show()

# Función para mostrar el segundo gráfico
def mostrar_grafico2():
    """
    Esta función genera y muestra un gráfico de barras que representa las ventas diarias
    en los meses de junio y julio para los años 2017 y 2018.
    """
    # Filtrar los datos para los meses de junio y julio de 2017
    junio_julio_2017 = df[(df['Mes'].isin([6, 7])) & (df['Año'] == 2017)]
    # Filtrar los datos para los meses de junio y julio de 2018
    junio_julio_2018 = df[(df['Mes'].isin([6, 7])) & (df['Año'] == 2018)]

    # Agrupar por día y sumar las ventas para 2017
    ventas_junio_julio_2017 = junio_julio_2017.groupby('Fecha')['Ventas'].sum().reset_index()
    # Agrupar por día y sumar las ventas para 2018
    ventas_junio_julio_2018 = junio_julio_2018.groupby('Fecha')['Ventas'].sum().reset_index()

    # Crear un nuevo gráfico de barras
    plt.figure(figsize=(10, 6))
    # Graficar las ventas diarias de junio y julio de 2017
    plt.bar(ventas_junio_julio_2017['Fecha'], ventas_junio_julio_2017['Ventas'], color='blue', alpha=0.7, label='Junio y Julio 2017')
    # Graficar las ventas diarias de junio y julio de 2018
    plt.bar(ventas_junio_julio_2018['Fecha'], ventas_junio_julio_2018['Ventas'], color='orange', alpha=0.7, label='Junio y Julio 2018')
    plt.title('Ventas diarias en junio y julio de ambos años')   # Establecer el título del gráfico
    plt.xlabel('Fecha')
    plt.ylabel('Ventas diarias')
    plt.legend()
    plt.grid(True)
    plt.show()

# Marco para centrar los botones verticalmente
frame = tk.Frame(root, bd=5)        # Crear un marco con un borde de 5 píxeles
frame.place(relx=0.5, rely=0.5, relwidth=0.75, relheight=0.75, anchor='center')  # Ubicar el marco en el centro de la ventana

# Botón para mostrar el primer gráfico
btn_grafico1 = tk.Button(frame, text='Media mensual', font=40, command=mostrar_grafico1)  # Crear un botón
btn_grafico1.pack(side='top', fill='x', padx=10, pady=10) # Empaquetar el botón dentro del marco

# Botón para mostrar el segundo gráfico
btn_grafico2 = tk.Button(frame, text='Ventas diarias', font=40, command=mostrar_grafico2)  # Crear otro botón
btn_grafico2.pack(side='top', fill='x', padx=10, pady=10) # Empaquetar el botón dentro del marco

root.mainloop()                      # Iniciar el bucle principal de la aplicación Tkinter para mostrar la interfaz