from copy import deepcopy as copy
from os import system

# version 2.2

def clear():
    system('clear')

def inputoff():
    system('stty -echo')

def inputon():
    system('stty echo')

def getrows():
    system('tput lines')
    
def getrows():
    system('tput cols')



def overlay(maingrid, layergrid, overlaypoint):
    xconst = list(overlaypoint)
    newgrid = list(maingrid)
    xconst[0] = xconst[0] * 2
    point = copy(xconst)
    for row in layergrid:
        for character in row:
            newgrid[point[1]][point[0]] = character
            point[0] += 1
        point[0] = xconst[0]
        point[1] += 1
    return newgrid



def muting_overlay(maingrid, layergrid, overlaypoint):
    xconst = list(overlaypoint)
    newgrid = maingrid
    xconst[0] = xconst[0] * 2
    point = list(xconst)
    for row in layergrid:
        for character in row:
            newgrid[point[1]][point[0]] = character
            point[0] += 1
        point[0] = xconst[0]
        point[1] += 1
    return newgrid



def superimpose(maingrid, layergrid, overlaypoint):
    chdata = False
    xconst = copy(overlaypoint)
    newgrid = copy(maingrid)
    xconst[0] = xconst[0] * 2
    point = copy(xconst)
    for row in layergrid:
        for character in row:
            if chdata:
                chdata = False
                if character == ' ' and transparent:
                    newgrid[point[1]][point[0]] = maingrid[point[1]][point[0]]
                else:
                    newgrid[point[1]][point[0]] = character
            else:
                chdata = True
                if character == '0':
                    transparent = True
                    newgrid[point[1]][point[0]] = maingrid[point[1]][point[0]]
                elif not '48;2;' in character:
                    transparent = True
                    colorindex = maingrid[point[1]][point[0]].find('48;2;')
                    pointcolor = ';'.join(maingrid[point[1]][point[0]][colorindex:].split(';')[:5])
                    newgrid[point[1]][point[0]] = character + ';' + pointcolor
                else:
                    transparent = False
                    newgrid[point[1]][point[0]] = character
            point[0] += 1
        point[0] = xconst[0]
        point[1] += 1
    return newgrid



def slicegrid(grid, start, end):
    gridslice = []
    end[1] += 1
    end[0] += 1
    start[0] = (start[0] * 2)
    end[0] = (end[0] * 2)
    for row in grid[start[1]:end[1]]:
        gridslice.append(row[start[0]:end[0]])
    return gridslice



def editgrid(row, column, grid, newchr, newform='0'):
    formcolumn = (column * 2)
    charcolumn = formcolumn + 1
    newgrid = copy(grid)
    newgrid[int(row)][int(charcolumn)] = newchr
    newgrid[int(row)][int(formcolumn)] = newform
    return newgrid



def newgrid(hight, width, fillchr=" ", fillform="0"):
    grid = []
    for x in range(0, hight):
        grid.append([])
    for y in grid:
        for z in range(0, width):
            y.append(fillform)
            y.append(fillchr)
    return grid



def flatten(grid):
    strlist = ''
    for group in grid:
        for item in group:
            strlist = strlist + item + "`"
    strlist = strlist[:-1]
    return strlist



def reconstruct(xbound, ybound, flatgrid):
    fgrid = flatgrid.split("`")
    grid = []
    index = 0
    for y in range(0, ybound):
        subgrid = []
        for x in range(0, xbound):
            subgrid.append(fgrid[index])
            index += 1
        grid.append(subgrid)
    return grid



def loadgrid(filename, miftarget=0):
    target = miftarget + 2
    file_ = open(filename, 'r')
    lines = file_.readlines()
    file_.close()
    filedata = []
    for item in lines:
        filedata.append(item.strip('\n'))
    xbound = int(filedata[0])
    ybound = int(filedata[1])
    fgrid = filedata[target].split("`")
    grid = []
    index = 0
    for y in range(0, ybound):
        subgrid = []
        for x in range(0, xbound):
            subgrid.append(fgrid[index])
            index += 1
        grid.append(subgrid)
    return grid



def savegrid(grid, filename):
    ybound = len(grid)
    xbound = len(grid[0])
    file_ = open(filename, 'w')
    index = 0
    strlist = ''
    for group in grid:
        for item in group:
            strlist = strlist + item + "`"
        index += 1
    strlist = strlist[:-1]
    data = [str(xbound), str(ybound), strlist]
    for item in data:
        file_.write(item + '\n')
    file_.close()



def appendgrid(grid, filename, forced=False):
    file_ = open(filename, 'r+')
    lines = file_.readlines()
    ywid = str(len(grid))
    xwid = str(len(grid[0]))
    if (xwid == lines[0].strip('\n') and ywid == lines[1].strip('\n')) or forced:
        file_.write(flatten(grid)+'\n')
        file_.close()
        return True
    else:
        print("grid size does not match file perameters")
        file_.close()
        return False



def replacegrid(grid, filename, miftarget, forced=False):
    file_ = open(filename, 'r')
    lines = file_.readlines()
    ywid = str(len(grid))
    xwid = str(len(grid[0]))
    if (xwid == lines[0].strip('\n') and ywid == lines[1].strip('\n')) or forced:
        lines[miftarget+2] = flatten(grid) + '\n'
        file_ = open(filename, 'w')
        for line in lines:
            file_.write(line)
        file_.close()
        return True
    else:
        print("grid size does not match file perameters")
        file_.close()
        return False
    
        




