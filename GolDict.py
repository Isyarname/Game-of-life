from matrix_reload import *
from copy import copy, deepcopy
from random import randint, choice
import pygame as p
import sys


Width = 200
Height = 150

tileSize = 3


clock = p.time.Clock()
p.init()
surf = p.display.set_mode((Width * tileSize, Height * tileSize))
matrix = Matrix(Width, Height, homogeneous=True, value=0)
countDict = {}
points = []
gliderl =  [[0,1,0],
			[0,0,1],
			[1,1,1]]
kl = [[0,0,1],
	  [1,1,1],
	  [0,0,1]]
glider = Matrix(ls=gliderl)
k = Matrix(ls=kl)

def o(x,y):
	pass

def prikol(a=3):
	for i in range(0, a):											# количество групп
		d = 5														# диаметр разброса клеток
		sx, sy = randint(0, Width-d-1), randint(0, Height-d-1)
		for j in range(0,9):										# максимальное число клеток в группе
			matrix[randint(0, d) + sy][randint(0, d) + sx] = 1


def glideromet(y, x, figure):
	tm = turner(figure, choice((1, -1, 2, 0)))
	for i in range(3):
		for j in range(3):
			matrix[y+i-len(matrix)][x+j-len(matrix[0])] = tm[i][j]
			if tm[i][j] == 1:
				count(y+i, x+j)

def count(y, x):
	ym = (y-1) % Height
	yp = (y+1) % Height
	xm = (x-1) % Width
	xp = (x+1) % Width
	p = [[ym,xm], [ym,x], [ym,xp], [y,xm], 
			[y,xp], [yp,xm], [yp,x], [yp,xp]]
	for i in p:
		if not i[0] in countDict.keys():
			countDict.update({i[0]:{i[1]:1}})
			continue
		elif not i[1] in countDict[i[0]].keys():
			countDict[i[0]].update({i[1]:1})
			continue
		countDict[i[0]][i[1]] += 1

def play():
	tm = matrix.copy()
	tcd = countDict.copy()
	countDict.clear()
	for y in tcd.keys():
		for x in tcd[y].keys():
			matrix[y][x] = rules[tm[y][x]][tcd[y][x]]
			if matrix[y][x] == 1:
				count(y, x)
			form = [(x*tileSize, y*tileSize), (x*tileSize, y*tileSize + tileSize-2),
			(x*tileSize + tileSize-2, y*tileSize + tileSize-2), (x*tileSize + tileSize-2, y*tileSize)]
			color = colors[matrix[y][x]]
			p.draw.polygon(surf, color, form)


def events():
	for event in p.event.get():
		if event.type == p.QUIT:
			p.quit()
			sys.exit()
		elif event.type == p.MOUSEBUTTONDOWN:
			x, y = event.pos[0] // tileSize, event.pos[1] // tileSize
			matrix[y][x] = 1
			glideromet(y, x, glider)

	

rules = [{0:0, 1:0, 2:0, 3:1, 4:0, 5:0, 6:0, 7:0, 8:0},
		 {0:0, 1:0, 2:1, 3:1, 4:0, 5:0, 6:0, 7:0, 8:0}]
colors = {0:(0,0,0), 1:(255, 255, 255)}
R, G = 0, 20
gradationR, gradationG = "+", "+"
def background(R, G, gradationR, gradationG):
	if gradationR == "+":
		R += 1
		if R >= 40:
			gradationR = "-"
	elif gradationR == "-":
		R -= 1
		if R <= 0:
			gradationR = "+"
	if gradationG == "+":
		G += 1
		if G >= 40:
			gradationG = "-"
	elif gradationG == "-":
		G -= 1
		if G <= 0:
			gradationG = "+"
	surf.fill((R, G, 81-R-G))
	return R, G, gradationR, gradationG

for x in range(Width):
	for y in range(Height):		
		form = [(x*tileSize, y*tileSize), (x*tileSize, y*tileSize + tileSize-2),
		(x*tileSize + tileSize-2, y*tileSize + tileSize-2), (x*tileSize + tileSize-2, y*tileSize)]
		color = colors[matrix[y][x]]
		p.draw.polygon(surf, color, form)
while True:
	#print(m)
	R, G, gradationR, gradationG = background(R, G, gradationR, gradationG)
	pos = p.mouse.get_pos()
	p.draw.circle(surf, (R*3+130, G*3, (81-R-G)*3), pos, 15) #255, 0, 50
	events()
	play()


	clock.tick()
	p.display.set_caption(str(clock))
	p.display.update()
	p.display.flip()