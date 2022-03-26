import PySimpleGUI as sg

def HorizontalPar(word):
    xorTotal = 0
    for i in range(len(word)):
        xorTotal = word[i] ^ xorTotal

    return xorTotal


def VerticalPar(word1, word2, word3):
    vertical = []
    for i in range(len(word1)):
        xorTotal = word1[i] ^ word2[i] ^ word3[i]
        vertical.append(xorTotal)
    return vertical


sg.change_look_and_feel('darkGrey1')
layout = [
    [sg.Text('Palavra 1'), sg.Input(size=(20, 0), key='word1'), sg.Text('Palavra 2'),
     sg.Input(size=(20, 0), key='word2'), sg.Text('Palavra 3'), sg.Input(size=(20, 0), key='word3')],
    [sg.T("")],
    [sg.Text('Largura em Bits'), sg.Combo((['8', '16']), size=(20, 0), default_value="Escolha um tamanho", key='tam'),
     sg.T("\t\t"), sg.Button('Send', size=(10, 0), button_color="darkGrey"), sg.T("   "),
     sg.Button('Receive', size=(10, 0), button_color="darkGrey")],
    [sg.Output(size=(100, 15), key='print')],
    [sg.T("")], [sg.Text("Autores: Gustavo Mafra, Nathália de Oliveira e Sydney Matheus")],
]
janela = sg.Window('2DimentionalParityCheck', size=(700, 400), element_justification='l').layout(layout)
event, value = janela.read()
while True:
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Send':
        tam = value['tam']
        word1 = list(map(int, (value['word1'])))
        word2 = list(map(int, (value['word2'])))
        word3 = list(map(int, (value['word3'])))

        try:
            tam = int(tam)
        except ValueError:
            sg.Popup('Escolha um valor válido de bits!', keep_on_top=True)
            event, value = janela.read()

        if ((len(word1) != tam) or (len(word2) != tam) or (len(word3) != tam)):
            sg.Popup('Tamanhos diferentes!', keep_on_top=True)
            event, value = janela.read()
        else:
            janela['print'].update(value='')
            horizontal = [HorizontalPar(word1), HorizontalPar(word2), HorizontalPar(word3)]
            horizontal.append(HorizontalPar(list(horizontal)))
            vertical = VerticalPar(word1, word2, word3)

            print('\n\n')
            print('\t\t', *word1, '  |', horizontal[0])
            print('\t\t', *word2, '  |', horizontal[1])
            print('\t\t', *word3, '  |', horizontal[2])
            print('\t\t', '---' * tam + '----')
            print('\t\t', *vertical, '  |', horizontal[3])
            event, value = janela.read()

    elif event == 'Receive':
        tam = int(value['tam'])
        wordBit1 = list(map(int, (value['word1'])))
        wordBit2 = list(map(int, (value['word2'])))
        wordBit3 = list(map(int, (value['word3'])))
        cond = 1
        if ((len(wordBit1) != tam) or (len(wordBit2) != tam) or (len(wordBit3) != tam)):
            sg.Popup('Tamanhos diferentes!', keep_on_top=True)
            event, value = janela.read()
        else:
            janela['print'].update(value='')
            horizontalBit = [(HorizontalPar(wordBit1)), (HorizontalPar(wordBit2)), (HorizontalPar(wordBit3))]
            horizontalBit.append(HorizontalPar(list(horizontalBit)))
            verticalBit = VerticalPar(wordBit1, wordBit2, wordBit3)
            print('\n\n')
            print('\t\t', *word1, '  |', horizontal[0], "\t\t\t\t", *wordBit1, '  |', horizontalBit[0])
            print('\t\t', *word2, '  |', horizontal[1], "\t\t\t\t", *wordBit2, '  |', horizontalBit[1])
            print('\t\t', *word3, '  |', horizontal[2], "\t\t\t\t", *wordBit3, '  |', horizontalBit[2])
            print('\t\t', '---' * tam + '----', "\t\t\t\t", '---' * tam + '----')
            print('\t\t', *vertical, '  |', horizontal[3], "\t\t\t\t", *verticalBit, '  |', horizontalBit[3])

            linha = 0
            for i in range(len(horizontal) - 1):
                if horizontal[i] != horizontalBit[i]:
                    if(linha != 0):
                        linha = -1
                    else:
                        linha = i+1

            coluna = 0
            for i in range(len(vertical)):
                if vertical[i] != verticalBit[i]:
                    if(coluna != 0):
                        coluna = -1
                    else:
                        coluna = i+1

            if coluna > 0 and linha > 0:
                print("\n\t\tFalta detectada no bit ", coluna, " na palavra ", linha, ", iniciando processo de reparação ...")
            elif coluna == 0 and linha == 0:
                print("\n\t\tNenhuma falta detectada")
            else:
                print("\n\t\tFalta detectada, porém não foi possível realizar a reversão da mesma")

            event, value = janela.read()
