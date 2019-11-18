#!/usr/bin/python
# -*- coding utf-8 -*-



#                                                 
#  Verfahren für Aufgaben im R^3           
#  
                                               
#
# This file is part of agla
#
#
# Copyright (c) 2019 Holger Böttcher  hbomat@posteo.de
#
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License
# You may obtain a copy of the License at
#  
#      http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#  



# Inhalt 
#
#  AEE    	AbstandEbeneEbene			   
#  AGE    	AbstandGeradeEbene			
#  AGG    	AbstandGeradeGeradeVersion0		  
#  AGG1    		            ...Version1		  
#  AGG2   		            ...Version2		  
#  APE    	AbstandPunktEbeneVersion0		   
#  APE1    		          ...Version1		   
#  APE2    		          ...Version2		   
#  APG    	AbstandPunktGeradeVersion0  			
#  APG1   		           ...Version1  		  		
#  APG2   		           ...Version2  		   		
#  APG3                    ...Version3  		   		
#  APP    	AbstandPunktPunkt	
#
#  LEE    	LageEbeneEbene			                
#  LGE    	LageGeradeEbeneVersion0			                
#  LGE1   		        ...Version1			                
#  LGG    	LageGeradeGeradeVersion0			
#  LGG1   		         ...Version1			
#  LPD    	LagePunktDreieckVersion0			 
#  LPD1   		         ...Version1    		 
#  LPE    	LagePunktEbene			
#  LPG    	LagePunktGerade			
#  LPV    	LagePunktViereck
#  LPK          LagePunktKugel			
#  LGK          LageGeradeKugel			
#  LEK          LageEbeneKugel			
#
#  WEE    	WinkelEbeneEbene			
#  WGE    	WinkelGeradeEbene			
#  WVV    	WinkelVektorVektor	
		
#           Umwandlung einer Ebenengleichung
#  EK2P	    EbeneKoord2PrgVersion0	Koordinatenform -> Parameterform	    
#  EK2P1 		       ...Version1  ebenso		    
#  EN2P	    EbeneNf2Prg             Normalenform -> Parameterform				  
#  EP2K     EbenePrg2KoordVersion0	Parameterform -> Koordinatenform		   
#  EP2K1               ...Version1  ebenso		  
#  EP2N     EbenePrg2Nf             Parameterform -> Normalenform
#	
#  RV	 	RichtVektor             Ermittlung von 2 Richtungsvektoren 	( = ERV )	
#
#  NV		NormVektorVersion0      Ermittlung eines Normalenvektors       ( = ENV ) 		
#  NV1             ...Version1      einer Ebene / zu 2 gegebenen Vektoren  ( = ENV1 )			
	


from IPython.display import display, Math	
	
from sympy.core.symbol import Symbol
from sympy.core.numbers import Integer, Float, Rational 	
from sympy.core.function import expand
from sympy.simplify.simplify import simplify, nsimplify
from sympy.solvers.solvers import solve	
from sympy.polys.polytools import Poly, gcd, lcm	
from sympy.functions.elementary.miscellaneous import sqrt	
from sympy import Abs
from sympy.core.evalf import N	
from sympy.printing import latex
from sympy.abc import *

from agla.lib.objekte.vektor import Vektor, v, O, O2, X, X2																																																																																																																																																							
from agla.lib.objekte.ebene import Ebene
from agla.lib.objekte.gerade import Gerade
from agla.lib.objekte.dreieck import Dreieck
from agla.lib.objekte.viereck import Viereck
from agla.lib.objekte.kugel import Kugel
from agla.lib.objekte.lgs import LGS

from agla.lib.funktionen.funktionen import (Gleichung, parallel, loese, 
    identisch, mit_param, arcsing, arccosg, kollinear)
	
abs = Abs




# ------------------
# AbstandEbeneEbene
# ------------------

def AbstandEbeneEbene(*args, **kwargs):

    if kwargs.get('h'):
        print("\nAbstandEbeneEbene - Verfahren\n")
        print("Abstand zwischen zwei Ebenen\n")
        print("Aufruf     AEE( ebene1, ebene2 )\n")		                     
        print("                ebene    Ebene\n")
        return		
		
    if len(args) != 2:
        print("agla: zwei Ebenen angeben")
        return
				
    anf = '     '				
    e1, e2 = args
    if not (isinstance(e1, Ebene) and isinstance(e2, Ebene)):
        print("agla: zwei Ebenen angeben")
        return
		
    if mit_param(e1) or mit_param(e2):		
        print("agla: nicht implementiert, Parameter")
        return

    print("\nAbstand zwischen zwei Ebenen\n")
    print("Gegeben:\n")
    lat1 = 'E1 : \;'
    if e1._typ == 1:
        lat1 += pnf(e1, X)
    elif e1._typ == 2:
        lat1 += pprg(e1) 
    else:
        lat1 += pkoord(e1, X)	
    lat2 = 'E2 : \;'
    if e2._typ == 1:
        lat2 += pnf(e2, X)
    elif e2._typ == 2:
        lat2 += pprg(e2) 
    else:
        lat2 += pkoord(e2, X)	
    display(Math('\quad \quad ' + lat1 + ', \quad \quad ' + lat2))
    if e1._typ == 1:
        gl1 = "Normalenform"
    elif e1._typ == 2:
        gl1 = "Parametergleichung"
    elif e1._typ == 3:
        gl1 = "Koordinatenform"
    if e2._typ == 1:
        gl2 = "Normalenform"
    elif e2._typ == 2:
        gl2 = "Parametergleichung"
    elif e2._typ == 3:
        gl2 = "Koordinatenform"
    print("\nE1 - " + gl1 +",  " + "E2 - " + gl2)	
    txt = ''	
    if e1._typ == 2 and e2._typ == 2:
        txt = 'E1 und E2'	
    elif e1._typ == 2:
        txt = 'E1'	
    elif e2._typ == 2:
        txt = 'E2'
    if txt:
        print("\nErmittlung eines Normalenvektors von " + txt +  \
                                    "   (s.a. ENV - EbeneNormalenVektor)")	
    print("\nNormalenvektoren der Ebenen sind")
    display(Math('\quad \quad ' + latex(e1.norm) + ', ' + latex(e2.norm)))

    print("\nUntersuchung auf Parallelität:")
    print('\n' + anf + "Die Vektoren sollen kollinear sein")
    if not parallel(e1, e2):
        print('\n' + anf + "Die Bedingung ist nicht erfüllt, die Ebenen schneiden sich\n")
        display(Math('Abstand: \\;\; ' + latex("d(E1, E2) = 0")))	
        print("\n")		
        return		
	
    print(anf + "Die Ebenen sind parallel")
    print("\nErmittlung des Abstandes:\n")
	
    print(anf + "Ermittlung des Abstandes eines Punktes von der Ebene E2 zur Ebene ")
    print(anf + "E1 durch Einsetzen der Punktkoordinaten in die linke Seite der Hes-")
    print(anf + "seschen Normalenform  ( s.a. APE - AbstandPunktEbene )")	
    print("\n" + anf + "Hessesche Normalenform von E1")
    lat = latex('\\left[') + latex(X)+'-'+ latex(e1.stuetz) + \
              latex('\\right]') + latex('\circ') + \
              (latex(1/e1.norm.betrag) if e1.norm.betrag != 1 else '') \
			    + latex(e1.norm) + latex('=') + latex(0) 
    display(Math('\quad \quad ' + lat))
    if e2._typ == 3:
        gl = e2.koord.lhs.subs({x:0, y:0})
        L = solve(gl)
        pp = Vektor(0, 0, L[0])		
        txt = 'eines beliebigen Punktes von E2, z.B. (0,0,' + str(L[0]) + ')'
    else:
        pp = e2.stuetz
        txt = 'des Stützvektors von E2'
    print("\n" + anf + "Einsetzen " + txt)	
    lat = latex('d = \\left[') + latex(pp)+'-'+ latex(e1.stuetz) + \
              latex('\\right]') + latex('\circ') + \
              (latex(1/e1.norm.betrag) if e1.norm.betrag != 1 else '') \
			    + latex(e1.norm) 
    display(Math('\quad \quad ' + lat))
    pp = pp - e1.stuetz	
    lat = 'd =' + latex(pp) + latex('\circ') + \
              (latex(1/e1.norm.betrag) if e1.norm.betrag != 1 else '') \
			    + latex(e1.norm)  
    display(Math('\quad \quad ' + lat))
    lat = 'd =' + '\\left(' + psp(pp, e1.norm) + '\\right)' + \
        ('\cdot' if e1.norm.betrag != 1 else '') + \
        (latex(1/e1.norm.betrag) if e1.norm.betrag != 1 else '')		  
    display(Math('\quad \quad ' + lat))
    dd = abs(e1.abstand(e2))
    if isinstance(dd, (int, Integer, float, Float)):
        dm('Abstand: \;\;' + 'd(E1, E2) =' + latex(dd) )
    else:		
        dm('Abstand: \;\;' + 'd(E1, E2) =' + latex(dd) + \
        '\\quad [ \;' + latex(float(dd)) + '\ ]' )	
    print("\n")		
	
AEE = AbstandEbeneEbene
	

	
# ---------------
# LageEbeneEbene
# ---------------
	
def LageEbeneEbene(*args, **kwargs):

    if kwargs.get('h'):
        print("\nLageEbeneEbene - Verfahren\n")
        print("Lage zweier Ebenen zueinander\n")
        print("Aufruf     LEE( ebene1, ebene2 )\n")		                     
        print("                ebene    Ebene\n")
        return		
		
    if len(args) != 2:
        print("agla: zwei Ebenen angeben")
        return
				
    anf = '     '				
    e1, e2 = args
    if not (isinstance(e1, Ebene) and isinstance(e2, Ebene)):
        print("agla: zwei Ebenen angeben")
        return

    if mit_param(e1) or mit_param(e2):		
        print("agla: nicht implementiert, Parameter")
        return		
		
    if e1._typ == 2:
        r, s = Symbol('r'), Symbol('s')				
        e1 = Ebene(e1.stuetz, e1.richt[0], e1.richt[1], r, s)
    if e2._typ == 2:
        if e1._typ == 2:	
            t, u = Symbol('t'), Symbol('u')			
            e2 = Ebene(e2.stuetz, e2.richt[0], e2.richt[1], t, u)
        else:
            r, s = Symbol('r'), Symbol('s')			
            e2 = Ebene(e2.stuetz, e2.richt[0], e2.richt[1], r, s)
    print("\nLage zweier Ebenen\n")
    print("Gegeben:\n")
    if e1._typ != 2 and e2._typ == 2 or e1._typ == 3 and e2._typ == 1:
        [e1, e2] = [e2, e1]	
        print(anf + "(die Reihenfolge wurde geändert)\n")	   
		
    lat1 = 'E1 : \;'
    if e1._typ == 1:
        lat1 += pnf(e1, X)
    elif e1._typ == 2:
        lat1 += pprg(e1) 
    else:
        lat1 += pkoord(e1, X)	
    lat2 = 'E2 : \;'
    if e2._typ == 1:
        lat2 += pnf(e2, X)
    elif e2._typ == 2:
        lat2 += pprg(e2) 
    else:
        lat2 += pkoord(e2, X)	
    display(Math('\quad \quad ' + lat1 + ', \quad \quad ' + lat2))
	
    if e1._typ == 1:
        gl1 = "Normalenform"
    elif e1._typ == 2:
        gl1 = "Parametergleichung"
    elif e1._typ == 3:
        gl1 = "Koordinatenform"
    if e2._typ == 1:
        gl2 = "Normalenform"
    elif e2._typ == 2:
        gl2 = "Parametergleichung"
    elif e2._typ == 3:
        gl2 = "Koordinatenform"
    print("\nE1 - " + gl1 +",  " + "E2 - " + gl2)	

    if e1._typ != 2 and e2._typ != 2:	
        print("\nUntersuchung auf Parallelität:\n")
        print(anf + "Normalenvektoren der Ebenen sind")			
        lat = latex(e1.norm) + ', \;\;\;' + latex(e2.norm)	
        display(Math('\quad \quad ' + lat))
        if parallel(e1, e2):
            print(anf + "Die Normalenvektoren sollen kollinear sein, es ist")
            t = Symbol('t')
            L = loese(e2.norm - t*e1.norm)	
            lat = latex(e2.norm) + '=' + latex(L[t]) + '\cdot' + latex(e1.norm)	
            display(Math('\quad \quad ' + lat))
            print('\n' + anf + "Die Ebenen sind parallel oder identisch")
            print("\nUntersuchung auf Identität:\n")
            if identisch(e1, e2):
                if e1._typ == 3 and e2._typ == 3:
                    print(anf + "die Gleichungen beschreiben dieselbe Ebene")
                elif e1._typ == 1 and e2._typ == 3:
                    print(anf + "Einsetzen des Stützvektors von E1 in die Gleichung von E2")
                    a = e2.args[:4]			
                    vv = e1.stuetz					
                    lat = psp(Vektor(a[0], a[1], a[2]), vv) + \
                         ('+' if a[3] >= 0 else '-') + latex(Abs(a[3])) + '=0'					
                    display(Math('\quad \quad \;' + lat))
                    display(Math('\quad \quad \;' + '0 = 0'))
                    print(anf + "die Gleichung ist erfüllt")
                elif e1._typ == 1 and e2._typ == 1:
                    print(anf + "Einsetzen des Stützvektors von E1 in die Gleichung von E2")
                    lat = latex('\\left[') + latex(e1.stuetz)+'-'+ latex(e2.stuetz) + \
                         latex('\\right]') + latex('\circ') + latex(e2.norm) + \
                         latex('=') + latex(0) 
                    display(Math('\quad \quad \;' + lat))
                    lat = psp2(e1.stuetz, e2.stuetz, e2.norm) 			
                    display(Math('\quad \quad \;' + lat + '= 0'))					
                    display(Math('\quad \quad \;' + '0 = 0'))
                    print(anf + "die Gleichung ist erfüllt")
                print("\nDie Ebenen sind identisch\n")
                return	
            else:				
                if e1._typ == 3 and e2._typ == 3:
                    print(anf + "die Gleichungen beschreiben verschiedene Ebene")
                elif e1._typ == 1 and e2._typ == 3:
                    print(anf + "Einsetzen des Stützvektors von E1 in die Gleichung von E2")
                    a = e2.args[:4]			
                    vv = e1.stuetz	
                    aa = Vektor(a[0], a[1], a[2])					
                    lat = psp(aa, vv) + \
                         ('+' if a[3] >= 0 else '-') + latex(Abs(a[3])) + '=0'					
                    display(Math('\quad \quad \;' + lat))
                    display(Math('\quad \quad \;' + \
                        latex(aa.sp(vv) + a[3]) + '= 0'))
                    print(anf + "die Gleichung ist nicht erfüllt")
                elif e1._typ == 1 and e2._typ == 1:
                    print(anf + "Einsetzen des Stützvektors von E1 in die Gleichung von E2")
                    lat = latex('\\left[') + latex(e1.stuetz)+'-'+ latex(e2.stuetz) + \
                         latex('\\right]') + latex('\circ') + latex(e2.norm) + \
                         latex('=') + latex(0) 
                    display(Math('\quad \quad \;' + lat))
                    lat = psp2(e1.stuetz, e2.stuetz, e2.norm) 			
                    display(Math('\quad \quad \;' + lat + '= 0'))					
                    display(Math('\quad \quad \;' + \
                        latex((e1.stuetz-e2.stuetz).sp(e2.norm)) + '= 0'))
                    print(anf + "die Gleichung ist nicht erfüllt")
					
            print("\nDie Ebenen sind parallel\n")
            return				
        else:
            print(anf + "die Normalenvektoren sollen kollinear sein, die aufgeführten")
            lat = latex(e1.norm) + ', \;' + latex(e2.norm)
            #display(Math('\quad \quad \;' + lat))			
            print(anf + "Vektoren sind es nicht - die Ebenen schneiden sich")
            print("\nErmittlung einer Parametergleichung von E1:\n")	
            print(anf + "Zwei Richtungsvektoren (orthogonal zum Normalenvektor, nicht kollinear) sind")	
            print(anf + "(siehe auch ERV - EbeneRichtungsVektoren)")	
            lat = latex(e1.richt[0]) + ', \;' + latex(e1.richt[1])
            display(Math('\quad \quad \;' + lat))
            print(anf + "eine Parametergleichung ist")
            lat = latex(X)+ latex('=') + latex(e1.stuetz) + latex('+ r') + \
                 latex(e1.richt[0]) + latex('+ s') + latex(e1.richt[1])			
            display(Math('\quad \quad \;' + lat))
            print("\nErmittlung der Schnittgeraden:\n")			
            print(anf + "Die Parametergleichung ist äquivalent zu")	
            r, s = Symbol('r'), Symbol('s')			
            pp = e1.stuetz + r * e1.richt[0] + s * e1.richt[1]
            lat = 'x = ' + latex(pp.x) + ', \; y = ' + latex(pp.y) + ', \; z = ' + latex(pp.z)
            display(Math('\quad \quad \;' + lat))
            x, y, z = Symbol('x'), Symbol('y'), Symbol('z')
            gl = e2.koord.lhs.subs({x:pp.x, y:pp.y, z:pp.z})			
            if gl.has(r):
                var = str(r)
                L = solve(gl, r)
            else:
                var = str(s)
                L = solve(gl, s)				
            print(anf + "Einsetzen in die Gleichung von E2, nach " + var + " auflösen")
            lat = latex(gl) + '= 0'
            display(Math('\quad \quad \;' + lat))	
            lat = var +'=' + latex(L[0])
            display(Math('\quad \quad \;' + lat))
            print(anf + "Einsetzen in die Parametergleichung von E1")			
            lat = latex(X) + latex('=') + latex(e1.stuetz) + '+' + \
                 ('\\left(' + latex(L[0]) + '\\right)' if var == 'r' else latex('r')) + \
                 latex(e1.richt[0]) + '+' + \
				   ('\\left('  + latex(L[0]) + '\\right)' if var == 's' else latex('s')) + \
				 latex(e1.richt[1]) 
            display(Math('\quad \quad \;' + lat))
            print(anf + "und Zusammenfassen ergibt die Gleichung einer Geraden,")			
            print(anf + "in der sich die Ebenen schneiden")			
            vv = e1.stuetz + (L[0] if var == 'r' else r) * e1.richt[0] + \
				   (L[0] if var == 's' else s) * e1.richt[1] 			
            gg = Gerade(vv)
            lat = pgerade(gg)			
            display(Math('\quad \quad \;' + lat))
            print("\n")			

    if e1._typ == 2:
        if e2._typ == 2:
            print("\n" +"Gleichsetzen der rechten Seiten der beiden Gleichungen ergibt das ")
            print("Gleichungssystem\n")	
            lgs = LGS(e1.pkt(r, s) - e2.pkt(t, u))
            lgs.ausg_ohne_nr			
            c1, c2 = Symbol('c1'), Symbol('c2')
            L = lgs.loes	
            if not L:   # keine Lösung
                print('\n' + anf + "es hat keine Lösung, die Ebenen schneiden sich nicht")
                print("\nDie Ebenen sind parallel\n")
                return	
            elif any([val.has(c1) for val in L.values() \
                           if not isinstance(val, (int, float))]) and \
                any([val.has(c2) for val in L.values() \
                           if not isinstance(val, (int, float))]):   # 2 Parameter					   
                print('\n' + anf + "seine Lösung ist\n")
                print(anf + anf + 'r = ' + str(L[r]) + ',  s = ' + str(L[s]) + \
                    ',  t = ' + str(L[t]) + ',  u = ' + str(L[u]))
                print('\n' + anf + "sie besitzt also zwei Parameter")
                print("\nDie Ebenen sind identisch\n")
            else:    # 1 Parameter				
                print('\n'+ anf + "seine Lösung ist\n")		
                print(anf + anf + 'r = ' + str(L[r]) + ',  s = ' + str(L[s]) + \
                    ',  t = ' + str(L[t]) + ',  u = ' + str(L[u]))
                print('\n' + anf + "sie besitzt also einen Parameter, was auf eine Gerade führt")
                print('\n' + "Ermittlung der Schnittgeraden\n")	
                print(anf + "Einsetzen der Werte in die Parametergleichung von E2")				    				
                print(anf + "(der Parameter wurde in t umbenannt)\n")				    				
                lat = latex(X)+ latex('=') + latex(e2.stuetz) + latex('+') + '\\left(' +\
                      latex(L[t].subs({c1:t, c2:t})) + '\\right)' + \
                      latex(e2.richt[0]) + latex('+') + '\\left(' + \
                      latex(L[u].subs({c1:t, c2:t})) + '\\right)' + latex(e2.richt[1])	
                display(Math('\quad \quad \;' + lat))
                print(anf + "und Zusammenfassen ergibt die Schnittgerade")	
                vv = e2.stuetz + L[t].subs({c1:t, c2:t}) * e2.richt[0] + \
                L[u].subs({c1:t, c2:t}) * e2.richt[1]
                gg = Gerade(vv)								
                lat = latex(X) + latex('=') + latex(gg.stuetz) + '+' + latex(t) + latex(gg.richt)	
                display(Math('\quad \quad \;' + lat))
                print('\n')
        else:
            print("\nDie Parametergleichung von E1 ist äquivalent zu")	
            r, s = Symbol('r'), Symbol('s')			
            pp = e1.stuetz + r * e1.richt[0] + s * e1.richt[1]
            lat = 'x = ' + latex(pp.x) + ', \; y = ' + latex(pp.y) + ', \; z = ' + latex(pp.z)
            display(Math('\quad \quad \;' + lat))
            print(anf + "Einsetzen in die Gleichung von E2")	
            if e2._typ == 3:	
                gl = latex(pkoord(e2, pp))
                display(Math('\quad \quad \;' + gl))
                if isinstance(e1.schnitt(e2), set):		
                    print(anf + "die Gleichung hat keine Lösung, die Ebenen schneiden sich nicht")	
                    print("\nDie Ebenen sind parallel\n")	
                elif isinstance(e1.schnitt(e2), Ebene):		
                    print(anf + "die Gleichung ist für alle Punkte von E1 erfüllt")	
                    print("\nDie Ebenen sind identisch\n")	
                else:
                    print(anf + "Auflösen nach einer Variablen")
                    x, y, z = Symbol('x'), Symbol('y'), Symbol('z')					
                    gl = e2.koord.subs({x:pp.x, y:pp.y, z:pp.z}).lhs
                    var = gl.free_symbols.pop()	
                    L = solve(gl, var)
                    lat = latex(var) + '=' + latex(L[0])				
                    display(Math('\quad \quad \;' + lat))
                    print("\nEinsetzen in die Gleichung von E1")
                    par = e1.par	
                    lat = latex(X)+ latex('=') + latex(e1.stuetz) + '+' + \
                          ('\\left(' + latex(L[0]) + '\\right)' if var == par[0] \
                                                 else str(par[0])) + \
                          latex(e1.richt[0]) + '+' + \
					          ('\\left(' + latex(L[0]) + '\\right)' if var == par[1] \
                                                 else str(par[1])) + \
                          latex(e1.richt[1])	
                    display(Math('\quad \quad \;' + lat))
                    print(anf + "und Zusammenfassen führt auf die Gleichung einer Geraden,")
                    print(anf + "in der sich die Ebenen schneiden")
                    vv = e1.stuetz + \
                          (L[0] if var == par[0] else par[0]) * e1.richt[0] + \
					          (L[0] if var == par[1] else par[1]) * e1.richt[1]	
                    gg = Gerade(vv)
                    lat = pgerade(gg)
                    display(Math('\quad \quad \;' + lat))
                    print("\n")
            elif e2._typ == 1:	
                lat = pnf(e2, pp)
                dm('\quad \quad \;' + lat) 
                lat = latex(	pp - e2.stuetz) + '\\circ' + latex(e2.norm) + '= 0'			
                dm('\quad \quad \;' + lat) 
                lat = psp(pp - e2.stuetz, e2.norm) + '= 0'			
                dm('\quad \quad \;' + lat) 
                lat = latex((pp - e2.stuetz).sp(e2.norm)) + '= 0'			
                dm('\quad \quad \;' + lat) 
                if isinstance(e1.schnitt(e2), set):
                    print(anf + "die Gleichung hat keine Lösung, die Ebenen schneiden sich nicht")	
                    print("\nDie Ebenen sind parallel\n")
                    return					
                if isinstance(e1.schnitt(e2), Ebene):
                    print(anf + "die Gleichung wird von allen Punkten von E1 erfüllt")	
                    print("\nDie Ebenen sind identisch\n")	
                    return					
                print(anf + "Auflösen nach einer Variablen")	
                gl = (pp - e2.stuetz).sp(e2.norm)
                var = gl.free_symbols.pop()	
                L = solve(gl, var)
                lat = latex(var) + '=' + latex(L[0])				
                display(Math('\quad \quad \;' + lat))
				
                print(anf + "Einsetzen in die Gleichung von E1")
                par = e1.par	
                lat = latex(X)+ latex('=') + latex(e1.stuetz) + '+' + \
                      ('\\left(' + latex(L[0]) + '\\right)' if var == par[0] \
                                                 else str(par[0])) + \
                      latex(e1.richt[0]) + '+' + \
					      ('\\left(' + latex(L[0]) + '\\right)' if var == par[1] \
                                                 else str(par[1])) + \
                      latex(e1.richt[1])	
                display(Math('\quad \quad \;' + lat))
                print(anf + "und Zusammenfassen führt auf die Gleichung einer Geraden,")
                print(anf + "in der sich die Ebenen schneiden")
                vv = e1.stuetz + \
                      (L[0] if var == par[0] else par[0]) * e1.richt[0] + \
					      (L[0] if var == par[1] else par[1]) * e1.richt[1]	
                gg = Gerade(vv)
                lat = pgerade(gg)
                display(Math('\quad \quad \;' + lat))
                print("\n")
				
