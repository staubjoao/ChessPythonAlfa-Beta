import os

diretorio = 'avaliacao\\\\'

for arquivo in os.listdir(diretorio):
    f = diretorio + arquivo
    
    with open(f, 'r') as dados:
        dados.readline()
        linha1 = dados.readline()
        linha2 = dados.readline()

        cor_ia = linha1.split(' ')[-1][:-1]
        cor_vencedor = linha2.split(' ')[-1][:-1]

        if cor_ia == cor_vencedor:
            vencedor = 'ia'
        
        else: 
            vencedor='jogador'

        print(vencedor)
