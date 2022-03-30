# Zelda
import pgzrun
import math
from pygame import image, Color

link = Actor("link_1",center=(400,400))
link.frame = link.movex = link.movey = link.dir = link.testx = link.testy = 0
sword = Actor("sword_1",center=(400,400))
sword.frame = sword.dir = 0
myDirs = [(0,1),(-1,0),(0,-1),(1,0)]
monstersXY = [(1325,375),(1025,-225),(300,-225),(1925,-225),(1925,375)]
monsters = []
for m in monstersXY:
    monsters.append(Actor('monster_1', center=(m[0], m[1])))
    l = len(monsters)-1
    monsters[l].state = 10
    monsters[l].frame = monsters[l].movex = monsters[l].movey = monsters[l].dir = monsters[l].testx = monsters[l].testy = 0
    
mymap = image.load('images/map.png')
mapx = 0
mapy = 10
mapScrollx = 0
mapScrolly = 0

def draw():
    screen.clear()
    screen.blit("logo",(612,10))
    screen.draw.text("W, A, S, D TO MOVE", center= (440, 30), color=(0,255,0) , fontsize=30)
    screen.draw.text("SPACE TO USE SWORD", center= (440, 70), color=(0,255,0) , fontsize=30)
    drawMap()
    drawChars()
    
def drawMap():
    xtest = math.floor(link.x/50 + (link.movex))
    ytest = math.floor((link.y-100)/50 + (link.movey))
    for x in range(16):
        for y in range(10):
            col = mymap.get_at((x+mapx,y+mapy))
            if col == (0,255,0): screen.blit("tree",(x*50,(y*50)+100))
            if col == (0,0,0): screen.blit("ground",(x*50,(y*50)+100))
            if col == (255,0,0): screen.blit("boulder",(x*50,(y*50)+100))
            if col == (255,255,0): screen.blit("rock",(x*50,(y*50)+100))
    maprect = Rect((10, 10), (266, 80))
    screen.draw.filled_rect(maprect, (100, 100, 100))
    mx = (mapx*50)+link.x
    my = (mapy*50)+link.y
    linkrect = Rect(((mx/12)+10, (my/12)), (4, 4))
    screen.draw.filled_rect(linkrect, (0, 255, 0))
    
def drawChars():
    link.image = "link_"+str(((link.dir*2)+1)+math.floor(link.frame/10))
    if sword.frame > 0 and sword.dir == 2:
        sword.draw()
    link.draw()
    if sword.frame > 0 and sword.dir != 2:
        sword.draw()
    for m in monsters:
        if onScreen(m.x,m.y) and m.state > 0:
            if m.state < 10:
                m.angle += 10
                m.state -= 1
            if m.state == 10: m.image = "monster_"+str(((m.dir*2)+1)+math.floor(m.frame/10))
            m.draw()
    
def update():
    global mapScrollx, mapScrolly,mapx,mapy
    checkInput()
    moveChars()
    if(mapScrollx > 0): mapScroll(1,0)
    if(mapScrollx < 0): mapScroll(-1,0)
    if(mapScrolly > 0): mapScroll(0,1)
    if(mapScrolly < 0): mapScroll(0,-1)
    if sword.frame > 0:
        if(sword.frame > 5):
            sword.x += myDirs[sword.dir][0]*2
            sword.y += myDirs[sword.dir][1]*2
        else:
            sword.x -= myDirs[sword.dir][0]*2
            sword.y -= myDirs[sword.dir][1]*2
        sword.frame -= 1
        for m in monsters:
            if m.collidepoint((sword.x, sword.y)):
                m.state = 9
            
def mapScroll(x,y):
    global mapScrollx, mapScrolly,mapx,mapy
    mapx += x
    mapScrollx -= x
    link.x -= x*50
    mapy += y
    mapScrolly -= y
    link.y -= y*50
    for m in monsters:
        m.x -= x*50
        m.y -= y*50

def checkInput():
    if keyboard.a: link.movex = -1
    if keyboard.d: link.movex = 1
    if keyboard.w: link.movey = -1
    if keyboard.s: link.movey = 1

def on_key_down(key):
    if key.name == "SPACE":
        sword.frame = 10
        sword.dir = link.dir
        sword.image = "sword_"+str(sword.dir)
        sword.x = link.x + (myDirs[sword.dir][0]*30)
        sword.y = link.y + (myDirs[sword.dir][1]*30)

def moveChars():
    global mapScrollx,mapScrolly,mapx,mapy
    getCharDir(link)
    if link.movex or link.movey:
        link.frame += 1
        if link.frame >= 20: link.frame = 0
        if link.movex == 1:
            link.testx = round((link.x-48)/50 + (link.movex))
        else:
            link.testx = round((link.x)/50 + (link.movex))
        if link.movey == 1:
            link.testy = round((link.y-148)/50 + (link.movey))
        else:
            link.testy = round((link.y-100)/50 + (link.movey))
        testmove = (link.testx+mapx,link.testy+mapy)
        if mymap.get_at(testmove) == Color('black'):
            link.x += link.movex*2
            link.y += link.movey*2
        link.movex = 0
        link.movey = 0
        if link.x > 800 and mapScrollx == 0:
            mapScrollx = 16
        if link.x < 0 and mapScrollx == 0:
            mapScrollx = -16
        if link.y > 600 and mapScrolly == 0:
            mapScrolly = 10
        if link.y < 100 and mapScrolly == 0:
            mapScrolly = -10
    for m in monsters:
        if onScreen(m.x,m.y) and m.state == 10:
            if (m.x > link.x+50):
                m.movex = -1
                m.testx = round((m.x)/50 + (m.movex))
            else:
                if (m.x < link.x-50):
                    m.movex = 1
                    m.testx = round((m.x-48)/50 + (m.movex))
            if (m.y > link.y+50):
                m.movey = -1
                m.testy = round((m.y-100)/50 + (m.movey))
            else:
                if (m.y < link.y-50):
                    m.movey = 1
                    m.testy = round((m.y-148)/50 + (m.movey))
            getCharDir(m)
            if m.movex or m.movey:
                m.frame += 1
                if m.frame >= 20: m.frame = 0
                testmove = (m.testx+mapx,m.testy+mapy)
                if mymap.get_at(testmove) == Color('black'):
                    m.x += m.movex*2
                    m.y += m.movey*2
                m.movex = 0
                m.movey = 0

def getCharDir(ch):
    for d in range(len(myDirs)):
        if myDirs[d] == (ch.movex,ch.movey):
            ch.dir = d

def onScreen(x,y):
    if(x>0 and x<800 and y>100 and y<800): return True
    return False

pgzrun.go()