LEE = LageEbeneEbene



# -----------------
# WinkelEbeneEbene
# -----------------

def WinkelEbeneEbene(*args, **kwargs):

    if kwargs.get('h'):
        print("\nWinkelEbeneEbene - Verfahren\n")
        print("Winkel zwischen zwei Ebenen\n")
        print("Aufruf     WEE( ebene1, ebene2 )\n")		                     
        print("                ebene    Ebene\n")
        return		
		
    if len(args) != 2:
        print("agla: zwei Ebenen angeben")
        return
				
    anf = '     '				
    e1, e2 = args
    if not (isinstance(e1, Ebene) and isinstance(e2, Ebene)):
        print("agla: zwei Ebenen angeben")
        return
		
    if mit_param(e1) or mit_param(e2):		
        print("agla: nicht implementiert, Parameter")
        return

    print("\nWinkel zwischen zwei Ebenen\n")
    print("Gegeben:")
    lat1 = 'E1 : \;'
    if e1._typ == 1:
        lat1 += pnf(e1, X)
    elif e1._typ == 2:
        lat1 += pprg(e1) 
    else:
        lat1 += pkoord(e1, X)	
    lat2 = 'E2 : \;'
    if e2._typ == 1:
        lat2 += pnf(e2, X)
    elif e2._typ == 2:
        lat2 += pprg(e2) 
    else:
        lat2 += pkoord(e2, X)	
    display(Math('\quad \quad ' + lat1 + ', \quad \quad ' + lat2))
    if e1._typ == 1:
        gl1 = "Normalenform"
    elif e1._typ == 2:
        gl1 = "Parametergleichung"
    elif e1._typ == 3:
        gl1 = "Koordinatenform"
    if e2._typ == 1:
        gl2 = "Normalenform"
    elif e2._typ == 2:
        gl2 = "Parametergleichung"
    elif e2._typ == 3:
        gl2 = "Koordinatenform"
    print("\nE1 - " + gl1 +",  " + "E2 - " + gl2)	
    txt = ''	
    if e1._typ == 2 and e2._typ == 2:
        txt = 'E1 und E2'	
    elif e1._typ == 2:
        txt = 'E1'	
    elif e2._typ == 2:
        txt = 'E2'
    if txt:
        print("\nErmittlung eines Normalenvektors von " + txt +  \
                                    "   (s.a. ENV - EbeneNormalenVektor)")	
    print("\nNormalenvektoren der Ebenen sind")
    n1, n2 = e1.norm, e2.norm
    display(Math('\quad \quad ' + '\\vec{m} =' + latex(n1) + ', \;\;\; \\vec{n} =' + latex(n2)))
    print("Der gesuchte Winkel ist der zwischen diesen beiden Vektoren, es ist")
    lat = '\cos \\alpha =' + '\\frac{\\left|\, \\vec{m} \\circ \\vec{n} \,\\right|}' + \
                         '{ \\left| \\vec{m} \\right| \\cdot \\left| \\vec{n} \\right|}' + \
         '\qquad \qquad 0 ^\\circ \\le \\alpha \\le 90 ^\\circ'						 
    display(Math('\quad \quad \;' + lat))
    print("Berechnung nach der Formel:")
    lat = '\cos \\alpha =' + '\\frac{\\left|\,' + latex(n1) + ' \\circ' + latex(n2) + '\,\\right|}' + \
                         '{' + latex(n1.betrag) + '\\cdot' + latex(n2.betrag) + '}'
    display(Math('\quad \quad \;' + lat))
    aa = abs((n1.sp(n2)/(n1.betrag*n2.betrag)))	
    lat = '\quad \:\:\:\,\, =' + '\\frac{' + latex(abs(n1.sp(n2))) + '}' + \
                         '{' + latex(n1.betrag * n2.betrag) + '}' + \
         ('=' + latex(aa.evalf()) if  not isinstance(aa, (int, Integer, float, Float)) else '')						 
    display(Math('\quad \quad \;' + lat))
    lat = ' \\alpha =' + latex((arccosg(abs((n1.sp(n2)/(n1.betrag*n2.betrag))))).evalf()) + '\,^\\circ'
    display(Math('\quad \quad \;' + lat))
	
WEE = WinkelEbeneEbene



# -------------------
# AbstandGeradeEbene
# -------------------

def AbstandGeradeEbene(*args, **kwargs):

    if kwargs.get('h'):
        print("\nAbstandGeradeEbene - Verfahren\n")     
        print("Abstand zwischen Gerade und Ebene\n")		
        print("Aufruf     AGE( gerade, ebene )\n")		                     
        print("                gerade   Gerade")
        print("                ebene    Ebene\n")
        return		
		
    if len(args) != 2:
        print("agla: Gerade und Eben angeben")
        return
				
    anf = '     '				
    gg, ee = args
    if not (isinstance(gg, Gerade) and isinstance(ee, Ebene)):
        if isinstance(ee, Gerade) and isinstance(gg, Ebene):
            gg, ee = ee, gg
        else:
            print("agla: Gerade und Ebene angeben")
            return
		
    if gg.dim != 3:
        print("agla: Gerade im Raum R^3 angeben")
        return
		
    if mit_param(gg) or mit_param(ee):		
        print("agla: nicht implementiert, Parameter")
        return

    print("\nAbstand zwischen Gerade und Ebene\n")
    print("Gegeben:\n")
    lat1 = 'g : \;' + pgerade(gg)
    lat2 = 'E : \;'
    if ee._typ == 1:
        lat2 += pnf(ee, X)
    elif ee._typ == 2:
        lat2 += pprg(ee) 
    else:
        lat2 += pkoord(ee, X)	
    dm('\quad \quad ' + lat1 + ', \quad \quad ' + lat2)
    txt = ''	
    if ee._typ == 2:
        print("\nErmittlung eines Normalenvektors der Ebene" +  \
                                    "   (s.a. ENV - EbeneNormalenVektor)")	
    print("\nRichtungsvektor der Geraden und Normalenvektor der Ebene sind")
    ri, nn = gg.richt, ee.norm	
    dm('\quad \quad ' + latex(ri) + ', \; ' + latex(nn))
    print("\nUntersuchung auf Parallelität:\n")
    print(anf + "Die Vektoren sollen orthogonal sein")
    dm('\quad \quad ' + latex(ri) + '\\circ' + latex(nn) + '= 0')
    dm('\quad \quad \;' + latex(ri.sp(nn)) + '= 0')
    if ri.sp(nn):
        print(anf + "Die Bedingung ist nicht erfüllt, keine Parallelität")
        print(anf + "die Gerade schneidet die Ebene")
        dm('Abstand \;\; d(g, E) = 0')
        print('\n')
        return		
    print(anf + "Die Bedingung ist erfüllt, die Gerade ist")
    print(anf + "parallel zur Ebene")
    print("\nErmittlung des Abstandes:\n")
    print(anf + "Ermittlung des Abstandes eines Punktes von g zur Ebene E")	
    print(anf + "durch Einsetzen der Punktkoordinaten in die linke Seite der")
    print(anf + "Hessesche Normalenform  (s.a. APE - AbstandPunktEbene)")
    print(anf + "Hessesche Normalenform von E")
    dm('\quad \quad \;' + phnf(ee, X))
    print(anf + "Einsetzen des Stützvektors von g")
    dm('\quad \quad \; d =' + phnf_ohne0(ee, gg.stuetz))
	
    lat = 'd = \\left(' + psp2(gg.stuetz, ee.stuetz, ee.norm) + '\\right)' + \
        ('\\cdot' if ee.norm.betrag != 1 else '') + \
        (latex(1/ee.norm.betrag) if ee.norm.betrag != 1 else '')		
    dm('\quad \quad \;' + lat)
    lat = 'd = ' + latex((gg.stuetz - ee.stuetz).sp(ee.norm)) + \
        ('\\cdot' if ee.norm.betrag != 1 else '') + \
        (latex(1/ee.norm.betrag) if ee.norm.betrag != 1 else '')		
    dm('\quad \quad \;' + lat)
    dd = abs(gg.abstand(ee))
    if isinstance(dd, (int, Integer, float, Float)):
        dm('Abstand: \;\;' + 'd(g, E) =' + latex(dd))
    else:		
        dm('Abstand: \;\;' + 'd(g, E) =' + latex(dd) + \
        '\\quad [ \;' + latex(float(dd)) + '\ ]' )
    print("\n")
	
AGE = AbstandGeradeEbene
	
	

# --------------------	
# AbstandGeradeGerade
# --------------------

def AbstandGeradeGerade(*args, **kwargs):

    if kwargs.get('h'):
        print("\nAbstandGeradeGerade - Verfahren\n")
        print("Abstand zwischen zwei Geraden, Version 0 über Abstand eines Punktes")
        print("von einer Ebene\n")
        print("Aufruf     AGG( gerade, gerade )\n")		                     
        print("                gerade   Gerade\n")
        return		
		
    if len(args) != 2:
        print("agla: zwei Geraden angeben")
        return
				
    anf = '     '				
    g1, g2 = args
    if not (isinstance(g1, Gerade) and isinstance(g2, Gerade)):
        print("agla: zwei Geraden angeben")
        return
		
    if g1.dim != 3 or g2.dim != 3:
        print("agla: zwei Geraden im Raum R^3 angeben")
        return
		
    if mit_param(g1) or mit_param(g2):		
        print("agla: nicht implementiert, Parameter")
        return

    print("\nAbstand zwischen zwei Geraden\n")
    print("Gegeben:\n")
    s, t = Symbol('s'), Symbol('t')	
    g1 = Gerade(g1.stuetz, g1.richt, s)	
    g2 = Gerade(g2.stuetz, g2.richt, t)	
    lat1 = 'g1 : \;' + pgerade(g1)
    lat2 = 'g2 : \;' + pgerade(g2)
    dm('\quad \quad ' + lat1 + ', \quad \quad ' + lat2)
    print("\nErmittlung der Lage der beiden Geraden:    (s.a. LGG - LageGeradeGerade)\n")
    if parallel(g1, g2):	
        if identisch(g1, g2):
            print(anf + "Die Geraden sind identisch")
            print("\nDer Abstand ist gleich 0\n")
            return			
        else:			
            print(anf + "Die Geraden sind parallel")
            print("\nErmittlung des Lotes vom Ort P des Stützvektor von g1 auf g2:\n")	
            print(anf + "Die zu g2 senkrechte Ebene durch P ist")
            P = g1.stuetz			
            ee = Ebene(P, g2.richt)
            dm('\quad \quad \;' + pnf(ee, X))
            print(anf + "g2 schneidet diese Ebene im Lotfußpunkt F  (s.a. LGE - LageGeradeEbene)")
            F = g2.schnitt(ee)			
            dm('\quad \quad \;' + 'F=' +latex(F))
            print("\nDer gesuchte Abstand zwischen den Geraden ist der zwischen ")
            print("den Punkten P und F")
            print('\n')			
            dd = P.abstand(F)			
            if isinstance(dd, (int, Integer, float, Float)):
                dm('Abstand: \;\;' + 'd(g1, g2) =' + latex(dd))
            dm('Abstand: \;\;' + 'd(g1, g2) =' + latex(dd) + \
                        '\\quad [ \;' + latex(float(dd)) + '\ ]' )
            print("\n")
            return						
    if g1.schnitt(g2):	
        print(anf + "Die Geraden schneiden sich")
        print("\nDer Abstand ist gleich 0\n")		
        return					
    print(anf + "Die Geraden sind windschief")	
    print("\nKonstruktion von zwei Hilfsebenen:\n")	
    print(anf + "Die beiden Ebenen, die jeweils mittels des Stützvektors von")
    print(anf + "g1 bzw. g2 sowie den beiden Richtungsvektoren erzeugt werden,")
    r, s = Symbol('r'), Symbol('s')	
    e1 = Ebene(g1.stuetz, g1.richt, g2.richt, r, s)
    e2 = Ebene(g2.stuetz, g1.richt, g2.richt, r, s)	
    dm('\quad \quad \;' + pprg(e1))
    dm('\quad \quad \;' + pprg(e2))

    print(anf + "sind parallel und haben den gleichen Abstand wie die beiden Geraden")
    print(anf + "(s.a. AEE - AbstandEbeneEbene)")
    dd = Abs(e1.abstand(e2))			
    if isinstance(dd, (int, Integer, float, Float)):
        dm('Abstand: \;\;' + 'd(g1, g2) =' + latex(dd))
    else:		
        dm('Abstand: \;\;' + 'd(g1, g2) =' + latex(dd) + \
             '\\quad [ \;' + latex(float(dd)) + '\ ]' )
    print("\n")

AGG = AbstandGeradeGerade
	
	
	
# ----------------------------	
# AbstandGeradeGeradeVersion1
# ----------------------------

def AbstandGeradeGeradeVersion1(*args, **kwargs):

    if kwargs.get('h'):
        print("\nAbstandGeradeGerade - Verfahren\n")
        print("Abstand zwischen zwei Geraden, Version 1 über eine Abstandsformel\n")
        print("Aufruf     AGG1( gerade, gerade )\n")		                     
        print("                 gerade   Gerade\n")
        return		
		
    if len(args) != 2:
        print("agla: zwei Geraden angeben")
        return
				
    anf = '     '				
    g1, g2 = args
    if not (isinstance(g1, Gerade) and isinstance(g2, Gerade)):
        print("agla: zwei Geraden angeben")
        return
		
    if g1.dim != 3 or g2.dim != 3:
        print("agla: zwei Geraden im Raum R^3 angeben")
        return
		
    if mit_param(g1) or mit_param(g2):		
        print("agla: nicht implementiert, Parameter")
        return

    print("\nAbstand zwischen zwei Geraden\n")
    print("Gegeben:\n")
    s, t = Symbol('s'), Symbol('t')	
    g1 = Gerade(g1.stuetz, g1.richt, s)	
    g2 = Gerade(g2.stuetz, g2.richt, t)	
    lat1 = 'g1 : \;' + pgerade(g1)
    lat2 = 'g2 : \;' + pgerade(g2)
    dm('\quad \quad ' + lat1 + ', \quad \quad ' + lat2)
    print("\nErmittlung der Lage der beiden Geraden:    (s.a. LGG - LageGeradeGerade)\n")
    if parallel(g1, g2):	
        if identisch(g1, g2):
            print(anf + "Die Geraden sind identisch")
            print("\nDer Abstand ist gleich 0\n")
            return			
        else:			
            print(anf + "Die Geraden sind parallel")
            print("\nDie Berechnung des Abstandes erfolgt anhand einer Formel\n")	
            print(anf + "Abstandsformel\n")			
            lat = 'd = \\sqrt{ (\\vec{q} - \\vec{p})^2 - ((\\vec{q} - \\vec{p}) \\circ \\vec{m}_0)^2}'			
            dm('\quad \quad \;' + lat)
            lat = 'd - gesuchter\; Abstand, \; \\vec{p} - Stuetzvektor\; von\; g1, \; \\vec{q} - Stuetzvektor \;von\ g2, \;'
            lat1 = '\\vec{m}_0 - Richtungseinheitsvekor \;der\; beiden\; Geraden'
            dm('\quad \quad \quad\;\;\;\;\;' + lat)
            dm('\quad \quad \quad\;\;\;\;\;' + lat1)
            p, q, m0 = g1.stuetz, g2.stuetz, g1.richt.einh_vekt			
            print("\nBerechnung nach der Formel")			
            lat = 'd = \\sqrt{ \\left(' + latex(q) + '-' + latex(p) + '\\right) \\circ \\left(' + \
                 latex(q) + '-' + latex(p) + '\\right)' + '-' + \
			       '\\left(' + latex(q) + '-' + '\\left(' + latex(p) + '\\right) \\circ' + latex(m0) + \
                 ' \\right) ^2}'			
            dm('\quad \quad \quad\;' + lat)
            lat = 'd = \\sqrt{' + latex(q-p) + '\\circ' + \
                 latex(q-p) + '-' + '\\left(' + \
			       latex(q-p) + '\\circ' + latex(m0) + '\\right) ^2}'			
            dm('\quad \quad \quad\;' + lat)
            lat = 'd = \\sqrt{' + latex((q-p).sp(q-p)) + '-' + latex((q-p).sp(m0)**2) + '}'			
            dm('\quad \quad \quad\;' + lat)
            print('\n')			
            dd = g1.abstand(g2)			
            if isinstance(dd, (int, Integer, float, Float)):
                dm('Abstand: \;\;' + 'd(g1, g2) =' + latex(dd))
            else:				
                dm('Abstand: \;\;' + 'd(g1, g2) =' + latex(dd) + \
                        '\\quad [ \;' + latex(float(dd)) + '\ ]' )
            print("\n")
            return						
    if g1.schnitt(g2):	
        print(anf + "Die Geraden schneiden sich")
        print("\nDer Abstand ist gleich 0\n")		
        return					
    print(anf + "Die Geraden sind windschief")
    print("\nDie Berechnung des Abstandes erfolgt anhand einer Formel  (s.a. APG... - AbstandPunktGerade...)\n")	
    print(anf + "Abstandsformel\n")	
    lat = 'd = \\left| \; (\\vec{q}-\\vec{p}) \\circ \\vec{n}_0 \; \\right| \qquad'	
    dm('\quad \quad \;' + lat)
    lat = 'd - gesuchter\; Abstand, \; \\vec{p} - Stuetzvektor\; von\; g1, \; \\vec{q} - Stuetzvektor \;von\ g2, \;'
    lat1 = '\\vec{n}_0 - Einheitsvektor,\; orthogonal\; zu\; den \;beiden\; Richtungsvekoren'
    dm('\quad \quad \quad\;\;\;\;\;' + lat)
    dm('\quad \quad \quad\;\;\;\;\;' + lat1)
    p, q = g1.stuetz, g2.stuetz
    n0 = g1.richt.vp(g2.richt).einh_vekt			
    print("\nBerechnung nach der Formel")			
    lat = 'd = \\left| \; \\left(' + latex(q) + '-' + latex(p) + '\\right)' + \
          '\\circ ' + latex(n0) + ' \; \\right| \qquad'	
    dm('\quad \quad \quad\;' + lat)
    lat = 'd = \\left| \;' + latex(q-p) + \
          '\\circ ' + latex(n0) + ' \; \\right| \qquad'	
    dm('\quad \quad \quad\;' + lat)
    lat = 'd = \\left| \; ' + psp(q-p, n0) + '\\right| \qquad'	
    dm('\quad \quad \quad\;' + lat)
    dd = abs(g1.abstand(g2))			
    lat = 'd =' + latex(dd)	
    dm('\quad \quad \quad\;' + lat)
    if isinstance(dd, (int, Integer, float, Float)):
        dm('Abstand: \;\;' + 'd(g1, g2) =' + latex(dd))
    else:		
        dm('Abstand: \;\;' + 'd(g1, g2) =' + latex(dd) + \
             '\\quad [ \;' + latex(float(dd)) + '\ ]' )
    print("\n")

AGG1 = AbstandGeradeGeradeVersion1
	

	
# ----------------------------	
# AbstandGeradeGeradeVersion2
# ----------------------------

def AbstandGeradeGeradeVersion2(*args, **kwargs):

    if kwargs.get('h'):
        print("\nAbstandGeradeGerade - Verfahren\n")
        print("Abstand zwischen zwei Geraden, Version 2 über die Ermittlung")
        print("der Lotfußpunkte\n")
        print("Aufruf     AGG2( gerade, gerade )\n")		                     
        print("                 gerade   Gerade\n")
        return		
		
    if len(args) != 2:
        print("agla: zwei Geraden angeben")
        return
				
    anf = '     '				
    g1, g2 = args
    if not (isinstance(g1, Gerade) and isinstance(g2, Gerade)):
        print("agla: zwei Geraden angeben")
        return
		
    if g1.dim != 3 or g2.dim != 3:
        print("agla: zwei Geraden im Raum R^3 angeben")
        return
		
    if mit_param(g1) or mit_param(g2):		
        print("agla: nicht implementiert, Parameter")
        return

    print("\nAbstand zwischen zwei Geraden\n")
    print("Gegeben:\n")
    s, t = Symbol('s'), Symbol('t')	
    g1 = Gerade(g1.stuetz, g1.richt, s)	
    g2 = Gerade(g2.stuetz, g2.richt, t)	
    lat1 = 'g1 : \;' + pgerade(g1)
    lat2 = 'g2 : \;' + pgerade(g2)
    dm('\quad \quad ' + lat1 + ', \quad \quad ' + lat2)
    print("\nDie Lotfußpunkte auf den beiden Ggeraden seien F (mit dem Parameterwert s)")
    print("und G (mit dem Parameterwert t), ihr Abstand ist der gesuchte Abstand\n")
    print("Es ist")
    lat = '\\vec{FG} =' + latex(g2.stuetz) + '+' + 't' + latex(g2.richt) + \
          '-' + latex(g1.stuetz) + '-' + 's' + latex(g1.richt)	
    dm('\quad \quad \;' + lat)
    vv = g2.stuetz + t*g2.richt - g1.stuetz - s*g1.richt	
    lat = '\\vec{FG} =' + latex(vv)	
    dm('\quad \quad \;' + lat)
    print("Der Vektor ist orthogonal zu den beiden Richtungsvektoren, das Skalarprodukt ist 0")	
    dm('\quad \quad \;' + latex(vv) + '\\circ ' + latex(g1.richt) + '=0')
    dm('\quad \quad \;' + latex(vv) + '\\circ ' + latex(g2.richt) + '=0')
    print("\nEs ergibt sich das LGS\n") 	
    lgs = LGS([vv.sp(g1.richt), vv.sp(g2.richt)])
    lgs.ausg_ohne_nr
    L = lgs.loes		
    c1 = Symbol('c1')
    L = lgs.loes	
    if any([val.has(c1) for val in L.values() \
        if not isinstance(val, (int, float))]):   # 1 Parameter, unendlich viele Lösungen					   
        txt = "(sie hat unendlich viele Elemente - die Geraden sind parallel\n" + anf + "oder identisch)"
        fall = 1		
    else:   # eine Lösung
        txt = "(sie ist eindeutig - die Geraden sind windschief oder\n" + anf + "schneiden sich)"
        fall = 2		
    print('\n' + anf + "mit der Lösung " + txt) 
    dm('\quad \quad \;' + latex(L))
    if fall == 1:
        s0, t0 = L[s].subs(c1, 0), L[t].subs(c1, 0)
        print("\nMit  s = " + str(s0) + ', t = ' + str(t0) + "  sind zwei zusammengehörende Lotfußpunkte")
        F, G = g1.pkt(s0), g2.pkt(t0)		
        dm('\quad \quad \;' + 'F = ' + latex(F) + ', \; G =' + latex(G))
    else:		
        s0, t0 = L[s], L[t]
        F, G = g1.pkt(s0), g2.pkt(t0)	
        print("\nDie Lotfußpunkte sind")		
        dm('\quad \quad \;' + 'F = ' + latex(F) + ', \; G =' + latex(G))
    print("\nDer gesuchte Abstand ist der Abstand zwischen diesen beiden Punkten")
    if F == G:
        print("sie fallen zusammen, der Abstand ist also gleich Null\n")
        return		
    dd = abs(g1.abstand(g2))			
    lat = 'd =' + latex(dd)	
    dm('\quad \quad \quad\;' + lat)
    if isinstance(dd, (int, Integer, float, Float)):
        dm('Abstand: \;\;' + 'd(g1, g2) =' + latex(dd))
    else:		
        dm('Abstand: \;\;' + 'd(g1, g2) =' + latex(dd) + \
             '\\quad [ \;' + latex(float(dd)) + '\ ]' )
    print("\n")
	
