import HDGS2 as hd
from HDGSrender import NARROW as render
import LDGS as ld
from HDGSvfx import recolor, texture, expand
from random import randint
from time import sleep
from os import listdir
import HKeasyLAN as lan
from random import randint as rand

def IVM():
    global switch
    switch = False
    input("Invalid move")
def Blocked():
    global switch
    switch = False
    input("Move is blocked")
def intcheck(var):
    try:
        var = int(var)
        return var
    except Exception:
        print("ERROR: invalid input: input must be an integer")
        sleep(1)
        input("press enter\n")
        hd.clear()
        inputoff()
        return False

assets = open('pieces.grid', 'r')
assetct = len(assets.readlines()) - 2
assets.close()
pieces = []
for x in range(0, assetct):
    piece = hd.loadgrid('pieces.grid', x)
    # pieces.append(piece)
    # pieces.append(recolor(piece, [255, 0, 0], [0, 255, 255]))
    pieces.append(recolor(piece, [255, 0, 0], [42, 173, 40]))
    pieces.append(recolor(piece, [255, 0, 0], [155, 63, 217]))

assets = hd.loadgrid('board.grid')
boardfrags = []
boardfrags.append(assets)
boardfrags.append(recolor(assets, [225,177,117], [128,57,25]))

nettest = False

while True:
    hd.clear()
    try:
        localmp = input("Start/join a local multiplayer game? (Y/N): ")
        if localmp.lower() == 'y':
            localmp = True
            host = input("Start game as Host? (Y/N): ")
            if host.lower() == 'y':
                while True:
                    input_ = input("Enter board size (5-9): ")
                    if input_:
                        input_ = intcheck(input_)
                    else:
                        input_ = 7
                    if input_ > 4 and input_ < 10:
                        boardsize = [input_, input_]
                        break
                    else:
                        input("Invalid board size")
                        continue
                name = input("Enter your screen name: ")
                host = True
                if nettest:
                    IP = "127.0.0.1"
                    port = 9090
                else:
                    IP = lan.socket.gethostbyname(lan.socket.gethostname() + '.local')
                    port = rand(1, 65535)
                server = lan.serverStart(IP, port)
                print("Address: " + str(IP) + '.' + str(port))
                print("Waiting for second player...")
                connection = lan.serverWaitForClient(server)[0]
                sleep(0.1)
                lan.sendTo(str(boardsize[0]), connection)
                sleep(0.1)
                lan.sendTo(name, connection)
                names = [name, lan.recieveFrom(connection)]
                hd.clear()
                break
            else:
                name = input("Enter your screen name: ")
                host = False
                if nettest:
                    IP = "127.0.0.1"
                    port = 9090
                else:
                    address = input("Address: ").split('.')
                    IP = '.'.join(address[:-1])
                    port = int(address[-1])
                connection = lan.clientConnect(IP, port)
                print("Connecting...")
                input_ = int(lan.recieveFrom(connection))
                boardsize = [input_, input_]
                names = [lan.recieveFrom(connection), name]
                sleep(0.1)
                lan.sendTo(name, connection)
                hd.clear()
                break
        else:
            while True:
                input_ = input("Enter board size (5-9): ")
                if input_:
                    input_ = intcheck(input_)
                else:
                    input_ = 7
                if input_ > 4 and input_ < 10:
                    boardsize = [input_, input_]
                    break
                else:
                    input("Invalid board size")
                    continue
            names = (input("Enter name for player 1 (Green): "), input("Enter name for player 2 (Purple): "))
            localmp = False
            host = True
            hd.clear()
            break
    except Exception:
        print("Multiplayer Error")
        continue

file_ = open("layouts", 'r')
messylayouts = file_.readlines()
file_.close()
layouts = []
for line in messylayouts:
    layouts.append(line.rstrip())
