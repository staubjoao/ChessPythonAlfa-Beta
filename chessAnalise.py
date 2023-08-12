import os
import re
from stockfish import Stockfish
import chess
import pandas as pd

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
        self.dictJogadas = {'jogada': [],
                       'melhoresJogadas': []}
        


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

        if self.corVencedor == 'empate':
            self.vencedor = ['empate', 'empate']

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

        for jogadaBranca, jogadaPreta in zip(self.jogadasBrancas, self.jogadasPretas):
            if jogadaBranca == '' or jogadaPreta == '':
                break
            
            jogadaBranca = jogadaBranca.split(',')[0]
            jogadaPreta = jogadaPreta.split(',')[0]

            
            if self.corIa == 'brancas':
                self.dictJogadas['jogada'].append(jogadaBranca)

                melhoresJogadas = list(map(lambda x: x['Move'], stockfish.get_top_moves(5)))
                self.dictJogadas['melhoresJogadas'].append(melhoresJogadas)

            tabuleiro.push_san(jogadaBranca)
            stockfish.set_fen_position(tabuleiro.fen())

            if self.corIa == 'pretas':
                self.dictJogadas['jogada'].append(jogadaPreta)

                melhoresJogadas = list(map(lambda x: x['Move'], stockfish.get_top_moves(5)))
                self.dictJogadas['melhoresJogadas'].append(melhoresJogadas)

            tabuleiro.push_san(jogadaPreta)
            stockfish.set_fen_position(tabuleiro.fen())

    def analisarMetadata(self):
        metadata = self.metadata.split('\n')
        metadata = list(map(lambda x: x.split(', '), metadata))[:-1]
        metadata = {'nós': [int(''.join(re.findall(r'\d+', metadata[x][0]))) for x in range(len(metadata)) ],
                    'tempo': [float(''.join(re.findall(r'\d+(?:.\d+)*',metadata[x][1].replace(',', '.')))) for x in range(len(metadata))]
        }
        
        self.metadata = metadata

    def construirDataFrameLances(self):
        df = pd.DataFrame(self.metadata)
        df['jogadas'] = self.dictJogadas['jogada']
        df['melhoresJogadas'] = self.dictJogadas['melhoresJogadas']

        return df

    def dadosStockfish(self):
        pass

    def dadosPartida(self, df, nome, corIa, vencedor):
        lances = df.shape[0]
        mediaNos = int(df['nós'].mean())
        
        mediaTempo = df['tempo'].mean()
        medianaTempo = df['tempo'].median()
        stdTempo = df['tempo'].std()

        cont = 0

        for jogada, melhores in zip(df['jogadas'], df['melhoresJogadas']):
            if re.search(rf'{jogada}', melhores):
                cont += 1
        
        nivel = self.dadosStockfish()
    
        dictDados = {
            'corIa': corIa,
            'vencedor': vencedor,
            'qtdLances': lances,
            'lancesIdeais': cont,
            'mediaNos': mediaNos,
            'mediaTempo': mediaTempo,
            'medianaTempo': medianaTempo,
            'stdTempo': stdTempo,
        }

        return dictDados

    def analisarPartidas(self):
        for arquivo in os.listdir(self.diretorio):
            
            f = self.diretorio + arquivo
            self.abrirArquivo(f)
            self.setCores()
            self.setJogadas()
            self.analisarJogadasIa()
            self.analisarMetadata()

            df = self.construirDataFrame()
            dictDados = self.dadosPartida(df, arquivo[:-4], self.corIa, self.vencedor)
            df.to_csv('avaliacaoCSV\\' + arquivo[:-4] + '.csv', index=False)

            self.fecharArquivo()
            break

if __name__ == '__main__':
    chessAnalise().analisarPartidas()
    


