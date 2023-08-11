import os
import re
from stockfish import Stockfish


class chessAnalise:
    def __init__(self) -> None:
        self.diretorio = 'avaliacao\\\\'
        self.arquivo = None
        self.corIa = None
        self.corVencedor = None
        self.vencedor = None


    def abrirArquivo(self, f):
        self.arquivo = open(f, 'r')


    def fecharArquivo(self):
        self.arquivo.close()
        

    def setCores(self):
        self.arquivo.readline()
        linha1 = self.arquivo.readline()
        linha2 = self.arquivo.readline()
        self.corIa = linha1.split(' ')[-1][:-1]
        self.corVencedor = linha2.split(' ')[-1][:-1]

        if self.corIa == self.corVencedor:
            self.vencedor = 'ia'
        
        else: 
            self.vencedor = 'jogador'


    def analisarJogadasIa(self):
        dados = self.arquivo.read()
        brancas = {}
        pretas = {}
        
        brancas['inicio'] = re.search('Jogadas brancas:\n', dados).end()
        brancas['fim'] = re.search('Jogadas pretas:\n', dados).start()
        pretas['inicio'] = re.search('Jogadas pretas:\n', dados).end()
        pretas['fim'] = re.search('debug_info_ia:\n', dados).start()
        debug = re.search('debug_info_ia:\n', dados).end()

        brancas = dados[brancas['inicio']:brancas['fim']]
        pretas = dados[pretas['inicio']:pretas['fim']]
        debug = dados[debug]

        

                

    def analisarPartidas(self):
        for arquivo in os.listdir(self.diretorio):
            f = self.diretorio + arquivo
            self.abrirArquivo(f)
            self.setCores()
            self.analisarJogadasIa()

            self.fecharArquivo()

if __name__ == '__main__':
    chessAnalise().analisarPartidas()
    


