import os
from gtts import gTTS as gs
import random as rd

## TODO: Contar letras corretas como tentativas
## TODO: Considerar iguais as letras com ou sem acento
## TODO: Fazer loop do jogo geral

#### PARAMETROS #####
frutas = ['LIMAO', 'ABACAXI', 'JABUTICABA', 'UVA', 'MELANCIA', 'ABACATE', 'MORANGO', 'PEQUI']
animais = ['CACHORRO', 'GATO', 'BALEIA']
insetos = ['FORMIGA', 'BESOURO', 'BARATA', 'CENTOPEIA', 'BORBOLETA', 'MOSQUITO']
opcoes = {
    '1 - FRUTAS': frutas,
    '2 - ANIMAIS': animais,
    '3 - INSETOS': insetos,
    '4 - NOVA PALAVRA': [],
}

### FUNCOES BASICAS ###

def fale(texto, language='pt'):
    audio = gs(text=texto, lang=language, slow=False)
    audio.save("audio.mp3")
    os.system("mpg123 -q audio.mp3")

def inicio():
    os.system('clear')
    print('----x----x---- JOGO DA FORCA ----x----x----\n')
    print('Escolha um tipo de palavra e digite o número correspondente: ')
    for tipo in opcoes.keys():
        print(f'--> {tipo}')
    fale(texto='Escolha um tipo de palavra e digite o número correspondente: ')

inicio()

jogo = ''

opcoes_num = {}

for key, value in opcoes.items():
    opcoes_num[key[0]] = value

while jogo not in opcoes_num.keys():
    jogo = input('Digite o número de um jogo: ').upper()
    if jogo not in opcoes_num.keys():
        os.system('clear')
        print(f'Não encontrei a opção {jogo}. Escreva novamente o nome do jogo.')
        fale(f'Não encontrei a opção {jogo}')
        inicio()
    else:
        break

if jogo == '4':
    palavra_escrita = input('Escreva a palavra: ').upper().strip()
    while len(palavra_escrita) < 2:
        print('Digite uma palavra de verdade!')
        fale(f'Digite uma palavra de verdade!')
        palavra_escrita = input('Escreva a palavra: ').upper().strip()
    lista = [palavra_escrita]
else:
    lista = opcoes_num[jogo]

def jogo_da_forca():
    os.system('clear')

    # Função para escolher uma palavra da lista aleatoriamente
    def palavra_aleatoria(lista):
        tamanho = len(lista) - 1
        sorteio = rd.randint(0, tamanho)
        palavra_aleatoria_selecionada = lista[sorteio]
        return palavra_aleatoria_selecionada

    # função para localizar as posições de uma letra em uma palavra
    def localizar(texto, letra):
        posicoes = []
        for i in range(0, len(texto)):
            if texto[i] == letra:
                posicoes.append(i)
        return posicoes

    palavra = palavra_aleatoria(lista)
    chances = 0
    pal_secreta = list('_' * len(palavra))
    letras_erradas = []
    letras_tentadas = []

    def exibe_palavra():
        os.system('clear')
        num_jogo = int(jogo)
        print(5 * '_-' + f' ADIVINHE A PALAVRA' + 5 * '_-' + '\n')
        print(f'DICA: A palavra tem {len(palavra)} letras')
        print('\n' + ' '.join(pal_secreta) + '\n')
        print('Letras tentadas e não contidas na palavra: ' + ', '.join(letras_erradas) + '\n')

    def chute():
        fale(texto='Já sabe qual é a palavra?')
        opcao = input('Já sabe qual é a palavra? (S ou N): ').upper()
        if opcao == 'S':
            resposta = input('Digite a palavra: ').upper().strip()
            if resposta == palavra:
                print('-------- X -------- X --------')
                ganhou = f'Parabéns!!\nA Palavra correta é {palavra}!'
                print(ganhou)
                fale(ganhou)
                print('-------- X -------- X --------')
                return True
            else:
                ainda_nao = 'Ainda não foi desta vez!'
                print(ainda_nao)
                fale(ainda_nao)
                return False
        else:
            return False

    exibe_palavra()

    while chances < 10:
        letra_digitada = input('Digite uma letra: ').upper().strip()
        while len(letra_digitada) != 1 or not letra_digitada.isalpha():
            fale('Digite apenas uma letra')
            letra_digitada = input('Digite uma letra: ').upper().strip()

        if letra_digitada in letras_tentadas:
            print(f'A letra {letra_digitada} já foi tentada.')
            fale(f'A letra {letra_digitada} já foi tentada.')
            continue

        letras_tentadas.append(letra_digitada)

        if letra_digitada in palavra:
            posicao = localizar(palavra, letra_digitada)
            for i in posicao:
                pal_secreta[i] = letra_digitada

            exibe_palavra()
            print(f'ACERTOU! A letra {letra_digitada} está contida na palavra')
            fale('Acertou')
            palavra_parcial = ''.join(pal_secreta)
            if palavra_parcial == palavra:
                ganhou = f'Parabéns!!\nA Palavra correta é {palavra}!'
                print(ganhou)
                fale(ganhou)
                print('-------- X -------- X --------')
                break

            if chute():
                break
            else:
                exibe_palavra()
                print(f'{9 - chances} chances restantes')

        else:
            letras_erradas.append(letra_digitada)
            exibe_palavra()
            print(f'A palavra NÃO tem a letra: {letra_digitada}')
            fale(f'A palavra não tem {letra_digitada}')
            chances += 1  # Incrementa a chance apenas se o usuário errar
            print(f'{9 - chances} chances restantes')

        if chances >= 10:
            print('-------- X GAME OVER X --------')
            print(f'A Palavra correta é {palavra}!')
            fale(f'A Palavra correta é {palavra}!')
            break

jogo_da_forca()

