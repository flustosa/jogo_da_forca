def jogo_da_forca():
    print('----x----x---- JOGO DA FORCA ----x----x----')
    print('----- ADIVINHE O NOME DE UMA FRUTA -----\n')    

    import random as rd
    lista = ['LIMAO','ABACAXI','JABUTICABA','UVA','MELANCIA','ABACATE','MORANGO','ABACATE','PEQUI']

    #Função para escolher uma palavra da lista aleatoriamente
    def palavra_aleatoria(lista):    
        tamanho = len(lista)
        sorteio = rd.randint(1,tamanho)    
        palavra_aleatoria = lista[sorteio] 
        return palavra_aleatoria
    
    #função para localizar as posições de uma letra em uma palavra
    def localizar(texto,palavra):
        posicoes = []
        for i in range(0,len(texto)):
            if texto[i] == palavra:
                posicoes.append(i)
        return posicoes

    palavra = palavra_aleatoria(lista)
    print(f'DICA: A palavra tem {len(palavra)} letras')

    chances = 0
    pal_secreta = list('_' * len(palavra))
    while chances <= 10:
        letra_digitada = input('Digite somente uma letra: ').upper()    
        if letra_digitada in palavra:
            print(f'A letra {letra_digitada} está contida na frase')                 
            posicao = localizar(palavra,letra_digitada)
            for i in posicao:    
                pal_secreta[i] = letra_digitada            
            print(pal_secreta)  
            opcao = input('Você já sabe qual é o nome da palavra? (S ou N): ')        
            if opcao.upper() == 'S':
                resposta = input('Digite o nome da palavra: ')
                if resposta.upper() == palavra:
                    print('-------- X -------- X --------') 
                    print(f'Parabéns!!\nA Palavra correta é {palavra}! ')
                    print('-------- X -------- X --------') 
                    break
                else:
                    print('Você errou!')
                    print(f'A Palavra correta é {palavra}!')
                    print('-------- X GAME OVER X --------') 
                    break
            else:
                print('-------- X -------- X --------\n')
                print(f'Você ainda tem mais {9-int(chances)} chances')             
        else:
            print(f'A letra {letra_digitada} NÃO está contida na frase')
            print(pal_secreta) 
            opcao = input('Você já sabe qual é o nome da palavra? (S ou N): ')
            if opcao.upper() == 'S':
                resposta = input('Digite o nome da palavra: ')
                if resposta.upper() == palavra:
                    print('-------- X -------- X --------') 
                    print(f'Parabéns!!\nA Palavra correta é {palavra}!')
                    print('-------- X -------- X --------') 
                    break
                else:
                    print('Você errou!')
                    print(f'A Palavra correta é {palavra}!')
                    print('-------- X GAME OVER X --------') 
                    break 
            else:
                print(f'Você ainda tem mais {9-int(chances)} chances')
                print('-------- X -------- X --------\n') 
                
        chances +=1
        if chances >= 10:
            print('-------- X GAME OVER X --------') 
            print(f'A Palavra correta é {palavra}!')

jogo_da_forca()
