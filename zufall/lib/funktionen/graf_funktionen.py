#!/usr/bin/python
# -*- coding utf-8 -*-

          
		  
#
#  zufall-Funktionen für Grafik                    
#                                                 
#                                                
                                  
#
#  This file is part of zufall
#
#
#  Copyright (c) 2019 Holger Böttcher  hbomat@posteo.de
#
#
#  Licensed under the Apache License, Version 2.0 (the "License")
#  you may not use this file except in compliance with the License
#  You may obtain a copy of the License at
#  
#      http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#  



# Inhalt:
#
#   balken1		Balkendiagramm 1 (Wahrscheinlichkeiten, Relative Häufigkeiten)
#   balken2		Balkendiagramm 2 (Absolute Häufigkeiten, DatenReihe)
#   balken_plus_balken		Vergleich 2-er Verteilungen (Wahrscheinlichkeiten, Relative Häufigkeiten)
#   balken_plus_stetig		Vergleich einer Verteilung mit einer stetigen (Wahrscheinlichkeiten, Relative Häufigkeiten)
#   polygon_zug		Polygonzug
#   poly_plus_poly   Vergleich 2-er Verteilungen (Wahrscheinlichkeiten, Relative Häufigkeiten)
#   vert_funktion   Verteilungsfunktion



import importlib

import numpy as np
from scipy.stats import norm, expon

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from sympy import floor

import zufall




# ----------------
# Balkendiagramm 1
# ----------------

def  balken1(daten, typ=None, titel=None, mark=None, ylabel=None):
    # daten dict( {k:f(k)}, ...) - Verteilung
    # typ: 'W' - Wahrscheinlichkeiten
    #      'R' - Relative Häufigkeiten
    
    n = len(daten.keys())
    if n-1 > 1000:
        print('zufall: nicht implementiert (Anzahl zu groß)')
        return
    
    print(' ')
    	
    plt.close('all')		
    fig = plt.figure(figsize=(4, 3))
    ax = fig.add_subplot(1, 1, 1)
    ymax = max(daten.values())
    plt.ylim(0, 1.4*float(ymax))	

    lw = 0.7			
    if typ =='W':
        fc = (1,1,0.6)   # RGB::YellowLight
        fcm = (1.0, 0.689993, 0.059999)   # RGB::CadmiumYellowLight
        ec = (0.6,0.2,0)   # RGB::Brown
        xlabel = "$k$"
        if not ylabel:
            ylabel = "$P\,(X \,=\, k)$"
    elif typ == "R":
        fc = (0.6039, 0.803903, 0.196097)   # RGB::YellowGreen
        ec = (0.333293, 0.419599, 0.184301)   # RGB::OliveGreenDark
        fcm = (0.333293, 0.419599, 0.184301)   # RGB::OliveGreenDark
        xlabel = "$k$"
        ylabel = "$Rel. \; H. $"
    elif typ == "A":
        fc = (0.8, 0.8, 0.8)   # RGB::Grey80
        ec = (0.333333, 0.333333, 0.333333)  # RGB::DarkGrey
        fcm = (0.333333, 0.333333, 0.333333)  
        xlabel = "$k$"
        ylabel = "$Abs. H.$"
        
    xpos, ypos = 0.05, 0   
	
    d1 = [[e, daten[e]] for e in daten]
    f = lambda x: x[0]
    d1.sort(key=f)
    daten1 = d1

    for k in daten1:  
        if mark and k[0] in mark:	
            re = patches.Rectangle((xpos, ypos), 0.1, k[1], lw=lw, 
                 facecolor=fcm, edgecolor=ec)
        else:			
            re = patches.Rectangle((xpos, ypos), 0.1, k[1], lw=lw,
                 facecolor=fc, edgecolor=ec)
        plt.gca().add_patch(re)
        xpos += 0.1	
	
    plt.title(titel, fontsize=10.5, color=(0.2, 0.2, 0.2))
    plt.xlabel(xlabel, fontsize=10)
    plt.ylabel(ylabel, fontsize=10)
    
    if n < 20:
        dx = 1
    elif n < 40:
        dx = 5 
    elif n < 150:
        dx = 10
    elif n < 300: 
        dx = 20
    elif n < 700:
        dx = 50
    else:
        dx = 100
                                 
    xtickspos = [0.1 + 0.1 * i for i in range(0, n+1, dx)]
    xticks = [e[0] for e in daten1]
    plt.xticks(xtickspos, xticks[::dx]) 		
    plt.axes().xaxis.set_ticks_position('none')
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(9)
        tick.label1.set_fontname('Arial')
        tick.label1.set_alpha(0.8)		
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(9)	
        tick.label1.set_fontname('Arial')
        tick.label1.set_alpha(0.8)		
    for pos in ('top', 'bottom', 'right', 'left'): 			
        ax.spines[pos].set_linewidth(0.5)		
    ax.tick_params(right='off')
	
    plt.show()
	
	
	
