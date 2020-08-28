from tkinter import *
import os
class Validacion:
    alfabeto = "abcdefghijklmnñopqrstuvwxyz0123456789"
    numeros = "0123456789"
    letras = "abcdefghijklmnñopqrstuvwxyz"
    NuL = "abcdefghijklmnñopqrstuvwxyz0123456789"
    operadores = "+-/^*"
    parentesis = "()"
    alfabeto_completo = "abcdefghijklmnñopqrstuvwxyz0123456789()+-/^*.;:= "
    
    def validarLexico (cadena):
        #Se usará para el nombre del programa y el identificador de las variables
        caracteresInvalidos = "\0"
        for char in cadena:
            if char not in Validacion.alfabeto:
                if caracteresInvalidos == "\0":
                    caracteresInvalidos = ""
                caracteresInvalidos += char
        return caracteresInvalidos

    def validarAlfabeto (cadena):
        caracteresInvalidos = "\0"
        for char in cadena:
            if char not in Validacion.alfabeto_completo:
                if caracteresInvalidos == "\0":
                    caracteresInvalidos = ""
                caracteresInvalidos += char
        return caracteresInvalidos

    def validarPrograma (nombre):
        try:
            fichero = open (nombre,'r')
            variables = {}
            programa = []
            for line in fichero:
                programa.append(line.strip('\n'))
            largo = len(programa)

            for i in range (len(programa)):
                #print (str(i) + ".- " + programa[i])
                if (".." in programa[i] or ". ." in programa[i]):
                    return "Error de sintaxis. No se permite el punto doble. En linea: " + str(i+1)
                validacion_alfabeto = Validacion.validarAlfabeto(programa[i])
                if (validacion_alfabeto != "\0"):
                    return "Error de lexico. Los siguientes caracteres no son validos: " + validacion_alfabeto + ". En linea: " + str(i+1)
                if ("  " in programa[i]):
                    return "Error de sintaxis. No valido doble espacio" + ". En linea: " + str(i+1)
                if (i == 0):
                    #Validar que diga programa, validar el nombre del programa y ;
                    palabra_programa = programa[i][:len("programa ")]
                    if ( programa[i][len(programa[i])-1] != ";" ):

                        return ("Error de sintaxis. Se esperaba \";\" al final" + ". En linea: " + str(i+1))
                    
                    if (palabra_programa != "programa "):

                        return ("Error de sintaxis. No se encontró palabra programa" + ". En linea: " + str(i+1))
                    
                    nombre_programa = programa[i][len("programa "):len(programa[i]) - 1]
                    if (nombre_programa[0] not in Validacion.letras):

                        return ("Error de lexico. El nombre del programa debe iniciar con una letra minúscula" + ". En linea: " + str(i+1))
                    
                    respuesta_validacion = Validacion.validarLexico(nombre_programa)
                    if (respuesta_validacion != "\0"):
                        respuesta = "Error de lexico. Se encontraron los siguientes caracteres inválidos en el nombre del programa: " + respuesta_validacion + ". En linea: " + str(i+1)
                        #print (respuesta_validacion)
                        for letra in respuesta_validacion:
                            respuesta += letra
                            respuesta += ' '
                        return respuesta
                elif (i == 1):
                    #Validar que diga iniciar solamente
                    if (programa[i] != "iniciar"):
                        return "Error de sintaxis. Instrucción inicial inválida \"iniciar\"" + ". En linea: " + str(i+1)
                elif (i > 1 and i< len(programa) -1 ):
                    #######################################################################################
                    #Validar las instrucciones (lo mas pesado)
                    if ( programa[i][len(programa[i])-1] != ";" ):

                        return ("Error de sintaxis. Se esperaba \";\". En línea " + str (i+1))
                    
                    # Si la instrucción es una instrucción de leer
                    if (programa[i][:len("leer ")] == "leer "):
                        identificador = programa[i][len("leer "):len(programa[i])-1]
                        if (identificador[0] not in Validacion.letras):

                            return ("Error de sintaxis. El nombre de las variables debe iniciar con una letra minúscula" + ". En linea: " + str(i+1))
                        
                        respuesta_validacion = Validacion.validarLexico(identificador)
                        if (respuesta_validacion != '\0'):

                            respuesta = "Error de sintaxis. Se encontraron los siguientes caracteres inválidos en el nombre de la variable. En línea: " + str(i+1)
                        
                        variables[identificador] = 0
                    
                    elif(programa[i][:len("imprimir ")] == "imprimir "):
                        impresion = programa[i][len("imprimir "):len(programa[i])-1]
                        if (impresion not in variables.keys()):
                            return ("Error de sintaxis. Variable " + impresion + " no ha sido declarada, no se puede imprimir. Error en línea: " + str(i+1))
                        

                    else:
                        instruccion = programa[i]
                        identificadores = []
                        identificador = ""
                        pos = 0
                        for ij in range(len(instruccion)):
                            if (instruccion[ij] != ':'):
                                identificador += instruccion[ij]
                            if (instruccion[ij] == ':'):
                                pos = ij
                                break
                            if (instruccion[ij] == ';'):
                                return ("Error de sintaxis. No se reconoce la instrucción " + instruccion + ". En línea: " + str(i+1) )
                            if (instruccion[ij] == '='):
                                return ("Error de sintaxis. Se espera : antes del igual"  + ". En línea " + str(i+1))
                            if (ij>0):
                                if (instruccion[ij] == ' ' and instruccion[ij-1] == ' '):
                                    return ("Error de lexico. No se permiten dobles espacios, error de sintaxis" + ". En linea: " + str(i+1))
                            
                        exprecion_tmp = instruccion[pos:]
                        exprecion = ""
                        if (identificador[len(identificador)-1] == " "):
                            identificador = identificador[:len(identificador)-1]
                        #print (identificador + ".\n" + exprecion_tmp)
                        if (identificador[0] not in Validacion.letras):

                            return ("Error de sintaxis. El nombre de las variables debe iniciar con una letra" + ". En linea: " + str(i+1))
                        
                        respuesta_validacion = Validacion.validarLexico(identificador)
                        if (respuesta_validacion != '\0'):

                            respuesta = "Error de lexico. Se encontraron los siguientes caracteres inválidos en el nombre de la variable. En línea: " + str(i+1)
                        if (exprecion_tmp[1] == "="):
                            if (exprecion_tmp[2] == " "):
                                exprecion = exprecion_tmp[3:len(exprecion_tmp)-1]
                            else:
                                exprecion = exprecion_tmp[2:len(exprecion_tmp)-1]
                        #print (exprecion)
                        pi = 0;
                        pd = 0;
                        cont = 0;
                        identificador_tmp = ""
                        ##########
                        for ij in range(len(exprecion)):
                            #print (str(ij) + ".- " + exprecion[ij])
                            if (exprecion[ij] == ")"):
                                pd += 1
                            if (exprecion[ij] == "("):
                                pi += 1
                            if (ij < len(exprecion)-1):
                                if ((exprecion[ij] != "(" or exprecion[ij+1] != "-" ) and (exprecion[ij] not in Validacion.operadores or exprecion[ij+1] != "-")):
                                    if (exprecion[ij] == " " and exprecion[ij+1] == " "):
                                        return ("Error de lexico. No válido doble espacio" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] == "." and exprecion[ij+1] == " "):
                                        return ("Error de sintaxis, uso inválido de punto decimal" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] == " " and exprecion[ij+1] == "."):
                                        return ("Error de sintaxis, uso inválido de punto decimal" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] == "." and exprecion[ij+1] in Validacion.letras):
                                        return ("Error de sintaxis, uso inválido de punto decimal" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] in Validacion.letras and exprecion[ij+1] == "."):
                                        return ("Error de sintaxis, uso inválido de punto decimal" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] == "/" and exprecion[ij+1] == "0"):
                                        return ("Error matemático, división entre 0" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] in Validacion.operadores and exprecion[ij+1] in Validacion.operadores):
                                        return ("Error de sintaxis, se espera expresión matemática entre operadores" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] == ")" and exprecion[ij+1] in Validacion.NuL):
                                        return ("Error de sintaxis, se espera operador entre ) y " + exprecion[ij+1] + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] in Validacion.NuL and exprecion[ij+1] == "("):
                                        return ("Error de sintaxis, se espera operador entre " + exprecion[ij] + " y (" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] == "(" and exprecion[ij+1] == ")"):
                                        return ("Error de sintaxis, se espera expresión matemática entre ( y )" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] == ")" and exprecion[ij+1] == "("):
                                        return ("Error de sintaxis, se espera operador o expresión matemática entre ) y (" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] == "(" and exprecion[ij+1] in Validacion.operadores ):
                                        return ("Error de sintaxis, operación incompleta" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] in Validacion.operadores and exprecion[ij+1] == ")" ):
                                        return ("Error de sintaxis, operación incompleta" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] in Validacion.operadores and exprecion[ij+1] == "(" and exprecion[ij] != "-"):
                                        return ("Error de sintaxis, operación incompleta" + ". En linea: " + str(i+1))
                            if (ij < len(exprecion)-2):
                                if ((exprecion[ij] not in Validacion.operadores or exprecion[ij+1] != " " or exprecion[ij+2] != "-") and (exprecion[ij] != "(" or exprecion[ij+1] != " " or exprecion[ij+2] != "-")):
                                    if (exprecion[ij] == " " and exprecion[ij+1] in Validacion.numeros and exprecion[ij+2] in Validacion.letras):
                                        return ("Error de léxico, un identificador debe empezar con una letra" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] in Validacion.operadores and exprecion[ij+1] in Validacion.numeros and exprecion[ij+2] in Validacion.letras):
                                        return ("Error de léxico, un identificador debe empezar con una letra" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] in Validacion.parentesis and exprecion[ij+1] in Validacion.numeros and exprecion[ij+2] in Validacion.letras):
                                        return ("Error de léxico, un identificador debe empezar con una letra" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] in Validacion.operadores and exprecion[ij+1] == " " and exprecion[ij+2] in Validacion.operadores):
                                        return ("Error de sintaxis, se espera expresión matemática entre operadores" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] in Validacion.NuL and exprecion[ij+1] == " " and exprecion[ij+2] in Validacion.NuL):
                                        return ("Error de sintaxis, entre constantes o variables se espera un operador" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] == ")" and exprecion[ij+1] == " " and exprecion[ij+2] in Validacion.NuL):
                                        return ("Error de sintaxis, se espera operador entre ) y " + exprecion[ij+2] + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] in Validacion.NuL and exprecion[ij+1] == " " and exprecion[ij+2] == "("):
                                        return ("Error de sintaxis, se espera operador entre " + exprecion[ij] + " y (" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] == "(" and exprecion[ij+1] == " " and exprecion[ij+2] == ")"):
                                        return ("Error de sintaxis, se espera expresión matemática entre ( y )" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] == ")" and exprecion[ij+1] == " " and exprecion[ij+2] == "("):
                                        return ("Error de sintaxis, se espera operador o expresión matemática entre ) y (" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] == "(" and exprecion[ij+1] == " " and exprecion[ij+2] in Validacion.operadores ):
                                        return ("Error de sintaxis, operación incompleta" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] in Validacion.operadores and exprecion[ij+1] == " " and exprecion[ij+2] == ")" ):
                                        return ("Error de sintaxis, operación incompleta" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] in Validacion.operadores and exprecion[ij+1] == " " and exprecion[ij+2] == "(" and exprecion[ij] != "-" ):
                                        return ("Error de sintaxis, operación incompleta" + ". En linea: " + str(i+1))
                            if (ij == len(exprecion)-1 and exprecion[ij] in Validacion.operadores):
                                return ("Error de sintaxis, operación incompleta" + ". En linea: " + str(i+1))
                            elif (ij == len(exprecion)-2 and exprecion[ij] in Validacion.operadores and exprecion[ij+1] == " "):
                                return ("Error de sintaxis, operación incompleta" + ". En linea: " + str(i+1))
                            if (i == 0):
                                if ( exprecion[ij] in Validacion.numeros and exprecion[ij+1] in Validacion.letras):
                                    return ("Error de léxico, un identificador debe empezar con una letra" + ". En linea: " + str(i+1))
                            if (ij == len(exprecion) - 1):
                                """if (exprecion[i] in letras):
                                    identificador_tmp += exprecion[i]
                                    identificadores.append(identificador_tmp)
                                    identificador_tmp = """""
                                if (identificador_tmp != ""):
                                    identificador_tmp += exprecion[ij]
                                    identificadores.append(identificador_tmp)
                                    identificador_tmp = ""
                            if (exprecion[ij] in Validacion.letras):
                                identificador_tmp += exprecion[ij]                            
                            if ((exprecion[ij] in Validacion.operadores or exprecion[ij] == " ") and identificador_tmp != ""):
                                identificadores.append(identificador_tmp)
                                identificador_tmp = ""
                            if (exprecion[ij] in Validacion.numeros and identificador_tmp != ""):
                                identificador_tmp += exprecion[ij]
                            cont += 1
                        if (pi != pd and cont == len(exprecion)):
                            return("Error de sintaxis, se espera un \")\" o \"(\" " + ". En linea: " + str(i+1))
                        #print (identificadores , variables.keys())
                        for variable in identificadores:
                            if (variable not in variables.keys()):
                                return ("Error de sintaxis. La variable " + variable + " no está inicializada" + ". En linea: " + str(i+1))
                        variables[identificador] = 0

                            ##########
                        ######################################################################################
                elif (i == len(programa) - 1):
                    #Validar que solanmente esté terminar
                    if (programa[i] != "terminar"):
                        return "Error de sintaxis. No se encontró instrucción final \"terminar\"" + ". En linea: " + str(i+1)
            #print(variables)
            return ("Texto Válido. No hubo errores.")
        
        except IOError:
            return("Texto no encontrado. Favor de verificar el nombre y que se encuentre en el directorio correspondiente")
        
    def ejecutarPrograma (cadena):
        print ("Ejecutando "+cadena+" ...")
        #a = input(".-")
        #print (a)
        nombre = cadena
        try:
            fichero = open (nombre,'r')
            variables = {}
            programa = []
            for line in fichero:
                programa.append(line.strip('\n'))
            largo = len(programa)

            for i in range (len(programa)):
                #print (str(i) + ".- " + programa[i])
                validacion_alfabeto = Validacion.validarAlfabeto(programa[i])
                if (validacion_alfabeto != "\0"):
                    return "Error de lexico. Los siguientes caracteres no son validos: " + validacion_alfabeto + ". En linea: " + str(i+1)
                if ("  " in programa[i]):
                    return "Error de sintaxis. No valido doble espacio" + ". En linea: " + str(i+1)
                if (i == 0):
                    #Validar que diga programa, validar el nombre del programa y ;
                    palabra_programa = programa[i][:len("programa ")]
                    if ( programa[i][len(programa[i])-1] != ";" ):

                        return ("Error de sintaxis. Se esperaba \";\" al final" + ". En linea: " + str(i+1))
                    
                    if (palabra_programa != "programa "):

                        return ("Error de sintaxis. No se encontró palabra programa" + ". En linea: " + str(i+1))
                    
                    nombre_programa = programa[i][len("programa "):len(programa[i]) - 1]
                    if (nombre_programa[0] not in Validacion.letras):

                        return ("Error de sintaxis. El nombre del programa debe iniciar con una letra minúscula" + ". En linea: " + str(i+1))
                    
                    respuesta_validacion = Validacion.validarLexico(nombre_programa)
                    if (respuesta_validacion != "\0"):
                        respuesta = "Error de lexico. Se encontraron los siguientes caracteres inválidos en el nombre del programa: " + respuesta_validacion + ". En linea: " + str(i+1)
                        #print (respuesta_validacion)
                        for letra in respuesta_validacion:
                            respuesta += letra
                            respuesta += ' '
                        return respuesta
                elif (i == 1):
                    #Validar que diga iniciar solamente
                    if (programa[i] != "iniciar"):
                        return "Error de sintaxis. Instrucción inicial inválida \"iniciar\"" + ". En linea: " + str(i+1)
                elif (i > 1 and i< len(programa) -1 ):
                    #######################################################################################
                    #Validar las instrucciones (lo mas pesado)
                    if ( programa[i][len(programa[i])-1] != ";" ):

                        return ("Error de sintaxis. Se esperaba \";\". En línea " + str (i+1))
                    
                    # Si la instrucción es una instrucción de leer
                    if (programa[i][:len("leer ")] == "leer "):
                        identificador = programa[i][len("leer "):len(programa[i])-1]
                        if (identificador[0] not in Validacion.letras):

                            return ("Error de sintaxis. El nombre de las variables debe iniciar con una letra minúscula" + ". En linea: " + str(i+1))
                        
                        respuesta_validacion = Validacion.validarLexico(identificador)
                        if (respuesta_validacion != '\0'):

                            respuesta = "Error de sintaxis. Se encontraron los siguientes caracteres inválidos en el nombre de la variable. En línea: " + str(i+1)
                        
                        
                        variables[identificador] = input ("Introdusca variable "+identificador+":")
                        if (not Validacion.validarNumero(variables[identificador]) or len(variables[identificador])==0):
                            return "Error en entrada. Solo se aceptan valores numéricos. En linea: " + str(i+1)
                        #print ("identificador = ." + variables[identificador]+".")
                    
                    
                    elif(programa[i][:len("imprimir ")] == "imprimir "):
                        impresion = programa[i][len("imprimir "):len(programa[i])-1]
                        if (impresion not in variables.keys()):
                            return ("Error de sintaxis. Variable " + impresion + " no ha sido declarada, no se puede imprimir. Error en línea: " + str(i+1))
                        else:
                            print (variables[impresion])
                        

                    else:
                        instruccion = programa[i]
                        identificadores = []
                        identificador = ""
                        pos = 0
                        for ij in range(len(instruccion)):
                            if (instruccion[ij] != ':'):
                                identificador += instruccion[ij]
                            if (instruccion[ij] == ':'):
                                pos = ij
                                break
                            if (instruccion[ij] == ';'):
                                return ("Error de sintaxis. No se reconoce la instrucción " + instruccion + ". En línea: " + str(i+1) )
                            if (instruccion[ij] == '='):
                                return ("Error de sintaxis. Se espera : antes del igual"  + ". En línea " + str(i+1))
                            if (ij>0):
                                if (instruccion[ij] == ' ' and instruccion[ij-1] == ' '):
                                    return ("Error de lexico. No se permiten dobles espacios, error de sintaxis" + ". En linea: " + str(i+1))
                            
                        exprecion_tmp = instruccion[pos:]
                        exprecion = ""
                        if (identificador[len(identificador)-1] == " "):
                            identificador = identificador[:len(identificador)-1]
                        #print (identificador + ".\n" + exprecion_tmp)
                        if (identificador[0] not in Validacion.letras):

                            return ("Error de sintaxis. El nombre de las variables debe iniciar con una letra" + ". En linea: " + str(i+1))
                        
                        respuesta_validacion = Validacion.validarLexico(identificador)
                        if (respuesta_validacion != '\0'):

                            respuesta = "Error de lexico. Se encontraron los siguientes caracteres inválidos en el nombre de la variable. En línea: " + str(i+1)
                        if (exprecion_tmp[1] == "="):
                            if (exprecion_tmp[2] == " "):
                                exprecion = exprecion_tmp[3:len(exprecion_tmp)-1]
                            else:
                                exprecion = exprecion_tmp[2:len(exprecion_tmp)-1]
                        #print (exprecion)
                        pi = 0;
                        pd = 0;
                        cont = 0;
                        identificador_tmp = ""
                        ##########
                        #print ("."+exprecion+".")
                        for ij in range(len(exprecion)):
                            #print (str(ij) + ".- " + exprecion[ij])
                            if (exprecion[ij] == ")"):
                                pd += 1
                            if (exprecion[ij] == "("):
                                pi += 1
                            if (ij < len(exprecion)-1):
                                if ((exprecion[ij] != "(" or exprecion[ij+1] != "-" ) and (exprecion[ij] not in Validacion.operadores or exprecion[ij+1] != "-")):
                                    if (exprecion[ij] == " " and exprecion[ij+1] == " "):
                                        return ("Error de lexico. No válido doble espacio" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] == "." and exprecion[ij+1] == " "):
                                        return ("Error de sintaxis, uso inválido de punto decimal" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] == " " and exprecion[ij+1] == "."):
                                        return ("Error de sintaxis, uso inválido de punto decimal" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] == "." and exprecion[ij+1] in Validacion.letras):
                                        return ("Error de sintaxis, uso inválido de punto decimal" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] in Validacion.letras and exprecion[ij+1] == "."):
                                        return ("Error de sintaxis, uso inválido de punto decimal" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] == "/" and exprecion[ij+1] == "0"):
                                        return ("Error matemático, división entre 0" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] in Validacion.operadores and exprecion[ij+1] in Validacion.operadores):
                                        return ("Error de sintaxis, se espera expresión matemática entre operadores" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] == ")" and exprecion[ij+1] in Validacion.NuL):
                                        return ("Error de sintaxis, se espera operador entre ) y " + exprecion[ij+1] + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] in Validacion.NuL and exprecion[ij+1] == "("):
                                        return ("Error de sintaxis, se espera operador entre " + exprecion[ij] + " y (" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] == "(" and exprecion[ij+1] == ")"):
                                        return ("Error de sintaxis, se espera expresión matemática entre ( y )" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] == ")" and exprecion[ij+1] == "("):
                                        return ("Error de sintaxis, se espera operador o expresión matemática entre ) y (" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] == "(" and exprecion[ij+1] in Validacion.operadores ):
                                        return ("Error de sintaxis, operación incompleta" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] in Validacion.operadores and exprecion[ij+1] == ")" ):
                                        return ("Error de sintaxis, operación incompleta" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] in Validacion.operadores and exprecion[ij+1] == "(" and exprecion[ij] != "-"):
                                        return ("Error de sintaxis, operación incompleta" + ". En linea: " + str(i+1))
                            if (ij < len(exprecion)-2):
                                if ((exprecion[ij] not in Validacion.operadores or exprecion[ij+1] != " " or exprecion[ij+2] != "-") and (exprecion[ij] != "(" or exprecion[ij+1] != " " or exprecion[ij+2] != "-")):
                                    if (exprecion[ij] == " " and exprecion[ij+1] in Validacion.numeros and exprecion[ij+2] in Validacion.letras):
                                        return ("Error de léxico, un identificador debe empezar con una letra" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] in Validacion.operadores and exprecion[ij+1] in Validacion.numeros and exprecion[ij+2] in Validacion.letras):
                                        return ("Error de léxico, un identificador debe empezar con una letra" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] in Validacion.parentesis and exprecion[ij+1] in Validacion.numeros and exprecion[ij+2] in Validacion.letras):
                                        return ("Error de léxico, un identificador debe empezar con una letra" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] in Validacion.operadores and exprecion[ij+1] == " " and exprecion[ij+2] in Validacion.operadores):
                                        return ("Error de sintaxis, se espera expresión matemática entre operadores" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] in Validacion.NuL and exprecion[ij+1] == " " and exprecion[ij+2] in Validacion.NuL):
                                        return ("Error de sintaxis, entre constantes o variables se espera un operador" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] == ")" and exprecion[ij+1] == " " and exprecion[ij+2] in Validacion.NuL):
                                        return ("Error de sintaxis, se espera operador entre ) y " + exprecion[ij+2] + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] in Validacion.NuL and exprecion[ij+1] == " " and exprecion[ij+2] == "("):
                                        return ("Error de sintaxis, se espera operador entre " + exprecion[ij] + " y (" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] == "(" and exprecion[ij+1] == " " and exprecion[ij+2] == ")"):
                                        return ("Error de sintaxis, se espera expresión matemática entre ( y )" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] == ")" and exprecion[ij+1] == " " and exprecion[ij+2] == "("):
                                        return ("Error de sintaxis, se espera operador o expresión matemática entre ) y (" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] == "(" and exprecion[ij+1] == " " and exprecion[ij+2] in Validacion.operadores ):
                                        return ("Error de sintaxis, operación incompleta" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] in Validacion.operadores and exprecion[ij+1] == " " and exprecion[ij+2] == ")" ):
                                        return ("Error de sintaxis, operación incompleta" + ". En linea: " + str(i+1))
                                    elif (exprecion[ij] in Validacion.operadores and exprecion[ij+1] == " " and exprecion[ij+2] == "(" and exprecion[ij] != "-" ):
                                        return ("Error de sintaxis, operación incompleta" + ". En linea: " + str(i+1))
                            if (ij == len(exprecion)-1 and exprecion[ij] in Validacion.operadores):
                                return ("Error de sintaxis, operación incompleta" + ". En linea: " + str(i+1))
                            elif (ij == len(exprecion)-2 and exprecion[ij] in Validacion.operadores and exprecion[ij+1] == " "):
                                return ("Error de sintaxis, operación incompleta" + ". En linea: " + str(i+1))
                            if (i == 0):
                                if ( exprecion[ij] in Validacion.numeros and exprecion[ij+1] in Validacion.letras):
                                    return ("Error de léxico, un identificador debe empezar con una letra" + ". En linea: " + str(i+1))
                            if (ij == len(exprecion) - 1):
                                """if (exprecion[i] in letras):
                                    identificador_tmp += exprecion[i]
                                    identificadores.append(identificador_tmp)
                                    identificador_tmp = """""
                                if (identificador_tmp != ""):
                                    identificador_tmp += exprecion[ij]
                                    identificadores.append(identificador_tmp)
                                    identificador_tmp = ""
                            if (exprecion[ij] in Validacion.letras):
                                identificador_tmp += exprecion[ij]                            
                            if ((exprecion[ij] in Validacion.operadores or exprecion[ij] == " ") and identificador_tmp != ""):
                                identificadores.append(identificador_tmp)
                                identificador_tmp = ""
                            if (exprecion[ij] in Validacion.numeros and identificador_tmp != ""):
                                identificador_tmp += exprecion[ij]
                            cont += 1
                        if (pi != pd and cont == len(exprecion)):
                            return("Error de sintaxis, se espera un \")\" o \"(\" " + ". En linea: " + str(i+1))
                        #print (identificadores , variables.keys())
                        for variable in identificadores:
                            if (variable not in variables.keys()):
                                return ("Error de sintaxis. La variable " + variable + " no está inicializada" + ". En linea: " + str(i+1))
                        #print (identificadores,variables)
                        keystmp = variables.keys()
                        keys1 = []
                        for jk in keystmp:
                            keys1.append(jk)
                        
                        keys1.sort(key=len, reverse=True)
                        for ik in keys1:
                            exprecion = exprecion.replace(ik,str(variables[ik]))
                        #print (exprecion)
                        exprecion = exprecion.replace("^","**")
                        #print (exprecion)
                        try:
                            evaluado = eval(exprecion)
                        except ZeroDivisionError:
                            return "Error matemático. Divicion entre cero. En linea: " + str(i+1)
                        else:
                            print (exprecion)
                            variables[identificador] = eval(exprecion)
                            print (identificador + " = " + str(variables[identificador]))

                            ##########
                        ######################################################################################
                elif (i == len(programa) - 1):
                    #Validar que solanmente esté terminar
                    if (programa[i] != "terminar"):
                        return "Error de sintaxis. No se encontró instrucción final \"terminar\"" + ". En linea: " + str(i+1)
            #print(variables)
            return ("Programa ejecutado con exito")
        
        except IOError:
            return("Texto no encontrado. Favor de verificar el nombre y que se encuentre en el directorio correspondiente")


    def validarNumero(cadena):
        for k in range(len(cadena)):
            if (cadena[k] not in Validacion.numeros and cadena[k] != "."):
                if (cadena[k] != "-" or k!=0):
                    return False
        return True    
            

