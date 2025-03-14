# Abrir el archivo y leer su contenido
archivo = open("Tramas_802-15-4.log")
text = archivo.read() # Leer todo el contenido del archivo

# Eliminar saltos de línea y espacios en blanco al principio y al final
text = text.replace("\n", "") # Eliminar saltos de línea
text = text.replace("\r", "") # Eliminar retorno de carro

# Convertir el texto en una lista de caracteres
textList = list(text)
#print(textList)


def calculaTramas(textList):
    # Iterar sobre los caracteres y buscar las tramas
    tramas = 0 
    if textList[0] == "7" and textList[1] == "E":
        tramas +=1  #si comienza con 7E lo tomamos como el comienzo de una trama

    for i in range(2, len(textList) - 1): # Comenzamos desde el índice 2 para evitar errores de índice
        if (textList[i] == "7" and textList[i+1] == "E" and textList[i-1] != "D" and textList[i-2] != "7"):
            tramas +=1  #Encuentra "7E" y no tiene "D7" antes
    
        if (textList[i] == "7" and textList[i+1] == "E"):
            if textList[i-1] == "D" and textList[i-2] != "7":
                tramas +=1 
            elif textList[i-1] != "D" and textList[i-2] == "7":
                tramas +=1
    return tramas


#Numero total de tramas con longitud correcta e incorrecta
def splitString(cadena):
    cadenaA = cadena[6:] #Elimino los primeros 6 elementos (bandera, longitud)
    cadenaB = cadenaA[:-2] #Elimina el ultimo byte
    return cadenaA + cadenaB #Devolvemos la concatenación de ambas


#Recibe una cadena de bytes en formato hexadecimal y devuelve una lista de bytes en formato decimal (enteros) 
def convierteADec(hex_string):
    # Dividir la cadena en pares de caracteres y convertir cada par a un valor decimal (entero) 
    bytes_hex = [int(hex_string[i:i+2], 16) for i in range(0, len(hex_string), 2)]
    return bytes_hex


#Separa en tramas 
def separaTramas(textList):
    tramas = []
    current = []

    if textList[0] == "7" and textList[1] == "E":
        current.append(textList[0])
        current.append(textList[1])

    for i in range(2, len(textList) - 1): # Comenzamos desde el índice 2 para evitar errores de índice
        if (textList[i] == "7" and textList[i+1] == "E" and textList[i-1] != "D" and textList[i-2] != "7"):
            if current: #Si la lista no está vacía
                tramas.append(current)
                current = []

        if (textList[i] == "7" and textList[i+1] == "E"):
            if textList[i-1] == "D" and textList[i-2] != "7":
                if current:
                    tramas.append(current)
                    current = []
            elif textList[i-1] != "D" and textList[i-2] == "7":
                if current:
                    tramas.append(current)
                    current = []
        current.append(textList[i])
    	
    #Agregar la última trama a la lista de tramas 
    if current:
        tramas.append(current)

    return tramas
    
def eliminaSecuenciaEscape(tramas):
    newTramas = []	
    for trama in tramas:
        i = 0
        while i < len(trama) - 3:  # Aseguramos que haya suficientes elementos para comparar
            if trama[i] == "7" and trama[i+1] == "D" and trama[i+2] == "7" and trama[i+3] == "E":
                del trama[i]  # Elimina "7"
                del trama[i]  # Elimina "D", 
            else:
                i += 1  # Solo avanzamos si no se eliminó nada
        newTramas.append(trama)
    return newTramas

def cuentaTramasSecuenciaEscape(tramas):
    count = 0
    for trama in tramas:
        i = 0
        while i < len(trama) - 3:  # Aseguramos que haya suficientes elementos para comparar
            if trama[i] == "7" and trama[i+1] == "D" and trama[i+2] == "7" and trama[i+3] == "E":
                count += 1
            i += 1
    return count

#Ignorar bandera (1 byte), longitud (2 bytes), check -sum (1 byte)
#Indicar el número de tramas con longitud correcta y con longitud incorrecta.


# Calcula la longitud real de la trama (según los bytes 2 y 3)
def longitud_real(trama):
    """Calcula la longitud esperada de la trama según IEEE 802.15.4."""
    longitud_hex = trama[2:6]  # Tomar bytes 2 y 3
    longitudHexString = "".join(longitud_hex)	
    return int(longitudHexString, 16)  # Convertir a decimal

# Calcula el checksum real de la trama
def calculaCheckSum(trama):
    bytes_trama = [int(trama[i:i+2], 16) for i in range(0, len(trama)-2, 2)] # Excluir el último byte (checksum)
    checksum = (0xFF - (sum(bytes_trama[3:]) & 0xFF)) & 0xFF  # Excluir bandera y longitud
    return checksum

def longitudCalculada(trama): 
    long = trama[6:-2]
    return len(long) // 2

def esLongitudCorrecta(trama):
    longitudReal = longitud_real(trama)
    longitud = longitudCalculada(trama)
    return longitudReal == longitud

def calculaTramasCorrectas(listaTramas):
    tramasCorrectas = 0
    for trama in listaTramas:
        if esLongitudCorrecta(trama):
            tramasCorrectas += 1
    return tramasCorrectas + 1

def calculaTramasIncorrectas(listaTramas):
    return len(listaTramas) - calculaTramasCorrectas(listaTramas)

def esCheckSumCorrecto(trama): 
    checksumReal = calculaCheckSum(trama)
    auxTrama = ''.join(trama)
    checksum = int(auxTrama[-2:], 16)
    return checksumReal == checksum

#Devuelve una lista con las tramas correctas
def tramasYCheckSumCorrectos(listaTramas): 
    correctas = 0 
    for trama in listaTramas:
        tramaAux = ''.join(trama)
        if esLongitudCorrecta(trama) and esCheckSumCorrecto(tramaAux):
            correctas += 1
    return correctas + 1


listaTramas = separaTramas(textList) #Lista de tramas 
tramasConEscape = cuentaTramasSecuenciaEscape(listaTramas) #Lista de tramas sin secuencia de escape
listaTramasS = eliminaSecuenciaEscape(listaTramas) #Lista de tramas sin secuencia de escape

print("Cantidad de tramas: ", calculaTramas(textList)) 
print("Cantidad de tramas correctas: ", calculaTramasCorrectas(listaTramas)) 
print("Cantidad de tramas incorrectas: ", calculaTramasIncorrectas(listaTramas))
print("Cantidad de tramas con longitud correcta y checksum correcto: ", tramasYCheckSumCorrectos(listaTramas))
print("Cantidad de tramas con longitud correcta y checksum incorrecto: ", calculaTramasCorrectas(listaTramas) - tramasYCheckSumCorrectos(listaTramas))
print("Canttidadd de tramas con secuencia de escape: ", tramasConEscape)