# ----------------
# Balkendiagramm 2
# ----------------

def  balken2(daten, typ=None, titel=None):
    # daten   dict( [k, f(k)], ... ) 
    # typ     'D' - DatenReihe
    
    n = len(daten.keys())
    if n-1 > 100:
        print('zufall: nicht implementiert (Anzahl zu groß)')
        return
    
    print(' ')
    	
    plt.close('all')		
		
    b, h = 4, 3
    if n > 70:
        b = 12
    elif n > 30:
        b = 8	
    fig = plt.figure(figsize=(b, h))
    ax = fig.add_subplot(1, 1, 1)

    if typ == "D":
        fc = (0.6, 0.8, 1.0)   # RGB::PaleBlue
        ec = (0.333333, 0.333333, 0.333333)  # RGB::DarkGrey
        xlabel = " $Position\; in\; der\; Datenliste$"
        ylabel = " "
        
    lw = 0.7		
    xpos, ypos = 0, 0
    ymax = max(daten.values())	
    for k in daten.keys():  
        re = patches.Rectangle((xpos, ypos), 1/n, daten[k], lw=lw,
                 facecolor=fc, edgecolor=ec)
        plt.gca().add_patch(re)
        xpos += 1/n
    
    plt.title(titel, fontsize=10.5, color=(0.2, 0.2, 0.2))
    plt.xlabel(xlabel, fontsize=10)
    plt.ylabel(ylabel, fontsize=10)
    
    xticks = [i for i in range(0, n)]   
    
    if n <= 50:   
        xtickspos = [1/(2*n) + i/n for i in range(0, n)]
        plt.xticks(xtickspos, xticks)
    else:
        xtickspos = [3/(4*n) + i/n for i in range(0, n)]
        plt.xticks(xtickspos, xticks, rotation=90, fontsize=(7 if n<80 else 6))
    plt.axes().xaxis.set_ticks_position('none')
    
    if ymax < 10:
        dy = 1 
    elif ymax < 50:
        dy = 5
    elif ymax < 100:
        dy = 10
    elif ymax < 1000:
        dy = 100
    elif ymax < 5000:
        dy = 500
    else:
        dy = 1000	
    ytickspos = []
	
    i = 1
    while True:
        ytickspos += [i*dy]
        i += 1
        if (i-1)*dy > ymax:
            break           
    yticks = [(i+1)*dy for i in range(len(ytickspos))]
    plt.yticks(ytickspos, [t for t in yticks])  
    for t in ytickspos:
        plt.plot([0, 1], [t, t], color=(0.4,0.4,0.4), linewidth=0.3)
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(9)
        tick.label1.set_fontname('Arial')
        tick.label1.set_alpha(0.8)		
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(9)	
        tick.label1.set_fontname('Arial')
        tick.label1.set_alpha(0.8)		
    for pos in ('top', 'bottom', 'right', 'left'): 			
        ax.spines[pos].set_linewidth(0.5)		
      
    plt.show()
	
	
	
# -----------------------------
# Balken-Plus-Balken - Diagramm
# -----------------------------

