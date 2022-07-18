from random import randint, seed
from copy import deepcopy as copy
# default visual effects pack for HDGS

# version 1.3

# an algorithm to add color texture to HD grids
def texture_surface(grid, dip=20, lift=10, threshold=6, seed_=None):
    dgrid = copy(grid)
    threshold = threshold - 1
    seed(seed_)
    formdata = True
    row = 0
    for rowlist in dgrid:
        column = 0
        for point in rowlist:
            if formdata:
                colorindex = point.find('48;2;')+5
                formdata = False
                pointcolor = point[colorindex:].split(';')[:3]
                surface = []
                flat = 0
                for pix in range(0,8):
                    if pix == 0:
                        offset = '-1,-2'
                    elif pix == 1:
                        offset = '-1,0'
                    elif pix == 2:
                        offset = '-1,2'
                    elif pix == 3:
                        offset = '0,-2'
                    elif pix == 4:
                        offset = '0,2'
                    elif pix == 5:
                        offset = '1,-2'
                    elif pix == 6:
                        offset = '1,0'
                    elif pix == 7:
                        offset = '1,2'
                    shifts = offset.split(',')
                    altrow = row + int(shifts[0])
                    altcolumn = column + int(shifts[1])
                    if not ((altrow < 0 or altcolumn < 0) or (altrow > len(grid)-1 or altcolumn > len(grid[0])-1)):
                        pixcolor = grid[altrow][altcolumn][colorindex:].split(';')[:3]
                        surface.append(offset + '`' + ';'.join(pixcolor))
                        if pixcolor == pointcolor:
                            flat += 1
                if flat >= threshold:
                    for pix in surface:
                        pix = pix.split('`')
                        offset = pix[0].split(',')
                        color = pix[1].split(';')
                        if color == pointcolor:
                            pixform = grid[row+int(offset[0])][column+int(offset[1])][colorindex:].split(';')
                            spare = grid[row+int(offset[0])][column+int(offset[1])][:colorindex]
                            shift = randint(dip*-1, lift)
                            index = 0
                            if not color == ['']:
                                for channel in color:
                                    channelcolor = int(channel) + shift
                                    if channelcolor > 255:
                                        channelcolor = 255
                                    if channelcolor < 0:
                                        channelcolor = 0
                                    pixform[index] = str(channelcolor)
                                    index += 1
                                dgrid[row+int(offset[0])][column+int(offset[1])] = spare + (';'.join(pixform))
                column += 2
            else:
                formdata = True
        row += 1
    return dgrid

def texture(grid, dip=20, lift=10, seed_=None):
    dgrid = copy(grid)
    seed(seed_)
    formdata = True
    row = 0
    for rowlist in dgrid:
        column = 0
        for point in rowlist:
            if formdata:
                colorindex = point.find('48;2;')+5
                formdata = False
                color = point[colorindex:].split(';')[:3]
                pixform = grid[row][column][colorindex:].split(';')
                spare = grid[row][column][:colorindex]
                shift = randint(dip*-1, lift)
                index = 0
                if not color == ['']:
                    for channel in color:
                        channelcolor = int(channel) + shift
                        if channelcolor > 255:
                            channelcolor = 255
                        if channelcolor < 0:
                            channelcolor = 0
                        pixform[index] = str(channelcolor)
                        index += 1
                    dgrid[row][column] = spare + (';'.join(pixform))
                column += 2
            else:
                formdata = True
        row += 1
    return dgrid

def texture_area(grid, start, end, dip=20, lift=10, seed_=None):
    from HDGS2 import slicegrid, overlay
    fgrid = copy(grid)
    dgrid = slicegrid(grid, start, end)
    dgrid = texture(dgrid)
    fgrid = overlay(fgrid, dgrid, start)
    return fgrid



