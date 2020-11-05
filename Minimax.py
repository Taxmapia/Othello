from Funciones import *
from Constantes import *
import math


def Mobility(jogador_val,karen_val):
    
    if len(jogador_val) < len(karen_val):
        m = (100.0 * jogador_val)/(jogador_val + karen_val)
    elif len(jogador_val) < len(karen_val):
        m = -(100.0 * jogador_val)/(jogador_val + karen_val)
    else: 
        m = 0
    return m
        

def Minimax(tablero,profundidad,f_jogador,f_karen):
    n_tab = tablero
    mejor_jugada = -math.inf

    movs_k = Mov_Valido(tablero,f_karen)
    movs_j = Mov_Valido(tablero,f_jogador)
    if movs_k == [] or profundidad == 0:
        return (-1,-1), Mobility(f_jogador,f_karen)
    else:
        for i in movs_k:
            n_tab = Valida_Mov(tablero,f_karen,i[0],i[1])
            if f_karen == FICHA_B:
                sig_j = FICHA_N
            else:
                sig_j = FICHA_B
            nueva_jugada , nuevo_puntaje = Minimax(n_tab,sig_j,profundidad-1,f_jogador,f_karen)
            if nuevo_puntaje > mejor_jugada:
                mejor_jugada = nuevo_puntaje
                mejor_movimiento=i
        return mejor_movimiento, mejor_jugada











































'''
def Num_Movimientos_Validos(self, opp, tablero):
	cont = 0
	for i in 6:
	    for j in 6:
	        if isLegalMove:
	return cont

def canmove(self,opp, *str):
	if not str[0] == opp:
    return False
	for (int ctr = 1; ctr < 8; ctr++) 
		if (str[ctr] == '-') return false;
		if (str[ctr] == self) return true;
	
	return false;


def isLegalMove(self, opp, grid,startx,starty):
	if(grid[startx][starty] != '-'):
        return false
	char str[10]
	int x, y, dx, dy, ctr
	for (dy = -1; dy <= 1; dy++)
		for (dx = -1; dx <= 1; dx++)    
	// keep going if both velocities are zero
			if (!dy && !dx) continue
			str[0] = '\0'
			for (ctr = 1; ctr < 8; ctr++)   
				x = startx + ctr*dx
				y = starty + ctr*dy
				if (x >= 0 && y >= 0 && x<8 && y<8) str[ctr-1] = grid[x][y]
				else str[ctr-1] = 0;
			
			if (canmove(self, opp, str)) return true
		
	return false
'''