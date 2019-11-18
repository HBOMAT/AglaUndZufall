#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  EreignisAlgebra - Klasse  von zufall           
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



from IPython.display import display, Math

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from sympy.abc import *    
from sympy.core.symbol import Symbol
from sympy import And
from sympy.printing.latex import latex

from zufall.lib.objekte.basis import ZufallsObjekt

from zufall.lib.objekte.ausnahmen import ZufallError
	
	
_alphabet = set([Symbol(x) for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'])
 
	
# EreignisAlgebra - Klasse  
# ------------------------
#
	
class EreignisAlgebra(ZufallsObjekt):                                      
    """
	
Ereignisalgebra

**Kurzname** **EA**
	
**Erzeugung** 
	
   EA( */[grundmenge]* )

**Parameter**

   *grundmenge* : Menge/Liste/Tupel (i.a. Ergbnismenge)
		
Wird kein Argument angegeben, wird eine Ereignisalgebra mit den 
englischen Großbuchstaben als Grundmenge erzeugt
		
    """
		
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            ereignis_algebra_hilfe(kwargs["h"])		
            return	
						
        try:						
            if args and len(args) > 1:
                raise ZufallError("ein Argument angeben")
            if not args:
                grundmenge = _alphabet
            else:				
                grundmenge = args[0]
                if not isinstance(grundmenge, (set, list, tuple)):
                    raise ZufallError("Grundmenge als Menge/Liste/Tupel angeben")
                grundmenge = set(grundmenge)			
                if not grundmenge:
                   raise ZufallError("die Grundmenge darf nicht leer sein") 
        except ZufallError as e:
            print('zufall:', str(e))
            return
			
        cls.OMEGA = grundmenge			
		
        return ZufallsObjekt.__new__(cls, grundmenge)

			
    def __str__(self):  
        a = self.args[0]
        return "EreignisAlgebra"	
		
		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def omega(self):
        """Grundmenge"""	
        return self.args[0]
		
		
    def berechnen(self, *args, **kwargs):
        """Berechnen von Ereignissen mittels Mengenalgebra"""	
        if kwargs.get('h'):
            print("\nBerechnen von Verknüpfungen von zwei Ereignissen\n")
            print("Aufruf   ea . berechnen( A, B, ausdruck )\n")		                     
            print("              A, B        Ereignisse (Teilmengen der Grundmenge von ea")
            print("                          als Liste/Tupel/Menge/Zeichenkette angegeben)")
            print("              ausdruck    zu berechnender Ausdruck in A, B; die Namen")
            print("                          sind zwingend\n")
            print("Der Ausdruck wird nach den Regeln für logische Ausdrücke gebildet, er ")
            print("ist immer als Zeichenkette einzugeben; als Operatoren werden verwendet\n")
            print("     nicht, und, oder \n")
            print("oder die entsprechenden englischen Wörter\n")
            print("     not, and, or\n")
            print("Als Operanden dienen die Bezeichner A und B; sie beziehen sich auf die ")
            print("ersten beiden Argumente (die eventuell andere Namen erhalten hatten)\n")
            print("Neben den damit erzeugbaren Ausdrücken sind folgende erlaubt, sie sind  ")
            print("exakt in der angeführten Form zu schreiben und können auch als Operanden ")
            print("in anderen Ausdrücken dienen, wobei sie hier in Klammern zu schreiben")
            print("sind\n")
            print("    gegen A                 gegen B          (für das Gegenereignis)")
            print("    sowohl A als auch B     sowohl B als auch A")
            print("    entweder A oder B       entweder B oder A")
            print("    weder A noch B          weder B noch A")
            print("    mindestens A oder B     mindestens B oder A")
            print("    höchstens A oder B     höchstens B oder A\n")
            print("Wird als Grundmenge das (große englische) Alphabet benutzt, müssen A ")
            print("und B als Wörter (Zeichenketten) oder Symbole angegeben werden\n")
            print("Zusatz   t=ja    Erläuterung mit Vier-Felder-Tafel")
            print("         v=ja    zusätzliche Erzeugung eines Venn-Diagramms")
            print("         vt=ja   alleinige Erzeugung der Vier-Felder-Tafel")
            print("         ve=ja   alleinige Erzeugung des Venn-Diagramms\n")
            print("Beispiele\n")
            print("ea = EA([1, 2, 3, 4, 5, 6])\n")
            print("ea.berechnen( [1, 2, 3], [2, 4, 6], 'A und B' )  ")
            print("ergibt als Ergebnis  { 2 }\n")
            print("ea.berechnen( [1, 2, 3], [2, 4, 6], 'nicht(weder A noch B)' )")
            print("ergibt als Ergebnis  { 1, 2, 3, 4, 6 } = A oder B \n")
            return			
		
        try:		
            if len(args) != 3:		 
                raise ZufallError("zwei Ereignisse und einen Ausdruck angeben')")
            A, B, ausdruck = args	
            if not isinstance(args[2], str):		 
                raise ZufallError("Ausdruck als Zeichenkette angeben")			
            if isinstance(A, str):
                A = list(set(A))			
                A.sort()
            if isinstance(B, str):
                A = list(set(A))			
                A.sort()
            omega = self.omega		
            if omega == _alphabet:
                AA = [Symbol(x) for x in  A]					
                BB = [Symbol(x) for x in  B]
                A, B = set(AA), set(BB)
            if all([isinstance(a, str) for a in A]):
                A = [Symbol(a) for a in A]			
            if all([isinstance(b, str) for b in B]):
                B = [Symbol(b) for b in B]			
            teil = lambda A, B: all([x in B for x in A])
            if not (teil(A, omega) and teil(B, omega)):
                raise ZufallError("die Ereignisse  müssen Teilmengen der Grundmenge sein")			
        except ZufallError as e:
            print('zufall:', str(e))
            return

        orig_ausdruck = ausdruck
        ausdruck = ausdruck.replace(' ', '')
		
        # Verarbeiten der zusätzlichen Operanden		
        if ausdruck.find('gegen') >= 0:
            ausdruck = ausdruck.replace('gegen', ' nicht ')		
        if ausdruck.find('minus') >= 0:
            ausdruck = ausdruck.replace('minus', ' und nicht ')		
        elif ausdruck.find('sowohl') >= 0:
            ausdruck = ausdruck.replace('sowohl', ' ')
            ausdruck = ausdruck.replace('alsauch', ' und ')	
        elif ausdruck.find('entweder') >= 0:
            if ausdruck.find(	'entwederAoderB') >= 0:	
                ausdruck = ausdruck.replace('entwederAoderB', ' (nicht A und B) oder (A und nicht B)')
            if ausdruck.find(	'entwederBoderA') >= 0:	
                ausdruck = ausdruck.replace('entwederBoderA', ' (nicht A und B) oder (A und nicht B)')
        elif ausdruck.find('weder') >= 0 and ausdruck.find('noch') >= 0:
            if ausdruck.find(	'wederAnochB') >= 0:			
                ausdruck = ausdruck.replace('wederAnochB', ' nicht A und nicht B ')
            if ausdruck.find(	'wederBnochA') >= 0:			
                ausdruck = ausdruck.replace('wederBnochA', ' nicht A und nicht B ')
        elif ausdruck.find('mindestens') >= 0:
            ausdruck = ausdruck.replace('mindestens', ' ')
        elif ausdruck.find('hoechstens') >= 0:
            if ausdruck.find(	'hoechstensAoderB') >= 0:			
                ausdruck = ausdruck.replace('hoechstensAoderB', ' nicht A oder nicht B ')
            if ausdruck.find(	'hoechstensBoderA') >= 0:			
                ausdruck = ausdruck.replace('hoechstensBoderA', ' nicht A oder nicht B ')
			
        ausdruck1 = ausdruck.replace('And', 'aaa')     		
        ausdruck1 = ausdruck1.replace('A', 'x').replace('B', 'y').replace('nicht', '~'). \
                          replace('und', '&').replace('oder', '|')
        ausdruck = ausdruck1.replace('aaa', 'And')     					  
        ausdruck = ausdruck.replace(' ', '')   
		
        ausdruck = ausdruck.replace('and', '&').replace('or', '|').replace('not', '~')  
		
        A, B = set(A), set(B)			
		
        # Anordnung der Felder für Markierungen in der Vier-Felder-Tafel:  
        #                                1  2   
        #                                3  4   
        # Markierungen im Venndiagramm:  'a'   A (ohne B)          = 3  (in der Tafel)
        #                                'b'   B (ohne A)          = 2
        #                                'ab'  A und B             = 1
        #                                'n'   nicht A und nicht B	 = 4	
        	
        x, y = Symbol('x'), Symbol('y')
        try:		
            vergl_ausdruck = eval(ausdruck)
        except NameError:
            print('zufall: bitte den Ausdruck überprüfen')
            return			
        		
        # Vergleichen des Ausdruckes mit allen Möglichkeiten für die Vier-Felder-Tafel				
        vergl = [1, 2, 3, 4, 12, 13, 14, 23, 24, 34, 123, 124, 134, 234, 1234]
        di = { '1':'x&y', '2':'~x&y', '3':'x&~y', '4':'~x&~y' }
        omega = self.omega		
        ende = False	
        for ver in vergl:
            ver = list(str(ver))
            aus = ''
            txt = ''			
            for i, v in enumerate(ver):
                aus += di[v]	
                txt += di[v].replace('x', 'A').replace('y', 'B').replace('~', 'nicht'). \
                                          replace('&', ' und ').replace('|', ' oder ') 
                if len(ver) > 1 and i < len(ver) - 1:
                    aus += '|'
                    txt += ' oder '                    				
				
            x, y = Symbol('x'), Symbol('y')	            			
            aus1 = eval(aus)						
            if wahr_tab(vergl_ausdruck) == wahr_tab(aus1):			
                mark = [int(x) for x in ver]
                aus = aus.strip().replace('x', 'A').replace('y', 'B')
                aus = aus.replace('~A', 'omega.difference(A)').replace('~B', 'omega.difference(B)')
                erg = eval(aus)				
                ende = True				
                break				
        if not ende:
            txt = 'unmögliches Ereignis'
            mark = []
            erg = set()			
			
        # Ausgabe der Informationen
		
        if not kwargs:			
            return erg

        elif kwargs.get('vt'):		
            vt_darstellung(mark)
            return			
		
        elif kwargs.get('ve'):
            venn_darstellung(mark)	
            return
			
        t, v = kwargs.get('t'), kwargs.get('v')			

        if t or v:			
            print("\nVerknüpfung von Ereignissen")
            vt_darstellung(mark)	
            print("Jedes Feld der Tafel beinhaltet das gemeinsame Eintreten der beiden be-")
            print("teiligten Ereignisse ('und' - Verknüpfung), das Zusammenfassen von zwei ")
            print("Feldern entspricht der 'oder' - Verknüpfung\n")
            print("Die berechnete Verknüpfung ist\n")
            orig = orig_ausdruck.strip()
            if orig == txt.strip():			
                print(orig + '\n')
            else:			
                print(orig + ' = ' + txt + '\n')
            display(Math('A = ' + latex(A)))		
            display(Math('B = ' + latex(B)))		
            display(Math('Ergebnis = ' + latex(erg)))		
            print(' ')			
			
            if v:			
                print("\nDarstellung als Venn-Diagramm:")
                venn_darstellung(mark)	
                print(' ')			
		

    def venn(self, *args, **kwargs):
        """Venn-Diagramm"""
        if kwargs.get('h'):
            print("\nVenn-Diagramm zur Darstellung der Verknüpfung von Ereignissen\n")
            print("Aufruf   ea . venn( A, B, ausdruck )\n")		                     
            print("              A, B       Ereignisse (Teilmengen der Grundmenge, als")
            print("                         Liste/Tupel/Menge/Zeichenkette angegeben)")
            print("              ausdruck   Ausdruck in A, B\n")
            print("Näheres siehe bei der Methode berechnen\n")
            return
        return self.berechnen(*args, ve=ja)
		
    def vt(self, *args, **kwargs):
        """Vier-Felder-Tafel-Diagramm"""	       
        if kwargs.get('h'):
            print("\nVier-Felder-Tafel-Diagramm zur Darstellung der Verknüpfung von Ereignissen\n")
            print("Aufruf   ea . vt( A, B, ausdruck )\n")		                     
            print("              A, B       Ereignisse (Teilmengen der Grundmenge, als")
            print("                         Liste/Tupel/Menge/Zeichenkette angegeben)")
            print("              ausdruck   Ausdruck in A, B\n")
            print("Näheres siehe bei der Methode berechnen\n")
            return
        return self.berechnen(*args, vt=ja)

    def einordnen(self, *args, **kwargs):
        """Einordnen in eine Vier-Felder-Tafel"""
		
        if kwargs.get('h'):
            print("\nEinordnen in eine Vier-Felder-Tafel\n")
            print("Aufruf   ea . einordnen( A, B )\n")		                     
            print("              A, B    Ereignisse (Teilmengen der Grundmenge, als")
            print("                      Liste/Tupel/Menge angegeben)")
            print("                      (Grundlage für die Vier-Felder-Tafel)\n")
            print("                      Wird als Grundmenge das (große englische) Alphabet")
            print("                      benutzt, müssen A und B als Wörter (Zeichenketten)")
            print("                      oder Symbole angegeben werden\n")
            print("Beispiele\n")
            print("ze = ZE({r:5, g:3, b:7}, 2)")
            print("ea = EA(ze.omega); A = ['bb', 'bg']; B = ['bb', 'bg', 'gg']")
            print("ea.einordnen( A, B )\n")			
            print("ea1 = EA(); ea1.einordnen( 'BERLIN', 'DRESDEN' )\n")
            return			
        if len(args) != 2:		 
            raise ZufallError("zwei Argumente angeben")
        AA, BB = args	
        typ = list, tuple, set, str		
        if not (isinstance(AA, typ) and isinstance(BB, typ)):
            print("zufall: als Argumente Listen, Tupel, Mengen oder Zeichenketten angeben")
            return
        if not (AA and BB):
            print("zufall: die Ereignisse dürfen nicht leer sein")
            return		
        omega = self.omega
        if omega == _alphabet:
            if not(isinstance(AA, str) and isinstance(BB, str)):		
                print("zufall: die Ereignisse müssen als Zeichenketten angegeben werden")
                return	
            AA, BB = [Symbol(x) for x in AA], [Symbol(x) for x in BB]
        AA, BB = list(AA), list(BB)			
        for i, e in enumerate(AA):
            if isinstance(e, str):
                AA[i] = Symbol(e)			
        for i, e in enumerate(BB):
            if isinstance(e, str):
                BB[i] = Symbol(e)			
        A, B = set(AA), set(BB)
        teil = lambda A, B: all([x in B for x in A])
        if not (teil(A, omega) and teil(B, omega)):
            print("zufall: die Ereignisse müssen Teilmengen der Grundmenge sein")			
            return
			
        def dm(x):
            return display(Math(x))

        print(' ')			
        print("Einordnen aller Elemente der Grundmenge in die auf den Ereignissen")
        print("A und B basierende Vier-Felder-Tafel")  
        print(' ')		
        print("Prinzip der Tafel:\n")  		
        print("Jedes Feld beinhaltet das gemeinsame Eintreten der beiden beteilig-")
        print("ten Ereignisse (und - Verknüpfung)")
		
        fig = plt.figure(figsize=(2.5, 1.8))
        ax = fig.add_subplot(1, 1, 1)

        for side in ['bottom', 'right', 'top', 'left']:
            ax.spines[side].set_visible(False)
        plt.axes().xaxis.set_ticks_position('none')
        plt.axes().yaxis.set_ticks_position('none')
        ax.set_xticks([])
        ax.set_yticks([])
     
        plt.xlim(0, 4.6)    
        plt.ylim(-0.2, 1.4)    

        f = (0.3, 0.3, 0.3)
        w = 0.8

        x0, x1, x2 = 1.5, 3., 4.5
        plt.plot([0.5, x2], [0.0, 0.0], color=f, lw=w)
        plt.plot([0.5, x2], [0.5, 0.5], color=f, lw=w)
        plt.plot([0.5, 4.5], [1.0, 1.0], color=f, lw=w)
        plt.plot([x2, x2], [0, 1.4], color=f, lw=w)
        plt.plot([x1, x1], [0, 1.4], color=f, lw=w)
        plt.plot([x0, x0], [0, 1.4], color=f, lw=w)

        ax.text(2.1, 1.2, '$A$', fontsize=11)
        ax.text(3.55, 1.2, '$\overline{A}$', fontsize=11)
        ax.text(0.8, 0.65, '$B$', fontsize=11)
        ax.text(0.81, 0.12, '$\overline{B}$', fontsize=11)

        ax.text(1.7, 0.65, '$A \, \\cap \, B$', fontsize=11)
        ax.text(1.7, 0.12, '$A \, \\cap \, \overline{B}$', fontsize=11)
        ax.text(3.2, 0.65, '$\overline{A} \, \\cap \, B$', fontsize=11)
        ax.text(3.2, 0.12, '$\overline{A} \, \\cap \, \overline{B}$', fontsize=11)

        plt.show()
		
        dm('A = ' + latex(A))		
        dm('B = ' + latex(B))
        dm('A \\cap B = ' + latex(A.intersection(B)))		
        dm('\\overline{A} \\cap B = ' + latex(omega.difference(A).intersection(B)))		
        dm('A \\cap \\overline{B} = ' + latex(A.intersection(omega.difference(B))))		
        dm('\\overline{A} \\cap \\overline{B} = ' + latex(omega.difference(A). \
                   intersection(omega.difference(B))))		
        print(' ')		
		
		
    def wort2menge(self, *args, **kwargs):
        """Wort -> Buchstabenmenge"""
        if kwargs.get('h'):
            print("\nMenge der Buchstaben eines Wortes\n")
            print("Aufruf   ea . wort2menge( wort )\n")		                     
            print("              wort    Wort - Zeichenkette (in ' ' bzw. \" \")")
            print("                      oder Symbol\n")
            print("Gebrauch bei einer Ereignisalgebra mit dem englischen")
            print("Alphabet als Grundmenge\n")			
            return			
        if len(args) != 1:
            print("zufall: ein Argument angeben")
            return
        wort = args[0]			
        if not isinstance(wort, (str, Symbol)):
            print("zufall: Wort als Zeichenkette oder Symbol angeben")
            return			
        if isinstance(wort, Symbol):
            wort = str(wort).upper()
        ll = []			
        for b in wort:
            bb = Symbol(b)		
            if bb not in _alphabet:
                print("zufall: das Wort darf nur englische Großbuchstaben enthalten")			
                return
            ll += [bb]	
        return set(ll)

    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        ereignis_algebra_hilfe(3)	
		
    h = hilfe					
		
		
				
# Benutzerhilfe für EreignisAlgebra
# ---------------------------------

def ereignis_algebra_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
EreignisAlgebra - Objekt

Kurzname     EA
		
Erzeugung    EreignisAlgebra( /[ grundmenge ] )

                 grundmenge    Menge/Liste/Tupel (i.a. Ergebnismenge)
				 
Wird kein Argument angegeben, wird eine Ereignisalgebra mit den 
englischen Großbuchstaben als Grundmenge erzeugt
		
Zuweisung     ea = EA(...)   (ea - freier Bezeichner)

Beispiele
EA( )     ( hat die Grundmenge {A, B, C,..., Z} )
EA( { 1, 2, 3, 4, 5, 6 } )
	   """)		
        return        
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für EreignisAlgebra
 
ea.hilfe              Bezeichner der Eigenschaften und Methoden
ea.berechnen(...)  M  Berechnen von Ereignissen	
ea.einordnen(...)  M  Einordnen in Vier-Felder-Tafel	
ea.omega              Grundmenge/Ergebnismenge	
ea.venn(...)       M  Venn-Diagramm - Darstellung	
ea.vt(...)         M  Vier-Felder-Tafel - Darstellung	
ea.wort2menge(...) M  Wort -> Menge seiner Buchstaben

Synonymer Bezeichner

hilfe    h
	   """)		
        return
	
EA = EreignisAlgebra

Ja = ja = mit = True
Nein = nein = ohne = False


		
# Darstellung einer Ereignis-Verknüpfung mit Vier-Felder-Tafel
		 
def vt_darstellung(mark):
    fig = plt.figure(figsize=(3*0.8, 2*0.8))
    ax = fig.add_subplot(111, aspect='equal')

    ax.axis('off')
     
    plt.xlim(0, 1.6)    
    plt.ylim(-0.01, 1.1)    

    f = (0.3, 0.3, 0.3)
    w = 0.8

    x0, x1, x2 = 0.6, 1.0, 1.4
    plt.plot([0.2, x2], [0.0, 0.0], color=f, lw=w)
    plt.plot([0.2, x2], [0.4, 0.4], color=f, lw=w)
    plt.plot([0.2, x2], [0.8, 0.8], color=f, lw=w)
    plt.plot([x2, x2], [0, 1.2], color=f, lw=w)
    plt.plot([x1, x1], [0, 1.2], color=f, lw=w)
    plt.plot([x0, x0], [0, 1.2], color=f, lw=w)
	
    ax.text(0.78, 0.93, '$A$', fontsize=11, horizontalalignment='center', \
                  verticalalignment='center')
    ax.text(1.18, 0.93, '$\\overline{A}$', fontsize=11, horizontalalignment='center', \
                  verticalalignment='center')
    ax.text(0.4, 0.58, '$B$', fontsize=11, horizontalalignment='center', \
                  verticalalignment='center')
    ax.text(0.4, 0.17, '$\\overline{B}$', fontsize=11, horizontalalignment='center', \
                  verticalalignment='center')

    for m in mark:
        if m == 1:
            re = patches.Rectangle((0.6, 0.4), 0.4, 0.4, color=(1.0, 0.6, 0.0))  	
        elif m == 2:
            re = patches.Rectangle((1.0, 0.4), 0.4, 0.4, color=(1.0, 0.6, 0.0))                         
        elif m == 3:
            re = patches.Rectangle((0.6, 0.0), 0.4, 0.4, color=(1.0, 0.6, 0.0))                                 
        else:		
            re = patches.Rectangle((1.0, 0.0), 0.4, 0.4, color=(1.0, 0.6, 0.0))                         
        plt.gca().add_patch(re)		

    plt.show()

	
	
# Darstellung einer Ereignis-Verknüpfung mit Venn-Diagramm

def venn_darstellung(mark):

    gl1 = 'np.sqrt(1.2**2 - (x-1.7)**2)+2.5'
    gl1m = '-np.sqrt(1.2**2 - (x-1.7)**2)+2.5'
    gl2 = 'np.sqrt(1.2**2 - (x-3.3)**2)+2.5'
    gl2m = '-np.sqrt(1.2**2 - (x-3.3)**2)+2.5'

    def fill(x0, x1, oben, unten):    
        if oben == 1:
            glo = gl1
        elif oben == -1:
            glo = gl1m
        elif oben == 2:
            glo = gl2
        elif oben == -2:
            glo = gl2m 
        else:
            glo = oben
        if unten == 1:
            glu = gl1
        elif unten == -1:
            glu = gl1m
        elif unten == 2:
            glu = gl2
        elif unten == -2:
            glu = gl2m
        else:
            glu = unten        
        x = np.arange(x0, x1, 0.01)
        yu, yo = eval(glu), eval(glo)    
        plt.fill_between(x, yu, yo, color=(1.0, 0.6, 0.0))
    			
    fig = plt.figure(figsize=(2.5*1.3, 1.5*1.3))
    fig.clf()

    plt.xlim(0, 5)
    plt.ylim(0, 5)
	
    ax = fig.add_subplot(1, 1, 1)
    kreis1 = patches.Circle((1.7, 2.5), 1.2, fill=None, 
                 edgecolor=(0,0,0), alpha=0.5)
    kreis2 = patches.Circle((3.3, 2.5), 1.2, fill=None, 
                 edgecolor=(0,0,0), alpha=0.5)
    plt.gca().add_patch(kreis1)
    plt.gca().add_patch(kreis2)
    	
    for m in mark:
        if m in ('a', 3):
            fill(0.5, 2.1, 1, -1)
            fill(2.1, 2.5, 2, 1)
            fill(2.1, 2.5, -2, -1)
        elif m in ('b', 2):
            fill(2.5, 2.9, 2, 1)
            fill(2.5, 2.9, -2, -1)
            fill(2.9, 4.5, 2, -2)
        elif m in ('ab', 1):
            fill(2.1, 2.5, 2, -2)
            fill(2.5, 2.9, 1, -1)
        else:		
            fill(0.0, 0.5, '5', '0')
            fill(0.5, 2.5, '5', 1)
            fill(0.5, 2.5, -1, '0')
            fill(2.5, 4.5, '5', 2)
            fill(2.5, 4.5, -2, '0')
            fill(4.49, 5.0, '5', '0')
	
    plt.axes().xaxis.set_ticks_position('none')
    plt.axes().yaxis.set_ticks_position('none')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(1, 2.8, '$A$', fontsize=11, alpha=0.8)
    ax.text(3.6, 2.8, '$B$', fontsize=11, alpha=0.8)
    ax.text(0.22, 4.3, '$\\Omega$', fontsize=11, alpha=0.8)
    [ax.spines[i].set_linewidth(0.5) for i in ('left', 'right', 'bottom', 'top')]	
    plt.show()
	

# Wahrheitstabelle eines logischen Ausdruckes

def wahr_tab(ausdruck):    # ausdruck - log. Ausduck in x, y
    x, y = Symbol('x'), Symbol('y')
    if isinstance(ausdruck, str):
        ausdruck = eval(ausdruck)	
    wert = [ ausdruck.replace(x, True).replace(y, True), 
            ausdruck.replace(x, True).replace(y, False), 
            ausdruck.replace(x, False).replace(y, True), 
            ausdruck.replace(x, False).replace(y, False) ]
    return wert			 
	