AGG2 = AbstandGeradeGeradeVersion2



# ------------------
# AbstandPunktPunkt
# ------------------

def AbstandPunktPunkt(*args, **kwargs):

    if kwargs.get('h'):
        print("\nAbstandPunktPunkt - Verfahren\n")
        print("Abstand zwischen zwei Punkten\n")
        print("Aufruf     APP( punkt, punkt )\n")		                     
        print("                punkt   Punkt\n")
        return		
		
    if len(args) != 2:
        print("agla: zwei Punkte angeben")
        return
				
    anf = '     '				
    p1, p2 = args
    if not (isinstance(p1, Vektor) and isinstance(p2, Vektor)):
        print("agla: zwei Punkte angeben")
        return
		
    if p1.dim != 3 or p2.dim != 3:
        print("agla: zwei Punkte im Raum R^3 angeben")
        return
				
    if mit_param(p1) or mit_param(2):		
        print("agla: nicht implementiert, Parameter")
        return

    print("\nAbstand zwischen zwei Punkten\n")
    print("Gegeben:\n")
    dm('\quad \quad \; P' + ppunkt(p1) + ', \qquad Q' + ppunkt(p2))
    print("\nAbstandsformel für zwei Punkte\n")
    lat = 'P_1(\; x_1 \; |\; y_1 \;|\; z_1\;)' + \
	      ', \qquad P_2(\; x_2 \; |\; y_2 \;|\; z_2\;)'	
    dm('\quad \quad \;' + lat)
    print('\n')	
    lat = 'd(P_1,P_2) = \\sqrt{ (x_2-x_1)^2 + (y_2-y_1)^2 + (z_2-z_1)^2}'         
    dm('\quad \quad \;' + lat)
    print("\nBerechnung nach der Formel\n")
    lat = 'd = \\sqrt{ (' + str(p2.x) + ('+' if p1.x <= 0 else '-') + str(abs(p1.x)) + ')^2 +' \
	      + '(' + str(p2.y) + ('+' if p1.y <= 0 else '-') + str(abs(p1.y)) + ')^2 +' \
	      + '(' + str(p2.z) + ('+' if p1.z <= 0 else '-') + str(abs(p1.z)) + ')^2 }' 
    dm('\quad \quad \;' + lat)
    lat = 'd = \\sqrt{' + latex((p2.x-p1.x)**2 + (p2.y-p1.y)**2 + (p2.z-p1.z)**2) + '}' 
    dm('\quad \quad \;' + lat)
    dd = abs(p1.abstand(p2))			
    if isinstance(dd, (int, Integer, float, Float)):
        dm('Abstand: \;\;' + 'd(P, Q) =' + latex(dd))
    else:		
        dm('Abstand: \;\;' + 'd(P, Q) =' + latex(dd) + \
             '\\quad [ \;' + latex(float(dd)) + '\ ]' )
    print("\n")
	
APP = AbstandPunktPunkt



# ------------------
# AbstandPunktEbene
# ------------------

def AbstandPunktEbene(*args, **kwargs):

    if kwargs.get('h'):
        print("\nAbstandPunktEbene - Verfahren\n")
        print("Abstand eines Punktes von einer Ebene, Version 0 über die")
        print("Hessesche Normalenform\n")
        print("Aufruf     APE( punkt, ebene )\n")		                     
        print("                punkt    Punkt")		
        print("                ebene    Ebene\n")
        return		
		
    if len(args) != 2:
        print("agla: Punkt und Ebene angeben")
        return
				
    anf = '     '				
    pp, ee = args
    if not (isinstance(pp, Vektor) and isinstance(ee, Ebene)):
        if isinstance(ee, Vektor) and isinstance(pp, Ebene):
            pp, ee = ee, pp
        else:
            print("agla: Punkt und Ebene angeben")
            return
		
    if pp.dim != 3:
        print("agla: Punkt des Raumes R^3 angeben")
        return
		
    if mit_param(pp) or mit_param(ee):		
        print("agla: nicht implementiert, Parameter")
        return

    print("\nAbstand eines Punktes von einer Ebene\n")
    print("Gegeben:\n")
    lat1 = 'P \\left( \;' + latex(pp.x) + '\; \\left| \; ' + latex(pp.y) + '\; \\right| \; ' \
          + latex(pp.z) + '\; \\right)'	
    lat2 = 'E : \;'
    if ee._typ == 1:
        lat2 += pnf(ee, X)
    elif ee._typ == 2:
        lat2 += pprg(ee) 
    else:
        lat2 += pkoord(ee, X)	
    dm('\quad \quad ' + lat1 + ', \quad \quad ' + lat2)
    if ee._typ != 1:	
        print("\nErmittlung einer Normalenform der Ebenengleichung")
        ee = Ebene(ee.stuetz, ee.norm)
        dm('\quad \quad \;' + pnf(ee, X))
    print("\nDer Abstand wird mit einer Abstandsformel berechnet\n")		
    lat = 'd = \\left[ \\vec{q} - \\vec{p} \\right] \\circ \\vec{n}_0'		
    dm('\quad \quad \; ' + lat)	
    lat = 'd - gesuchter\; Abstand, \; \\vec{p} - Ortsvektor\; des \;Punktes\; P, \; \\vec{q} - Stuetzvektor \;von\ E, \;'
    lat1 = '\\vec{n}_0 - Normaleneinheitsvektor\; von\; E'
    dm('\quad \quad \quad\;\;\;\;\; ' + lat)
    dm('\quad \quad \quad\;\;\;\;\; ' + lat1)
    print('\n' + anf + anf + "(Einsetzen der Punktkoordinaten in die Hessesche Normalenform von E)")
    print("\nBerechnung nach der Formel\n")
    print(anf + "Hessesche Normalenform")
    dm('\quad \quad \; ' + phnf(ee, X))
    dm('\quad \quad \; d =' + phnf_ohne0(ee, pp))
    if ee.norm.betrag != 1:	
        lat = 'd =' + latex(pp - ee.stuetz) + '\circ' + latex(ee.norm) \
            + '\cdot' + latex(1/ee.norm.betrag)  
    else:
        lat = 'd =' + latex(pp - ee.stuetz) + '\circ' + latex(ee.norm) 	
    dm('\quad \quad \; ' + lat)
    if ee.norm.betrag != 1:	
        lat = 'd = \\left(' + psp(pp-ee.stuetz, ee.norm) + '\\right) \cdot' + latex(1/ee.norm.betrag)
    else:
        lat = 'd =' + psp(pp-ee.stuetz, ee.norm)
    dm('\quad \quad \; ' + lat)
    if ee.norm.betrag != 1:	
        lat = 'd = ' + latex((pp - ee.stuetz).sp(ee.norm)) + '\\cdot' + latex(1/ee.norm.betrag)
    else:		
        lat = 'd = ' + latex((pp - ee.stuetz).sp(ee.norm))
    dm('\quad \quad \; ' + lat)
    dd = abs(pp.abstand(ee))			
    if isinstance(dd, (int, Integer, float, Float)):
        dm('Abstand: \;\;' + 'd(P, E) =' + latex(dd))
    else:		
        dm('Abstand: \;\;' + 'd(P, E) =' + latex(dd) + \
             '\\quad [ \;' + latex(float(dd)) + '\ ]' )
    print("\n")
	
APE = AbstandPunktEbene



# --------------------------
# AbstandPunktEbeneVersion1
# --------------------------

def AbstandPunktEbeneVersion1(*args, **kwargs):

    if kwargs.get('h'):
        print("\nAbstandPunktEbene - Verfahren\n")
        print("Abstand eines Punktes von einer Ebene, Version 1 über die")
        print("Ermittlung des Lotfußpunktes\n")
        print("Aufruf     APE1( punkt, ebene )\n")		                     
        print("                 punkt    Punkt")		
        print("                 ebene    Ebene\n")
        return		
		
    if len(args) != 2:
        print("agla: Punkt und Ebene angeben")
        return
				
    anf = '     '				
    pp, ee = args
    if not (isinstance(pp, Vektor) and isinstance(ee, Ebene)):
        if isinstance(ee, Vektor) and isinstance(pp, Ebene):
            pp, ee = ee, pp
        else:
            print("agla: Punkt und Ebene angeben")
            return
		
    if pp.dim != 3:
        print("agla: Punkt des Raumes R^3 angeben")
        return
		
    if mit_param(pp) or mit_param(ee):		
        print("agla: nicht implementiert, Parameter")
        return

    print("\nAbstand eines Punktes von einer Ebene\n")
    print("Gegeben:\n")
    lat1 = 'P \\left( \;' + latex(pp.x) + '\; \\left| \; ' + latex(pp.y) + '\; \\right| \; ' \
           + latex(pp.z) + '\; \\right)'	
    lat2 = 'E : \;'
    if ee._typ == 1:
        lat2 += pnf(ee, X)
    elif ee._typ == 2:
        lat2 += pprg(ee) 
    else:
        lat2 += pkoord(ee, X)	
    dm('\quad \quad ' + lat1 + ', \quad \quad ' + lat2)
    r, s = Symbol('r'), Symbol('s')		
    if ee._typ != 2:	
        print("\nErmittlung einer Parametergleichung der Ebene")
        ee = Ebene(ee.stuetz, ee.richt[0], ee.richt[1], r, s)
        dm('\quad \quad \;' + pprg(ee))
    print("\nRichtungsvektoren der Ebene sind")
    dm('\quad \quad \; \\vec{u} =' + latex(ee.richt[0]) + ', \;\; \\vec{v} =' + latex(ee.richt[1]))	
    print("\nErmittlung des Lotfußpunktes F:")
    print('\n' + anf + "Der Vekor v(P,F) steht senkrecht auf den Richtungsvektoren der Ebene,")
    print(anf + "es muss gelten")
    dm('\quad \quad \; \\vec{PF} \\circ \\vec{u} = 0')	
    dm('\quad \quad \; \\vec{PF} \\circ \\vec{v} = 0')	
    print("\n" + anf + "F ist Ebenenpunkt bei bestimmten Parameterwerten r und s, aus der")	
    print(anf + "Ebenengleichung ergibt sich über den Ortsvektor")	
    qq = ee.pkt(r, s)	
    dm('\quad \quad \; \\vec{OF} = ' + latex(qq))	
    dm('\quad \quad \; \\vec{PF} = ' + latex(qq) + '-' + latex(pp))	
    print("\n" + anf + "Einsetzen in die obigen Gleichungen und Ausmultiplizieren führt auf ein LGS")	
    lat = latex(qq - pp) + '\\circ' + latex(ee.richt[0]) + '= 0'
    dm('\quad \quad \; ' + lat)	
    lat = latex(qq - pp) + '\\circ' + latex(ee.richt[1]) + '= 0'
    dm('\quad \quad \; ' + lat)	
    lgs = LGS([(qq - pp).sp(ee.richt[0]), (qq - pp).sp(ee.richt[1])])
    print(anf + "also\n")	
    lgs.ausg_ohne_nr	
    print("\n" + anf + "Auflösen")	
    L = lgs.loes
    lat = 'r = ' + latex(L[r]) + ', \;\; s = ' + latex(L[s])	
    dm('\quad \quad \; ' + lat)	
    F = ee.pkt(L[r], L[s])	
    print(anf + "und in die Ebenengleichung einsetzen ergibt den Lotfußpunkt")	
    dm('\quad \quad \; F \left(\, ' + latex(F.x) + '\,\\left|  \,' + latex(F.y) + '\, \\right| \,'\
       + latex(F.z) + '\, \\right)')	
    print("\nDer gesuchte Abstand ist der zwischen P und F")	
    dm('\quad \quad \; d = ' + latex(pp.abstand(F)))	
    dd = abs(pp.abstand(ee))			
    if isinstance(dd, (int, Integer, float, Float)):
        dm('Abstand: \;\;' + 'd(P, E) =' + latex(dd))
    else:		
        dm('Abstand: \;\;' + 'd(P, E) =' + latex(dd) + \
             '\\quad [ \;' + latex(float(dd)) + '\ ]' )
    print("\n")
	
APE1 = AbstandPunktEbeneVersion1
	



# --------------------------
# AbstandPunktEbeneVersion2
# --------------------------

def AbstandPunktEbeneVersion2(*args, **kwargs):

    if kwargs.get('h'):
        print("\nAbstandPunktEbene - Verfahren\n")
        print("Abstand eines Punktes von einer Ebene, Version 2 über den")
        print("Schnitt mit der Lotgeraden\n")
        print("Aufruf     APE2( punkt, ebene )\n")		                     
        print("                 punkt    Punkt")		
        print("                 ebene    Ebene\n")
        return		
		
    if len(args) != 2:
        print("agla: Punkt und Ebene angeben")
        return
				
    anf = '     '				
    pp, ee = args
    if not (isinstance(pp, Vektor) and isinstance(ee, Ebene)):
        if isinstance(ee, Vektor) and isinstance(pp, Ebene):
            pp, ee = ee, pp
        else:
            print("agla: Punkt und Ebene angeben")
            return
		
    if pp.dim != 3:
        print("agla: Punkt des Raumes R^3 angeben")
        return
		
    if mit_param(pp) or mit_param(ee):		
        print("agla: nicht implementiert, Parameter")
        return

    print("\nAbstand eines Punktes von einer Ebene\n")
    print("Gegeben:\n")
    lat1 = 'P(\;' + latex(pp.x) + '\; |\; ' + latex(pp.y) + '\;|\; ' + latex(pp.z) + '\;)'	
    lat2 = 'E : \;'
    if ee._typ == 1:
        lat2 += pnf(ee, X)
    elif ee._typ == 2:
        lat2 += pprg(ee) 
    else:
        lat2 += pkoord(ee, X)	
    dm('\quad \quad ' + lat1 + ', \quad \quad ' + lat2)
    nn = ee.norm	
    print("\nNormalenvektor der Ebene und damit Richtungsvektor der Lotgeraden ist")
    dm('\quad \quad \;' + latex(nn))
    print("Die Lotgerade von P auf die Ebene E hat dann die Gleichung")
    r = Symbol('r')
    gg = Gerade(pp, nn, r)	
    dm('\quad \quad \;' + pgerade(gg))
    if ee._typ != 3:
        print("\nEine Koordinatengleichung der Ebene ist")	
        ee = Ebene(nn.x, nn.y, nn.z, -nn.sp(ee.stuetz))		
        dm('\quad \quad \;' + pkoord(ee, X))
    print("\nEinsetzen der rechten Seite der Geradengleichung in die Koordinaten-")
    print("gleichung der Ebene führt zu")    	
    dm('\quad \quad \;' + psp(ee.norm, gg.pkt(r)) + ('+' \
            if ee.args[3] >= 0 else '-') + latex(abs(ee.args[3])) + '= 0')
    dm('\quad \quad \;' + pkoord(ee, gg.pkt(r)))
    print(anf + "mit der Lösung")
    lgs = LGS([ee.norm.sp(gg.pkt(r)) + ee.args[3]])
    L = lgs.loes
    dm('\quad \quad \; r =' + latex(L[r]))
    print(anf + "Einsetzen in die Geradengleichung ergibt den Schnittpunkt (Lotfußpunkt)")
    F = gg.pkt(L[r])    
    lat = 'F \\left( \;' + latex(F.x) + '\; \\left| \; ' + latex(F.y) + '\;\\right| \; ' + \
          latex(F.z) + '\; \\right)'	
    dm('\quad \quad \; ' + lat)
    print("\nDer gesuchte Abstand ist der zwischen P und F")	
    dm('\quad \quad \; d =' + latex(pp.abstand(F)))
    dd = abs(pp.abstand(ee))			
    if isinstance(dd, (int, Integer, float, Float)):
        dm('Abstand: \;\;' + 'd(P, E) =' + latex(dd))
    else:		
        dm('Abstand: \;\;' + 'd(P, E) =' + latex(dd) + \
             '\\quad [ \;' + latex(float(dd)) + '\ ]' )
    print("\n")

APE2 = AbstandPunktEbeneVersion2



# -------------------
# AbstandPunktGerade
# -------------------

def AbstandPunktGerade(*args, **kwargs):

    if kwargs.get('h'):
        print("\nAbstandPunktGerade - Verfahren\n")
        print("Abstand eines Punktes von einer Geraden, Version 0 über eine")
        print("Hilfsebene mit Normalengleichung\n")
        print("Aufruf     APG( punkt, gerade )\n")		                     
        print("                punkt    Punkt")		
        print("                gerade   Gerade\n")
        return		
		
    if len(args) != 2:
        print("agla: Punkt und Gerade angeben")
        return
				
    anf = '     '				
    pp, gg = args
    if not (isinstance(pp, Vektor) and isinstance(gg, Gerade)):
        if isinstance(gg, Vektor) and isinstance(pp, Gerade):
            pp, gg = gg, pp
        else:
            print("agla: Punkt und Gerade angeben")
            return
		
    if pp.dim != 3 or gg.dim != 3:
        print("agla: Punkt und Gerade im Raum R^3 angeben")
        return
		
    if mit_param(pp) or mit_param(gg):		
        print("agla: nicht implementiert, Parameter")
        return
		
    t = Symbol('t')		
    gg = Gerade(gg.stuetz, gg.richt, t)
    print("\nAbstand eines Punktes von einer Geraden\n")
    print("Gegeben:\n")
    lat1 = 'P' + ppunkt(pp)
    lat2 = 'g : \;' + pgerade(gg)
    dm('\quad \quad ' + lat1 + ', \quad \quad ' + lat2)
    print("\nBestimmung der Ebene E, die senkrecht zu g ist und P enthält:\n")
    print(anf + "Normalenvektor ist der Richtungsvektor von g, Normalenform ist dann")
    ee = Ebene(pp, gg.richt)	
    dm('\quad \quad \;' + pnf(ee, X))
    print("\nBestimmung des Schnittpunktes der Geraden mit dieser Ebene:\n")
    print(anf + "Einsetzen der rechten Seite der Geradengleichung in die ")
    print(anf + "Normalengleichung")	
    qq = gg.pkt(gg.par)
    dm('\quad \quad \;' + pnf(ee, qq))
    dm('\quad \quad \;' + latex(qq - pp) + '\\circ' + latex(gg.richt) + '= 0')
    dm('\quad \quad \;' + psp(qq - pp, gg.richt) + '= 0')
    dm('\quad \quad \;' + latex((qq - pp).sp(gg.richt)) + '= 0')
    print(anf + "und Auflösen")
    lgs = LGS([(qq - pp).sp(gg.richt)])
    L = lgs.loes
    dm('\quad \quad \; t =' + latex(L[t]))
    print(anf + "ergibt nach Einsetzen in die Geradengleichung den Schnittpunkt")	
    F = gg.pkt(L[t])    	
    lat = 'F' + ppunkt(F)
    dm('\quad \quad \; ' + lat)
    print("\nDer gesuchte Abstand ist der zwischen P unf F")
    dm('\quad \quad \; d =' + latex(pp.abstand(F)))
    dd = abs(pp.abstand(gg))			
    if isinstance(dd, (int, Integer, float, Float)):
        dm('Abstand: \;\;' + 'd(P, g) =' + latex(dd))
    else:		
        dm('Abstand: \;\;' + 'd(P, g) =' + latex(dd) + \
             '\\quad [ \;' + latex(float(dd)) + '\ ]' )
    print("\n")
	
APG = AbstandPunktGerade
	


# ---------------------------
# AbstandPunktGeradeVersion1
# ---------------------------

def AbstandPunktGeradeVersion1(*args, **kwargs):

    if kwargs.get('h'):
        print("\nAbstandPunktGerade - Verfahren\n")
        print("Abstand eines Punktes von einer Geraden, Version 1 über eine Hilfsebene\n")
        print("Aufruf     APG1( punkt, gerade )\n")		                     
        print("                 punkt    Punkt")		
        print("                 gerade   Gerade\n")
        return		
		
    if len(args) != 2:
        print("agla: Punkt und Gerade angeben")
        return
				
    anf = '     '				
    pp, gg = args
    if not (isinstance(pp, Vektor) and isinstance(gg, Gerade)):
        if isinstance(gg, Vektor) and isinstance(pp, Gerade):
            pp, gg = gg, pp
        else:
            print("agla: Punkt und Gerade angeben")
            return
		
    if pp.dim != 3 or gg.dim != 3:
        print("agla: Punkt und Gerade im Raum R^3 angeben")
        return
		
    if mit_param(pp) or mit_param(gg):		
        print("agla: nicht implementiert, Parameter")
        return
		
    t = Symbol('t')		
    gg = Gerade(gg.stuetz, gg.richt, t)
    print("\nAbstand eines Punktes von einer Geraden\n")
    print("Gegeben:\n")
    lat1 = 'P(' + ppunkt(pp)
    lat2 = 'g : \;' + pgerade(gg)
    dm('\quad \quad ' + lat1 + ', \quad \quad ' + lat2)
    print("\nBestimmung der Ebene E, die senkrecht zu g, steht und P enthält:\n")
    print(anf + "Normalenvektor ist der Richtungsvektor von g, Koordinatenform ist")	
    ri = gg.richt
    d = Symbol('d')	
    ee = Ebene(ri.x, ri.y, ri.z, d)
    dm('\quad \quad \;' + pkoord(ee, X))
    print(anf + "Einsetzen der Koordinaten von P ergibt")
    lgs = LGS([ri.sp(pp) + ee.args[3]]) 
    L = lgs.loes	
    tt = str(ee.koord.subs({x:pp.x, y:pp.y, z:pp.z})).replace(' ', '')	
    if tt != 'd=0':
        dm('\quad \quad \;' + pkoord(ee, pp) +', \;\;  d = ' + latex(L[d])) 
    else:		
        dm('\quad \quad \;' + 'd = ' + latex(L[d]))  
    print(anf + "damit ist die Gleichung von E")	
    ee = Ebene(ri.x, ri.y, ri.z, L[d])
    dm('\quad \quad \;' + pkoord(ee, X))
    print("\nBestimmung des Schnittpunktes der Geraden mit dieser Ebene:\n")
    print(anf + "Einsetzen der rechten Seite der Geradengleichung in die")	
    print(anf + "Ebenengleichung")	
    qq = gg.pkt(gg.par)
    dm('\quad \quad \;' + psp(qq, gg.richt) + ('+' if L[d] >= 0 else '-')\
        + latex(abs(L[d])) + '= 0')
    dm('\quad \quad \;' + latex((gg.richt).sp(qq - pp)) + '= 0')
    print('\n' + anf + "und Auflösen")
    lgs = LGS([(qq - pp).sp(gg.richt)])
    L = lgs.loes
    dm('\quad \quad \; t =' + latex(L[t]))
    print(anf + "ergibt nach Einsetzen in die Geradengleichung den Schnittpunkt")	
    F = gg.pkt(L[t])    	
    lat = 'F' + ppunkt(F)
    dm('\quad \quad \;' + lat)
    print("\nDer gesuchte Abstand ist der zwischen P unf F")
    dm('\quad \quad \; d =' + latex(pp.abstand(F)))
    dd = abs(pp.abstand(gg))			
    if isinstance(dd, (int, Integer, float, Float)):
        dm('Abstand: \;\;' + 'd(P, g) =' + latex(dd))
    else:		
        dm('Abstand: \;\;' + 'd(P, g) =' + latex(dd) + \
             '\\quad [ \;' + latex(float(dd)) + '\ ]' )
    print("\n")
	