layout = ld.reconstruct(boardsize[0], boardsize[1], layouts[boardsize[1] - 5])
board = hd.newgrid(boardsize[1] * 5 + 1, boardsize[0] * 10 + 2)
targetY = 0
alterY = False
for y in range(0, boardsize[1]):
    targetX = 0
    if alterY:
        alterY = False
    else:
        alterY = True
    alterX = alterY
    for x in range(0, boardsize[0]):
        if alterX:
            alterX = False
            board = hd.overlay(board, boardfrags[1], [targetX, targetY])
        else:
            alterX = True
            board = hd.overlay(board, boardfrags[0], [targetX, targetY])
        targetX += 10
    targetY += 5

board = texture(board, 4, 6)

# options (
movecheck = True
checksides = True
showchords = True
AllPieceWin = False
# )

while True:
    if localmp:
        streaming = 'n'
    else:
        streaming = input("Stream moves from file? (Y/N): ")
    if streaming.lower() == 'y' and not localmp:
        while True:
            filelist = []
            index = 1
            print("File list:")
            for fname in listdir():
                if "mo" + str(boardsize[0]) in fname:
                    print(str(index) + ': ' + fname[0:-4])
                    filelist.append(fname)
                    index += 1
            fileindex = intcheck(input("Enter your selection: "))
            if fileindex:
                if fileindex > len(filelist) or fileindex < 1:
                    print("ERROR: invalid input: input must be an integer within range")
                    input()
                    continue
                else:
                    filename = filelist[fileindex - 1]
                    break
            else:
                continue
        file_ = open(filename, 'r')
        messyrecord = file_.readlines()
        file_.close()
        record = []
        for line in messyrecord:
            record.append(line.rstrip())
        names = (record[0], record[1])
        playspeed = int(input("Enter playback time: ")) / (len(record) - 2)
        moveindex = 2
        streaming = True
        recording = False
    else:
        recording = input("Record moves to file? (Y/N): ")
        if recording.lower() == 'y':
            filename = input("Enter a name for the recording: ") + '.mo' + str(boardsize[0])
            record = open(filename, 'w')
            record.writelines((names[0] + '\n', names[1] + '\n'))
            record.close()
            recording = True
        else:
            recording = False
        streaming = False
    
    prompts = ["Make your move, ", "Your turn, "]
    sidebar = ['','','','',names[0] + ' (Green):','','','','','',names[1] + ' (Purple):','','','']
    arrange = layout
    p1 = True
    hd.clear()
    while True:
        switch = False
        gboard = board
        p1fp = 0
        p1piecect = 0
        p1royalct = 0
        p2fp = 0
        p2piecect = 0
        p2royalct = 0
        targetY = 1
        for row in arrange:
            targetX = 2
            for space in row:
                if space[0] == 'L':
                    if space[1] == '2':
                        p2piecect += 1
                        p2fp += 1
                    else:
                        p1piecect += 1
                        p1fp += 1
                    piece = 0
                elif space[0] == 'A':
                    if space[1] == '2':
                        p2piecect += 1
                        p2fp += 1
                    else:
                        p1piecect += 1
                        p1fp += 1
                    piece = 2
                elif space[0] == 'J':
                    if space[1] == '2':
                        p2piecect += 1
                        p2fp += 2
                    else:
                        p1piecect += 1
                        p1fp += 2
                    piece = 4
                elif space[0] == 'Q':
                    if space[1] == '2':
                        p2piecect += 1
                        p2royalct += 1
                        p2fp += 3
                    else:
                        p1piecect += 1
                        p1royalct += 1
                        p1fp += 3
                    piece = 6
                elif space[0] == 'K':
                    if space[1] == '2':
                        p2piecect += 1
                        p2royalct += 1
                        p2fp += 3
                    else:
                        p1piecect += 1
                        p1royalct += 1
                        p1fp += 3
                    piece = 8
                elif space[0] == 'M':
                    if space[1] == '2':
                        p2piecect += 1
                        p2fp += 4
                    else:
                        p1piecect += 1
                        p1fp += 4
                    piece = 10
                elif space[0] == 'N':
                    if space[1] == '2':
                        p2piecect += 1
                        p2fp += 4
                    else:
                        p1piecect += 1
                        p1fp += 4
                    piece = 12
                else:
                    piece = -1
                if piece > -1:
                    if space[1] == '2':
                        piece += 1
                    gboard = hd.superimpose(gboard, pieces[piece], [targetX, targetY])
                if showchords:
                    chords = [['38;2;0;0;0', str(targetX / 10 + 1), '38;2;0;0;0', ',', '0', ' ', '38;2;0;0;0', str(targetY / 5 + 1)]]
                    gboard = hd.superimpose(gboard, chords, [targetX + 2, targetY + 1])
                targetX += 10
            targetY += 5
        
        if p1:
            name = 0
        else:
            name = 1
        prompt = randint(0, len(prompts)-1)
        sidebar[1] = prompts[prompt] + names[name]
        sidebar[5] = "   Firepower remaining: " + str(p1fp)
        sidebar[6] = "   Pieces remaining: " + str(p1piecect)
        sidebar[7] = "   Royals remaining: " + str(p1royalct)
        sidebar[11] = "   Firepower remaining: " + str(p2fp)
        sidebar[12] = "   Pieces remaining: " + str(p2piecect)
        sidebar[13] = "   Royals remaining: " + str(p2royalct)
        hd.clear()
        # gboard = expand(gboard, 2)
        render(gboard, sidebar)
        
        
        pwin = False
        rwin = False
        if AllPieceWin:
            pass
        else:
            if p1royalct == 0:
                winner = names[1]
                rwin = True
            elif p2royalct == 0:
                winner = names[0]
                rwin = True
        if p1piecect < 3 and p2piecect > 3:
            winner = names[1]
            pwin = True
        elif p2piecect < 3 and p1piecect > 3:
            winner = names[0]
            pwin = True
        elif p2piecect < 3 and p2piecect < 3:
            input("It's a draw!")
            break
        if pwin and rwin:
            input(winner + " wins by Royal Domination!")
            break
        elif pwin:
            input(winner + " wins by Domination!")
            break
        elif rwin:
            input(winner + " wins by Assasination!")
            break
        

        if streaming:
            if len(record) < moveindex + 1:
                streaming = False
                recording = True
                input("Returning input to players")
                continue
            sleep(playspeed)
            move = record[moveindex].split(';')
            target = move[0].split(',')
            dest = move[1].split(',')
            moveindex += 1
        elif localmp:
            if p1 and host:
                target = input("Piece to move: ").strip(' ').split(',')
                dest = input("Location to move to: ").strip(' ').split(',')
                selfmove = True
            elif p1:
                print("Waiting for " + names[0] + "...")
                move = lan.recieveFrom(connection).split(';')
                target = move[0].split(',')
                dest = move[1].split(',')
                selfmove = False
            elif host:
                print("Waiting for " + names[1] + "...")
                move = lan.recieveFrom(connection).split(';')
                target = move[0].split(',')
                dest = move[1].split(',')
                selfmove = False
            else:
                target = input("Piece to move: ").split(',')
                dest = input("Location to move to: ").split(',')
                selfmove = True
        else:
            target = input("Piece to move: ").split(',')
            dest = input("Location to move to: ").split(',')
        try:
            target[0] = int(target[0])
            target[0] -= 1
            target[1] = int(target[1])
            target[1] -= 1
            targetdata = arrange[target[1]][target[0]]
            if targetdata == '--':
                input("That space does not have a piece on it")
                continue
            if checksides:
                if (p1 and (targetdata[1] == '2')) or ((not p1) and (targetdata[1] == '1')):
                    input("You can't move your opponents piece")
                    continue
            dest[0] = int(dest[0])
            dest[0] -= 1
            dest[1] = int(dest[1])
            dest[1] -= 1
            destdata = arrange[dest[1]][dest[0]]
            if checksides:
                if destdata[1] == targetdata[1]:
                    input("You can't eliminate your own piece")
                    continue
        except Exception:
            input("Input Error")
            continue
        else:
            switch = True
        
        changeX = dest[0] - target[0]
        changeY = dest[1] - target[1]
        absoluteX = abs(changeX)
        absoluteY = abs(changeY)
        negativeX = changeX < 0
        negativeY = changeY < 0
        
        if movecheck:
            if targetdata[0] == 'K':
                blocked = False
                if changeY == 0:
                    for x in range(0, absoluteX - 1):
                        if negativeX:
                            shift = target[0] + (x * -1) - 1
                        else:
                            shift = target[0] + x + 1
                        if not arrange[target[1]][shift] == '--':
                            blocked = True
                elif changeX == 0:
                    for x in range(0, absoluteY - 1):
                        if negativeY:
                            shift = target[1] + (x * -1) - 1
                        else:
                            shift = target[1] + x + 1
                        if not arrange[shift][target[0]] == '--':
                            blocked = True
                else:
                    IVM()
                    continue
                if blocked:
                    Blocked()
                    continue
            elif targetdata[0] == 'Q':
                blocked = False
                if (absoluteX == absoluteY):
                    for x in range(0, absoluteX - 1):
                        if negativeX:
                            shiftX = target[0] + (x * -1) - 1
                        else:
                            shiftX = target[0] + x + 1
                        if negativeY:
                            shiftY = target[1] + (x * -1) - 1
                        else:
                            shiftY = target[1] + x + 1
                        if not arrange[shiftY][shiftX] == '--':
                            blocked = True
                else:
                    IVM()
                    continue
                if blocked:
                    Blocked()
                    continue
            elif targetdata[0] == 'L':
                if (absoluteY + absoluteX) == 1:
                    pass
                else:
                    IVM()
                    continue
            elif targetdata[0] == 'A':
                if absoluteX == absoluteY and absoluteX == 1:
                    pass
                else:
                    IVM()
                    continue
            elif targetdata[0] == 'J':
                if (absoluteY == 1 and absoluteX == 2) or (absoluteY == 2 and absoluteX == 1):
                    pass
                else:
                    IVM()
                    continue
            elif targetdata[0] == 'M':
                if (absoluteY + absoluteX) == 1:
                    pass
                else:
                    blocked = False
                    if (absoluteX == absoluteY):
                        for x in range(0, absoluteX - 1):
                            if negativeX:
                                shiftX = target[0] + (x * -1) - 1
                            else:
                                shiftX = target[0] + x + 1
                            if negativeY:
                                shiftY = target[1] + (x * -1) - 1
                            else:
                                shiftY = target[1] + x + 1
                            if not arrange[shiftY][shiftX] == '--':
                                blocked = True
                    else:
                        IVM()
                        continue
                    if blocked:
                        Blocked()
                        continue
            elif targetdata[0] == 'N':
                if absoluteX == absoluteY and absoluteX == 1:
                    pass
                else:
                    blocked = False
                    if changeY == 0:
                        for x in range(0, absoluteX - 1):
                            if negativeX:
                                shift = target[0] + (x * -1) - 1
                            else:
                                shift = target[0] + x + 1
                            if not arrange[target[1]][shift] == '--':
                                blocked = True
                    elif changeX == 0:
                        for x in range(0, absoluteY - 1):
                            if negativeY:
                                shift = target[1] + (x * -1) - 1
                            else:
                                shift = target[1] + x + 1
                            if not arrange[shift][target[0]] == '--':
                                blocked = True
                    else:
                        IVM()
                        continue
                    if blocked:
                        Blocked()
                        continue
        
        if switch:
            if p1:
                p1 = False
            else:
                p1 = True
        
        if recording:
            move = str(target[0] + 1) + ',' + str(target[1] + 1) + ';' + str(dest[0] + 1) + ',' + str(dest[1] + 1)
            record = open(filename, 'a')
            record.write(move + '\n')
            record.close()
        if localmp and selfmove:
            move = str(target[0] + 1) + ',' + str(target[1] + 1) + ';' + str(dest[0] + 1) + ',' + str(dest[1] + 1)
            lan.sendTo(move, connection)
        
        arrange = ld.editgrid(dest[1], dest[0], arrange, targetdata)
        arrange = ld.editgrid(target[1], target[0], arrange, '--')
