def  balken_plus_balken(daten1, daten2, typ1=None, typ2=None, titel=None, mark=None, ylabel=None):
    # daten dict( {k:f(k)}, ...) - Verteilung
    # typ: 'W' - Wahrscheinlichkeiten
    #      'R' - Relative Häufigkeiten
    
    n = max(len(daten1), len(daten2))
    if n > 200:
        print('zufall: nicht implementiert (Anzahl zu groß)')
        return
    
    print(' ')
    	
    dat = 	set(daten1.keys()).union(set(daten2.keys()))

    plt.close('all')		
		
    fig = plt.figure(figsize=(4, 3))
    ax = fig.add_subplot(1, 1, 1)
    ymax = max(max(daten1.values()), max(daten2.values()))
    plt.ylim(0, 1.4*float(ymax))	
    
    lw = 0.7			
    if typ1 =='W':
        if typ2 == 'W':
            fc1 = (1,1,0.6)   # RGB::YellowLight
            fc2 = (1.0, 0.689993, 0.059999)   # RGB::CadmiumYellowLight 
            ylabel = "$P\,(X \,=\, k)$"
        else:
            fc1 = (1,1,0.6)   # RGB::YellowLight
            fc2 = (0.6039, 0.803903, 0.196097)   # RGB::YellowGreen 		
            ylabel = "$P \; / \; h$ "
        ec = (0.6,0.2,0)   # RGB::Brown
        xlabel = "$k$"
    elif typ1 == "R":
        if typ2 == 'W':
            fc1 = (0.6039, 0.803903, 0.196097)   # RGB::YellowGreen 
            fc2 = (1,1,0.6)   # RGB::YellowLight
            ylabel = "$h \; / \; P $"
        else:		
            fc1 = (0.6039, 0.803903, 0.196097)   # RGB::YellowGreen
            fc2 = (0.333293, 0.419599, 0.184301)   # RGB::OliveGreenDark 
            ylabel = "$h$"
        ec = (0.333293, 0.419599, 0.184301)   # RGB::OliveGreenDark
        xlabel = "$k$"
        
    xpos, ypos = 0, 0   
    for k in dat: 
        try:	
            re1 = patches.Rectangle((xpos+0.01, ypos), 0.04, daten1[k], lw=lw,
                 facecolor=fc1, edgecolor=ec)
            plt.gca().add_patch(re1)
        except KeyError:
            pass
        try:	
            re2 = patches.Rectangle((xpos+0.05, ypos), 0.04, daten2[k], lw=lw, 
                 facecolor=fc2, edgecolor=ec)
            plt.gca().add_patch(re2)
        except KeyError:
            pass
        xpos += 0.1
    
    plt.title(titel, fontsize=10.5, color=(0.2, 0.2, 0.2))
    plt.xlabel(xlabel, fontsize=10)
    plt.ylabel(ylabel, fontsize=10)
    
    if n < 20:
        dx = 1
    elif n < 40:
        dx = 5 
    elif n < 150:
        dx = 10
    elif n < 300: 
        dx = 20
    elif n < 700:
        dx = 50
    else:
        dx = 100
                                 
    xtickspos = [0.05 + 0.1 * i for i in range(0, n, dx)]
    xticks = list(dat)
    xticks.sort()   
    plt.xticks(xtickspos, xticks[::dx])
    plt.axes().xaxis.set_ticks_position('none')
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(9)
        tick.label1.set_fontname('Arial')
        tick.label1.set_alpha(0.8)		
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(9)	
        tick.label1.set_fontname('Arial')
        tick.label1.set_alpha(0.8)		
    for pos in ('top', 'bottom', 'right', 'left'): 			
        ax.spines[pos].set_linewidth(0.5)		
    
    plt.show()
	
	
	
# -----------------------------
# Balken-Plus-stetig - Diagramm
# -----------------------------

