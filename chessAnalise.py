import os
import re
from stockfish import Stockfish
import chess


class chessAnalise:
    def __init__(self) -> None:
        self.diretorio = 'avaliacao\\\\'
        self.arquivo = None
        self.corIa = None
        self.corVencedor = None
        self.vencedor = None
        self.jogadasBrancas = None
        self.jogadasPretas = None
        self.metadata = None


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
            self.vencedor = ['ia', self.corVencedor]
        
        else: 
            self.vencedor = ['jogador', self.corVencedor]


    def setJogadas(self):
        dados = self.arquivo.read()
        brancas = {}
        pretas = {}
        
        brancas['inicio'] = re.search('Jogadas brancas:\n', dados).end()
        brancas['fim'] = re.search('Jogadas pretas:\n', dados).start()
        pretas['inicio'] = re.search('Jogadas pretas:\n', dados).end()
        pretas['fim'] = re.search('debug_info_ia:\n', dados).start()
        metadata = re.search('debug_info_ia:\n', dados).end()

        self.jogadasBrancas = dados[brancas['inicio']:brancas['fim']].split('\n')
        self.jogadasPretas = dados[pretas['inicio']:pretas['fim']].split('\n')
        self.metadata = dados[metadata:]

        
    def analisarJogadasIa(self):
        stockfish = Stockfish(path='stockfish\\stockfish-windows-x86-64-avx2.exe', depth=3,
                                  parameters={"Threads": 4, "Minimum Thinking Time": 300, 'Hash': 2048})
        
        tabuleiro = chess.Board()
        stockfish.set_fen_position(tabuleiro.fen())
        dictJogadas = {}
        
        
        for jogadaBranca, jogadaPreta in zip(self.jogadasBrancas, self.jogadasPretas):
            if jogadaBranca == '' or jogadaPreta == '':
                break

            tabuleiro.push_san(jogadaBranca)
            
                    

    def analisarPartidas(self):
        for arquivo in os.listdir(self.diretorio):
            f = self.diretorio + arquivo
            self.abrirArquivo(f)
            self.setCores()
            self.setJogadas()
            self.analisarJogadasIa()

            self.fecharArquivo()

if __name__ == '__main__':
    chessAnalise().analisarPartidas()
    