APG1 = AbstandPunktGeradeVersion1
	
	
	
# ---------------------------	
# AbstandPunktGeradeVersion2
# ---------------------------

def AbstandPunktGeradeVersion2(*args, **kwargs):

    if kwargs.get('h'):
        print("\nAbstandPunktGerade - Verfahren\n")
        print("Abstand eines Punktes von einer Geraden, Version 2 über")
        print("eine Abstandsformel\n")
        print("Aufruf     APG2( punkt, gerade )\n")		                     
        print("                 punkt    Punkt")		
        print("                 gerade   Gerade\n")
        return		
		
    if len(args) != 2:
        print("agla: Punkt und Gerade angeben")
        return
				
    anf = '     '				
    pp, gg = args
    if not (isinstance(pp, Vektor) and isinstance(gg, Gerade)):
        if isinstance(gg, Vektor) and isinstance(pp, Gerade):
            pp, gg = gg, pp
        else:
            print("agla: Punkt und Gerade angeben")
            return
		
    if pp.dim != 3:
        print("agla: Punkt des Raumes R^3 angeben")
        return
		
    if mit_param(pp) or mit_param(gg):		
        print("agla: nicht implementiert, Parameter")
        return
		
    t = Symbol('t')		
    gg = Gerade(gg.stuetz, gg.richt, t)
    print("\nAbstand eines Punktes von einer Geraden\n")
    print("Gegeben:\n")
    lat1 = 'P(' + ppunkt(pp)
    lat2 = 'g : \;' + pgerade(gg)
    dm('\quad \quad ' + lat1 + ', \quad \quad ' + lat2)
	
    print('\n' + anf + "Der Abstand wird mit einer Abstandsformel berechnet\n")			
    lat = 'd = \\sqrt{ (\\vec{q} - \\vec{p})^2 - ((\\vec{q} - \\vec{p}) \\circ \\vec{m}_0)^2}'			
    dm('\quad \quad \;' + lat)
    lat = 'd - gesuchter\; Abstand, \; \\vec{p} - Ortsvektor\; von\; P, \; \\vec{q} - Stuetzvektor \;von\ g, \;'
    lat1 = '\\vec{m}_0 - Richtungseinheitsvekor \;von\; g'
    dm('\quad \quad \quad\;\;\;\;' + lat)
    dm('\quad \quad \quad\;\;\;\;' + lat1)
    p, q, m0 = pp, gg.stuetz, gg.richt.einh_vekt			
    print("\nBerechnung nach der Formel\n")			
    lat = 'd = \\sqrt{ \\left(' + latex(q) + '-' + latex(p) + '\\right) \\circ \\left(' + \
        latex(q) + '-' + latex(p) + '\\right)' + '-' + \
	     '\\left(' + latex(q) + '-' + '\\left(' + latex(p) + '\\right) \\circ' + latex(m0) + \
        ' \\right) ^2}'			
    dm('\quad \quad \quad\;' + lat)
    lat = 'd = \\sqrt{' + latex(q-p) + '\\circ' + \
          latex(q-p) + '-' + '\\left(' + \
			latex(q-p) + '\\circ' + latex(m0) + '\\right) ^2}'			
    dm('\quad \quad \quad\;' + lat)
    lat = 'd = \\sqrt{' + latex((q-p).sp(q-p)) + '-' + latex((q-p).sp(m0)**2) + '}'			
    dm('\quad \quad \quad\;' + lat)			
    dd = abs(pp.abstand(gg))			
    if isinstance(dd, (int, Integer, float, Float)):
        dm('Abstand: \;\;' + 'd(P, g) =' + latex(dd))
    else:		
        dm('Abstand: \;\;' + 'd(P, g) =' + latex(dd) + \
             '\\quad [ \;' + latex(float(dd)) + '\ ]' )
    print("\n")
	
APG2 = AbstandPunktGeradeVersion2
	
	
	
# ---------------------------	
# AbstandPunktGeradeVersion3
# ---------------------------

def AbstandPunktGeradeVersion3(*args, **kwargs):

    if kwargs.get('h'):
        print("\nAbstandPunktGerade - Verfahren\n")
        print("Abstand eines Punktes von einer Geraden, Version 3 über")
        print("die Ermittlung des Lotfußpunktes\n")
        print("Aufruf     APG3( punkt, gerade )\n")		                     
        print("                 punkt    Punkt")		
        print("                 gerade   Gerade\n")
        return		
		
    if len(args) != 2:
        print("agla: Punkt und Gerade angeben")
        return
				
    anf = '     '				
    pp, gg = args
    if not (isinstance(pp, Vektor) and isinstance(gg, Gerade)):
        if isinstance(gg, Vektor) and isinstance(pp, Gerade):
            pp, gg = gg, pp
        else:
            print("agla: Punkt und Gerade angeben")
            return
		
    if pp.dim != 3:
        print("agla: Punkt des Raumes R^3 angeben")
        return
		
    if mit_param(pp) or mit_param(gg):		
        print("agla: nicht implementiert, Parameter")
        return
		
    t = Symbol('t')		
    gg = Gerade(gg.stuetz, gg.richt, t)
    print("\nAbstand eines Punktes von einer Geraden\n")
    print("Gegeben:\n")
    lat1 = 'P' + ppunkt(pp)
    lat2 = 'g : \;' + pgerade(gg)
    dm('\quad \quad ' + lat1 + ', \quad \quad ' + lat2)
    print('\n' + anf + "Der Richtungsvektor der Geraden ist")
    dm('\quad \quad \;' + '\\vec{u} =' + latex(gg.richt))
    print("\nErmittlung des Lotfußpunktes F:\n")
    print(anf + "Der Vektor v(P,F) steht senkrecht auf dem Richtungsvektor der Geraden,")
    print(anf + "es muß gelten")
    dm('\quad \quad \;' + '\\vec{PF} \\circ \\vec{u} = 0')
    print('\n' + anf + "F ist Geradenpunkt bei einem bestimmten t, der Ortsvektor ist")	
    qq = gg.pkt(t)	
    dm('\quad \quad \;' + '\\vec{OF} = ' + latex(qq))
    print(anf + "und damit")	
    dm('\quad \quad \;' + '\\vec{PF} = ' + latex(qq) + '-' + latex(pp) + '=' + latex(qq-pp))
    print(anf + "Einsetzen in die obere Gleichung, nach t auflösen")	
    dm('\quad \quad \;' + latex(qq - pp) + '\\circ ' + latex(gg.richt) + '= 0')
    dm('\quad \quad \;' + psp(qq - pp, gg.richt) + '= 0')
    dm('\quad \quad \;' + latex((qq - pp).sp(gg.richt)) + '= 0')	
    lgs = LGS([(qq - pp).sp(gg.richt)])	
    L = lgs.loes
    dm('\quad \quad \; t =' + latex(L[t]))	
    print(anf + "und Einsetzen in die Geradengleichung ergibt den Lotfußpunkt")
    F = gg.pkt(L[t])
    dm('\quad \quad \; F' + ppunkt(F))	
    print("\nDer gesuchte Abstand ist der zwischen P und F")
    dm('\quad \quad \; d =' + latex(pp.abstand(F)))	
    dd = abs(pp.abstand(gg))			
    if isinstance(dd, (int, Integer, float, Float)):
        dm('Abstand: \;\;' + 'd(P, g) =' + latex(dd))
    else:		
        dm('Abstand: \;\;' + 'd(P, g) =' + latex(dd) + \
             '\\quad [ \;' + latex(float(dd)) + '\ ]' )
    print("\n")
	
APG3 = AbstandPunktGeradeVersion3
	
	


# ----------------
# LageGeradeEbene
# ----------------

def LageGeradeEbene(*args, **kwargs):

    if kwargs.get('h'):
        print("\nLageGeradeEbene - Verfahren\n")     
        print("Lage von Gerade und Ebene zueinander, Version 0 mit")
        print("Schnittpunktbestimmung\n")		
        print("Aufruf     LGE( gerade, ebene )\n")		                     
        print("                gerade   Gerade")
        print("                ebene    Ebene\n")
        return		
		
    if len(args) != 2:
        print("agla: Gerade und Ebene angeben")
        return
				
    anf = '     '				
    gg, ee = args
    if not (isinstance(gg, Gerade) and isinstance(ee, Ebene)):
        if isinstance(ee, Gerade) and isinstance(gg, Ebene):
            gg, ee = ee, gg
        else:
            print("agla: Gerade und Ebene angeben")
            return
		
    if gg.dim != 3:
        print("agla: Gerade im Raum R^3 angeben")
        return
		
    if mit_param(gg) or mit_param(ee):		
        print("agla: nicht implementiert, Parameter")
        return

    print("\nLage von Gerade und Ebene zueinander\n")
    print("Gegeben:\n")
    lat1 = 'g : \;' + pgerade(gg)
    lat2 = 'E : \;'
    if ee._typ == 1:
        lat2 += pnf(ee, X)
    elif ee._typ == 2:
        lat2 += pprg(ee) 
    else:
        lat2 += pkoord(ee, X)	
    dm('\quad \quad ' + lat1 + ', \quad \quad ' + lat2)
    txt = ''	
    if ee._typ == 2:
        print("\nErmittlung eines Normalenvektors der Ebene" +  \
                                    "   (s.a. ENV - EbeneNormalenVektor)")	
    print("\nRichtungsvektor der Geraden und Normalenvektor der Ebene sind")
    ri, nn = gg.richt, ee.norm	
    dm('\quad \quad ' + latex(ri) + ', \; ' + latex(nn))
    print("\nUntersuchung auf Parallelität:\n")
    print(anf + "Die Vektoren sollen orthogonal sein")
    dm('\quad \quad ' + latex(ri) + '\\circ' + latex(nn) + '= 0')
    dm('\quad \quad \;' + latex(ri.sp(nn)) + '= 0')
    if ri.sp(nn) == 0:
        print(anf + "Die Bedingung ist erfüllt, die Gerade ist parallel zur Ebene")
        print("\nUntersuchung auf Enthaltensein:\n")
        if ee._typ != 3:
            print(anf + "Eine Koordinatengleichung von E ist")		
            ee = Ebene(ee.norm.x, ee.norm.y, ee.norm.z, -ee.stuetz.sp(ee.norm))
            dm('\quad \quad \;' + pkoord(ee, X))
        if gg.stuetz.abstand(ee) == 0:
            print(anf + "Der Stützvektor von g erfüllt die Koordinatengleichung von E")
            print(anf + "Die Gerade liegt in der Ebene\n") 			
        else:
            print(anf + "Der Stützvektor von g erfüllt die Koordinatengleichung von E nicht")
            print(anf + "Die Gerade liegt nicht in der Ebene\n") 
        return			
    print(anf + "Die Bedingung ist nicht erfüllt, die Gerade schneidet die Ebene")
    print("\nErmittlung des Schnittpunktes:\n")
    if ee._typ != 3:
        print(anf + "Eine Koordinatengleichung von E ist")		
        ee = Ebene(ee.norm.x, ee.norm.y, ee.norm.z, -ee.stuetz.sp(ee.norm))
        dm('\quad \quad \;' + pkoord(ee, X))
    x, y, z = Symbol('x'), Symbol('y'), Symbol('z')	
    po = Poly(ee.koord.lhs, [x, y, z])
    pox, poy, poz = po.subs({y:0, z:0}), po.subs({x:0, z:0}), \
        po.subs({x:0, y:0})
    dix, diy, diz = dict(pox.all_terms()), dict(poy.all_terms()), \
        dict(poz.all_terms())
    aa = []
    try:
        aa += [dix[(1,)]]
    except KeyError:
        aa += [0]	
    try:
        aa += [diy[(1,)]]
    except KeyError:
        aa += [0]	
    try:
        aa += [diz[(1,)]]
    except KeyError:
        aa += [0]	
    try:
        aa += [dix[(0,)]]
    except KeyError:
        aa += [0]		
    av = Vektor(aa[:3])	
    print(anf + "Die Geradengleichung ist äquivalent zu")
    t = Symbol('t')	
    pp = gg.pkt(t)	
    dm('\quad \quad \; x=' + latex(pp.x) + ', \; y = ' + latex(pp.y) + ', \; z = ' + latex(pp.z))
    print(anf + "Einsetzen in die Koordinatengleichung, nach t auflösen")
    dm('\quad \quad \; ' + psp(av, pp) + ('+' if aa[3] >= 0 else '-') \
        + latex(abs(aa[3])) + '=0')
    dm('\quad \quad \; ' + pkoord(ee, pp))
    lgs = LGS([av.sp(pp) + aa[3]])
    L = lgs.loes
    S = gg.pkt(L[t])	
    dm('\quad \quad \; t =' + latex(L[t]))
    print(anf + "führt nach Einsetzen in die Geradengleichung auf den Schnittpunkt")	
    dm('\quad \quad \; S' + ppunkt(S))	
    print('\n')
    return		
	
LGE = LageGeradeEbene
	
	
	
# ------------------------	
# LageGeradeEbeneVersion1
# ------------------------

def LageGeradeEbeneVersion1(*args, **kwargs):

    if kwargs.get('h'):
        print("\nLageGeradeEbene - Verfahren\n")     
        print("Lage von Gerade und Ebene zueinander, Version 1 über")
        print("Linearkombinationen\n")		
        print("Aufruf     LGE1( gerade, ebene )\n")		                     
        print("                 gerade   Gerade")
        print("                 ebene    Ebene\n")
        return		
		
    if len(args) != 2:
        print("agla: Gerade und Ebene angeben")
        return
				
    anf = '     '				
    gg, ee = args
    if not (isinstance(gg, Gerade) and isinstance(ee, Ebene)):
        if isinstance(ee, Gerade) and isinstance(gg, Ebene):
            gg, ee = ee, gg
        else:
            print("agla: Gerade und Ebene angeben")
            return
		
    if gg.dim != 3:
        print("agla: Gerade im Raum R^3 angeben")
        return
		
    if ee._typ != 2:		
        print("agla: das verfahren ist nur für Ebenen mit Parametergleichung implementiert")
        return

    print("\nLage von Gerade und Ebene zueinander\n")
    print("Gegeben:\n")
    lat1 = 'g : \;' + pgerade(gg)
    lat2 = 'E : \;' + pprg(ee) 
    dm('\quad \quad ' + lat1 + ', \quad \quad ' + lat2)
    print("\n" + anf + "mit den Stütz- und Richtungsvektoren\n")	
    dm('\quad \quad \;' + '\\vec{p} =' + latex(gg.stuetz) + ', \;\; \\vec{q} =' + latex(ee.stuetz))
    dm('\quad \quad \;' + '\\vec{m} =' + latex(gg.richt) + ', \;\;' + \
          '\\vec{n} =' + latex(ee.richt[0]) + ', \;\;\\vec{o} =' + latex(ee.richt[1]))
    print("\nUntersuchung, ob m eine Linearkombination von n und o ist:\n")	
    print(anf + "Es soll gelten")	
    r, s = Symbol('r'), Symbol('s')	
    dm('\quad \quad \;' + '\\vec{m} =' + 'r' + latex(ee.richt[0]) + ' + s' + latex(ee.richt[1]))
    print(anf + "Das resultierende LGS\n")
    lgs = LGS(-gg.richt + r*ee.richt[0] + s*ee.richt[1])
    L = lgs.loes	
    lgs.ausg_ohne_nr	
    if not L:
        print('\n' + anf + "hat keine Lösung; die Vektoren m, n, o sind linear unabhängig\n")
        print(anf + "Die Gerade schneidet die Ebene\n")
        if gg.richt.sp(ee.richt[0]) == 0:		
            print(anf + "Da das Skalarprodukt von m und n gleich Null ist, liegt die ")
            print(anf + "Gerade orthogonal zur Ebene\n")
        return	
    print('\n' + anf + "hat die Lösung")
    dm('\quad \quad \;' + 'r =' + latex(L[r]) + ', \;\;s =' + latex(L[s]))
    print(anf + "die Vektoren m, n und o sind linear abhängig, es ist")    		    
    dm('\quad \quad \;' + latex(gg.richt) + '=' + latex(L[r]) + '\\cdot' + \
        latex(ee.richt[0]) + '+' + latex(L[s]) + '\\cdot' + latex(ee.richt[1]))	
    if gg.stuetz == ee.stuetz:
        print("\n" + anf + "Die Stützvektoren von Gerade und Ebene fallen zusammen\n")	
        print(anf + "Die Gerade liegt in der Ebene\n")
        return
    print("\nUntersuchung, ob q-p eine Linearkombination von n und o ist:\n")	
    print(anf + "Es soll gelten")	
    dm('\quad \quad \;' + latex(ee.stuetz - gg.stuetz) + '=' + 'r' + \
      latex(ee.richt[0]) + '+ s' + latex(ee.richt[1]))
    print(anf + "Das resultierende LGS\n")
    lgs = LGS(-(ee.stuetz - gg.stuetz - r*ee.richt[0] - s*ee.richt[1]))
    L = lgs.loes	
    lgs.ausg_ohne_nr	
    if not L:
        print('\n' + anf + "hat keine Lösung; die Vektoren q-p, n, o sind linear unabhängig\n")
        print(anf + "Die Gerade ist parallel zur Ebene\n")
        return	
    print('\n' + anf + "hat die Lösung")	
    dm('\quad \quad \;' + 'r =' + latex(L[r]) + ', \;\;s =' + latex(L[s]))
    print(anf + "die Vektoren q-p, n, o sind linear abhängig, es ist")
    dm('\quad \quad \;' + latex(ee.stuetz - gg.stuetz) + '=' + latex(L[r]) + \
        '\\cdot' + latex(ee.richt[0]) + '+' + latex(L[s]) + '\\cdot' + latex(ee.richt[1]))
    print('\n' + anf + "die Gerade liegt in der Ebene\n")
	
LGE1 = LageGeradeEbeneVersion1



# -----------------
# LageGeradeGerade
# -----------------

def LageGeradeGerade(*args, **kwargs):

    if kwargs.get('h'):
        print("\nLageGeradeGerade - Verfahren\n")
        print("Lage zweier Geraden zueinander, Version 0 mit Ermittlung")
        print("des Schnittpunktes\n")
        print("Aufruf     LGG( gerade, gerade )\n")		                     
        print("                gerade   Gerade\n")
        return		
		
    if len(args) != 2:
        print("agla: zwei Geraden angeben")
        return
				
    anf = '     '				
    g1, g2 = args
    if not (isinstance(g1, Gerade) and isinstance(g2, Gerade)):
        print("agla: zwei Geraden angeben")
        return
		
    if g1.dim != 3 or g2.dim != 3:
        print("agla: zwei Geraden im Raum R^3 angeben")
        return
		
    if mit_param(g1) or mit_param(g2):		
        print("agla: nicht implementiert, Parameter")
        return

    print("\nLage zweier Geraden zueinander\n")
    print("Gegeben:\n")
    s, t = Symbol('s'), Symbol('t')	
    g1 = Gerade(g1.stuetz, g1.richt, s)	
    g2 = Gerade(g2.stuetz, g2.richt, t)	
    lat1 = 'g1 : \;' + pgerade(g1)
    lat2 = 'g2 : \;' + pgerade(g2)
    dm('\quad \quad ' + lat1 + ', \quad \quad ' + lat2)

    print("\nUntersuchung auf Parallelität:\n")
    print(anf + "Es soll gelten")
    r = Symbol('r')	
    dm('\quad \quad \;' + latex(g2.richt) + '=' + 'r \\cdot' + latex(g1.richt))
    lgs = LGS(-(g2.richt - r*g1.richt))
    L = lgs.loes
    print(anf + "Das zugehörige LGS ist\n")
    lgs.ausg_ohne_nr		
    if parallel(g1, g2):
        print('\n' + anf + "es hat die Lösung r = " + str(L[r]))	
        print(anf + "die Geraden sind parallel oder identisch")	
        print("\nUntersuchung auf Identität:\n")      		
        print(anf + "Einsetzen des Stützvektors von g1 in die Gleichung von g2")	
        dm('\quad \quad \;' + latex(g1.stuetz) + '=' + latex(g2.stuetz) + \
            '+' + 't' + latex(g2.richt))
        print('\n' + anf + "Das resultierende LGS\n")
        lgs = LGS(-g1.stuetz + g2.stuetz + t*g2.richt)
        L = lgs.loes
        lgs.ausg_ohne_nr
        if identisch(g1, g2):		
            print('\n' + anf + "hat die Lösung")
            dm('\quad \quad \; t =' + latex(L[t]))
            print(anf + "folglich liegt der Punkt auf g2, die Geraden haben einen gemeinsamen Punkt")
            print('\n' + anf + "Die Geraden sind identisch")
            print('\n')		
            return
        else:			
            print('\n' + anf + "hat keine Lösung, folglich liegt der Punkt nicht auf g2")
            print('\n' + anf + "Die Geraden sind parallel")
            print('\n')		
            return		
    print('\n' + anf + "Es hat keine Lösung, die Richtungsvektoren sind nicht kollinear")	
    print(anf + "Die Geraden sind nicht parallel")	
    print("\nUntersuchung auf einen Schnittpunkt:\n")	
    print(anf + "Gleichsetzen der rechten Seiten der Geradengleichungen ergibt das LGS\n")
    s, t = Symbol('s'), Symbol('t')	
    lgs = LGS(g1.pkt(s) - g2.pkt(t))
    L = lgs.loes
    lgs.ausg_ohne_nr
    if not L:
        print('\n' + anf + "Es hat keine Lösung, die Geraden schneiden sich nicht\n")	
        print(anf + "Die Geraden sind windschief\n")	
        return		
    print('\n' + anf + "Es hat die Lösung")	
    dm('\quad \quad \; s =' + latex(L[s]) + ', \;\; t =' + latex(L[t]))
    print(anf + "Einsetzen von s in die Gleichung von g1 ergibt den Schnittpunkt")
    S = g1.pkt(L[s])
    dm('\quad \quad \; S' + ppunkt(S))
    print("\n")	
    	
LGG = LageGeradeGerade	



# -------------------------
# LageGeradeGeradeVersion1
# -------------------------

