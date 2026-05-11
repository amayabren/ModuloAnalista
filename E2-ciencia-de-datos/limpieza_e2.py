import pandas as pd

# Cargamos el dataset en un dataframe
df = pd.read_csv("Dataset_Trafico_Cordoba.csv", sep=",")

#  Información incial del dataset
print("Primeras filas del dataset:")
print(df.head())

print("\nInformación general del dataset:")
print(df.info())

print("\nCantidad de filas y columnas:")
print(df.shape)

#-------------------------  1. Creamos una copia del dataset original ------------------------- 
df_limpio = df.copy()

#-------------------------  2. Normalizamos nombres de columnas ------------------------- 
# Pasamos nombres de columnas a minúsculas y eliminamos espacios innecesarios
df_limpio.columns = (
    df_limpio.columns
    .str.strip() 
    .str.lower()
    .str.replace(" ", "_")
)
print("\nColumnas normalizadas:")
print(df_limpio.columns)

#-------------------------  3. Verificamos y eliminamos duplicados ------------------------- 
duplicados = df_limpio.duplicated().sum()
print("\nCantidad de filas duplicadas:", duplicados)
df_limpio = df_limpio.drop_duplicates()

#-------------------------  4. Normalizamos las columnas de texto ------------------------- 
columnas_texto = df_limpio.select_dtypes(include="object").columns
# Excluimos fecha porque será tratada aparte
columnas_texto = columnas_texto.drop("fecha")
for columna in columnas_texto:
    df_limpio[columna] = (
        df_limpio[columna]
        .fillna("")        # reemplaza nulos por vacío
        .astype(str)       # convierte a string
        .str.strip()       # elimina espacios
        .str.lower()       # convierte a minúsculas
        .str.title()       # primera letra mayúscula
    )
print("\nNormalización de texto completada.")

#-------------------------  5. Convertimos las columnas numéricas ------------------------- 
# Detectamos automáticamente columnas numéricas
columnas_numericas = df_limpio.select_dtypes(include=["int64", "float64"]).columns

print("Columnas numéricas detectadas:")
print(columnas_numericas)

for columna in columnas_numericas:
    df_limpio[columna] = pd.to_numeric(
        df_limpio[columna],
        errors="coerce"
    )

print("\nConversión de columnas numéricas completada.")

#-------------------------  6 ETL: Corrección de fechas y días de la semana------------------------- 
# Convertimos la columna fecha a datetime
df_limpio['fecha'] = pd.to_datetime(
    df_limpio['fecha'],
    dayfirst=True,
    errors='coerce'
)

# Diccionario para traducir días al español
dias_espanol = {
    'Monday': 'Lunes',
    'Tuesday': 'Martes',
    'Wednesday': 'Miércoles',
    'Thursday': 'Jueves',
    'Friday': 'Viernes',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}

# Recalculamos el día real según la fecha
df_limpio['dia_semana'] = (
    df_limpio['fecha']
    .dt.day_name()
    .map(dias_espanol)
)

print("ETL: Fechas corregidas y días sincronizados.")
print(df_limpio[['fecha', 'dia_semana']].head())

#-------------------------  7. Verificamos valores nulos ------------------------- 
print("\nCantidad de valores nulos por columna:")
print(df_limpio.isnull().sum())


#-------------------------  8. Eliminamos las filas completamente vacías ------------------------- 
# Eliminamos filas completamente vacías
df_limpio = df_limpio.dropna(how="all")


#-------------------------  9. Detectamos inconsistencias ------------------------- 
print("\nResumen estadístico:")
print(df_limpio.describe(include="all"))


#-------------------------  10. Verificación de valores únicos ------------------------- 
print("\nValores únicos de columnas categóricas:")

for columna in columnas_texto:
    print(f"\n{columna}:")
    print(df_limpio[columna].unique())


#-------------------------  11. Detección de posibles outliers -------------------------

print("\nDetección básica de valores extremos:")

for columna in columnas_numericas:
    print(f"\n{columna}")
    print("Mínimo:", df_limpio[columna].min())
    print("Máximo:", df_limpio[columna].max())

#------------------------- 12. DATASET FINAL ------------------------- 
print("\nInformación final del dataset limpio:")
print(df_limpio.info())

print("\nDimensiones finales:")
print(df_limpio.shape)


# EXPORTACIÓN DEL DATASET LIMPIO

df_limpio.to_csv(
    "Dataset_Trafico_Cordoba_Limpio.csv",
    index=False
)

print("\nDataset limpio exportado correctamente.")