#!usr/bin/env pybricks-micropython
""" A primeira linha deve ser sempre essa acima:
ela indica qual interpretador exatamente o programa
deve usar quando for executado como script (será o caso dentro do Ev3)."""

#Importacoes de bibliotecas
from pybricks.ev3devices import Motor, ColorSensor, GyroSensor, InfraredSensor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.tools import print, StopWatch

#Definicao da classe do Robo
"""A classe será como um novo tipo de dado dentro do nosso código.
Esse novo tipo de dado terá suas próprias variáveis e funções.
As funções "dentro" desse novo tipo de dado (dessa nova classe) são chamadas de MÉTODOS.
"""
class Robot:
    """Classe do Robo"""

    """Todos os métodos tem como primeiro parâmetro a palavra-chave 'self' e é ela que faz a referência
    a outras variáveis e métodos dentro da classe 'Robot'.

    Os outros parametros funcionam da mesma forma que em funcoes normais.
    """

    def __init__(self, portaMotorEsquerdo, portaMotorDireito):
        """Esse metodo é a função de inicialização de um novo dado do tipo 'Robot'.
        Podemos dizer, então, que é o método de inicialização de um novo objeto da classe 'Robot'.

        Passamos os parametros:
        'self', por ser um método, e as portas que serão associadas aos elementos do robo:"""

        self.motorEsquerdo = Motor(portaMotorEsquerdo)
        self.motorDireito = Motor(portaMotorDireito)
        self.sensor = None # Como nao sabemos qual tipo de sensor será conectado, vamos deixar a variável <sensor> sem nenhum valor por enquanto
        self.tipoSensor = "nenhum" # Podemos usar essa string para verificar qual o tipo de sensor conectado antes de utilizar ele no codigo

    """ Cada tipo de sensor diferente que pode ser conectado tem uma inicialização diferente
    Por isso podemos definir uma inicialização para cada tipo que poderemos utilizar
    Se soubessemos exatamente quais sensores estariam no robo, eles poderiam ser inicializados direto no metodo <__init__>,
    assim como foram os motores.
    Nesse caso, nao seria necessario verificar o tipo de sensor, pois sempre saberiamos qual o tipo e de que forma utiliza-lo."""

    def iniciaSensorCor(self, portaSensor): # Para o sensor de cor
        self.sensor = ColorSensor(portaSensor)
        self.tipoSensor = "cor"

    def iniciaSensorUltra(self, portaSensor): # Para o sensor ultrassonico
        self.sensor = UltrasonicSensor(portaSensor)
        self.tipoSensor = "ultra"

    def iniciaSensorInfra(self, portaSensor): # Para o sensor infravermelho
        self.sensor = InfraredSensor(portaSensor)
        self.tipoSensor = "infra"

    def iniciaSensorGiro(self, portaSensor): # Para o sensor giroscopio
        self.sensor = GyroSensor(portaSensor)
        self.tipoSensor = "giro"

    """Metodos para utilizacao dos recursos do robo:"""

    def andarTempo(self, velocEsquerda, velocDireita, tempo):
        cronometro = StopWatch() # Definimos um cronometro
        cronometro.reset() # Resetamos o tempo marcado no cronometro

        while cronometro.time() < tempo:
            self.motorDireito.run(velocEsquerda)
            self.motorEsquerdo.run(velocDireita)

        self.motorDireito.stop()
        self.motorEsquerdo.stop()

    def andarRetoGraus(self, veloc, graus):
        while (self.motorEsquerdo.angle() < graus) and (self.motorDireito.angle() < graus):
            self.motorDireito.run(veloc)
            self.motorEsquerdo.run(veloc)

        self.motorDireito.stop()
        self.motorEsquerdo.stop()

    def curvaGiro(self, veloc, graus): # Curva com os dois motores utilizando o giroscopio
        if self.tipoSensor != "giro": # Verifica se o sensor do tipo certo esta conectado
            print("ERRO: GIROSCOPIO NAO CONECTADO.")
            return False # Interrompe o metodo

        self.sensor.reset_angle(0)
        while self.sensor.angle() < graus:
            self.motorDireito.run(-veloc)
            self.motorEsquerdo.run(veloc)

        self.motorDireito.stop()
        self.motorEsquerdo.stop()

    def andaAteObstaculo(self, veloc, distancia):
        if self.tipoSensor != "ultra" and self.tipoSensor != "infra": # O mesmo codigo funciona pro ultrassonico e pro infravermelho
            print("ERRO: SENSOR DE DISTANCIA NAO CONECTADO")
            return False # Interrompe o metodo

        while self.sensor.distance() < distancia:
            self.motorEsquerdo.run(veloc)
            self.motorDireito.run(veloc)
        self.motorEsquerdo.stop()
        self.motorDireito.stop()

    def andaAteCor(self, veloc, cor):
        if self.tipoSensor != "cor":
            print("ERRO: SENSOR DE COR NAO CONECTADO")
            return False # Interrompe o metodo

        while self.sensor.color() != cor:
            self.motorEsquerdo.run(veloc)
            self.motorDireito.run(veloc)
        self.motorEsquerdo.stop()
        self.motorDireito.stop()

    def angPoligono(self, lados):
        if lados <= 2 :
            print("NAO EH UM POLIGONO")
            return False
        if self.tipoSensor != "giro":
            print("ERRO: SENSOR GIROSCOPIO NAO CONECTADO")
            return False # Interrompe o metodo
        angint = (((lados - 2)*180)/lados)
        #calculo para angulos internos de um polígono"
        return angint




def main():
    """essa main contém a instanciação do robô e
    uma ideia para a realização de polígonos regulares"""
    brabo = Robot(portaMotorEsquerdo = Port.A, portaMotorDireito = Port.B)
    #declaração do robô e as portas usadas
    brabo.iniciaSensorGiro(Port.S1)
    #instanciação

    for i in range(lados):
        brabo.curvaGiro(veloc, brabo.angPoligono(lados))
        brabo.andarTempo(velocEsquerda, velocDireita, tempo)
        #iteração para cada lado do polígono

def main2():
    """essa main contém a instanciação do robô e
    uma ideia para a realização de desvio de obstáculos"""
    brabo2 = Robot(portaMotorEsquerdo = Port.A, portaMotorDireito = Port.B)
    brabo2.iniciaSensorGiro(Port.S1)
    brabo2.iniciaSensorUltra(Port.S2)
    #declaração do robô e as portas usadas
    while True:
        brabo2.andaAteObstaculo(veloc,distancia)
        brabo2.curvaGiro(veloc, 45)
        #código de loop, usando as funções do giroscopio e do ultrassonico


def main3():
        """essa main contém a instanciação do robô e
        uma ideia para a realização de zigue zagues"""
    brabo3 = Robot(portaMotorEsquerdo = Port.A, portaMotorDireito = Port.B)
    brabo3.iniciaSensorGiro(Port.S1)
        #declaração do robô e as portas usadas
    while True:
        brabo3.curvaGiro(veloc,90)
        brabo3.andarTempo(velocEsquerda, velocDireita, tempo)
        brabo3.curvaGiro(veloc,-90)
        brabo3.andarTempo(velocEsquerda, velocDireita, tempo)
        brabo3.curvaGiro(veloc,-90)
        brabo3.andarTempo(velocEsquerda, velocDireita, tempo)
        brabo3.curvaGiro(veloc,90)
        brabo3.andarTempo(velocEsquerda, velocDireita, tempo)
        #código de loop, usando as funções do giroscopio para realização do zigue zague

main()
#main2()
#main3()