Validacion.ejecutarPrograma = staticmethod(Validacion.ejecutarPrograma)
Validacion.validarPrograma = staticmethod(Validacion.validarPrograma)
Validacion.validarLexico = staticmethod(Validacion.validarLexico)
Validacion.validarNumero = staticmethod(Validacion.validarNumero)

def funcion_archivo():
    os.system("cls")
    nombre=enter.get()
    a = Validacion.validarPrograma(nombre+".txt")
    print (a)
    if (a == "Texto Válido. No hubo errores."):
        impresion_tk["text"]=("\n\n"+a+"\n El programa se ejecutara en la ventana de comando")
        b=Validacion.ejecutarPrograma(nombre+".txt")
        print (b)
        print ("Volver a la ventana principal y analizar otro archivo")
    else:
        impresion_tk["text"]=("\n\nTexto Invalido. "+a)


"""variables = {"var":2,"a":3,"suma":4,"dos":5,"b":6}

string = "var+a+b+suma"
keystmp = variables.keys()
keys = []
for j in keystmp:
    keys.append(j)

keys.sort(key=len, reverse =True)

for i in keys:
    string = string.replace(i,str(variables[i]))
print (eval(string))"""

#VENTANA
color='#dce3f7'
ventana=Tk()
ventana.geometry("1200x900")
ventana['background']=color
#titulo
main_title=Label(text="Producto Integrador de Aprendizaje", font=("MS Sans Serif", 20,"normal"), justify="center")
main_title.pack(padx=10,pady=10)
main_title['background']=color
title=Label(text="Teoría de Autómatas", font=("MS Sans Serif", 18,"normal"), justify="center")
title.pack(padx=10,pady=1)
title['background']=color
#descripcion
instrucciones=Label(text="Este programa es un analizador de lenguaje, que toma como entrada un archivo de texto, que es analizado en su léxico y sintaxis. \nNo se aceptan strings en las entradas, en la salidas, ni en la definición de las variables.\nDebe cumplir con los siguientes requerimientos para que sea válido: \n(Favor de asegurarse que el archivo de texto se encuentre en la misma carpeta que el archivo ejectuable)\nIntrodusca el nombre del archivo sin la extencion", font=("Verdana", 12,"normal"), justify="center")
instrucciones.pack(padx=10,pady=15)
instrucciones['background']=color
instrucciones2=Label(text="1 - El nombre de programa estará compuesto sólo con una letra del abecedario, seguida de 0 o más letras y/o dígitos del 0 al 9.\n\n2 - El listado de instrucciones puede constar de una sola o de varias separadas por un símbolo de “;”\n\n3 - El identificador deberá iniciar con una letra seguido de (0 o más) letras y/o dígitos.\n\n4 - Las expresiones aritméticas serán las siguientes: suma, multiplicación, resta, división y potencia. Serán válidos los paréntesis.\n\n5 - Las letras sólo serán minúsculas.\n\n6 - El resultado del analizador deberá decir si hubo error en el léxico o en la sintaxis de acuerdo a lo analizado. En caso de no tener error, deberá decir que no hubo errores.", font=("Verdana", 10,"normal"), justify="center")
instrucciones2.pack(padx=15,pady=15)
instrucciones2['background']=color


