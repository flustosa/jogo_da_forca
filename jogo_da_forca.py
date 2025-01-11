import os
import subprocess
import unicodedata
from gtts import gTTS as gs
import random as rd

## TODO: Contar letras corretas como tentativas
## TODO: Fazer loop do jogo geral
## TODO: Tratar nomes compostos, com espaços e traços

#### PARAMETROS #####
with open('./animais.txt') as animais_list:
    animais = animais_list.read().splitlines()

with open('./insetos.txt') as insetos_list:
    insetos = insetos_list.read().splitlines()

with open('./frutas.txt') as frutas_list:
    frutas = frutas_list.read().splitlines()


opcoes = {
    '1 - FRUTAS': frutas,
    '2 - ANIMAIS': animais,
    '3 - INSETOS': insetos,
    '4 - NOVA PALAVRA': [],
}

### FUNCOES BASICAS ###

# Captura a saída do comando uname -o
op_sys = subprocess.check_output("uname -o", shell=True).decode().strip()


def fale(texto, language='pt', print_word=True, same_line=False):
    audio = gs(text=texto, lang=language, slow=False)
    audio.save("audio.mp3")
    if print_word and same_line:
        print(f'{texto}', end='')
    elif print_word and not same_line:
        print(f'{texto}')

    # Verifica o sistema operacional e executa o player adequado
    if op_sys == "Android":
        os.system("mpv --really-quiet audio.mp3")
    else:
        os.system("mpg123 -q audio.mp3")

def acertou():
    if op_sys == "Android":
        os.system("mpv --really-quiet ./audio/certa_resposta.mp3")
    else:
        os.system("mpg123 -q ./audio/certa_resposta.mp3")

def errou():
    if op_sys == "Android":
        os.system("mpv --really-quiet ./audio/errou.mp3")
    else:
        os.system("mpg123 -q ./audio/errou.mp3")


def remove_acentos(texto):
    """ Normaliza o texto para a forma compatível com a decomposição Unicode """
    texto_normalizado = unicodedata.normalize('NFD', texto)
    # Filtra os caracteres não acentuados
    texto_sem_acento = ''.join(char for char in texto_normalizado if unicodedata.category(char) != 'Mn')
    return texto_sem_acento


def palavra_aleatoria(lista):
    """ Escolhe uma palavra da lista aleatoriamente"""
    tamanho = len(lista) - 1
    sorteio = rd.randint(0, tamanho)
    palavra_aleatoria_selecionada = lista[sorteio].upper()
    return palavra_aleatoria_selecionada


def localizar(texto, letra):
    """Localizar as posições de uma letra em uma palavra"""
    posicoes = []
    for i in range(0, len(texto)):
        if remove_acentos(texto[i]) == remove_acentos(letra):
            posicoes.append(i)
    return posicoes

def menu_inicial(opcoes_num):
    os.system('clear')
    print('----x----x---- JOGO DA FORCA ----x----x----\n')
    for tipo in opcoes.keys():
        print(f'--> {tipo}')
    for key, value in opcoes.items():
        opcoes_num[key[0]] = value
    fale('Escolha um tipo de palavra e digite o número correspondente: ', print_word=False, same_line=True)


def inicio(opcoes_list):
    jogo = ''
    opcoes_num = {}
    while jogo not in opcoes_num.keys():
        menu_inicial(opcoes_num)
        jogo = input('Digite o número de um jogo: ').upper()
        if jogo not in opcoes_num.keys():
            print('\n')
            fale(f'Não encontrei a opção {jogo}')
        else:
            break

    if jogo == '4':
        fale('Escreva a palavra: ', same_line=True)
        palavra_escrita = input().upper().strip()
        while len(palavra_escrita) < 2:
            fale(f'Digite uma palavra de verdade!', print_word=False)
            palavra_escrita = input('Escreva a palavra: ').upper().strip()
        return ([palavra_escrita], jogo)
    else:
        return (opcoes_num[jogo], jogo)


def gera_palavra_secreta(palavra):
    palavra_secreta = [] 
    print(type(palavra_secreta))
    for letra in palavra:
        if letra == '-':
            palavra_secreta.append('-')
        else:
            palavra_secreta.append('_')
    return palavra_secreta


def jogo_da_forca(lista, jogo):
    os.system('clear')
    palavra = palavra_aleatoria(lista)
    palavra_unicode = remove_acentos(palavra)
    chances = 0
    palavra_secreta = list('_' * len(palavra))
    palavra_secreta = gera_palavra_secreta(palavra)
    letras_erradas = []
    letras_tentadas = []

    def tela_jogo():
        os.system('clear')
        print(5 * '_-' + f' ADIVINHE A PALAVRA' + 5 * '_-' + '\n')
        print(f'DICA: A palavra tem {len(palavra)} letras')
        print(f'CHANCES: {9 - chances}')
        print('LETRAS: ' + ', '.join(letras_erradas))
        print('\n' + ' '.join(palavra_secreta) + '\n')

    def chute():
        fale(texto='Já sabe qual é a palavra?', same_line=True)
        opcao = input(' (S ou N): ').upper()
        if opcao == 'S':
            resposta = input('Digite a palavra: ').upper().strip()
            if remove_acentos(resposta) == palavra_unicode:
                print('-------- X -------- X --------')
                ganhou = f'Parabéns!!\nA Palavra correta é {palavra}!'
                fale(ganhou)
                print('-------- X -------- X --------')
                return True
            else:
                fale('Ainda não foi desta vez!')
                return False
        else:
            return False

    while chances < 10:
        tela_jogo()
        letra_digitada = input('Digite uma letra: ').upper().strip()
        while len(letra_digitada) != 1 or not letra_digitada.isalpha():
            fale('Digite apenas uma letra', print_word=False)
            letra_digitada = input('Digite uma letra: ').upper().strip()

        if remove_acentos(letra_digitada) in letras_tentadas:
            fale(f'A letra {letra_digitada} já foi tentada.')
            continue

        letras_tentadas.append(remove_acentos(letra_digitada))

        if remove_acentos(letra_digitada) in palavra_unicode:
            posicao = localizar(palavra, letra_digitada)
            for i in posicao:
                palavra_secreta[i] = palavra[i]

            tela_jogo()
            print(f'ACERTOU! A letra {letra_digitada} está contida na palavra')
            
            acertou()
            palavra_parcial = ''.join(palavra_secreta)
            if palavra_parcial == palavra:
                ganhou = f'Parabéns!!\nA Palavra correta é {palavra}!'
                fale(ganhou)
                print('-------- X -------- X --------')
                break

            if chute():
                break

        else:
            letras_erradas.append(letra_digitada)
            tela_jogo()
            errou()
            fale(f'A palavra não tem "{letra_digitada}"')
            chances += 1  # Incrementa a chance apenas se o usuário errar

        if chances >= 10:
            print('-------- X GAME OVER X --------')
            fale(f'Não foi desta vez!\nA Palavra correta é {palavra}!')
            break

lista, jogo = inicio(opcoes)
jogo_da_forca(lista, jogo)

