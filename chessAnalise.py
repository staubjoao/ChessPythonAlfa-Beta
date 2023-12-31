import os
import re
from stockfish import Stockfish
import chess
import pandas as pd


class chessAnalise:
    def __init__(self) -> None:
        self.diretorio = 'resultados\\'
        # self.diretorio = 'resultados\\stockfish_r_1\\'
        self.arquivo = None
        self.corIa = None
        self.corVencedor = None
        self.vencedor = None
        self.jogadasBrancas = None
        self.jogadasPretas = None
        self.metadata = None
        self.dictJogadas = {'jogada': [],
                            'melhoresJogadas': []}

        self.dadosCompletos = {'corIa': [],
                               'vencedor': [],
                               'adversario': [],
                               'qtdLances': [],
                               'lancesIdeais': [],
                               'mediaNos': [],
                               'mediaTempo': [],
                               'medianaTempo': [],
                               'stdTempo': []}

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
            self.vencedor = 'empate'

        elif self.corIa == self.corVencedor:
            self.vencedor = 'ia'

        else:
            self.vencedor = 'jogador'

    def setJogadas(self):
        dados = self.arquivo.read()
        brancas = {}
        pretas = {}

        brancas['inicio'] = re.search('Jogadas brancas:\n', dados).end()
        brancas['fim'] = re.search('Jogadas pretas:\n', dados).start()
        pretas['inicio'] = re.search('Jogadas pretas:\n', dados).end()
        pretas['fim'] = re.search('debug_info_ia:\n', dados).start()
        metadata = re.search('debug_info_ia:\n', dados).end()

        self.jogadasBrancas = dados[brancas['inicio']:brancas['fim']].split('\n')[
            :-1]
        self.jogadasPretas = dados[pretas['inicio']:pretas['fim']].split('\n')[
            :-1]
        self.metadata = dados[metadata:]

    def analisarJogadasIa(self):
        stockfish = Stockfish(path='stockfish\\stockfish-windows-x86-64-avx2.exe', depth=4,
                              parameters={"Threads": 4, "Minimum Thinking Time": 300, 'Hash': 2048})

        tabuleiro = chess.Board()
        stockfish.set_fen_position(tabuleiro.fen())

        for jogadaBranca, jogadaPreta in zip(self.jogadasBrancas, self.jogadasPretas):

            jogadaBranca = jogadaBranca.split(',')[0]
            jogadaPreta = jogadaPreta.split(',')[0]

            if self.corIa == 'brancas':
                self.dictJogadas['jogada'].append(jogadaBranca)

                melhoresJogadas = list(
                    map(lambda x: x['Move'], stockfish.get_top_moves(5)))
                self.dictJogadas['melhoresJogadas'].append(melhoresJogadas)

            tabuleiro.push_san(jogadaBranca)
            stockfish.set_fen_position(tabuleiro.fen())

            if self.corIa == 'pretas':
                self.dictJogadas['jogada'].append(jogadaPreta)

                melhoresJogadas = list(
                    map(lambda x: x['Move'], stockfish.get_top_moves(5)))
                self.dictJogadas['melhoresJogadas'].append(melhoresJogadas)

            tabuleiro.push_san(jogadaPreta)
            stockfish.set_fen_position(tabuleiro.fen())

    def analisarMetadata(self):
        metadata = self.metadata.split('\n')
        metadata = list(map(lambda x: x.split(', '), metadata))[:-1]
        metadata = {'nós': [int(''.join(re.findall(r'\d+', metadata[x][0]))) for x in range(len(metadata))],
                    'tempo': [float(''.join(re.findall(r'\d+(?:.\d+)*', metadata[x][1].replace(',', '.')))) for x in range(len(metadata))]
                    }

        self.metadata = metadata

    def construirDataFrameLances(self):
        df = pd.DataFrame(self.metadata)

        if self.corIa == 'brancas' and (self.corVencedor == 'brancas' or self.corVencedor == 'empate') and len(self.jogadasBrancas) > len(self.jogadasPretas):
            self.dictJogadas['jogada'].append(' ')
            self.dictJogadas['melhoresJogadas'].append(' ')

        df['jogadas'] = self.dictJogadas['jogada']
        df['melhoresJogadas'] = self.dictJogadas['melhoresJogadas']

        return df

    def dadosStockfish(self, nome):
        nome = nome.split('_')

        if nome[0] == 'stockfish':
            nivel = int(nome[1])

        else:
            nivel = 'humano'

        return nivel

    def dadosPartida(self, df, nome, corIa, vencedor):
        lances = df.shape[0]
        mediaNos = int(df['nós'].mean())

        mediaTempo = df['tempo'].mean()
        medianaTempo = df['tempo'].median()
        stdTempo = df['tempo'].std()

        cont = 0

        for jogada, melhores in zip(df['jogadas'], df['melhoresJogadas']):
            if type(melhores) == str:
                if re.search(rf'{jogada}', melhores):
                    cont += 1

            else:
                if jogada == None:
                    break
                elif jogada in melhores:
                    cont += 1

        self.dadosCompletos['corIa'].append(corIa)
        self.dadosCompletos['vencedor'].append(vencedor)
        self.dadosCompletos['adversario'].append(self.dadosStockfish(nome))
        self.dadosCompletos['qtdLances'].append(lances)
        self.dadosCompletos['lancesIdeais'].append(cont)
        self.dadosCompletos['mediaNos'].append(mediaNos)
        self.dadosCompletos['mediaTempo'].append(mediaTempo)
        self.dadosCompletos['medianaTempo'].append(medianaTempo)
        self.dadosCompletos['stdTempo'].append(stdTempo)

    def analisarPartidas(self):
        for pasta in os.listdir(self.diretorio):

            for arquivo in os.listdir(self.diretorio + pasta + '\\'):
                # for arquivo in os.listdir(self.diretorio):

                self.dictJogadas = {'jogada': [],
                                    'melhoresJogadas': []}

                # f = self.diretorio + arquivo
                # print(f)
                f = self.diretorio + pasta + '\\' + arquivo
                print(f)
                self.abrirArquivo(f)
                self.setCores()
                self.setJogadas()
                self.analisarJogadasIa()
                self.analisarMetadata()

                df = self.construirDataFrameLances()
                self.dadosPartida(df, arquivo[:-4], self.corIa, self.vencedor)

                self.fecharArquivo()

        df = pd.DataFrame(self.dadosCompletos)
        df.to_csv('resultadosFinal.csv', index=False)


if __name__ == '__main__':
    chessAnalise().analisarPartidas()