#nombre archivo
enter=Entry(ventana, font=("Verdana",25,"normal"), justify="center" )
enter.pack(padx=10,pady=10)


#boton
obtain_data=Button(ventana,text="Analizar texto",font=("Verdana", 15,"normal"), justify="center",command=lambda: funcion_archivo())
obtain_data.place(x=5, y=5) 
obtain_data.pack(padx=0,pady=0)

#salida
impresion_tk=Label(ventana,fg="black", font=("Verdana",15,"normal"),justify="center")
impresion_tk.pack(padx=0,pady=0)
impresion_tk['background']=color

#datos equipo
acerca=Label(text="Equipo: \n 1863549 Ester Abigail Celada López \n 1941416 Eduardo Alan Hernández Villasana \n 1847284 Brayan Adrián Montoya Morales", font=("Verdana", 9,"normal"), justify="right")
acerca.pack(padx=10,pady=10)
acerca.place(x=900,y=2)
acerca['background']=color
acerca2=Label(text="Correos: \n abigailcelada1222@gmail.com\n eduardo.hernandezvll@uanl.edu.mx\n brayan.montoyams@uanl.edu.mx", font=("Verdana", 9,"normal"), justify="left")
acerca2.pack(padx=10,pady=10)
acerca2.place(x=10,y=2)
acerca2['background']=color


ventana.mainloop()