def  balken_plus_stetig(daten, stetige_verteilung, typ=None, titel=None, ylabel=None):
    # daten dict( {k:f(k), ...} ) - Verteilung
    # typ: 'W' - Wahrscheinlichkeiten
    #      'R' - Relative Häufigkeiten
    # stetige_verteilung - stetige Verteilung (NV oder EV)
    
    nv = importlib.import_module('zufall.lib.objekte.normal_verteilung')
    ev = importlib.import_module('zufall.lib.objekte.exponential_verteilung')
    NormalVerteilung = nv.NormalVerteilung	
    ExponentialVerteilung = ev.ExponentialVerteilung
	
    n = len(daten)
    if n > 200:
        print('zufall: nicht implementiert (Anzahl zu groß)')
        return
    
    print(' ')
 		
    plt.close('all')		
		
    fig = plt.figure(figsize=(4, 3))
    ax = fig.add_subplot(1, 1, 1)
    
    ymax = max(daten.values())
    plt.ylim(0, 1.4*float(ymax))	
    lw = 0.7	
    if typ =='W':
        fc = (1,1,0.6)   # RGB::YellowLight
        ylabel = "$P\,(X \,=\, k)$"
        ec = (0.6,0.2,0)   # RGB::Brown
        xlabel = "$k$"
    elif typ == "R":
        fc = (0.6039, 0.803903, 0.196097)   # RGB::YellowGreen 
        ylabel = "$h \; / \; P $"
        ec = (0.333293, 0.419599, 0.184301)   # RGB::OliveGreenDark
        xlabel = "$k$"
        
    xpos, ypos = 0, 0   
    for k in daten: 
        try:	
            re = patches.Rectangle((xpos+0.01, ypos), 0.1, daten[k], lw=lw,
                 facecolor=fc, edgecolor=ec)
            plt.gca().add_patch(re)
        except KeyError:
            pass
        xpos += 0.1

    if isinstance(stetige_verteilung, NormalVerteilung):	
        mi, ma = float(min(daten.keys()))*0.1, float(max(daten.keys()))*0.1
        xu, xo = mi, ma
        si = float(stetige_verteilung.sigma)		
        X = norm(float(stetige_verteilung.erw), si) 
        x = np.linspace(0.0, xo+0.05, 100)
        plt.plot(x-0.05, X.pdf(10*x), color=(1, 0, 0), linewidth=1.5)      
    else:	# Exponentialverteilung
        X = expon(loc=0, scale=float(1/stetige_verteilung.par))
        xu, xo = 0.0, float(max(daten.keys()))		
        x = np.linspace(xu, xo*0.1+0.05, 100)
        plt.ylim(0, 1.0)
        plt.plot(x, X.pdf(10.0*x), color=(1, 0, 0), linewidth=1.5)      
	
    plt.title(titel, fontsize=10.5, color=(0.2, 0.2, 0.2))
    plt.xlabel(xlabel, fontsize=10)
    plt.ylabel(ylabel, fontsize=10)
    
    if n < 20:
        dx = 1
    elif n < 40:
        dx = 5 
    elif n < 150:
        dx = 10
    elif n < 300: 
        dx = 20
    elif n < 700:
        dx = 50
    else:
        dx = 100
              
    ax.set_xticks([])         
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(9)
        tick.label1.set_fontname('Arial')
        tick.label1.set_alpha(0.8)		
    for pos in ('top', 'bottom', 'right', 'left'): 			
        ax.spines[pos].set_linewidth(0.5)		
       
    plt.show()
	
	
	
	
	
# ---------------------	
# Polygonzug - Diagramm
# ---------------------

