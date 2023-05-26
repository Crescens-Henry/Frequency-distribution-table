import math
from decimal import Decimal
import numpy

# Credito por estruturamiento inicial principal del funcionamiento
#   * https://github.com/GJZ26


# Funciones de ordamiento de datos (Sólo numéricos) - Estables
# Crédito: https://github.com/LWH-21

# Funciones de ordenamiento (Sólo numérico) - Inestable
# Crédito: https://github.com/LWH-21

# Funciones de normalización de tipo de variables


def listToDecimal(data: list):
    for i in range(0, len(data)):
        data[i] = Decimal(str(data[i]))
    return data


# Funciones para cálculo de Distribuciones de Frecuencias :)

letterForNames = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def klassesNumber(data: list):
    return round(1 + 3.322 * math.log10(len(data)))


def dataRange(sortedData: list, isSorted: bool = True):
    if isSorted:
        return sortedData[len(sortedData) - 1] - sortedData[0]
    else:
        tempList = numpy.sort(sortedData)
        return tempList[len(tempList) - 1] - tempList[0]


def dataAmplitudeByList(data: list, isSorted: bool = True):
    range = dataRange(data, isSorted)
    classesNumber = klassesNumber(data)
    uv = variationUnit(data)
    if variationUnit(data) == 1:
        if "." in str(range / classesNumber):
            return Decimal(str(math.ceil(Decimal(str(range / classesNumber)))))
        else:
            return Decimal(str(math.ceil(Decimal(str(range / classesNumber))))) + 1

    return Decimal(str((math.ceil(Decimal(str(range / classesNumber)) / uv) * uv)))


def dataAmplitudeByVariables(range: int, classesNumber: int):
    if (math.ceil(range / classesNumber)) is int:
        return math.ceil(range / classesNumber) + 1
    else:
        return math.ceil(range / classesNumber)


def variationUnit(data: list):
    maxDecimalNumber = 0
    for i in data:
        if "." in str(i):
            maxDecimalNumber = (
                len(str(i).split(".")[1])
                if len(str(i).split(".")[1]) > maxDecimalNumber
                else maxDecimalNumber
            )

    return Decimal(str(math.pow(10, -(maxDecimalNumber))))


def calculateFrecuencyByDataList(
    sortedData: list,
    classesNumber: int,
    amplitude: Decimal,
    variationUnit: Decimal,
):
    result = []
    limInf = sortedData[0]
    totalData = len(sortedData)
    cumulative_freq = 0
    cumulative_freq_list = []

    for i in range(0, classesNumber):
        limSup = limInf + amplitude - variationUnit
        freq_abs = frecuencyInRange(
            sortedData, limInf, limSup
        )  # Obtener la frecuencia absoluta
        freq_complementaria = (
            totalData - freq_abs
        )  # Calcular la frecuencia complementaria
        cumulative_freq += freq_abs
        cumulative_freq_list.append(cumulative_freq)
        result.append(
            [
                letterForNames[i],  # Clase
                limInf,  # Límite Inferior
                limInf - (variationUnit / 2),  # Limite Inferior Exacto
                limSup,  # Límite Superior
                limSup + (variationUnit / 2),  # Límite Superior Exacto
                frecuencyInRange(sortedData, limInf, limSup),  # Frecuencia
                (limSup + limInf) / 2,  # Marca de la clase,
                (freq_abs * 100),
                cumulative_freq,
                freq_abs,
                freq_complementaria,
            ]
        )
        limInf = limSup + variationUnit

    return result


def frecuencyInRange(data: list, limInf: Decimal, limSup: Decimal):
    frecuency = 0
    for i in data:
        if i <= limSup and i >= limInf:
            frecuency += 1
    return frecuency


def arithmetic_average(data: list, limInf: Decimal, limSup: Decimal):
    total = sum(data)
    result_arithmetic_average = 0
    if len(data) > 0:
        result_arithmetic_average = total / len(data)
    return result_arithmetic_average


def median(data: list):
    return numpy.median(data)


def statistical_mode(data: list):
    # Obtener los valores únicos y sus conteos utilizando numpy.unique()
    valores, conteos = numpy.unique(data, return_counts=True)

    # Encontrar el índice del valor con el conteo máximo
    indice_maximo = numpy.argmax(conteos)

    # Obtener la moda a partir del índice encontrado
    moda = valores[indice_maximo]
    return moda
