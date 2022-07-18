
# default renderers for HDGS

def GGF(grid):
    for x in grid:
        index = 0
        chdata = False
        line = '|'
        for y in x:
            if chdata:
                chdata = False
                if index < len(x) - 1:
                    if x[index - 1] == x[index + 1] or len(y)>1:
                        gapfill = "\033[" + x[index - 1] + "m"
                        if x[index] == x[index + 2] or len(y)>1:
                            if len(y)>1 and y[-2:] == '-g':
                                gapfill = gapfill + ' '
                            else:
                                gapfill = gapfill + y
                        else:
                            gapfill = gapfill + ' '
                        y = "\033[" + x[index - 1] + "m" + y[0] + "\033[0m"
                        line = line + y + gapfill
                    else:
                        y = "\033[" + x[index - 1] + "m" + y + "\033[0m"
                        line = line + y + ' '
                else:
                    y = "\033[" + x[index - 1] + "m" + y + "\033[0m"
                    line = line + y + '|'
            else:
                chdata = True    
            index += 1
        print(line)



def NARROW(grid, sideprint=[]):
    row = 0
    for x in grid:
        index = 0
        chdata = False
        line = '|'
        for y in x:
            if chdata:
                chdata = False
                y = y[0]
                if index < len(x) - 1:
                    y = "\033[" + x[index - 1] + "m" + y + "\033[0m"
                    line = line + y
                else:
                    y = "\033[" + x[index - 1] + "m" + y + "\033[0m"
                    line = line + y + '|'
            else:
                chdata = True    
            index += 1
        if row < len(sideprint):
            line = line + ' ' + sideprint[row]
        print(line)
        row += 1



def BLOCKS(grid, sideprint=[]):
    row = 0
    for x in grid:
        index = 0
        chdata = False
        line = '|'
        for y in x:
            if chdata:
                chdata = False
                if len(y)>1 and y[-2:] == '-g':
                    y = y[0]
                    pix = y + ' '
                else:
                    y = y[0]
                    pix = y * 2
                if index < len(x) - 1:
                    pix = "\033[" + x[index - 1] + "m" + pix + "\033[0m"
                    line = line + pix
                else:
                    pix = "\033[" + x[index - 1] + "m" + pix + "\033[0m"
                    line = line + pix + '|'
            else:
                chdata = True    
            index += 1
        if row < len(sideprint):
            line = line + ' ' + sideprint[row]
        print(line)
        row += 1



def transrender(grid, renderer):
    if renderer == 'GGF':
        base = newgrid(len(grid),len(grid[0])-1)
        row = 0
        for x in grid:
            column = 0
            chdata = False
            for y in x:
                pix = ''
                if chdata:
                    chdata = False
                    if column < len(x) - 1:
                        if x[column - 1] == x[column + 1] or len(y)>1:
                            gapform = x[column - 1]
                            if x[column] == x[column + 2] or len(y)>1:
                                if len(y)>1 and y[-2:] == '-g':
                                    y = y[0]
                                    gapfill = ' '
                                else:
                                    y = y[0]
                                    gapfill = y
                            else:
                                gapfill = ' '
                            pix = y + gapfill
                        else:
                            gapform = '0'
                            pix = y + ' '
                    else:
                        pix = y
                    form = x[column - 1]
                    editcolumn = column * 2 - 1
                    base[row][editcolumn] = pix[0]
                    base[row][editcolumn-1] = form
                    if len(pix) > 1:
                        base[row][editcolumn + 2] = pix[1]
                        base[row][editcolumn + 1] = gapform
                else:
                    chdata = True
                column += 1
            row += 1
        return base
    elif renderer == 'BLOCKS':
        base = newgrid(len(grid),len(grid[0]))
        row = 0
        for x in grid:
            column = 0
            chdata = False
            for y in x:
                if chdata:
                    chdata = False
                    if len(y)>1 and y[-2:] == '-g':
                        y = y[0]
                        pix = y + ' '
                    else:
                        y = y[0]
                        pix = y * 2
                    form = x[column - 1]
                    editcolumn = column * 2 - 1
                    base[row][editcolumn] = pix[0]
                    base[row][editcolumn - 1] = form
                    base[row][editcolumn + 2] = pix[1]
                    base[row][editcolumn + 1] = form
                else:
                    chdata = True    
                column += 1
            row += 1
        return base
    else:
        print("a transrenderer for '" + renderer + "' does not exist")