def  polygon_zug(daten, typ=None, titel=None):
    # daten dict( {k:f(k), ...} ) - Verteilung
    # typ   'W' - Wahrscheinlichkeiten
    #       'R' - Relative Häufigkeiten
    #       'D' - DatenReihe
    
    n = len(daten.keys())
    if n-1 > 1000:
        print('zufall: nicht implementiert (Anzahl zu groß)')
        return
    
    print(' ')

    plt.close('all')		
    
    fig = plt.figure(figsize=(4, 3))
    ax = fig.add_subplot(1, 1, 1)
    ymax = max(daten.values())
    plt.ylim(0, 1.4*float(ymax))	

    if typ =='W':
        fc = (1.0, 0.689993, 0.059999)   # RGB::CadmiumYellowLight
        ec = (0.6,0.2,0)   # RGB::Brown
        xlabel = "$k$"
        ylabel = "$P\,(X = k)$"
    elif typ == "R":
        fc = (0.6039, 0.803903, 0.196097)   # RGB::YellowGreen
        ec = (0.333293, 0.419599, 0.184301)   # RGB::OliveGreenDark
        xlabel = "$k$"
        ylabel = "$h$"
    elif typ == "A":
        fc = (0.8,0.8,0.8)   # RGB::Grey80
        ec = (0.333333, 0.333333, 0.333333)  # RGB::DarkGrey
        xlabel = "$k$"
        ylabel = "$H$"
    elif typ == "D":
        fc = (0.6, 0.8, 1.0)   # RGB::PaleBlue
        ec = (0.333333, 0.333333, 0.333333)  # RGB::DarkGrey
        xlabel = "$Position\, in\, der\, Datenliste$ "
        ylabel = " "
        
    dat = [[k, daten[k]] for k in daten]
    dat.sort(key=lambda x: x[0])
    xmin = min(daten.keys())	
    x = [0.05+0.1*(e[0]-xmin) for e in dat] 
    y = [e[1] for e in dat]
    plt.plot(x, y, linewidth=2., color=fc, marker='o', markersize=4., 
	        markerfacecolor=(1, 1, 1), markeredgecolor=ec)
    plt.plot(0, 0, linewidth=3., color=(1, 1, 1))			        
    plt.title(titel, fontsize=10.5, color=(0.2, 0.2, 0.2))
    plt.xlabel(xlabel, fontsize=10)
    plt.ylabel(ylabel, fontsize=10)
    
    if n < 20:
        dx = 1
    elif n < 40:
        dx = 5 
    elif n < 150:
        dx = 10
    elif n < 300: 
        dx = 20
    elif n < 700:
        dx = 50
    else:
        dx = 100
     
    xtickspos = [0.05 + 0.1 * i for i in range(0, n+1, dx)]	
    xticks = [e[0] for e in dat] 
    plt.xticks(xtickspos, xticks[::dx]) 
    plt.axes().xaxis.set_ticks_position('none')
    if typ == 'D':
        xmax, ymax = len(daten), max(daten.values())
        plt.plot((xmax+1)*0.1, ymax*1.1, color=(1,1,1))  
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(9)
        tick.label1.set_fontname('Arial')
        tick.label1.set_alpha(0.8)		
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(9)
        tick.label1.set_fontname('Arial')
        tick.label1.set_alpha(0.8)		
    for pos in ('top', 'bottom', 'right', 'left'): 			
        ax.spines[pos].set_linewidth(0.5)		
				
    plt.show()	
	
	
	
# -------------------------------------	
# Polygonzug-Plus-Polygonzug - Diagramm
# -------------------------------------