# an algorithm to replace a color with another color in a grid
def recolor(grid, color, newcolor, text=False):
    colorindex = 0
    for item in color:
        color[colorindex] = str(item)
        colorindex += 1
    colorindex = 0
    for item in newcolor:
        newcolor[colorindex] = str(item)
        colorindex += 1
    dgrid = copy(grid)
    
    formdata = True
    row = 0
    for rowlist in grid:
        column = 0
        for point in rowlist:
            if formdata:
                if text:
                    colorindex = point.find('38;2;')+5
                else:
                    colorindex = point.find('48;2;')+5
                formdata = False
                pointcolor = point[colorindex:].split(';')[:3]
                if pointcolor == color:
                    colorchannel = 0
                    pointform = point[colorindex:].split(';')
                    spare = point[:colorindex]
                    for item in newcolor:
                        pointform[colorchannel] = item
                        colorchannel += 1
                    dgrid[row][column] = spare + (';'.join(pointform))
            else:
                formdata = True
            column += 1
        row += 1
    return dgrid

def recolor_area(grid, start, end, color, newcolor, text=False):
    from HDGS2 import slicegrid, overlay
    fgrid = copy(grid)
    dgrid = slicegrid(grid, start, end)
    dgrid = recolor(dgrid, color, newcolor, text)
    fgrid = overlay(fgrid, dgrid, start)
    return fgrid



# an algorithm that blurs colors in a grid
def blur(grid):
    dgrid = copy(grid)
    formdata = True
    row = 0
    for rowlist in grid:
        column = 0
        for point in rowlist:
            if formdata:
                colorindex = point.find('48;2;')+5
                pointcolor = point[colorindex:].split(';')[:3]
                formdata = False
                newcolor = ['0','0','0']
                fullpix = 1
                for pix in range(0,8):
                    if pix == 0:
                        offset = '-1,-2'
                    elif pix == 1:
                        offset = '-1,0'
                    elif pix == 2:
                        offset = '-1,2'
                    elif pix == 3:
                        offset = '0,-2'
                    elif pix == 4:
                        offset = '0,2'
                    elif pix == 5:
                        offset = '1,-2'
                    elif pix == 6:
                        offset = '1,0'
                    elif pix == 7:
                        offset = '1,2'
                    else:
                        break
                    shifts = offset.split(',')
                    altrow = row + int(shifts[0])
                    altcolumn = column + int(shifts[1])
                    if not ((altrow < 0 or altcolumn < 0) or (altrow > len(grid)-1 or altcolumn > len(grid[0])-1)):
                        pixcolor = grid[altrow][altcolumn][colorindex:].split(';')[:3]
                        if not (pixcolor == [''] or pointcolor == ['']):
                            blankcolor = []
                            for x in range(0,3):
                                newchannel = int(pixcolor[x]) + int(newcolor[x])
                                blankcolor.append(newchannel)
                            fullpix += 1
                            newcolor = blankcolor
                if not (newcolor == [''] or pointcolor == ['']):
                    blankcolor = []
                    for x in range(0,3):
                        newchannel = (int(pointcolor[x])*(10-fullpix)) + int(newcolor[x])
                        blankcolor.append(newchannel)
                    newcolor = blankcolor
                    blankcolor = []
                    for x in newcolor:
                        blankcolor.append(str(int(int(x)/9)))
                    newcolor = blankcolor
                    colorchannel = 0
                    pointform = point[colorindex:].split(';')
                    spare = point[:colorindex]
                    for item in newcolor:
                        pointform[colorchannel] = item
                        colorchannel += 1
                    dgrid[row][column] = spare + (';'.join(pointform))
            else:
                formdata = True
            column += 1
        row += 1
    return dgrid



def blur_area(grid, start, end):
    from HDGS2 import slicegrid, overlay
    fgrid = copy(grid)
    dgrid = slicegrid(grid, start, end)
    dgrid = blur(dgrid)
    fgrid = overlay(fgrid, dgrid, start)
    return fgrid



def expand(grid, factor):
    from HDGS2 import newgrid, overlay
    base = newgrid(len(grid)*factor,int(len(grid[0])/2)*factor)
    row = 0
    for x in grid:
        column = 0
        chdata = False
        for y in x:
            if chdata:
                pix = newgrid(factor, factor, grid[row][column], grid[row][column-1])
                base = overlay(base, pix, [int(((column*factor)-factor)/2),row*factor])
                chdata = False
            else:
                chdata = True
            column += 1
        row += 1
    return base