def LageGeradeGeradeVersion1(*args, **kwargs):

    if kwargs.get('h'):
        print("\nLageGeradeGerade - Verfahren\n")
        print("Lage zweier Geraden zueinander, Version 1 über lineare Abhängigkeit,")
        print("ohne Schnittpunkte\n")
        print("Aufruf     LGG1( gerade, gerade )\n")		                     
        print("                 gerade   Gerade\n")
        return		
		
    if len(args) != 2:
        print("agla: zwei Geraden angeben")
        return
				
    anf = '     '				
    g1, g2 = args
    if not (isinstance(g1, Gerade) and isinstance(g2, Gerade)):
        print("agla: zwei Geraden angeben")
        return
		
    if g1.dim != 3 or g2.dim != 3:
        print("agla: zwei Geraden im Raum R^3 angeben")
        return
		
    if mit_param(g1) or mit_param(g2):		
        print("agla: nicht implementiert, Parameter")
        return

    print("\nLage zweier Geraden zueinander\n")
    print("Gegeben:\n")
    s, t = Symbol('s'), Symbol('t')	
    g1 = Gerade(g1.stuetz, g1.richt, s)	
    g2 = Gerade(g2.stuetz, g2.richt, t)	
    lat1 = 'g1 : \;' + pgerade(g1)
    lat2 = 'g2 : \;' + pgerade(g2)
    dm('\quad \quad ' + lat1 + ', \quad \quad ' + lat2)
    print('\n' + anf + "mit den Stütz- und Richtungsvektoren")
    dm('\quad \quad \; \\vec{p} =' + latex(g1.stuetz) + ', \;\; \\vec{q} =' + latex(g2.stuetz))
    dm('\quad \quad \; \\vec{m} =' + latex(g1.richt) + ', \;\; \\vec{n} =' + latex(g2.richt))	
    print("\nUntersuchung auf Parallelität:\n")
    print(anf + "Es soll gelten")
    r = Symbol('r')	
    dm('\quad \quad \;' + latex(g2.richt) + '=' + 'r \\cdot' + latex(g1.richt))
    lgs = LGS(-(g2.richt - r*g1.richt))
    L = lgs.loes
    print(anf + "Das zugehörige LGS ist\n")
    lgs.ausg_ohne_nr		
    if parallel(g1, g2):
        print('\n' + anf + "Es hat die Lösung r = " + str(L[r]))	
        print(anf + "Die Geraden sind parallel oder identisch")
        print("\nUntersuchung von q-p und u auf Kollinearität:\n")
        print(anf + "Es soll gelten")
        r = Symbol('r')	
        dm('\quad \quad \;' + latex(g2.stuetz - g1.stuetz) + '=' + 'r \\cdot' + latex(g1.richt))
        lgs = LGS(-(g2.stuetz -g1.stuetz - r*g1.richt))
        L = lgs.loes
        print(anf + "Das zugehörige LGS ist\n")
        lgs.ausg_ohne_nr	
        if identisch(g1, g2):		
            print('\n' + anf + "Es hat die Lösung")
            dm('\quad \quad \; r =' + latex(L[r]))
            print(anf + "folglich sind die Vektoren kollinear")
            print('\n' + anf + "Die Geraden sind identisch")
            print('\n')		
            return
        else:			
            print('\n' + anf + "Es hat keine Lösung, die Vektoren sind nicht kollinear")
            print('\n' + anf + "Die Geraden sind parallel")
            print('\n')		
            return		
    print('\n' + anf + "Es hat keine Lösung, die Richtungsvektoren sind nicht kollinear")	
    print(anf + "Die Geraden schneiden sich oder sind windschief")	
    print("\nUntersuchung der Vektoren q-p, m und n auf lineare Abhängigkeit:\n")
    if g1.stuetz == g2.stuetz:
        print('\n' + anf + "q-p ist der Nullvektor - die Vektoren sind linear abhängig")
        print('\n' + anf + "Die Geraden schneiden sich")
        print('\n')	
        return	
    print(anf + "Es soll gelten")
    r, s, t = Symbol('r'), Symbol('s'), Symbol('t')	
    dm('\quad \quad \;' + 'r \\cdot' + latex(g2.stuetz - g1.stuetz) + '+ s \\cdot' + \
      latex(g1.richt) + '+ t \\cdot' + latex(g2.richt) + '=' + latex(Vektor(0, 0, 0)))
    lgs = LGS(r*(g2.stuetz - g1.stuetz) + s*g1.richt + t*g2.richt)
    L = lgs.loes
    print('\n' + anf + "Das zugehörige LGS ist\n")
    lgs.ausg_ohne_nr		
    print('\n' + anf + "Es hat die Lösung")	
    dm('\quad \quad \;' + latex(L))
    if L[r] == 0 and L[s] == 0 and L[t] == 0:	
        print('\n' + anf + "Die Vektoren sind linear unabhängig")
        print('\n' + anf + "Die Geraden sind windschief")
    else:
        print('\n' + anf + "die Vektoren sind linear abhängig")
        print('\n' + "Die Geraden schneiden sich")
    print('\n')	
    	
LGG1 = LageGeradeGeradeVersion1	




# -----------------
# LagePunktDreieck
# -----------------

def LagePunktDreieck(*args, **kwargs):

    if kwargs.get('h'):
        print("\nLagePunktDreieck - Verfahren\n")
        print("Lage eines Punktes bezüglich eines Dreiecks, Version 0 mitels")
        print("Linearkombination\n")
        print("Aufruf     LPD( punkt, dreieck )\n")		                     
        print("                punkt     Punkt")
        print("                dreieck   Dreieck\n")
        return		
		
    if len(args) != 2:
        print("agla: Punkt und Dreieck angeben")
        return
				
    anf = '     '				
    pp, dd = args
    if not (isinstance(pp, Vektor) and isinstance(dd, Dreieck)):
        if isinstance(pp, Dreieck) and isinstance(dd, Vektor):
            pp, dd = dd, pp
        else:
            print("agla: Punkt und Dreieck angeben")
            return
			
    if pp.dim != 3 or dd.dim != 3:
        print("agla: Punkt und Dreieck im Raum R^3 angeben")
        return
		
    if mit_param(pp) or mit_param(dd):		
        print("agla: nicht implementiert, Parameter")
        return

    print("\nLage eines Punktes bezüglich eines Dreiecks\n")
    print("Gegeben:\n")
    print("Der Punkt P und das Dreieck mit den Eckpunkten A, B, C")	
    A, B, C = dd.punkte	
    dm('\quad \quad \; P' + ppunkt(pp) + '\qquad A' + ppunkt(A) + \
       ', \;\; B' + ppunkt(B) + ', \;\; C' + ppunkt(C))
    print("Untersuchung, ob die Koordinaten des Punktes im Bereich des Dreiecks")    	
    print("liegen:")    	
    print('\n' + anf + "Bereich für jede Koordinate  [min. Eckwert, max. Eckwert]")
    x_ber = [min(min(A.x, B.x), C.x), max(max(A.x, B.x), C.x)]	
    y_ber = [min(min(A.y, B.y), C.y), max(max(A.y, B.y), C.y)]	
    z_ber = [min(min(A.z, B.z), C.z), max(max(A.z, B.z), C.z)]
    lage = True
    if x_ber[0] <= pp.x <= x_ber[1]:	
        print(anf + "x-Wert   " + str(pp.x) +  ' liegt in ' + str(x_ber))
    else:
        print(anf + "x-Wert   " + str(pp.x) +  ' liegt nicht in ' + str(x_ber))
        lage = False		
    if y_ber[0] <= pp.y <= y_ber[1]:	
        print(anf + "y-Wert   " + str(pp.y) +  ' liegt in ' + str(y_ber))
    else:
        print(anf + "y-Wert   " + str(pp.y) +  ' liegt nicht in ' + str(y_ber))
        lage = False		
    if z_ber[0] <= pp.z <= z_ber[1]:	
        print(anf + "z-Wert   " + str(pp.z) +  ' liegt in ' + str(z_ber))
    else:
        print(anf + "z-Wert   " + str(pp.z) +  ' liegt nicht in ' + str(z_ber))
        lage = False		
    if not lage:
        print('\n' + anf + "Nicht alle Koordinaten liegen im entsprechenden Bereich\n")	
        print("Der Punkt liegt nicht im Dreieck\n")	
        return	
    print('\n' + anf + "Alle Koordinaten liegen im entsprechenden Bereich, es muss weiter")	
    print(anf + "untersucht werden")
    print("\nErmittlung einer Linearkombination:\n")	
    print(anf + "Der Vektor v(A,P) soll als Linearkombination der Vektoren v(A,B) und")
    print(anf + "v(A,C) dargestellt  werden; zu lösen ist die Vektorgleichung")
    r, s = Symbol('r'), Symbol('s')
    dm('\quad \quad \; \\vec{AP} = r \, \cdot\\vec{AB} + s \, \cdot \\vec{AC}')
    print(anf + "Einsetzen der gegebenen Werte")	
    dm('\quad \quad \; ' + latex(Vektor(A, pp)) +'= r' + \
      latex(Vektor(A, B)) + '+ s' + latex(Vektor(A, C)))
    print(anf + "führt zu dem LGS\n")	
    lgs = LGS(-(Vektor(A, pp) - r*Vektor(A, B) - s*Vektor(A, C)))	
    L = lgs.loes
    lgs.ausg_ohne_nr		
    if L:
        print('\n' + anf + "mit der Lösung")	
        dm('\quad \quad \; ' + latex(L))
    else:
        print(anf + "es existiert keine Lösung")	
    print("\nInterpretation der Ergebnisse:\n")	
    if L:
        r0, s0 = L[r], L[s]
        if	 0 <= r0 <= 1 and 0 <= s0 <= 1:
            if r0 + s0 <= 1:
                print("Der Punkt liegt innerhalb des durch die Vektoren aufgespannten")
                print("Parallelogramms, da r und s beide in [0,1] liegen\n")			
                print("Der Punkt liegt innerhalb des Dreiecks, da r+s <= 1 ist\n")
            else:	
                print("Der Punkt liegt außerhalb des Dreiecks, da r+s > 1 ist\n")
        else:				
            print("Der Punkt liegt außerhalb des durch die Vektoren aufgespannten")
            print("Parallelogramms, da r und s nicht beide in [0,1] liegen\n")			
    else:	
        print("Der Punkt liegt nicht in der Ebene des Dreiecks\n")	
        print("Der Punkt liegt nicht im Dreieck\n")	
	
LPD = LagePunktDreieck
	
	
	
# -------------------------	
# LagePunktDreieckVersion1
# -------------------------

def LagePunktDreieckVersion1(*args, **kwargs):

    if kwargs.get('h'):
        print("\nLagePunktDreieck - Verfahren\n")
        print("Lage eines Punktes bezüglich eines Dreiecks, Version 1 über")
        print("die Lage von Geraden\n")
        print("Aufruf     LPD1( punkt, dreieck )\n")		                     
        print("                 punkt     Punkt")
        print("                 dreieck   Dreieck\n")
        return		
		
    if len(args) != 2:
        print("agla: Punkt und Dreieck angeben")
        return
				
    anf = '     '				
    pp, dd = args
    if not (isinstance(pp, Vektor) and isinstance(dd, Dreieck)):
        if isinstance(pp, Dreieck) and isinstance(dd, Vektor):
            pp, dd = dd, pp
        else:
            print("agla: Punkt und Dreieck angeben")
            return
		
    if pp.dim != 3 or dd.dim != 3:
        print("agla: Punkt und Dreieck im Raum R^3 angeben")
        return
		
    if mit_param(pp) or mit_param(dd):		
        print("agla: nicht implementiert, Parameter")
        return
		
    print("\nLage eines Punktes bezüglich eines Dreiecks\n")
    print("Gegeben:\n")
    print("Der Punkt P und das Dreieck mit den Eckpunkten A, B, C")	
    A, B, C = dd.punkte	
    dm('\quad \quad \; P' + ppunkt(pp) + '\qquad A' + ppunkt(A) + \
       ', \;\; B' + ppunkt(B) + ', \;\; C' + ppunkt(C))
    if A==pp or B==pp or C==pp:
        print("Der Punkt fällt mit einem Eckpunkt des Dreiecks zusammen\n")	
        print("Der Punkt liegt im Dreieck\n")	
        return     	
    print("Untersuchung, ob die Koordinaten des Punktes im Bereich des Dreiecks")    	
    print("liegen:")    	
    print('\n' + anf + "Bereich für jede Koordinate  [min. Eckwert, max. Eckwert]")
    x_ber = [min(min(A.x, B.x), C.x), max(max(A.x, B.x), C.x)]	
    y_ber = [min(min(A.y, B.y), C.y), max(max(A.y, B.y), C.y)]	
    z_ber = [min(min(A.z, B.z), C.z), max(max(A.z, B.z), C.z)]
    lage = True
    if x_ber[0] <= pp.x <= x_ber[1]:	
        print(anf + "x-Wert   " + str(pp.x) +  ' liegt in ' + str(x_ber))
    else:
        print(anf + "x-Wert   " + str(pp.x) +  ' liegt nicht in ' + str(x_ber))
        lage = False		
    if y_ber[0] <= pp.y <= y_ber[1]:	
        print(anf + "y-Wert   " + str(pp.y) +  ' liegt in ' + str(y_ber))
    else:
        print(anf + "y-Wert   " + str(pp.y) +  ' liegt nicht in ' + str(y_ber))
        lage = False		
    if z_ber[0] <= pp.z <= z_ber[1]:	
        print(anf + "z-Wert   " + str(pp.z) +  ' liegt in ' + str(z_ber))
    else:
        print(anf + "z-Wert   " + str(pp.z) +  ' liegt nicht in ' + str(z_ber))
        lage = False		
    if not lage:
        print('\n' + anf + "Nicht alle Koordinaten liegen im entsprechenden Bereich\n")	
        print("Der Punkt liegt nicht im Dreieck\n")	
        return	
    print('\n'+ anf + "Alle Koordinaten liegen im entsprechenden Bereich, es muss weiter")	
    print(anf + "untersucht werden")
    print("\nUntersuchung der Lage der Geraden durch A und P und der Geraden durch\nB und C:")	
    r, s = Symbol('r'), Symbol('s')	
    gAP = Gerade(A, Vektor(A, pp), r)	
    gBC = Gerade(B, Vektor(B, C), s)	
    dm('\quad \quad \; g_{AP}: \quad' + pgerade(gAP))
    dm('\quad \quad \; g_{BC}: \quad' + pgerade(gBC))
    print("Gleichsetzen der rechten Seiten führt zu dem LGS\n")	
    lgs = LGS(gAP.pkt(r) - gBC.pkt(s))
    L = lgs.loes
    lgs.ausg_ohne_nr	
    if L:
        print('\n' + anf + "Seine Lösung (sie ergibt den Schnittpunkt der Geraden) ist")
        dm('\quad \quad \;' + latex(L))
        r0, s0 = L[r], L[s]
    else:
        print("Es existiert keine Lösung, die Geraden schneiden sich nicht")	
    print("\nInterpretation der Ergebnisse:\n")
    if L:	
        if r0 >= 1 and 0 <= s0 <= 1:
            print("Der Punkt liegt im Dreieck, da r >= 1 und 0 <= s <= 1 ist\n")
        else:			
            print("Der Punkt liegt nicht im Dreieck, da nicht gleichzeitig r >= 1 ")
            print("und 0 <= s <= 1 ist\n")		
    else:
        print("Der Punkt liegt nicht im Dreieck\n")
	
LPD1 = LagePunktDreieckVersion1




# ---------------
# LagePunktEbene
# ---------------

def LagePunktEbene(*args, **kwargs):

    if kwargs.get('h'):
        print("\nLagePunktEbene - Verfahren\n")
        print("Lage eines Punktes bezüglich einer Ebene\n")
        print("Aufruf     LPE( punkt, ebene )\n")		                     
        print("                punkt    Punkt")		
        print("                ebene    Ebene\n")
        return		
		
    if len(args) != 2:
        print("agla: Punkt und Ebene angeben")
        return
				
    anf = '     '				
    pp, ee = args
    if not (isinstance(pp, Vektor) and isinstance(ee, Ebene)):
        if isinstance(ee, Ebene) and isinstance(pp, Vektor):
            pp, ee = ee, pp
        else:
            print("agla: Punkt und Ebene angeben")
            return
		
    if pp.dim != 3:
        print("agla: Punkt des Raumes R^3 angeben")
        return
		
    if mit_param(pp) or mit_param(ee):		
        print("agla: nicht implementiert, Parameter")
        return

    print("\nLage eines Punktes bezüglich einer Ebene\n")
    print("Gegeben:")
    lat1 = 'P' + ppunkt(pp)	
    lat2 = 'E : \;'
    if ee._typ == 1:
        lat2 += pnf(ee, X)
    elif ee._typ == 2:
        lat2 += pprg(ee) 
    else:
        lat2 += pkoord(ee, X)	
    dm('\quad \quad ' + lat1 + ', \quad \quad ' + lat2)
    if ee._typ == 2:
        print("Der Ortsvektor des Punktes soll die Ebenengleichung erfüllen")
        r, s = Symbol('r'), Symbol('s')
        dm('\quad \quad  \;' + latex(pp) + '=' + latex(ee.stuetz) + '+ r' + '\\cdot' + \
            latex(ee.richt[0]) + '+ s' + '\\cdot' + latex(ee.richt[1]))
        print(anf + "Das zugehörige LGS\n")
        lgs = LGS(-(pp - ee.pkt(r, s)))
        L = lgs.loes
        lgs.ausg_ohne_nr	
        if L:
            print('\n' + anf + "hat die Lösung")
            dm('\quad \quad  \;' + latex(L))
            print("Es ist")
            r, s = L[r], L[s]		
            dm('\quad \quad  \; P =' + latex(ee.stuetz) + '+' + latex(r) + '\\cdot' + \
              latex(ee.richt[0]) + '+' + latex(s) + '\\cdot' + latex(ee.richt[1]))
            print("\nDer Punkt liegt in der Ebene\n")    	
        else:	
            print("\n" + anf + "hat keine Lösung\n")
            print("Der Punkt liegt nicht in der Ebene\n")    	
    elif ee._typ == 3:
        nn = Vektor(ee.args[:3])	
        print("Die Koordinaten des Punktes sollen die Ebenengleichung erfüllen")
        dm('\quad \quad  \;' + psp(pp, nn) + ('+' if ee.args[3] >= 0 else '-') \
           + latex(abs(ee.args[3])) + '= 0')		   
        dm('\quad \quad  \;' + latex(pp.sp(nn) + ee.args[3]) + '= 0')
        if pp.sp(nn) +ee.args[3] == 0:
            print(anf + "Die Gleichung ist erfüllt\n")		
            print("Der Punkt liegt in der Ebene\n") 
        else:
            print(anf + "Die Gleichung ist nicht erfüllt\n")		
            print("Der Punkt liegt nicht in der Ebene\n")    	
    elif ee._typ == 1:
        print("\nDer Ortsvektor des Punktes soll die Ebenengleichung erfüllen")
        dm('\quad \quad  \;' + pnf(ee, pp))
        dm('\quad \quad  \; ' + latex(pp - ee.stuetz) + '\\circ' \
           + latex(ee.norm) + '= 0')
        dm('\quad \quad  \; ' + psp(pp - ee.stuetz, ee.norm) + '=  0')
        dm('\quad \quad  \; ' + latex((pp - ee.stuetz).sp(ee.norm)) + '=  0')
        if (pp - ee.stuetz).sp(ee.norm) == 0:	
            print(anf + "Die Gleichung ist erfüllt\n")		
            print("Der Punkt liegt in der Ebene\n") 
        else:
            print(anf + "Die Gleichung ist nicht erfüllt\n")		
            print("Der Punkt liegt nicht in der Ebene\n")    	
	
LPE = LagePunktEbene



# ----------------
# LagePunktGerade
# ----------------

def LagePunktGerade(*args, **kwargs):

    if kwargs.get('h'):
        print("\nLagePunktGerade - Verfahren\n")
        print("Lage eines Punktes bezüglich einer Geraden\n")
        print("Aufruf     LPG( punkt, gerade )\n")		                     
        print("                punkt    Punkt")		
        print("                gerade   Gerade\n")
        return		
		
    if len(args) != 2:
        print("agla: Punkt und Gerade angeben")
        return
				
    anf = '     '				
    pp, gg = args
    if not (isinstance(pp, Vektor) and isinstance(gg, Gerade)):
        if isinstance(gg, Vektor) and isinstance(pp, Gerade):
            pp, gg = gg, pp
        else:
            print("agla: Punkt und Gerade angeben")
            return
		
    if pp.dim != 3:
        print("agla: Punkt des Raumes R^3 angeben")
        return
		
    if mit_param(pp) or mit_param(gg):		
        print("agla: nicht implementiert, Parameter")
        return
		
    t = Symbol('t')		
    gg = Gerade(gg.stuetz, gg.richt, t)
    print("\nLage  eines Punktes bezüglich einer Geraden\n")
    print("Gegeben:")
    lat1 = 'P(' + ppunkt(pp)
    lat2 = 'g : \;' + pgerade(gg)
    dm('\quad \quad ' + lat1 + ', \quad \quad ' + lat2)
    print("Der Ortsvektor des Punktes soll die Geradengleichung erfüllen")	
    dm('\quad \quad \; ' + latex(pp) + '=' + latex(gg.stuetz) + \
        '+ t \\cdot' + latex(gg.richt))
    print(anf + "Das zugehörige LGS\n")
    lgs = LGS(-(pp - gg.stuetz - t*gg.richt))	
    L = lgs.loes
    lgs.ausg_ohne_nr
    if L:
        print('\n' + anf + "hat die Lösung")
        dm('\quad \quad \; ' + latex(L))
        t = L[t]
        print(anf + "Es ist")
        dm('\quad \quad \; P =' + latex(gg.stuetz) + \
          ('+' if t>=0 else '-') + latex(abs(t)) + \
          '\\cdot' + latex(gg.richt))
        print("\nDer Punkt liegt auf der Geraden\n")
    else:
        print('\n' + anf + "hat keine Lösung\n")
        print("Der Punkt liegt nicht auf der Geraden\n")
	
LPG = LagePunktGerade



# -----------------
# LagePunktViereck
# -----------------

def LagePunktViereck(*args, **kwargs):

    if kwargs.get('h'):
        print("\nLagePunktViereck - Verfahren\n")
        print("Lage eines Punktes bezüglich eines Vierecks\n")
        print("Aufruf     LPV( punkt, viereck )\n")		                     
        print("                punkt     Punkt")
        print("                viereck   Viereck\n")
        return		
		
    if len(args) != 2:
        print("agla: Punkt und Viereck angeben")
        return
				
    anf = '     '				
    pp, ve = args
    if not (isinstance(pp, Vektor) and isinstance(ve, Viereck)):
        if isinstance(ve, Vektor) and isinstance(pp, Viereck):
            pp, ve = ve, pp
        else:
            print("agla: Punkt und Viereck angeben")
            return
		
    if pp.dim != 3 or ve.dim != 3:
        print("agla: Punkt und Viereck im Raum R^3 angeben")
        return
		
    if mit_param(pp) or mit_param(ve):		
        print("agla: nicht implementiert, Parameter")
        return

    print("\nLage eines Punktes bezüglich eines Vierecks\n")
    print("Gegeben:\n")
    print("Der Punkt P und das Viereck mit den Eckpunkten A, B, C, D")	
    A, B, C, D = ve.punkte	
    dm('\quad \quad \; P' + ppunkt(pp) + '\qquad A' + ppunkt(A) + \
       ', \;\; B' + ppunkt(B) + ', \;\; C' + ppunkt(C) + ', \;\; D' + ppunkt(D))
    print("Untersuchung, ob die Koordinaten des Punktes im Bereich des Vierecks")    	
    print("liegen:\n")    	
    print(anf + "Bereich für jede Koordinate  [min. Eckwert, max. Eckwert]\n")
    x_ber = [min(min(A.x, B.x), min(C.x, D.x)), max(max(A.x, B.x), max(C.x, D.x))]	
    y_ber = [min(min(A.y, B.y), min(C.y, D.y)), max(max(A.y, B.y), max(C.y, D.y))]	
    z_ber = [min(min(A.z, B.z), min(C.z, D.z)), max(max(A.z, B.z), max(C.z, D.z))]	
    lage = True
    if x_ber[0] <= pp.x <= x_ber[1]:	
        print(anf + "x-Wert   " + str(pp.x) +  ' liegt in ' + str(x_ber))
    else:
        print(anf + "x-Wert   " + str(pp.x) +  ' liegt nicht in ' + str(x_ber))
        lage = False		
    if y_ber[0] <= pp.y <= y_ber[1]:	
        print(anf + "y-Wert   " + str(pp.y) +  ' liegt in ' + str(y_ber))
    else:
        print(anf + "y-Wert   " + str(pp.y) +  ' liegt nicht in ' + str(y_ber))
        lage = False		
    if z_ber[0] <= pp.z <= z_ber[1]:	
        print(anf + "z-Wert   " + str(pp.z) +  ' liegt in ' + str(z_ber))
    else:
        print(anf + "z-Wert   " + str(pp.z) +  ' liegt nicht in ' + str(z_ber))
        lage = False		
    if not lage:
        print("\n" + anf + "Nicht alle Koordinaten liegen im entsprechenden Bereich\n")	
        print("Der Punkt liegt nicht im Viereck\n")	
        return	
    print("\n" + anf + "Alle Koordinaten liegen im entsprechenden Bereich, es muss weiter")	
    print(anf + "untersucht werden")
    print("\nUntersuchung, ob das Viereck ein Parallelogramm ist")	
    if parallel(Vektor(A, B), Vektor(C, D)) and \
                parallel(Vektor(A, D), Vektor(B, C)):   # Parallelogramm
        print("\n" + anf + "Das Viereck ist ein Parallelogramm, da")
        dm('\quad \quad \; \\vec{AB}\; || \;\\vec{CD}, \;\; \\vec{AD} \;||\; \\vec{BC}')	
        print(anf + "Spannvektoren sind")	
        dm('\quad \quad \; \\vec{AB} = ' + latex(B - A) + ', \quad \; \
            \\vec{AD} = ' + latex(D - A))
        print("Ermittlung einer Linearkombination:\n")	
        print(anf + "Der Vektor v(A,P) soll als Linearkombination der Spannvektoren")	
        print(anf + "dargestellt werden; zu lösen ist die Vektorgleichung")		
        r, s = Symbol('r'), Symbol('s')
        dm('\quad \quad \; \\vec{AP} = r \cdot \\vec{AB} + s \cdot \\vec{AD}')
        print(anf + "Einsetzen der gegebenen Werte")	
        dm('\quad \quad \; ' + latex(Vektor(A, pp)) +'= r' + \
            latex(Vektor(A, B)) + '+ s' + latex(Vektor(A, D)))
        print(anf + "führt zu dem LGS\n")	
        lgs = LGS(-(Vektor(A, pp) - r*Vektor(A, B) - s*Vektor(A, D)))	
        L = lgs.loes
        lgs.ausg_ohne_nr		
        if L:
            print("\n" + anf + "mit der Lösung")	
            dm('\quad \quad \; ' + latex(L))
        else:
            print(anf + "es existiert keine Lösung")
        print("\nInterpretation der Ergebnisse\n")	
        if L:
            r0, s0 = L[r], L[s]
            if 0 <= r0 <= 1 and 0 <= s0 <= 1:
                print("Der Punkt liegt innerhalb des Parallelogramms,")
                print("da r und s beide in [0,1] liegen")			
                print("\nDer Punkt liegt im Viereck\n")
            else:				
                print("Der Punkt liegt nicht innerhalb des Parallelogramms")
                print("da r und s nicht beide in [0,1] liegen")			
                print("\nDer Punkt liegt nicht im Viereck\n")			
        else:	
            print("Der Punkt liegt nicht in der Ebene des Vierecks\n")	
            print("\nDer Punkt liegt folglich nicht im Viereck\n")	

    else:
        print("\n" + anf + "Das Viereck ist kein Parallelogramm; es kann in zwei")	
        print(anf + "Dreiecke zerlegt werden")	
        dd = ve.dreiecke
        A1, B1, C1 = dd[0].punkte		
        A2, B2, C2 = dd[1].punkte		
        dm('\quad \quad \; d_1: \;\; Dreieck(' + ppunkt(A1) + ', \;' \
          + ppunkt(B1) + ', \;' + ppunkt(C1) + ')')
        dm('\quad \quad \; d_2: \;\; Dreieck(' + ppunkt(A2) + ', \;' \
          + ppunkt(B2) + ', \;' + ppunkt(C2) + ')')
        print("Die Untersuchung wird für jedes Dreieck einzeln durchgeführt")
        print("(s.a. LPD - LagePunktDreieck)\n")
        if dd[0].schnitt(pp):
            print(anf + "Der Punkt liegt in d1")		
            print("\nDer Punkt liegt im Viereck\n")		
        else:
            print(anf + "Der Punkt liegt nicht in d1")		
            if dd[1].schnitt(pp):
                print(anf + "Der Punkt liegt in d2")		
                print("\nDer Punkt liegt im Viereck\n")		
            else:
                print(anf + "Der Punkt liegt nicht in d2")		
                print("\nDer Punkt liegt nicht im Viereck\n")		
				