def  poly_plus_poly(daten1, daten2, typ1=None, typ2=None, titel=None, mark=None, ylabel=None):
    # daten dict( {k:f(k), ...} ) - Verteilung
    # typ   'W' - Wahrscheinlichkeiten
    #       'R' - Relative Häufigkeiten
    
    n = max(len(daten1), len(daten2))
    if n > 200:
        print('zufall: nicht implementiert (Anzahl zu groß)')
        return
    
    print(' ')
		
    dat = set(daten1.keys()).union(set(daten2.keys()))
    plt.close('all')		
	
    fig = plt.figure(figsize=(4, 3))
    ax = fig.add_subplot(1, 1, 1)
    ymax = max(max(daten1.values()), max(daten2.values()))
    plt.ylim(0, 1.4*float(ymax))	

    if typ1 =='W':
        if typ2 == 'W':	
            fc1 = (1.0, 0.689993, 0.059999)   # RGB::CadmiumYellowLight 
            fc2 = (0.6,0.2,0)   # RGB::Brown
            ylabel = "$P\,(X \,=\, k)$"
        else:
            fc1 = (1.0, 0.689993, 0.059999)   # RGB::CadmiumYellowLight 
            fc2 = (0.6039, 0.803903, 0.196097)   # RGB::YellowGreen 		
            ylabel = "$P \; / \; h$ "
        ec = (0.6,0.2,0)   # RGB::Brown
        xlabel = "$k$"
    elif typ1 == "R":
        if typ2 == 'W':
            fc1 = (0.6039, 0.803903, 0.196097)   # RGB::YellowGreen 
            fc2 = (1.0, 0.689993, 0.059999)   # RGB::CadmiumYellowLight 
            ylabel = "$h \; / \; P $"
        else:		
            fc1 = (0.6039, 0.803903, 0.196097)   # RGB::YellowGreen
            fc2 = (0.333293, 0.419599, 0.184301)   # RGB::OliveGreenDark 
            ylabel = "$h$"
        ec = (0.333293, 0.419599, 0.184301)   # RGB::OliveGreenDark
        xlabel = "$k$"
        
    x = [0.05+0.1*k for k in dat] 
    y1, y2 = [], []
    for k in dat:
        try:
            y1 += [daten1[k]]
        except KeyError:
            y1 += [0]		
        try:
            y2 += [daten2[k]]
        except KeyError:
            y2 += [0]		
    plt.plot(x, y1, linewidth=2., color=fc1, marker='o', markersize=4., 
	        markerfacecolor=(1, 1, 1), markeredgecolor=ec)
    plt.plot(x, y2, linewidth=2., color=fc2, marker='o', markersize=4., 
	        markerfacecolor=(1, 1, 1), markeredgecolor=ec)
    plt.plot(0, 0, linewidth=3., color=(1, 1, 1))			

    plt.title(titel, fontsize=10.5, color=(0.2, 0.2, 0.2))
    plt.xlabel(xlabel, fontsize=10)
    plt.ylabel(ylabel, fontsize=10)
    plt.ylabel(ylabel, fontsize=11)
    
    if n < 20:
        dx = 1
    elif n < 40:
        dx = 5 
    elif n < 150:
        dx = 10
    elif n < 300: 
        dx = 20
    elif n < 700:
        dx = 50
    else:
        dx = 100
    dat = list(dat)	 
    m = floor(max(dat)) + 1
    xtickspos = [0.05 + 0.1 * dat[i] for i in range(len(dat))]	
    xticks = dat
    if 0 not in dat:	
        xtickspos = [0.05] + xtickspos
        xticks = [0] + xticks		
    plt.xticks(xtickspos[::dx], xticks[::dx])
    plt.axes().xaxis.set_ticks_position('none')
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(9)
        tick.label1.set_fontname('Arial')
        tick.label1.set_alpha(0.8)		
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(9)
        tick.label1.set_fontname('Arial')
        tick.label1.set_alpha(0.8)		
    for pos in ('top', 'bottom', 'right', 'left'): 			
        ax.spines[pos].set_linewidth(0.5)		
		
    plt.show()	
	


# --------------------
# Verteilungsfunktion
# --------------------

