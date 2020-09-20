from time import sleep, time
'''
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

#GPIO Pins
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setwarnings(False) # Ignore warning for now

#-------KeyPad Outputs Rows---------------------------------------
GPIO.setup(8,  GPIO.OUT, initial=GPIO.HIGH) # Set pin 8 as  row 1
GPIO.setup(11, GPIO.OUT, initial=GPIO.HIGH) # Set pin 11 as row 2
GPIO.setup(13, GPIO.OUT, initial=GPIO.HIGH) # Set pin 13 as row 3
GPIO.setup(15, GPIO.OUT, initial=GPIO.HIGH) # Set pin 15 as row 4
#-------KeyPad Inputs Columns-----------------------------------------------
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 12 as column 5
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 16 as column 6
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 18 as column 7
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 22 as column 8
#--------------------------------------------------------------------------
'''

def armar_bomba():
    codigoCorrecto=[]
    print('Armando bomba...')
    minutosArmados = int(input('¿Cuantos minutos dura la cuenta atrás?'))
    print(f'Bomba armada correctamente para {minutosArmados}:00 minutos')
    longitudCodigoCorrecto = int(input('Cuantos caracteres tiene el código correcto?'))
    
    for i in range(longitudCodigoCorrecto):
        codigoCorrecto.append(input(f'Escribe el caracter {i+1} del código de desactivación (Numeros de 0 a 9 y letras de A a D):  '))
        i +=1
    
    return minutosArmados,codigoCorrecto

def activar (minutosArmados):
    print('Activando bomba')
    tiempoInicio = int(time())

    while minutosArmados > 0:
        minutosArmados -=1
        segundosArmados = 59
        
        while segundosArmados >= 0:
            print (f'{minutosArmados}m {segundosArmados}s')
            print(int(time()))
            segundosArmados -=1
            sleep(1)
         
    if minutosArmados == 0:
        estado = 'explosion'
    

    return estado    
        
def cuenta_atras (minutosArmados):
    estado = 'activado'
    tiempoInicio = int(time())
    tiempoFinal = tiempoInicio + (minutosArmados*60)
    listaKeypad = []
    while int(time())<=tiempoFinal:
        listaKeypad = comprobar_keypad(listaKeypad)
        estado = comprobar_codigo(listaKeypad,codigoCorrecto)
        if estado == 'desactivado':
            break
        
        tiempoRestante = tiempoFinal - int(time())
        minutosRestantes = tiempoRestante//60
        segundosRestantes = tiempoRestante %60
        print(f'{minutosRestantes}m {segundosRestantes}s')
        sleep(1)

    return estado

def comprobar_keypad(listaKeypad):
    print('Comprobando keypad.')
    caracter = leer_keypad() 
    if caracter == '':
        pass
    elif caracter == '*':
        listaKeypad = []
    else:  
        listaKeypad.append(caracter)

    #comprobar si hay algun valor introducido en el teclado y si lo hay hacer un append a la lista de keypad para actualizarla
    return listaKeypad

def leer_keypad():
    key = '' # No key was detected
    GPIO.output(8,GPIO.LOW) # Set 8 - Low check 1,2,3,A
    if(GPIO.input(12) == 0):
        key = '1'   
    elif(GPIO.input(16) == 0):
        key = '2' 
    elif(GPIO.input(18) == 0):
        key = '3'
    elif(GPIO.input(22) == 0):
        key = 'A'
    GPIO.output(8,GPIO.HIGH) # Set 8 - High
    #-------------------------------------------------------
  
    #-------------------------------------------------------
    GPIO.output(11,GPIO.LOW) # Set 11 - Low check 4,5,6,B
    if(GPIO.input(12) == 0):
        key = '4'
    elif(GPIO.input(16) == 0):
        key = '5'
    elif(GPIO.input(18) == 0):
        key = '6'
    elif(GPIO.input(22) == 0):
        key = 'B'
    GPIO.output(11,GPIO.HIGH) # Set 11 - High
    #-------------------------------------------------------

    #-------------------------------------------------------
    GPIO.output(13,GPIO.LOW) # Set 13 - Low check 7,8,9,C
    if(GPIO.input(12) == 0):
        key = '7'
    elif(GPIO.input(16) == 0):
        key = '8'
    elif(GPIO.input(18) == 0):
        key = '9'
    elif(GPIO.input(22) == 0):
        key = 'C'
    GPIO.output(13,GPIO.HIGH) # Set 13 - High
    #-------------------------------------------------------

    #-------------------------------------------------------
    GPIO.output(15,GPIO.LOW) # Set 15 - Low check *,0,#,D
    if(GPIO.input(12) == 0):
        key = '*'
    elif(GPIO.input(16) == 0):
        key = '0'
    elif(GPIO.input(18) == 0):
        key = '#'
    elif(GPIO.input(22) == 0):
        key = 'D'
    GPIO.output(15,GPIO.HIGH) # Set 15 - High
    return key

def comprobar_codigo(listaKeypad,codigoCorrecto):
    if '#' in listaKeypad:
        if listaKeypad == codigoCorrecto:
            return 'desactivado'
    else:
        return 'activado'
   
def final (estado):
    
    if estado == 'activado':
        print('Misión Fallida. La bomba ha explotado.')
    elif estado == 'desactivado':
        print('Mision Cumplida. Desactivasteis la bomba.')



if __name__ == "__main__":

    print('Inicializando raspi_bomb.')
    minutos, codigoCorrecto = armar_bomba()
    input('Presiona ENTER para activar la bomba.')
    estado = cuenta_atras(minutos)
    #estado = activar(minutos)
    final(estado)