LPV = LagePunktViereck
	

	
# ------------------	
# WinkelGeradeEbene
# ------------------

def WinkelGeradeEbene(*args, **kwargs):

    if kwargs.get('h'):
        print("\nWinkelGeradeEbene - Verfahren\n")     
        print("Winkel zwischen Gerade und Ebene\n")		
        print("Aufruf     WGE( gerade, ebene )\n")		                     
        print("                gerade   Gerade")
        print("                ebene    Ebene\n")
        return		
		
    if len(args) != 2:
        print("agla: Gerade und Ebene angeben")
        return
				
    anf = '     '				
    gg, ee = args
    if not (isinstance(gg, Gerade) and isinstance(ee, Ebene)):
        if isinstance(gg, Ebene) and isinstance(ee, Gerade):
            gg, ee = ee, gg
        else:
            print("agla: Gerade und Ebene angeben")
            return
    if gg.dim != 3:
        print("agla: Gerade im Raum R^3 angeben")
        return
		
    if mit_param(gg) or mit_param(ee):		
        print("agla: nicht implementiert, Parameter")
        return

    print("\nWinkel zwischen Gerade und Ebene\n")
    print("Gegeben:\n")
    lat1 = 'g : \;' + pgerade(gg)
    lat2 = 'E : \;'
    if ee._typ == 1:
        lat2 += pnf(ee, X)
    elif ee._typ == 2:
        lat2 += pprg(ee) 
    else:
        lat2 += pkoord(ee, X)	
    dm('\quad \quad ' + lat1 + ', \quad \quad ' + lat2)
    txt = ''	
    if ee._typ == 2:
        print("\nErmittlung eines Normalenvektors der Ebene")
        print("(s.a. ENV - EbeneNormalenVektor)\n")	
    print("Richtungsvektor der Geraden und Normalenvektor der Ebene sind")
    ri, nn = gg.richt, Vektor(ee.args[:3]) if ee._typ == 3 else ee.norm	
    dm('\quad \quad \; \\vec{m} =' + latex(ri) + ', \;\; \\vec{n} = ' + latex(nn))
    print("Formel zur Berechnung des Winkels:")
    dm('\quad \quad \; \sin \\alpha = \\frac{ \\left|\, \\vec{m} \\circ \\vec{n} \
        \,\\right|}{ \\left| \\vec{m} \\right| \\cdot \\left| \\vec{n} \\right|}' + \
       '\qquad 0^\\circ \\le \\alpha \\le 90^\\circ')
    print("Berechnung nach der Formel:")
    dm('\quad \quad \; \sin \\alpha = \\frac{ \\left|\,' + latex(ri) + '\\circ' \
       + latex(nn) + '\,\\right|} { ' + latex(ri.betrag) + ' \\cdot ' + \
       latex(nn.betrag) + '}') 
    swi = abs(ri.sp(nn) / ri.betrag / nn.betrag)	
    dm('\quad \quad \; \quad\:\:\:\: = \\frac{ \\left|' + latex(ri.sp(nn)) + '\\right|}' + \
       '{' + latex(ri.betrag * nn.betrag) + '}' + \
       '= ' + latex(swi))
    dm('\quad \quad \; \\alpha = ' + latex(float(arcsing(swi))) + '\, ^\\circ') 
	
WGE = WinkelGeradeEbene	



# -------------------
# WinkelVektorVektor
# ------------------

def WinkelVektorVektor(*args, **kwargs):

    if kwargs.get('h'):
        print("\nWinkelVektorVektor - Verfahren\n")     
        print("Winkel zwischen zwei Vektoren\n")		
        print("Aufruf     WVV( vektor, vektor )\n")		                     
        print("                vektor   Vektor\n")
        return		
		
    if len(args) != 2:
        print("agla: Zwei Vektoren angeben")
        return
				
    anf = '     '				
    v1, v2 = args
    if not (isinstance(v1, Vektor) and isinstance(v2, Vektor)):
        print("agla: Zwei Vektoren angeben")
        return
		
    if v1.dim != 3 or v2.dim != 3:
        print("agla: Vektoren im Raum R^3 angeben")
        return
		
    if mit_param(v1) or mit_param(v2):		
        print("agla: nicht implementiert, Parameter")
        return

    if v1.betrag == 0 or v2.betrag == 0:		
        print("agla: nicht definiert, Nullvektor")
        return

    print("\nWinkel zwischen zwei Vektoren\n")
    print("Gegeben:")
    lat1 = 'v_1 =' + latex(v1)
    lat2 = 'v_2 =' + latex(v2)
    dm('\quad \quad ' + lat1 + ', \quad \quad ' + lat2)
    print("Formel für zwei Vektoren")
    a_1, a_2, a_3 = Symbol('a_1'), Symbol('a_2'), Symbol('a_3')	
    b_1, b_2, b_3 = Symbol('b_1'), Symbol('b_2'), Symbol('b_3')	
    aa, bb = Vektor(a_1, a_2, a_3), Vektor(b_1, b_2, b_3)	
    dm('\quad \quad \; \\vec{a} =' + latex(aa) + ', \quad \quad  \\vec{b} =' + latex(bb))
    dm('\quad \quad \; \\cos \\alpha =' + '\\frac{' + latex(a_1*b_1+a_2*b_2+a_3*b_3) + '}' \
        + '{' + latex(aa.betrag) + '\\cdot' + latex(bb.betrag) + '}' + \
        '\qquad oder')
    dm('\quad \quad \; \\cos \\alpha =' + '\\frac{ \\vec{a} \\circ \\vec{b}}' + \
        '{ \\left| \\vec{a} \\right| \\cdot \\left| \\vec{b} \\right|}'+ \
        '\qquad\qquad 0^\\circ \\le \\alpha \\le 180^\\circ'	)
    print("Berechnung nach der Formel:")
    dm('\quad \quad \; \cos \\alpha = \\frac{ \,' + latex(v1) + '\\circ' \
       + latex(v2) + '\,} { ' + latex(v1.betrag) + ' \\cdot ' + \
       latex(v2.betrag) + '}') 
    swi = abs(v1.sp(v2) / v1.betrag / v2.betrag)	
    dm('\qquad \qquad \: = \\frac{ ' + latex(v1.sp(v2)) + '}' + \
       '{' + latex(v1.betrag * v2.betrag) + '} = ' + latex(swi))
    dm('\quad \quad \; \\alpha = ' + latex(float(arccosg(swi))) + '\, ^\\circ') 

WVV = WinkelVektorVektor
	
	
	
# -----------------------	
# EbeneKoord2PrgVersion0	
# -----------------------

def EbeneKoord2Prg(*args, **kwargs):

    if kwargs.get('h'):
        print("\nEbeneKoord2Prg - Verfahren\n")     
        print("Bestimmung einer Parameterform einer Ebenengleichung anhand ")
        print("der Koordinatenform, Version 0 über Parameterersetzung\n")		
        print("Aufruf     EK2P( ebene )\n")		                     
        print("                 ebene   Ebene (Koordinatenform)\n")
        return		
		
    if len(args) != 1:
        print("agla: Ebene angeben")
        return
				
    anf = '     '				
    ee = args[0]
    if not isinstance(ee, Ebene):
        print("agla: Ebene angeben")
        return
		
    if ee._typ != 3:
        print("agla: Ebene in Koordinatenform angeben")
        return
		
    if mit_param(ee):		
        print("agla: nicht implementiert, Parameter")
        return

    print("\nBestimmung einer Parameterform der Ebenengleichung anhand der Koordi-")
    print("natenform\n")
    print("Gegeben:")
    lat = 'E: \;' + pkoord(ee, X)
    dm('\quad \quad ' + lat)
    x, y, z, r, s = Symbol('x'), Symbol('y'), Symbol('z'), Symbol('r'), Symbol('s')	
    ersetz = True	
    if ee.koord.lhs.has(z):
        txt = 'z'
        L = solve(ee.koord.lhs, z)      
        gl = {z:L[0], x:r, y:s}	
    elif ee.koord.lhs.has(y):
        txt = 'y'
        L = solve(ee.koord.lhs, y)      
        gl = {y:L[0], x:r, z:s}	
    else:		
        txt = 'x'
        L = solve(ee.koord.lhs, x)      
        gl = {x:L[0], y:r, z:s}	
        ersetz = False	
    print("Die Ebenengleichung wird nach " + txt + " aufgelöst, die anderen beiden")
    print("Variablen werden durch die Parameter r und s ersetzt")	
    dm('\quad \quad  x =' + latex(gl[x]))
    dm('\quad \quad  y =' + latex(gl[y]))
    dm('\quad \quad  z =' + latex(gl[z]))
    vv = Vektor(gl[x], gl[y], gl[z])	
    if ersetz:	
        print("Die Parameterersetzung wird auch in der aufgelösten Gleichung")
        print("durchgeführt")
        dm('\quad \quad  x =' + latex(gl[x].subs({y:gl[y], z:gl[z]})))
        dm('\quad \quad  y =' + latex(gl[y].subs({x:gl[x], z:gl[z]})))
        dm('\quad \quad  z =' + latex(gl[z].subs({x:gl[x], y:gl[y]})))
        vv = Vektor(gl[x].subs({y:gl[y], z:gl[z]}), \
             gl[y].subs({x:gl[x], z:gl[z]}), gl[z].subs({x:gl[x], y:gl[y]}))	
    print("Die drei Gleichungen können in Vektorform geschrieben werden")
    dm('\quad \quad \;' + latex(X) + '=' + latex(vv))
    frei, rir, ris = [], [], []
    for k in vv.komp:
        po = Poly(k, [r, s])
        dis = dict(po.subs({r:0}).all_terms())
        dir = dict(po.subs({s:0}).all_terms())
        frei += [dis[(0,)]]
        try:
            ris += [dis[(1,)]]
        except KeyError:
            ris += [0]
        try:
            rir += [dir[(1,)]]
        except KeyError:
            rir += [0]
    stuetz, richt1, richt2 = Vektor(frei), Vektor(rir), Vektor(ris) 
    print("oder auch in der gewohnten Parameterform")
    dm('\quad \quad \;' + latex(X) + '=' + latex(stuetz) + '+ r \,' + latex(richt1) \
        + '+ s \,' + latex(richt2))
					
    def fakt(v):
        kk = v.komp	
        f = 1		
        if any([(isinstance(x, Rational) and x.q > 1) for x in kk]):
            for k in kk:
                if isinstance(k, Rational) and k.q > f:	
                    f = lcm(k.q, f)				
        return f
		
    f1, f2 = fakt(richt1), fakt(richt2)
    if f1 > 1 or f2 > 1:	
        print("Bei Bedarf können Brüche in den Spannvektoren beseitigt werden")
        richt1 *= f1
        richt2 *= f2
        dm('\quad \quad \;' + latex(X) + '=' + latex(stuetz) + '+ r \,' + latex(richt1) \
            + '+ s \,' + latex(richt2))
    print("")			
			
EK2P = EbeneKoord2Prg	
	


# -----------------------
# EbeneKoord2PrgVersion1	
# -----------------------

def EbeneKoord2PrgVersion1(*args, **kwargs):

    if kwargs.get('h'):
        print("\nEbeneKoord2PrgVersion1 - Verfahren\n")     
        print("Bestimmung einer Parameterform einer Ebenengleichung anhand ")
        print("der Koordinatenform, Version 1 über die Ermittlung von")
        print("drei Ebenenpunkten\n")		
        print("Aufruf     EK2P1( ebene )\n")		                     
        print("                  ebene   Ebene (Koordinatenform)\n")
        return		
		
    if len(args) != 1:
        print("agla: Ebene angeben")
        return
				
    anf = '     '				
    ee = args[0]
    if not isinstance(ee, Ebene):
        print("agla: Ebene angeben")
        return
		
    if ee._typ != 3:
        print("agla: Ebene in Koordinatenform angeben")
        return
		
    if mit_param(ee):		
        print("agla: nicht implementiert, Parameter")
        return

    print("\nBestimmung einer Parameterform der Ebenengleichung anhand der Koordi-")
    print("natenform\n")
    print("Gegeben:")
    lat = 'E: \;' + pkoord(ee, X)
    dm('\quad \quad ' + lat)
    x, y, z, r, s = Symbol('x'), Symbol('y'), Symbol('z'), Symbol('r'), Symbol('s')	
    print("Prinzip: Festlegung von jeweils 2 Koordinaten und Berechnung der drit-")
    print("ten aus der Koordinatengleichung, etwa:")
    if ee.koord.lhs.has(z):
        z0 = solve(ee.koord.lhs.subs({x:0, y:0}))[0]
        z1 = solve(ee.koord.lhs.subs({x:0, y:1}))[0]
        z2 = solve(ee.koord.lhs.subs({x:1, y:0}))[0]		
        p0 = {x:0, y:0, z:z0}	
        p1 = {x:0, y:1, z:z1}	
        p2 = {x:1, y:0, z:z2}
        dm('\quad \quad \; x = 0,\: y = 0, \; ' + \
           latex(ee.koord.lhs.subs({x:0, y:0})) + ' = 0' + '\\rightarrow z =' + latex(z0) )
        dm('\quad \quad \; x = 0,\; y = 1, \; ' + \
           latex(ee.koord.lhs.subs({x:0, y:1})) + ' = 0' + '\\rightarrow z =' + latex(z1) )
        dm('\quad \quad \; x = 1,\; y = 0,\; ' \
           + latex(ee.koord.lhs.subs({x:1, y:0})) + ' = 0' + '\\rightarrow z =' + latex(z2))
    elif ee.koord.lhs.has(y):
        y0 = solve(ee.koord.lhs.subs({x:0, z:0}))[0]	
        y1 = solve(ee.koord.lhs.subs({x:0, z:1}))[0]	
        y2 = solve(ee.koord.lhs.subs({x:1, z:0}))[0]	
        p0 = {x:0, z:0, y:y0}	
        p1 = {x:0, z:1, y:y1}	
        p2 = {x:1, z:0, y:y2}	
        dm('\quad \quad \; x = 0,\: z = 0, \; ' + \
           latex(ee.koord.lhs.subs({x:0, z:0})) + ' = 0' + '\\rightarrow y =' + latex(y0) )
        dm('\quad \quad \; x = 0,\; z = 1, \; ' + \
           latex(ee.koord.lhs.subs({x:0, z:1})) + ' = 0' + '\\rightarrow y =' + latex(y1) )
        dm('\quad \quad \; x = 1,\; z = 0,\; ' \
           + latex(ee.koord.lhs.subs({x:1, z:0})) + ' = 0' + '\\rightarrow y =' + latex(y2))
    else:
        x0 = solve(ee.koord.lhs.subs({z:0, y:0}))[0]
        x1 = solve(ee.koord.lhs.subs({z:0, y:1}))[0]
        x2 = solve(ee.koord.lhs.subs({z:1, y:0}))[0]		
        p0 = {z:0, y:0, x:x0}	
        p1 = {z:0, y:1, x:x1}	
        p2 = {z:1, y:0, x:x2}	
        dm('\quad \quad \; z = 0,\: y = 0, \; ' + \
           latex(ee.koord.lhs.subs({z:0, y:0})) + ' = 0' + '\\rightarrow x =' + latex(x0) )
        dm('\quad \quad \; z = 0,\; y = 1, \; ' + \
           latex(ee.koord.lhs.subs({z:0, y:1})) + ' = 0' + '\\rightarrow x =' + latex(x1) )
        dm('\quad \quad \; z = 1,\; y = 0,\; ' \
           + latex(ee.koord.lhs.subs({z:1, y:0})) + ' = 0' + '\\rightarrow x =' + latex(x2))
		
    P1 = Vektor(p0[x], p0[y], p0[z])	
    P2 = Vektor(p1[x], p1[y], p1[z])	
    P3 = Vektor(p2[x], p2[y], p2[z])	
    print("Das ergibt die Punkte")	
    dm('\quad \quad ' + 'P_1' + ppunkt(P1) + ', \; P_2' + ppunkt(P2) + \
       ', \; P_3' + ppunkt(P3))
    print("Aufstellen der Parametergleichung mit diesen 3 Punkten")
    dm('\quad \quad \; ' + latex(X) + '=' + latex(P1) + ' + r' + \
       latex(Vektor(P1, P2)) + '+ s' + latex(Vektor(P1, P3)))
    stuetz, richt1, richt2 = P1, Vektor(P1, P2), Vektor(P1, P3)
	
    def fakt(v):
        kk = v.komp	
        f = 1		
        if any([(isinstance(x, Rational) and x.q > 1) for x in kk]):
            for k in kk:
                if isinstance(k, Rational) and k.q > f:	
                    f = k.q				
        return f
		
    f1, f2 = fakt(richt1), fakt(richt2)
    if f1 > 1 or f2 > 1:	
        print("Bei Bedarf können Brüche in den Spannvektoren beseitigt werden")
        richt1 *= f1
        richt2 *= f2
        dm('\quad \quad \;' + latex(X) + '=' + latex(stuetz) + '+ r \,' + latex(richt1) \
            + '+ s \,' + latex(richt2))
    print("")			
	
EK2P1 = EbeneKoord2PrgVersion1	
	
	
	
# ------------	
# EbeneNf2Prg
# ------------

def EbeneNf2Prg(*args, **kwargs):

    if kwargs.get('h'):
        print("\nEbeneNf2Prg - Verfahren\n")     
        print("Bestimmung einer Parameterform einer Ebenengleichung anhand ")
        print("der Normalenform\n")		
        print("Aufruf     EN2P( ebene )\n")		                     
        print("                 ebene   Ebene (Normalenform)\n")
        return		
		
    if len(args) != 1:
        print("agla: Ebene angeben")
        return
				
    anf = '     '				
    ee = args[0]
    if not isinstance(ee, Ebene):
        print("agla: Ebene angeben")
        return
		
    if ee._typ != 1:
        print("agla: Ebene in Normalenform angeben")
        return
		
    if mit_param(ee):		
        print("agla: nicht implementiert, Parameter")
        return

    print("\nBestimmung einer Parameterform der Ebenengleichung anhand der Normalen-")
    print("form\n")
    print("Gegeben:")
    lat = 'E: \;' + pnf(ee, X) + ', \\qquad \\vec{n} = ' + latex(ee.norm)
    dm('\quad \quad ' + lat)
    r, s = Symbol('r'), Symbol('s')	
    print("Ermittlung von zwei Richtungsvektoren\n")
    print(anf + "Die gesuchten Vektoren müssen zum Normalenvektor orthogonal und")
    print(anf + "untereinander nicht kollinear sein")
    print("\n" + anf + "Vorgehen:\n")
    print(anf + anf + "Sind alle Komponenten ungleich Null, erhalten die gesuchten")
    print(anf + anf + "Vektoren die Komponenten (0, n.z, -n.y)  und (n.z, 0, -n.x)")
    print(anf + anf + "Ist eine Komponente Null, erhalten die gesuchten Vektoren an ")
    print(anf + anf + "dieser Stelle unterschiedliche Werte, die anderen beiden Kom-")
    print(anf + anf + "ponenten werden vertauscht, eine mit Wechseln des Vorzeichens")
    nn = ee.norm	
    if nn.x == 0:
        ri1, ri2 = Vektor(1, nn.z, -nn.y), Vektor(2, nn.z, -nn.y)   	
    elif nn.y == 0:
        ri1, ri2 = Vektor(nn.z, 1, -nn.x), Vektor(nn.z, 2, -nn.x)   	
    elif nn.z == 0:
        ri1, ri2 = Vektor(nn.y, -nn.x, 1), Vektor(nn.y, -nn.x, 2) 
    else:
        ri1, ri2 = Vektor(0, nn.z, -nn.y), Vektor(nn.z, 0, -nn.x)
    print('\n' + anf + "Es ergeben sich z.B.")	
    dm('\quad \quad \;' + latex(ri1) + ', \;\;' + latex(ri2))	
    print('\n' + anf + "Die Skalarprodukte mit dem Normalenvektor sind gleich Null")		
    dm('\quad \quad ' + latex(ri1) + '\\circ' + latex(nn) + '=' + \
       latex(ri1.sp(nn)) + ', \;\;' + latex(ri2) + '\\circ' + latex(nn) + \
       '=' + latex(ri2.sp(nn)) )	
    print(anf + "Die Nichtkollinearität der Vektoren ist leicht zu überprüfen")	
    print("\nAufstellen der Parametergleichung mit dem gegebenen Stützvektor und ")
    print("diesen beiden Vektoren")	
    dm('\quad \quad \; ' + latex(X) + '=' + latex(ee.stuetz) + '+ r' + \
       latex(ri1) + '+ s' + latex(ri2))
    print('')			
    	
EN2P = EbeneNf2Prg
	
	
	
# ---------------	
# EbenePrg2Koord
# ---------------

