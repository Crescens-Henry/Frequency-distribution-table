##! deberemos obtener la tabla de frecuencia
# Libreria para calculos
import numpy as np
import pandas as pd

cant_Num = int(input("cuantos datos desea ingresar? "))
# se insertan en el array
# creamos el array con los espacios necesarios
arr = np.empty(cant_Num, dtype=float)
for i in range(cant_Num):
    valor = float(input("valor numero {}:".format(i+1)))
    arr[i] = valor
print(f"Conjunto de datos NO ordenados:\n {arr}")

# funcion con complejidad -> Θ(n).
arr_sorted = np.sort(arr)
print(f"Conjunto de datos Si ordenados:\n {arr_sorted}")


def resolutions(cant_Num, arr_sorted):
    K = 1 + (3.322 * np.log10(cant_Num))
    K_round = round(K)
    print(f"K = 1 + 3.322 log10({cant_Num}) = {K}")
    print(f"K = {K_round}")
    R = arr_sorted[-1] - arr_sorted[0]
    print(f"R = Xmax - Xmin = {arr_sorted[-1]} - {arr_sorted[0]} = {R}")
    A = R/K_round
    print(f"A = {R}/{K_round} = {A}")
    A_round = round(A+0.1)
    print(f"A = {A_round}")
    #! table
    variabilidad = 1  # !importante dependiendo la lista de datos
    valor_min = arr_sorted[0]
    datos = np.zeros((6, 6))  # ! fila, columna
    df = pd.DataFrame(
        datos, columns=["LimInf", "LimSup", "Frecuencia", "Marca de clase", "LimInfExacta", "LimSupExacta"])

    df.iloc[0, 0] = valor_min
    df.iloc[0, 1] = valor_min+A_round-variabilidad
    for i in range(1, df.shape[0]):
        df.iloc[i, 0] = df.iloc[i-1, 1] + 1  # type: ignore
        df.iloc[i, 1] = df.iloc[i, 0]+A_round-variabilidad
        df.iloc[:, 2] = [np.sum((arr_sorted >= df.iloc[i, 0]) & (  # type: ignore
            arr_sorted <= df.iloc[i, 1])) for i in range(df.shape[0])]
        df.iloc[:, 3] = (df["LimInf"] + df["LimSup"]) / 2
        df.iloc[:, 4] = (df["LimInf"]-(variabilidad/2))
        df.iloc[:, 5] = (df["LimSup"]+(variabilidad/2))
    print(df)


resolutions(cant_Num, arr_sorted)