def  vert_funktion(objekt, typ=None, titel=None):
    # objekt   ZufallsGröße, DatenReihe
    # typ: 'W' - Wahrscheinlichkeiten
    #      'D' - Datenreihe
	
    F = objekt.F
	
    if typ =='W':	
        daten = objekt._vert_kum	
        ldaten = list(daten.keys())
        ldaten.sort()
    else:
        if not objekt.is_ganz:	
            print('zufall: Datenelemente nicht ganzzahlig')
            return            
        ldaten = objekt.F(alle=True)	
    	
    if typ == 'W':		
        n = len(ldaten)
        m, M = ldaten[0], ldaten[-1]   # minimaler, maximaler x-Wert
    else:
        n = objekt.n
        m, M = objekt.min, objekt.max
	
    if n > 101:
        print('zufall: nicht implementiert (Anzahl zu groß)')
        return
    
    print(' ')
    
    plt.close('all')		
	
    fig = plt.figure(figsize=(4, 3))
    ax = fig.add_subplot(1, 1, 1)

    if typ =='W':
        fc = (0.956893, 0.643101, 0.376507)   # RGB::SandyBrown
        ec = (0.6,0.2,0)   # RGB::Brown
        xlabel = "$k$"
        ylabel = "$F(k)$"
    elif typ == "D":
        fc = (0.6, 0.8, 1.0)   # RGB::PaleBlue
        ec = (0.333333, 0.333333, 0.333333)  # RGB::DarkGrey
        xlabel = "$x$"
        ylabel = "$F(x)$"

    plt.ylim(-0.01, 1.15)
    plt.xlim(float(m-3), float(M+3))
	
    N = 50   # Anzahl der Unterteilungen (x-Achse)	
    
    x0, y0 = 2, 0	
    strich = [[m-3, m], [0, 0]]
    plt.plot(strich[0], strich[1], linewidth=3., color=fc)	
	
    for n in range(N):
        x0 = n
        y = F(x0)  
        x1 = x0
        if F(x1) > 1-1e-6:
            break		
        while F(x1) == y:
            x1 += 1
            if F(x1) > y:
                strich = [[x0+0.1, x1], [y, y]]
                plt.plot(strich[0], strich[1], linewidth=3., color=fc)	
                plt.plot(x1, y, linewidth=2., color=fc, marker='o', 
                   markersize=3., markerfacecolor=(1, 1, 1), markeredgecolor=ec)
                break
    strich = [[x1, M+3], [1, 1]]
    plt.plot(strich[0], strich[1], linewidth=3., color=fc)				
							
    plt.title(titel, fontsize=10.5, color=(0.2, 0.2, 0.2))
    plt.xlabel(xlabel, fontsize=10)
    plt.ylabel(ylabel, fontsize=10)
    
    if n < 20:
        dx = 1
    elif n < 40:
        dx = 5 
    elif n < 150:
        dx = 10
    elif n < 300: 
        dx = 20
    elif n < 700:
        dx = 50
    else:
        dx = 100

    if typ == 'W':		
        xtickspos = [0.05 + ldaten[i] for i in range(len(ldaten))]
        xticks = ldaten  
        plt.xticks(xtickspos[::dx], xticks[::dx])
        plt.axes().xaxis.set_ticks_position('none')
        ax.tick_params(left='off', right='off')
		
    ymax = 1.2	
    dy = 0.1 if ymax > 0.1 else 0.01 
    ytickspos = [0]
    i = 1
    while True:
        ytickspos += [i*2*dy]
        i += 1
        if (i-2)*2*dy > ymax:
            break           
    yticks = [0.0] + [eval(format((i+1)*2*dy, '.1f')) for i in range(len(ytickspos))]
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(9)
        tick.label1.set_fontname('Arial')
        tick.label1.set_alpha(0.8)		
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(9)
        tick.label1.set_fontname('Arial')
        tick.label1.set_alpha(0.8)		
    for pos in ('top', 'bottom', 'right', 'left'): 			
        ax.spines[pos].set_linewidth(0.5)		
    for t in ytickspos[:-2]:
        plt.plot([-10**6, M+3], [t, t], color=(0.3,0.3,0.3), linewidth=0.15)
		
    plt.show()	
	

	
# --------------
# Verlaufsgrafik
# --------------

def  verlauf(daten, vergl=None, art=None, xlabel=None):
    # daten   np.array - Versuchsausgänge
    # vergl   Vergleichswert
    # art     Berechnungsart

    n = len(daten)
    dat = np.array([daten[0]])
    if art == 'summe':
        for i in range(1, n):
            dat = np.append(dat, [dat[i-1] + daten[i]]) 
    elif art == 'mittel':            # gleitendes Mittel
        for i in range(1, n):
            dat = np.append(dat, [((i-1)*dat[i-1] + daten[i])/i])
	
    plt.close('all')		

    fig = plt.figure(figsize=(7, 3))	
    ax = plt.gca()	
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(9)
        tick.label1.set_fontname('Arial')
        tick.label1.set_alpha(0.8)		
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(9)
        tick.label1.set_fontname('Arial')
        tick.label1.set_alpha(0.8)		
    for pos in ('top', 'bottom', 'right', 'left'): 			
        ax.spines[pos].set_linewidth(0.5)		
    x = np.array([i for i in range(n)])	
    plt.plot([0, n], [vergl, vergl], color=(0,1,0), linewidth=0.8)
    a = 0.1
    plt.xlabel(xlabel, fontsize=10.5, color=(0.2, 0.2, 0.2))	
    plt.plot(x, dat, color=(a,a,a), linewidth=0.4)
    plt.show() 
	

	
	
	