def EbenePrg2Koord(*args, **kwargs):

    if kwargs.get('h'):
        print("\nEbenePrg2Koord - Verfahren\n")     
        print("Bestimmung einer Koordinatenform der Ebenengleichung anhand der Para-")
        print("meterform, Version 0 über die Elimination der Parameter\n")		
        print("Aufruf     EP2K( ebene )\n")		                     
        print("                 ebene   Ebene (Parameterform)\n")
        return		
		
    if len(args) != 1:
        print("agla: Ebene angeben")
        return
				
    anf = '     '				
    ee = args[0]
    if not isinstance(ee, Ebene):
        print("agla: Ebene angeben")
        return
		
    if ee._typ != 2:
        print("agla: Ebene in Parameterform angeben")
        return
		
    if mit_param(ee):		
        print("agla: nicht implementiert, Parameter")
        return

    print("\nBestimmung einer Koordinatenform der Ebenengleichung anhand der Para-")
    print("meterform\n")
    print("Gegeben:")
    lat = 'E: \;' + pprg(ee)
    dm('\quad \quad ' + lat)
    r, s, x, y, z = Symbol('r'), Symbol('s')	, Symbol('x'), Symbol('y'), Symbol('z')
    gl = list(ee.pkt(r, s).komp)
    X = [x, y, z]
    print("Das äquivalente Gleichungssystem ist")
    gl1 = []	
    for i, g in enumerate(gl):	
        g = '\quad \quad ' + latex(X[i]) + '=' + latex(g)	
        dm(g)
        gl1 += [g]		
    print("Elimination der Parameter:\n")
    for i, g in enumerate(gl):
        if not g.has(r) and not g.has(s):	
            print("    Die %s. Gleichung hat keinen Parameter" % (i+1))
            print("\nKoordinatengleichung der Ebene")
            dm(gl1[i])
            print('')			
            return	
			
    if gl[0].has(r) and gl[0].has(s):
        gl1 = [x-gl[0], y-gl[1]]
        wahl = [1, 2]		
    elif gl[0].has(r):
        if gl[1].has(s):	
            gl1 = [x-gl[0], y-gl[1]]
            wahl = [1, 2]		
        else:	
            gl1 = [x-gl[0], z-gl[2]]
            wahl = [1, 3]		
    else:
        if gl[1].has(r):	
            gl1 = [x-gl[0], y-gl[1]]
            wahl = [1, 2]		
        else:	
            gl1 = [x-gl[0], z-gl[2]]
            wahl = [1, 3]		
    print(anf + "Eliminieren von r und s aus zwei der drei Gleichungen\n")
    print(anf + "hier werden die %s. und die %s. Geichung benutzt\n" % (wahl[0], wahl[1]))
    print(anf + "Auflösen des LGS nach r und s; die Lösung ist")
    L = solve(gl1, [r, s])	
    dm('\quad \quad ' + latex(L))
    ngl3 = 2 if 3 in wahl else 3
    gl3 = Gleichung(y, gl[1]) if 3 in wahl else Gleichung(z, gl[2])
    print(anf + "r und s in die %s. Gleichung einsetzen" %ngl3)	
    gl3 = Gleichung(gl3.lhs, gl3.rhs.subs(L))
    dm('\quad \quad ' + latex(gl3))
    print("Koordinatengleichung der Ebene")	
    gl = Gleichung(gl3.lhs - gl3.rhs, 0)
    dm('\quad \quad ' + latex(gl))
    px = Poly(gl.lhs.subs({y:0, z:0}), x)	
    py = Poly(gl.lhs.subs({x:0, z:0}), y)	
    pz = Poly(gl.lhs.subs({x:0, y:0}), z)	
    dix = dict(px.all_terms())
    diy = dict(py.all_terms())
    diz = dict(pz.all_terms())
    try:
        k0 = dix[(0,)]
    except KeyError:
        k0 = 0	
    try:
        k1 = dix[(1,)]
    except KeyError:
        k1 = 0	
    try:
        k2 = diy[(1,)]
    except KeyError:
        k2 = 0	
    try:
        k3 = diz[(1,)]
    except KeyError:
        k3 = 0	
		
    kk = [ k0, k1, k2, k3 ] 
	
    def fakt():
        f = 1		
        if any([(isinstance(x, Rational) and x.q > 1) for x in kk]):
            for k in kk:
                if isinstance(k, Rational) and k.q > f:	
                    f = k.q				
        return f
		
    f = fakt()
    if f > 1:	
        gl = Gleichung(f*gl.lhs, 0)
        print("Bei Bedarf können die Brüche beseitigt werden " + \
             "(Multiplikation mit %s)" %f)	
        dm('\quad \quad ' + latex(gl))
    print('')
	
EP2K = EbenePrg2Koord		   
	
	
	
# -----------------------	
# EbenePrg2KoordVersion1
# -----------------------

def EbenePrg2KoordVersion1(*args, **kwargs):

    if kwargs.get('h'):
        print("\nEbenePrg2KoordVersion1 - Verfahren\n")   
        print("Bestimmung einer Koordinatenform der Ebenengleichung anhand der Para-")
        print("meterform, Version 1 über die Normalengleichung\n")		
        print("Aufruf     EP2K1( ebene )\n")		                     
        print("                  ebene   Ebene (Parameterform)\n")
        return		
		
    if len(args) != 1:
        print("agla: Ebene angeben")
        return
				
    anf = '     '				
    ee = args[0]
    if not isinstance(ee, Ebene):
        print("agla: Ebene angeben")
        return
		
    if ee._typ != 2:
        print("agla: Ebene in Parameterform angeben")
        return
		
    if mit_param(ee):		
        print("agla: nicht implementiert, Parameter")
        return

    print("\nBestimmung einer Koordinatenform der Ebenengleichung anhand der Parame-")
    print("terform\n")
    print("Gegeben:")
    lat = 'E: \;' + pprg(ee)
    dm('\quad \quad ' + lat)
    nn = ee.norm	
    print("Ein Normalenvektor der Ebene und die Normalengleichung (als Stützvektor")
    print("wird der gegebene verwendet) sind")
    x, y, z = Symbol('x'), Symbol('y'), Symbol('z')
    X = Vektor(x, y, z)	
    dm('\quad \quad \;' + latex(nn) + ',\;\;\;\;' + pnf(ee, X))
    print("Ermittlung der Koordinatengleichung:\n")	
    print(anf + "Ausmultiplizieren der Normalengleichung und Vereinfachen")	
    dm('\quad \quad \;' + psp2(X, ee.stuetz, nn) + '= 0')
    dm('\quad \quad \;' + latex((X - ee.stuetz).sp(nn)) + '= 0')
    gl = Gleichung((X - ee.stuetz).sp(nn), 0)	
    px = Poly(gl.lhs.subs({y:0, z:0}), x)	
    py = Poly(gl.lhs.subs({x:0, z:0}), y)	
    pz = Poly(gl.lhs.subs({x:0, y:0}), z)	
    dix = dict(px.all_terms())
    diy = dict(py.all_terms())
    diz = dict(pz.all_terms())
    try:
        k0 = dix[(0,)]
    except KeyError:
        k0 = 0	
    try:
        k1 = dix[(1,)]
    except KeyError:
        k1 = 0	
    try:
        k2 = diy[(1,)]
    except KeyError:
        k2 = 0	
    try:
        k3 = diz[(1,)]
    except KeyError:
        k3 = 0	
		
    kk = [ k0, k1, k2, k3 ]
	
    def fakt():
        f = 1		
        if any([(isinstance(x, Rational) and x.q > 1) for x in kk]):
            for k in kk:
                if isinstance(k, Rational) and k.q > f:	
                    f = lcm(k.q, f)				
        return f
		
    f = fakt()
    if f > 1:	
        gl = Gleichung(f*gl.lhs, 0)
        print("Bei Bedarf können die Brüche beseitigt werden " + \
             "(Multiplikation mit %s)" %f)	
        dm('\quad \quad ' + latex(gl))
    print('')
	
EP2K1 = EbenePrg2KoordVersion1    	
	
	
	
# ------------	
# EbenePrg2Nf
# ------------

def EbenePrg2Nf(*args, **kwargs):

    if kwargs.get('h'):
        print("\nEbenePrg2Nf - Verfahren\n")     
        print("Bestimmung einer Normalenform der Ebenengleichung anhand der Para-")
        print("meterform\n")		
        print("Aufruf     EP2N( ebene )\n")		                     
        print("                 ebene   Ebene (Parameterform)\n")
        return		
		
    if len(args) != 1:
        print("agla: Ebene angeben")
        return
				
    anf = '     '				
    ee = args[0]
    if not isinstance(ee, Ebene):
        print("agla: Ebene angeben")
        return
		
    if ee._typ != 2:
        print("agla: Ebene in Parameterform angeben")
        return
		
    if mit_param(ee):		
        print("agla: nicht implementiert, Parameter")
        return

    print("\nBestimmung einer Normalenform der Ebenengleichung anhand der Para-")
    print("meterform\n")
    print("Gegeben:")
    lat = 'E: \;' + pprg(ee)
    dm('\quad \quad ' + lat)
    print("Ermittlung einer Normalenform:\n")	
    nn = ee.norm	
    print(anf + "Ein Normalenvektor der Ebene ist") 
    dm('\quad \quad \;' + latex(nn))
    print(anf + "Der Stützvektor wird aus der Parametergleichung übernommen, die ")	
    print(anf + "gesuchte Gleichung ist")	
    x, y, z = Symbol('x'), Symbol('y'), Symbol('z')
    X = Vektor(x, y, z)	
    dm('\quad \quad \;' + pnf(ee, X))

    kk = nn.komp
	
    def fakt():
        f = 1		
        if any([(isinstance(x, Rational) and x.q > 1) for x in kk]):
            for k in kk:
                if isinstance(k, Rational) and k.q > f:	
                    f = lcm(k.q, f)				
        return f
		
    f = fakt()
    if f > 1:	
        nn *= f
        print("Bei Bedarf können die Brüche im Normalenvektor beseitigt werden")
        print("(Multiplikation mit %s)" %f)	
        ee = Ebene(ee.stuetz, nn)			 
        dm('\quad \quad \;' + pnf(ee, X))
    kk = nn.komp	
    ff = gcd(gcd(kk[0], kk[1]), kk[2])	
    if kk[0] <= 0 and kk[1] <= 0 and kk[2] <= 0:
        ff = -ff	
    if abs(ff) > 1 or ff == -1:	
        nn *= ff
        print("Bei Bedarf können gemeinsame Faktoren in den Komponenten des Normalen-")	
        print("vektors gekürzt werden")	
        print("(hier " + str(ff) + ")")	
        ee = Ebene(ee.stuetz, nn)		
        dm('\quad \quad \;' + pnf(ee, X))
		
    print(' ')
	
EP2N = EbenePrg2Nf



# ------------
# RichtVektor
# ------------

def RichtVektor(*args, **kwargs):

    if kwargs.get('h'):
        print("\nRichtVektor - Verfahren\n")     
        print("Bestimmung von zwei Richtungsvektoren einer Ebene\n")		
        print("Aufruf     ERV( ebene )\n")		                     
        print("                ebene   Ebene\n")
        print("Statt ERV kann auch RV verwendet werden\n")	
        return		

    if len(args) != 1:
        print("agla: Ebene angeben")
        return
				
    anf = '     '				
    ee = args[0]
    if not isinstance(ee, Ebene):
        print("agla: Ebene angeben")
        return
		
    if mit_param(ee):		
        print("agla: nicht implementiert, Parameter")
        return

    print("\nErmittlung von zwei Richtungsvektoren der Ebene\n")
    print("Gegeben:")
    x, y, z = Symbol('x'), Symbol('y'), Symbol('z')	
    X = Vektor(x, y, z)	
    lat = 'E : \;'
    if ee._typ == 1:
        lat += pnf(ee, X)
    elif ee._typ == 2:
        lat += pprg(ee) 
    else:
        lat += pkoord(ee, X)	
    dm('\quad \quad ' + lat)
		
    if ee._typ == 2:
        print("Die Vektoren sind aus der Gleichung ablesbar")
        dm('\quad \quad ' + latex(ee.richt[0]) + ',\;\;\;' + latex(ee.richt[1]))
        return
    print("Ein Normalenvektor der Ebene ist")
    dm('\quad \quad \;' + '\\vec{n} =' + latex(ee.norm))
    print("Ermittlung von zwei Richtungsvektoren\n")
    print(anf + "Die gesuchten Vektoren müssen zum Normalenvektor orthogonal und")
    print(anf + "untereinander nicht kollinear sein")
    print("\n" + anf + "Vorgehen:\n")
    print(anf + anf + "Sind alle Komponenten ungleich Null, erhalten die gesuch-")
    print(anf + anf + "ten Vektoren die Komponenten (0, n.z, -n.y)  und ")
    print(anf + anf + "(n.z, 0, -n.x). Ist eine Komponente Null, erhalten die ge-")
    print(anf + anf + "suchten Vektoren an dieser Stelle unterschiedliche Werte, ")
    print(anf + anf + "die anderen beiden Komponenten werden vertauscht, eine mit") 
    print(anf + anf + "Wechseln des Vorzeichens")
    nn = ee.norm	
    if nn.x == 0:
        ri1, ri2 = Vektor(1, nn.z, -nn.y), Vektor(2, nn.z, -nn.y)   	
    elif nn.y == 0:
        ri1, ri2 = Vektor(nn.z, 1, -nn.x), Vektor(nn.z, 2, -nn.x)   	
    elif nn.z == 0:
        ri1, ri2 = Vektor(nn.y, -nn.x, 1), Vektor(nn.y, -nn.x, 2) 
    else:
        ri1, ri2 = Vektor(0, nn.z, -nn.y), Vektor(nn.z, 0, -nn.x)
    print('\n' + anf + "Es ergeben sich z.B.")	
    dm('\quad \quad \;' + latex(ri1) + ', \;\;' + latex(ri2))	
    print(anf + "Die Skalarprodukte mit dem Normalenvektor sind gleich Null")		
    dm('\quad \quad ' + latex(ri1) + '\\circ' + latex(nn) + '=' + \
       latex(ri1.sp(nn)) + ', \;\;' + latex(ri2) + '\\circ' + latex(nn) + \
       '=' + latex(ri2.sp(nn)) )	
    print(anf + "Die Nichtkollinearität der Vektoren ist leicht zu überprüfen\n")	

ERV = RichtVektor
RV = RichtVektor



# -----------
# NormVektor
# -----------

def NormVektor(*args, **kwargs):

    if kwargs.get('h'):
        print("\nNormVektor - Verfahren\n")     
        print("Bestimmung eines Normalenvektors einer Ebene oder zu zwei")
        print("gegebenen Vektoren, Version 0 mit Lösung eines LGS\n")		
        print("Aufruf     ENV( ebene | vektor1, vektor2 )\n")		                     
        print("                ebene   Ebene")
        print("                vektor  Vektor\n")
        print("Statt ENV kann auch NV verwendet werden\n")	
        return		

    if len(args) not in (1, 2):
        print("agla: ein oder zwei Argumente angeben")
        return
		
    if len(args) == 1:		
        ee = args[0]
        if not isinstance(ee, Ebene):
            print("agla: Ebene angeben")
            return		
        if mit_param(ee):		
            print("agla: nicht implementiert, Parameter")
            return
        v1, v2 = ee.richt			
    elif len(args) == 2:	
        v1, v2 = args	
        if not (isinstance(v1, Vektor) and isinstance(v2, Vektor)): 
            print("agla: Zwei Vektoren angeben")
            return
        if not v1.dim == 3 and v2.dim == 3: 
            print("agla: Zwei Vektoren im Raum R^3 angeben")
            return
        if kollinear(v1, v2): 
            print("agla: die Vektoren dürfen nicht kollinear sein")
            return
    anf = '     '				
		
    print("\nErmittlung eines Normalenvektors einer Ebene oder zu zwei gegebenen ")
    print("Vektoren\n")
    print("Gegeben:")
    if len(args) == 1:	
        x, y, z = Symbol('x'), Symbol('y'), Symbol('z')	
        X = Vektor(x, y, z)	
        lat = 'E : \;'
        if ee._typ == 1:
            lat += pnf(ee, X)
        elif ee._typ == 2:
            lat += pprg(ee) 
        else:
            lat += pkoord(ee, X)	
        dm('\quad \quad ' + lat)
        if ee._typ == 2:
            print(anf + "mit den Richtungsvektoren\n")
            dm('\quad \quad \;' + latex(v1) + ',\;\;\; ' + latex(v2))
        if ee._typ in (1, 3):
            print("der Normalenvektor ist aus der Gleichung ablesbar")
            dm('\quad \quad \;' + '\\vec{n} =' + latex(ee.norm))
            return			
    else:
        dm('\quad \quad \;' + latex(v1) + ',\;\;\;' + latex(v2))
    print("Ermittlung eines Normalenvektors\n")
    print(anf + "Der Normalenvektor sei")
    n_x, n_y, n_z = Symbol('n_x'), Symbol('n_y'), Symbol('n_z')
    nn = Vektor(n_x, n_y, n_z)	
    dm('\quad \quad \;' + '\\vec{n} =' + latex(nn))
    print(anf + "Er soll orthogonal zu den beiden Vektoren sein, es muss gelten")
    dm('\quad \quad \;' + latex(v1) + '\\circ' + latex(nn) + '= 0')
    dm('\quad \quad \;' + latex(v2) + '\\circ' + latex(nn) + '= 0')
    print(anf + "Ausmultiplizieren führt zu dem LGS")
    dm('\quad \quad \;' + latex(v1.sp(nn)) + '= 0')
    dm('\quad \quad \;' + latex(v2.sp(nn)) + '= 0')
    print(anf + "Mit der Lösung")
    lgs = LGS([v1.sp(nn), v2.sp(nn)])
    L = lgs.loes	
    dm('\quad \quad \;' + latex(L))
    c1 = Symbol("c1")
    hasc1 = False
    try:	
        if L[n_x].has(c1):
             xk = L[n_x].subs(c1, 1)	
             hasc1 = True
        else:
            xk = L[n_x]		
    except KeyError:
        xk = 1
        print(anf + "Die x-Komponente wird auf 1 gesetzt")
        dm('\quad \quad \;' + latex(n_x) + '= 1')		
    try:	
        if L[n_y].has(c1):
             yk = L[n_y].subs(c1, 1)	
             hasc1 = True
        else:
            yk = L[n_y]		
    except KeyError:
        yk = 1	
        print(anf + "Die y-Komponente wird auf 1 gesetzt")
        dm('\quad \quad \;' + latex(n_y) + '= 1')		
    try:	
        if L[n_z].has(c1):
             zk = L[n_z].subs(c1, 1)	
             hasc1 = True
        else:
            zk = L[n_z]		
    except KeyError:
        zk = 1
        print(anf + "Die z-Komponente wird auf 1 gesetzt")
        dm('\quad \quad \;' + latex(n_z) + '= 1')		

    nn = Vektor(xk, yk, zk)
    c2 = Symbol('c2')	
    if hasc1:
        print(anf + "Mit")
        dm('\quad \quad \;' + latex(c1) + ' = 1')
        print(anf + "ergibt sich ein Normalenvektor")
    elif nn.has(c2):		
        print(anf + "Mit")
        dm('\quad \quad \;' + latex(c2) + ' = 1')
        print(anf + "ergibt sich ein Normalenvektor")
        nn = nn.subs(c2, 1)		
    else:
        print(anf + "Es ergibt sich ein Normalenvektor")
    dm('\quad \quad \;' + latex(nn))
	
    kk = nn.komp
	
    def fakt():
        f = 1		
        if any([(isinstance(x, Rational) and x.q > 1) for x in kk]):
            for k in kk:
                if isinstance(k, Rational) and k.q > f:	
                    f = k.q				
        return f
		
    f = fakt()
    if f > 1:	
        nn *= f
        print("Bei Bedarf können die Brüche beseitigt werden " + \
             "(Multiplikation mit %s)" %f)	
        dm('\quad \quad ' + latex(nn))
    kk = nn.komp	
    ff = gcd(gcd(kk[0], kk[1]), kk[2])	
    if kk[0] <= 0 and kk[1] <= 0 and kk[2] <= 0:
        ff = -ff	
    if abs(ff) > 1 or ff == -1:	
        print("Bei Bedarf können gemeinsame Faktoren in den Komponenten gekürzt werden")	
        print("(hier " + str(ff) + ")")	
        nn = Vektor(nn.x/ff, nn.y/ff, nn.z/ff)		
        dm('\quad \quad ' + latex(nn))
    print(' ')
	
NV = NormVektor
ENV = NormVektor

	
	
# -------------------	
# NormVektorVersion1
# -------------------

def NormVektorVersion1(*args, **kwargs):

    if kwargs.get('h'):
        print("\nNormVektor - Verfahren\n")     
        print("Bestimmung eines Normalenvektors einer Ebene oder zu zwei")
        print("gegebenen Vektoren, Version 1 mit dem Vektorprodukt\n")			
        print("Aufruf     ENV1( ebene | vektor1, vektor2 )\n")		                     
        print("                 ebene   Ebene")
        print("                 vektor  Vektor\n")
        print("Statt ENV1 kann auch NV1 verwendet werden\n")	
        return		
		
    if len(args) not in (1, 2):
        print("agla: ein oder zwei Argumente angeben")
        return
		
    if len(args) == 1:		
        ee = args[0]
        if not isinstance(ee, Ebene):
            print("agla: Ebene angeben")
            return		
        if mit_param(ee):		
            print("agla: nicht implementiert, Parameter")
            return
        v1, v2 = ee.richt			
    elif len(args) == 2:	
        v1, v2 = args	
        if not (isinstance(v1, Vektor) and isinstance(v2, Vektor)): 
            print("agla: Zwei Vektoren angeben")
            return
        if not v1.dim == 3 and v2.dim == 3: 
            print("agla: Zwei Vektoren im Raum R^3 angeben")
            return
        if kollinear(v1, v2): 
            print("agla: die Vektoren dürfen nicht kollinear sein")
            return
    anf = '     '				
		
    print("\nErmittlung eines Normalenvektors einer Ebene oder zu zwei gegebenen Vektoren\n")
    print("Gegeben:")
    if len(args) == 1:	
        x, y, z = Symbol('x'), Symbol('y'), Symbol('z')	
        X = Vektor(x, y, z)	
        lat = 'E : \;'
        if ee._typ == 1:
            lat += pnf(ee, X)
        elif ee._typ == 2:
            lat += pprg(ee) 
        else:
            lat += pkoord(ee, X)	
        dm('\quad \quad ' + lat)
        if ee._typ == 2:
            print(anf + "mit den Richtungsvektoren")
            dm('\quad \quad \;' + latex(v1) + ',\;\;\; ' + latex(v2))
        if ee._typ in (1, 3):
            print("Der Normalenvektor ist aus der Gleichung ablesbar")
            dm('\quad \quad \;' + '\\vec{n} =' + latex(ee.norm))
            return			
    else:
        dm('\quad \quad \;' + latex(v1) + ',\;\;\;' + latex(v2))
    print("Ermittlung eines Normalenvektors:\n")
    a_1, a_2, a_3, b_1, b_2, b_3 = Symbol('a_1'), Symbol('a_2'), Symbol('a_3'), \
        Symbol('b_1'), Symbol('b_2'), Symbol('b_3')	
    aa, bb = Vektor(a_1, a_2, a_3), Vektor(b_1, b_2, b_3)
    print(anf + "Es wird die Eigenschaft des Vektorproduktes ausgenutzt, dass dieser")
    print(anf + "Vektor orthogonal zu den beiden Vektoren ist, auf deren Grundlage")	
    print(anf + "er gebildet wurde")	
    print('\n' + anf + "Das Vektorprodukt (auch Kreuzprodukt) zweier Vektoren")
    dm('\quad \quad \;' + latex(aa) + ',\;\;\;' + latex(bb))
    print(anf + "ist der Vektor")
    lat = '\\left(\\begin{matrix}a_2 b_3 - a_3 b_2\\\\a_3 b_1 - a_1 b_3\\\\' + \
          'a_1 b_2 - a_2 b_1\\end{matrix}\\right)'	
    dm('\quad \quad \;' + lat)
    print("\nDie Berechnung der Komponenten kann günstig nach folgendem Schema")
    print("erfolgen (Sarrus'sche Regel):")	
    	
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
	
    left, width = 0, 1.2
    bottom, height = 0, 1
    fig = plt.figure(figsize=(5, 3))
    ax = fig.add_subplot(111)
    p = patches.Rectangle(
        (left, bottom), width, height, color='grey', lw=0.3, fill=False, clip_on=False)
    ax.add_patch(p)
    posx = 0.2
    posy, dy = 0.9, 0.15
    st, st1 = 12, 9	
    ax.text(posx, posy, '$a_1$', size=st)
    ax.text(posx, posy-dy, '$a_2$', size=st)
    ax.text(posx,posy-2*dy, '$a_3$', size=st)
    ax.text(posx, posy-3*dy, '$a_1$', size=st)
    ax.text(posx, posy-4*dy, '$a_2$', size=st)
    posx1 = 0.4
    ax.text(posx1, posy, '$b_1$', size=st)
    ax.text(posx1, posy-dy, '$b_2$', size=st)
    ax.text(posx1, posy-2*dy, '$b_3$', size=st)
    ax.text(posx1, posy-3*dy, '$b_1$', size=st)
    ax.text(posx1, posy-4*dy, '$b_2$', size=st)
    x, y = [posx+0.07, posx1-0.01], [0.89-dy, 0.8-dy]
    ax.plot(x, y, color=(1,0,0))
    x, y = [posx+0.07, posx1-0.01], [0.89-2*dy, 0.8-2*dy]
    ax.plot(x, y, color=(1,0,0))
    x, y = [posx+0.07, posx1-0.01], [0.89-3*dy, 0.8-3*dy]
    ax.plot(x, y, color=(1,0,0))
    x, y = [posx1-0.01, posx+0.07], [0.89-dy, 0.8-dy]
    ax.plot(x, y, color=(0,0,1))
    x, y = [posx1-0.01, posx+0.07], [0.89-2*dy, 0.8-2*dy]
    ax.plot(x, y, color=(0,0,1))
    x, y = [posx1-0.01, posx+0.07], [0.89-3*dy, 0.8-3*dy]
    ax.plot(x, y, color=(0,0,1))
    ax.text(posx1+0.18, posy-0.1, 'Vektorprodukt', size=st1, family='serif')
    ax.text(posx1+0.18, posy-0.1-dy, '1. Komp.', size=st1, family='serif')
    ax.text(posx1+0.45, posy-0.1-dy, '$a_2 b_3-a_3 b_2$', size=st)
    ax.text(posx1+0.18, posy-0.1-2*dy, '2. Komp.', size=st1, family='serif')
    ax.text(posx1+0.45, posy-0.1-2*dy, '$a_3 b_1-a_1 b_3$', size=st)
    ax.text(posx1+0.18, posy-0.1-3*dy, '3. Komp.', size=st1, family='serif')
    ax.text(posx1+0.45, posy-0.1-3*dy, '$a_1 b_2-a_2 b_1$', size=st)
    x, y = [posx+0.07, posx1-0.01], [0.8-4.3*dy, 0.8-4.3*dy]
    ax.plot(x, y, color=(1,0,0))
    ax.text(posx1+0.1, 0.8-4.3*dy, 'Addition', size=st1, family='serif')
    x, y = [posx1-0.01, posx+0.07], [0.8-4.8*dy, 0.8-4.8*dy]
    ax.plot(x, y, color=(0,0,1))
    ax.text(posx1+0.1, 0.8-4.8*dy, 'Subtraktion', size=st1, family='serif')
    plt.axis('off')
    plt.show()	
    	
    A, B = v1, v2
	
    if all([isinstance(x, (int, Integer)) for x in A.komp + B.komp]):
	
        print("Schema, auf die vorliegenden Vektoren angewendet:")	
	
        def platex(x):
            if x < 0:
                return '(' + latex(x) + ')'
            return latex(x)
    
        left, width = 0, 1.5
        bottom, height = 0, 1
        fig1 = plt.figure(figsize=(5.29, 3))
        ax = fig1.add_subplot(111)
        p = patches.Rectangle(
            (left, bottom), width, height, color='grey', lw=0.3, 
			  fill=False, clip_on=False)
        ax.add_patch(p)
        posx = 0.2
        posy, dy = 0.9, 0.15
        st, st1 = 9, 9	
        ax.text(posx, posy, latex(A.x), size=st, family='serif')
        ax.text(posx, posy-dy, latex(A.y), size=st, family='serif')
        ax.text(posx,posy-2*dy, latex(A.z), size=st, family='serif')
        ax.text(posx, posy-3*dy, latex(A.x), size=st, family='serif')
        ax.text(posx, posy-4*dy, latex(A.y), size=st, family='serif')
        posx1 = 0.4
        ax.text(posx1, posy, latex(B.x), size=st, family='serif')
        ax.text(posx1, posy-dy, latex(B.y), size=st, family='serif')
        ax.text(posx1, posy-2*dy, latex(B.z), size=st, family='serif')
        ax.text(posx1, posy-3*dy, latex(B.x), size=st, family='serif')
        ax.text(posx1, posy-4*dy, latex(B.y), size=st, family='serif')
        x, y = [posx+0.07, posx1-0.01], [0.89-dy, 0.8-dy]
        ax.plot(x, y, color=(1,0,0))
        x, y = [posx+0.07, posx1-0.01], [0.89-2*dy, 0.8-2*dy]
        ax.plot(x, y, color=(1,0,0))
        x, y = [posx+0.07, posx1-0.01], [0.89-3*dy, 0.8-3*dy]
        ax.plot(x, y, color=(1,0,0))
        x, y = [posx1-0.01, posx+0.07], [0.89-dy, 0.8-dy]
        ax.plot(x, y, color=(0,0,1))
        x, y = [posx1-0.01, posx+0.07], [0.89-2*dy, 0.8-2*dy]
        ax.plot(x, y, color=(0,0,1))
        x, y = [posx1-0.01, posx+0.07], [0.89-3*dy, 0.8-3*dy]
        ax.plot(x, y, color=(0,0,1))
        ax.text(posx1+0.245, posy-0.1-dy, platex(A.y) + ' $\cdot$ ' + platex(B.z) + ' $\minus$ ' \
            + platex(A.z) + ' $\cdot$ ' + platex(B.y) + ' = ' + latex(A.y*B.z-A.z*B.y), \
            size=st1, family='serif')
        ax.text(posx1+0.245, posy-0.1-2*dy, platex(A.z) + ' $\cdot$ ' + platex(B.x) + \
            ' $\minus$ ' + platex(A.x) + ' $\cdot$ ' + platex(B.z) + ' = ' + latex(A.z*B.x-A.x*B.z), \
            size=st1, family='serif')
        ax.text(posx1+0.245, posy-0.1-3*dy, platex(A.x) + ' $\cdot$ ' + platex(B.y) + \
            ' $\minus$ ' + platex(A.y) + ' $\cdot$ ' + platex(B.x) + ' = ' + \
            latex(A.x*B.y-A.y*B.x), size=st1, family='serif')
        x, y = [posx+0.07, posx1-0.01], [0.8-4.3*dy, 0.8-4.3*dy]
        ax.plot(x, y, color=(1,0,0))
        st1 = 9
        ax.text(posx1+0.1, 0.8-4.3*dy, 'Addition', size=st1, family='serif')
        x, y = [posx1-0.01, posx+0.07], [0.8-4.8*dy, 0.8-4.8*dy]
        ax.plot(x, y, color=(0,0,1))
        ax.text(posx1+0.1, 0.8-4.8*dy, 'Subtraktion', size=st1, family='serif')
        plt.axis('off')
        plt.show()	
	
    nn = v1.vp(v2)	
    print("Ein Normalenvektor ist somit")	
    dm('\quad \quad \;' + latex(nn))
    kk = nn.komp
	
    def fakt():
        f = 1		
        if any([(isinstance(x, Rational) and x.q > 1) for x in kk]):
            for k in kk:
                if isinstance(k, Rational) and k.q > f:	
                    f = k.q				
        return f
		
    f = fakt()
    if f > 1:	
        nn *= f
        print("Bei Bedarf können die Brüche beseitigt werden " + \
             "(Multiplikation mit %s)" %f)	
        dm('\quad \quad ' + latex(nn))	
    kk = nn.komp	
    ff = gcd(gcd(kk[0], kk[1]), kk[2])	
    if kk[0] <= 0 and kk[1] <= 0 and kk[2] <= 0:
        ff = -ff	
    if abs(ff) > 1 or ff == -1:	
        print("Bei Bedarf können gemeinsame Faktoren in den Komponenten gekürzt ")	
        print("werden (hier %s)" %ff)	
        nn = Vektor(nn.x/ff, nn.y/ff, nn.z/ff)		
        dm('\quad \quad ' + latex(nn))
    print(' ')
	
NV1 = NormVektorVersion1
ENV1 = NormVektorVersion1

	
	
# ---------------	
# LagePunktKugel
# ---------------

def LagePunktKugel(*args, **kwargs):

    if kwargs.get('h'):
        print("\nLagePunktKugel - Verfahren\n")
        print("Lage eines Punktes bezüglich einer Kugel\n")
        print("Aufruf     LPK( punkt, kugel )\n")		                     
        print("                punkt   Punkt")		
        print("                kugel   Kugel\n")
        return		
		
    if len(args) != 2:
        print("agla: Punkt und Kugel angeben")
        return
				
    anf = '     '				
    pp, kk = args
    if not (isinstance(pp, Vektor) and isinstance(kk, Kugel)):
        if isinstance(pp, Kugel) and isinstance(kk, Vektor):
            pp, kk = kk, pp
        else:
            print("agla: Punkt und Kugel angeben")
            return
		
    if pp.dim != 3:
        print("agla: Punkt des Raumes R^3 angeben")
        return
		
    if mit_param(pp) or mit_param(kk):		
        print("agla: nicht implementiert, Parameter")
        return
		
    print("\nLage eines Punktes bezüglich einer Kugel\n")
    print("Gegeben:")
    lat1 = 'P(' + ppunkt(pp)
    lat2 = 'k : \;' + pkugel(kk)
    dm('\quad \quad ' + lat1 + ', \quad \quad ' + lat2)
    print("Ermittlung des Abstandes des Punktes vom Mittelpunkt der Kugel:")
    print("\n" + anf + "Mittelpunkt und  Radius der Kugel und der gesuchte Abstand")	
    print(anf + "sind")
    r = kk.radius	
    rr = latex(r) if isinstance(r, (int, Integer, float, Float)) else \
        latex(r) + '=' + latex(r.evalf())	
    dd = pp.abstand(kk.mitte)	
    if isinstance(dd, (int, Integer, float, Float)):	
        dm('\quad \quad \; M' + kk.mitte.punkt_ausg_(s=1) + ', \quad  r =' + \
            rr + ', \quad  d(P, M) =' + latex(dd))
    else:		
        dm('\quad \quad \; M' + kk.mitte.punkt_ausg_(s=1) + ', \quad  r =' + \
            rr + ', \quad  d(P, M) =' + latex(dd) + '=' + \
            latex(dd.evalf()))
    print("Es ist")		
    if dd == kk.radius:
        dm('\quad \quad \; d(P, M) = r')
        print("Der Punkt liegt auf der Kugeloberfläche\n")		
    elif dd < kk.radius:
        dm('\quad \quad \; d(P, M) \\lt r')
        print("Der Punkt liegt im Inneren der Kugel\n")		
    elif dd > kk.radius:
        dm('\quad \quad \; d(P, M) \\gt r')
        print("Der Punkt liegt außerhalb der Kugel\n")		

LPK = LagePunktKugel



# ----------------
# LageGeradeKugel
# ----------------

def LageGeradeKugel(*args, **kwargs):

    if kwargs.get('h'):
        print("\nLageGeradeKugel - Verfahren\n")
        print("Lage einer Geraden bezüglich einer Kugel\n")
        print("Aufruf     LGK( gerade, kugel )\n")		                     
        print("                gerade  Gerade")		
        print("                kugel   Kugel\n")
        return		
		
    if len(args) != 2:
        print("agla: Gerade und Kugel angeben")
        return
				
    anf = '     '				
    gg, kk = args
    if not (isinstance(gg, Gerade) and isinstance(kk, Kugel)):
        if isinstance(gg, Kugel) and isinstance(kk, Gerade):
            gg, kk = kk, gg
        else:
            print("agla: Gerade und Kugel angeben")
            return
		
    if gg.dim != 3:
        print("agla: Gerade im Raum R^3 angeben")
        return
		
    if mit_param(gg) or mit_param(kk):		
        print("agla: nicht implementiert, Parameter")
        return
		
    print("\nLage einer Geraden bezüglich einer Kugel\n")
    print("Gegeben:")
    t = Symbol('t')
    gg = Gerade(gg.stuetz, gg.richt, t)	
    lat1 = 'g : \;' + pgerade(gg)
    lat2 = 'k : \;' + pkugel(kk)
    dm('\quad \quad ' + lat1 + ', \quad \quad ' + lat2)
    print("Bestimmen der Schnittmenge der Geraden mit der Kugel:")
    print('\n' + anf + "Die rechte Seite der Geradengleichung wird in die Kugelgleichung")
    print(anf + "eingesetzt")
    pp = gg.pkt(t)	
    x, y, z = Symbol('x'), Symbol('y'), Symbol('z')	
    dm('\quad \quad \;' + latex(kk.gleich.lhs.subs({x:pp.x, y:pp.y, z:pp.z})) + \
        '=' + latex(kk.gleich.rhs))	
    gl = expand(kk.gleich.lhs.subs({x:pp.x, y:pp.y, z:pp.z}) - kk.gleich.rhs)		
    dm('\quad \quad \;' + latex(gl) + '= 0')
    po = Poly(gl, t)
    di = dict(po.all_terms())	
    if di[(0,)] == 0 and di[(1,)] != 0:
        print(anf + "t wird ausgeklammert, die quadratische Gleichung")
        dm('\quad \quad \;' + latex(t) + '\\cdot \\left(' + \
            latex(di[(2,)]*t+di[(1,)]) + '\\right) = 0')
        L = solve(di[(2,)]*t+di[(1,)], t)			
        t1, t2 = 0, L[0]
        if t1 != t2:		
            print(anf + "hat die Lösungen")
            dm('\quad \quad \; t_1 = 0, \; t_2 =' + latex(t2))
        else:		
            print(anf + "hat die Lösung")
            dm('\quad \quad \; t = 0')
    else:
        if di[(2,)] != 1:
            print(anf + "Division durch den Koeffizienten bei t^2 führt zu")		
            gl = t**2 + di[(1,)]/di[(2,)]*t + di[(0,)]/di[(2,)]		
            dm('\quad \quad \;' + latex(gl) + '= 0')
            pi2 = -di[(1,)]/di[(2,)]/2			
            q = di[(0,)]/di[(2,)]	
        else:
            pi2 = -di[(1,)]/2			
            q = di[(0,)]	
        print(anf + "Mit der Lösungsformel für quadratische Gleichungen ergibt sich")	
        dm('\quad \quad \; t_{1,2} = ' + latex(pi2) + '\\pm \\sqrt{' + \
            latex(pi2**2) + '-' + ('\\left(' if q < 0 else '') + latex(q) + \
            ('\\right)' if q < 0 else '') + '}')
        if pi2**2-q < 0:
            print(anf + "Der Ausdruck unter der Wurzel ist negativ, es existiert keine ")
            print(anf + "Lösung")			
            print("\nDie Gerade schneidet die Kugel nicht\n")
            return				
        elif pi2**2-q > 0:
            print(anf + "Damit existieren zwei Lösungen")
            t1, t2 = pi2 + sqrt(pi2**2 - q), pi2 - sqrt(pi2**2 - q)			
            dm('\quad \quad \; t_1 =' + (latex(pi2) if pi2 != 0 else '') + \
			    '\\sqrt{' + latex(pi2**2-q) + '}' + \
			      ', \;\; t_2 =' + (latex(pi2) if pi2 != 0 else '') + '-' + \
				   '\\sqrt{' + latex(pi2**2-q) + '}')
        elif pi2**2-q == 0:
            print(anf + "Der Ausdruck unter der Wurzel ist Null, es existiert")
            print(anf + "eine Lösung")
            t1, t2 = pi2, pi2 			
            dm('\quad \quad \; t =' + latex(pi2))
	
    if t1 != t2:	
        print("Einsetzen der berechneten t-Werte in die Geradengleichung ergibt")
        print("zwei Schnittpunkte\n")
    else:		
        print("Einsetzen des berechneten t-Wertes in die Geradengleichung ergibt")
        print("einen Berührpunkt\n")
    if t1 != t2:
        S1, S2 = gg.pkt(t1), gg.pkt(t2)	
        print("Die Gerade schneidet die Kugel in den beiden Punkten")
        dm('\quad \quad \;' + latex(S1) + ', \;\;\;' + latex(S2))
    elif t1 == t2:
        S = gg.pkt(t1)	
        print("Die Gerade berührt die Kugel in dem Punkt")
        dm('\quad \quad \;' + latex(S)) 

LGK = LageGeradeKugel




# ---------------
# LageEbeneKugel
# ---------------

def LageEbeneKugel(*args, **kwargs):

    if kwargs.get('h'):
        print("\nLageEbeneKugel - Verfahren\n")
        print("Lage einer Ebene bezüglich einer Kugel\n")
        print("Aufruf     LEK( ebene, kugel )\n")		                     
        print("                ebene   Ebene")		
        print("                kugel   Kugel\n")
        return		
		
    if len(args) != 2:
        print("agla: Ebene und Kugel angeben")
        return
				
    anf = '     '				
    ee, kk = args
    if not (isinstance(ee, Ebene) and isinstance(kk, Kugel)):
        if isinstance(ee, Kugel) and isinstance(kk, Ebene):
            ee, kk = kk, ee
        else:
            print("agla: Ebene und Kugel angeben")
            return
		
    if mit_param(ee) or mit_param(kk):		
        print("agla: nicht implementiert, Parameter")
        return
		
    print("\nLage einer Ebene bezüglich einer Kugel\n")
    print("Gegeben:")
    lat1 = 'E : \;'
    if ee._typ == 1:
        lat1 += pnf(ee, X)
    elif ee._typ == 2:
        lat1 += pprg(ee) 
    else:
        lat1 += pkoord(ee, X)	
    lat2 = 'k : \;' + pkugel(kk)
    dm('\quad \quad ' + lat1 + ', \quad \quad ' + lat2)
    print("Bestimmung der Schnittmenge der Ebene mit der Kugel:")
    print('\n' + anf + "Mittelpunkt und Radius der Kugel sind")
    dm('\quad \quad \; M' + kk.mitte.punkt_ausg_(s=1) + ', \quad r =' + latex(kk.radius.evalf()))	
    print(anf + "Der Abstand der Ebene vom Mittelpunkt der Kugel wird berechnet")
    dd = abs(ee.abstand(kk.mitte))
    if isinstance(dd, (int, Integer, float, Float)):	
        dm('\quad \quad \; d = d(E, M) =' + latex(dd))	
    else:		
        dm('\quad \quad \; d = d(E, M) =' + latex(dd) + '=' + latex(dd.evalf()))	
    if dd > kk.radius:	
        print(anf + "Es ist")
        dm('\quad \quad \; d > r')	
        print("Die Ebene schneidet die Kugel nicht\n")
    elif dd == kk.radius:	
        print(anf + "Es ist")
        dm('\quad \quad \; d = r')	
        print("\nDie Ebene berührt die Kugel in einem Punkt; der Berührpunkt (er wird als")
        print("Schnittpunkt der Ebene mit der zu ihr senkrechten Geraden durch M ermittelt)")
        print("ist")
        gg = Gerade(kk.mitte, ee.norm)
        B = gg.schnitt(ee)		
        dm('\quad \quad \;' + latex(B))	
    elif dd == 0:	
        print(anf + "Es ist")
        dm('\quad \quad \; d = 0')	
        print("Die Ebene schneidet die Kugel in einem Großkreis")
        print("\nTrägerebene des Kreises ist die gegebene Ebene, Mittelpunkt und")
        print("Radius sind die gleichen wie bei der Kugel\n")
    elif dd < kk.radius:	
        print(anf + "Es ist")
        dm('\quad \quad \; 0 < d < r')	
        print("Die Ebene schneidet die Kugel in einem Kleinkreis\n")
        gg = Gerade(kk.mitte, ee.norm)
        M1 = gg.schnitt(ee)	
        r1 = sqrt(kk.radius**2 - M1.abstand(kk.mitte)**2)		
        print("Trägerebene des Kreises ist die gegebene Ebene, sein Mittelpunkt ")
        print("der Durchstoßpunkt der zu ihr senkrechten Geraden durch M durch ")
        print("die Ebene und sein Radius (nach dem Satz des Pythagoras) sind")		
        dm('\quad \quad \;' + latex(M1) + ', \;\;' + latex(r1))
		
LEK = LageEbeneKugel
	
	
	
# -------------------------------	
# Funktionen zur pretty Ausgabe
# ------------------------------	
	
def dm(s):
   display(Math(s)) 	
	

# Ausgabe Punkt

def ppunkt(P):   
    return P.punkt_ausg_(s=1)	
	
	
# Ausgabe Geradengleichung

def pgerade (g):
    return latex(X) + latex('=') + latex(g.stuetz) + '+' + \
                                latex(g.par) + '\,' + latex(g.richt)	
	
	
# Ausgabe Koordinatengleichung Ebene   mit Einsetzen eines Punktes
	
def pkoord(e, p):	
    a, b, c, d = e.args[0:4]
    f = gcd(gcd(a, b), gcd(c, d))
    a, b, c, d = a/f, b/f, c/f, d/f        		  
    x, y, z = Symbol("x"), Symbol("y"), Symbol("z")
    gl = Gleichung(expand(simplify(a*x + b*y + c*z + d)))
    if p:
        return latex(gl.subs({x:p.x, y:p.y, z:p.z}))
    return latex(gl)		
	
	
# Ausgabe Normalenform Ebene   mit Einsetzen eines Punktes
	
def pnf(e, p):	
    lat = latex('\\left[') + latex(p) + '-'+ latex(e.stuetz) + \
          latex('\\right]') + latex('\circ') + latex(e.norm) + \
          latex('=') + latex(0) 
    return lat		  

	
# Ausgabe Hessesche Normalenform Ebene   mit Einsetzen eines Punktes
	
def phnf(e, p):	
    lat = latex('\\left[') + latex(p) + '-'+ latex(e.stuetz) + \
          latex('\\right]') + latex('\circ') + latex(1/e.norm.betrag) + \
          latex(e.norm) + latex('=') + latex(0) 
    return lat		  

def phnf_ohne0(e, p):	
    lat = latex('\\left[') + latex(p) + '-'+ latex(e.stuetz) + \
          latex('\\right]') + latex('\circ') + latex(1/e.norm.betrag) + \
          latex(e.norm) 
    return lat		  
	

# Ausgabe Parameterform Ebene
	
def pprg(e):	
    lat = latex(X)+ latex('=') + latex(e.stuetz) + '+' + \
          latex(e.par[0]) + '\,' + latex(e.richt[0]) + '+' + latex(e.par[1]) +\
			'\,' + latex(e.richt[1])	
    return lat 
	
	
# Ausgabe Skalarprodukt   x ° y
	
def pitem(x):
    if isinstance(x, (int, Integer)) and x >= 0:
        return latex(x)
    return '\\left(' + latex(x) + '\\right)'

def psp(x, y):         
    s = pitem(x.x)
    s += '\cdot' 
    s += pitem(y.x) 
    s += '+'
    s += pitem(x.y)
    s += '\cdot' 
    s += pitem(y.y)     
    s += '+' 
    s += pitem(x.z)
    s += '\cdot'
    s += pitem(y.z)    
    return s
	
	
# Ausgabe Skalarprodukt	  (x-y) ° z
	
def psp2(x, y, z):   
    s = '('
    s += str(x.x)
    s += '+' if y.x < 0 else '-'
    s += str(abs(y.x))
    s += ')'
    s += '\cdot'
    s += '(-' if z.x < 0 else ''
    s += str(abs(z.x))
    s += ')' if z.x < 0 else ''
    s += '+'
    s += '('
    s += str(x.y)
    s += '+' if y.y < 0 else '-'
    s += str(abs(y.y))
    s += ')'
    s += '\cdot'
    s += '(-' if z.y < 0 else ''
    s += str(abs(z.y))
    s += ')' if z.y < 0 else '' 
    s += '+'
    s += '('
    s += str(x.z)
    s += '+' if y.z < 0 else '-'
    s += str(abs(y.z))
    s += ')'
    s += '\cdot'
    s += '(-' if z.z < 0 else ''
    s += str(abs(z.z))
    s += ')' if z.z < 0 else ''
    return s	
	
	
def pkugel(k):
    gl = k.gleich
    return latex(gl.lhs) + '=' + latex(gl.rhs)	
	
	
	