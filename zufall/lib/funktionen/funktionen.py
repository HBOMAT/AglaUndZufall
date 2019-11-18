#!/usr/bin/python
# -*- coding utf-8 -*-

                           
						   
#                                                 
#  zufall - Funktionen                    
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



#
#  Inhalt:
#
#   abs, sqrt, ...      - Mathematische Funktionen
#   is_zahl             - Test auf Zahl
#   mit_param           - Test auf Parameter
#   permutationen, perm - Permutationen
#   kombinationen, komb - Kombinationen
#   variationen         - Variationen
#   zuf_zahl            - Erzeugung von Zufallszahlen
#   anzahl              - Anzahl des Vorkommens eines Elementes in 
#                         einer DatenReihe / Liste
#   anzahl_treffer      - Anzahl Treffer 
#   summe               - Summe der Elemente einer Liste / DatenReihe 
#   ja_nein             - Bewertung logischer Ausdrücke
#   auswahlen           - k-Auswahlen aus n Objekten
#   gesetze             - Einige Gesetze der Wahrscheinlichkeitsrechnung
#   stochastisch        - Test auf stochastischen Vektor / Matrix
#   löse                - Solver für Gleichungen / Ungleichungen
#   einfach             - Vereinfachung von Vektoren / Matrizen
#   ja, nein, ...       - Hilfsgrößen für True/False
#   Hilfe               - Hilfefunktion
	
	

import importlib

from itertools import (product, permutations, combinations, 
     combinations_with_replacement)
from Lib.random import randint, sample

from IPython.display import display, Math

from sympy import (Symbol, nsimplify, simplify, solve, radsimp, trigsimp, 
   signsimp)
from sympy.core.compatibility import iterable
from sympy import (Integer, Rational, Float, Add, Mul, Pow, Mod,  
    N, factorial, binomial as Binomial)
from sympy.core.numbers import Zero, One, NegativeOne, Half, E
from sympy.core.sympify  import sympify
from sympy.core.containers import Tuple
from sympy import (
    Abs, sqrt as Sqrt, exp as Exp, log as Log, 
    sin as Sin, cos as Cos, tan as Tan, cot as Cot,
	asin as Asin, acos as Acos, atan as Atan, acot as Acot,
	sinh as Sinh, cosh as Cosh, tanh as Tanh, 
	asinh as Asinh, acosh as Acosh, atanh as Atanh,
	re as Re, im as Im, conjugate as Conjugate)
from sympy.functions.elementary.miscellaneous import Max, Min
	 
from sympy.printing.latex import latex
from sympy.matrices import Matrix as SympyMatrix
from sympy import solveset, S, pi

from zufall.lib.objekte.basis import ZufallsObjekt
from zufall.lib.objekte.ausnahmen import ZufallError

import zufall

		
		
# ---------------------------
# Umrechnung Bogenmaß in Grad
# ---------------------------

def deg(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nUmrechnung Bogen- in Gradmaß - Funktion\n")
        print("Aufruf      deg( winkel )\n")
        print("                 winkel   Winkel in Bogenmaß\n")
        print("Synonymer Bezeichner   grad\n")	
        print("Rückgabe    Winkel in Grad\n")		
        print("Zusatz      d=n   Dezimaldarstellung")
        print("                  n - Anzahl der Nachkommastellen\n")
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben") 
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")
        return		
    wert = number * 180 / pi
    d = kwargs.get('d')
    if d:	
        return wert_ausgabe(wert, d)
    return wert
	
grad = deg	


# ---------------------------
# Umrechnung Grad in Bogenmaß
# ---------------------------

def rad(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nUmrechnung Grad- in Bogenmaß - Funktion\n")
        print("Aufruf      rad( winkel )\n")
        print("                 winkel   Winkel in Grad\n")
        print("Synonymer Bezeichner   bog\n")		
        print("Rückgabe    Winkel in Bogenmaß\n")		
        print("Zusatz      d=n   Dezimaldarstellung")
        print("                  n - Anzahl der Nachkommastellen\n")
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben") 
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl aus [-1, 1] angeben")
        return		
    wert = number / 180 * pi
    d = kwargs.get('d')
    if d:	
        return wert_ausgabe(wert, d)
    return nsimplify(wert, [pi])

bog = rad


# -----------------------------------
# Allgemeine mathematische Funktionen
# -----------------------------------

def abs(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nBetrags - Funktion\n")
        print("Aufruf      abs( x )\n")
        print("                x   Zahl\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben")                     
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = Abs(number)
    if kwargs.get("d"):
        return N(wert)
    return wert
	
def sqrt(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nWurzel - Funktion\n")
        print("Aufruf      sqrt( x )\n")
        print("                x   Zahl\n")
        print("Rückgabe einer reellen Zahl bei x > 0\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben")                     
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return	
    wert = Sqrt(number)
    if kwargs.get("d"):
        return N(wert)
    return wert

def exp(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nExponential - Funktion\n")
        print("Aufruf      exp( x )\n")
        print("                x   Zahl\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben")                     
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return	
    wert = Exp(number)
    if kwargs.get("d"):
        return N(wert)
    return wert
	
def log(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nNatürlicher Logarithmus - Funktion\n")
        print("Aufruf      ln( x )")
        print("oder       log( x )\n")
        print("                x   Zahl\n")
        print("Rückgabe einer reellen Zahl bei x > 0\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben")                     
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = Log(number)
    if kwargs.get("d"):
        return N(wert)
    return wert
	
ln = log

def lg(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nDekadischer Logarithmus - Funktion\n")
        print("Aufruf      lg( x )\n")
        print("                x   Zahl\n")
        print("Rückgabe einer reellen Zahl bei x > 0\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben")                     
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = Log(number, 10)
    if kwargs.get("d"):
        return N(wert)
    return wert

def max(*numbers, **kwargs):                                   
    if kwargs.get("h"):
        print("\nGrößte Zahl in einer Folge von Zahlen\n")
        print("Aufruf      max( x1, x2, ... )\n")
        print("                x   Zahl\n")
        return
    if isinstance(numbers[0], (list, tuple, Tuple, set, dict)):
        zahlen = [x for x in numbers[0]]
    else:
        zahlen = [x for x in numbers]                     
    if not all([is_zahl(x) for x in zahlen]):
        print("agla:  nur Zahlen angeben")          
        return		
    wert = Max(*zahlen)
    return wert
	
def min(*numbers, **kwargs):                                   
    if kwargs.get("h"):
        print("\nKleinste Zahl in einer Folge von Zahlen\n")
        print("Aufruf      min( x1, x2, ... )\n")
        print("                x   Zahl\n")
        return
    if isinstance(numbers[0], (list, tuple, Tuple, set, dict)):
        zahlen = [x for x in numbers[0]]
    else:
        zahlen = [x for x in numbers]                     
    if not all([is_zahl(x) for x in zahlen]):
        print("agla:  nur Zahlen angeben")          
        return		
    wert = Min(*zahlen)
    return wert

def re(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nRealteil einer komplexen Zahl\n")
        print("Aufruf      re( z )\n")
        print("                z   komplexe Zahl\n")
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben")                     
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine komplexe Zahl angeben")          
        return		
    wert = Re(number)
    return wert

def im(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nImaginärteil einer komplexen Zahl\n")
        print("Aufruf      im( z )\n")
        print("                z   komplexe Zahl\n")
        return
    if len(number) != 1:
        print("agla:  eine komplexe Zahl angeben")                     
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = Im(number)
    return wert
	
def conjugate(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nKonjugiert - komplexe Zahl\n")
        print("Aufruf      conjugate( z )")
        print("  oder      konjugirt( z )\n")
        print("                z   komplexe Zahl\n")
        return
    if len(number) != 1:
        print("agla:  eine komplexe Zahl angeben")                     
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = Conjugate(number)
    return wert
	
konjugiert = conjugate


# -------------------------------------------------
# Trigonometrische und Umkehr-Funktionen - Bogenmaß
# -------------------------------------------------

def sin(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nSinus - Funktion\n")
        print("Aufruf      sin( winkel )\n")
        print("                winkel   Winkel in Bogenmaß\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben")                     
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = Sin(number)
    if kwargs.get("d"):
        return N(wert)
    return wert	
	
def arcsin(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nArkussinus - Funktion\n")
        print("Aufruf      arcsin( x )")
        print("  oder        asin( x )\n")
        print("                x   Zahl\n")
        print("Rückgabe einer reellen Zahl bei x in [-1, 1]\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben")                     
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = Asin(number)
    if kwargs.get("d"):
        return N(wert)
    return wert	
	
asin = arcsin
	
def cos(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nKosinus - Funktion\n")
        print("Aufruf      cos( winkel )\n")
        print("                winkel   Winkel in Bogenmaß\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben")                     
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = Cos(number)
    if kwargs.get("d"):
        return N(wert)
    return wert	
	
def arccos(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nArkuskosinus - Funktion\n")
        print("Aufruf      arccos( x )")
        print("  oder        acos( x )\n")
        print("                x   Zahl\n")
        print("Rückgabe einer reellen Zahl bei x in [-1, 1]\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben")                     
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = Acos(number)
    if kwargs.get("d"):
        return N(wert)
    return wert	
		
acos = arccos
		
def tan(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nTangens - Funktion\n")
        print("Aufruf      tan( winkel )\n")
        print("                winkel   Winkel in Bogenmaß\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben")                     
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = Tan(number)
    if kwargs.get("d"):
        return N(wert)
    return wert	
	
def arctan(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nArkustangens - Funktion\n")
        print("Aufruf      arctan( x )")
        print("  oder        atan( x )\n")
        print("                x   Zahl\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben")                     
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = Atan(number)
    if kwargs.get("d"):
        return N(wert)
    return wert	
	
atan = arctan
	
def cot(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nKotangens - Funktion\n")
        print("Aufruf      cot( winkel )\n")
        print("                winkel   Winkel in Bogenmaß\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben")                     
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = Cot(number)
    if kwargs.get("d"):
        return N(wert)
    return wert	

def arccot(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nArkuskotangens - Funktion\n")
        print("Aufruf      arccot( x )")
        print("  oder        acot( x )\n")
        print("                x   Zahl\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben")                     
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = Acot(number)
    if kwargs.get("d"):
        return N(wert)
    return wert	
	
acot = arccot
	
# ------------------------------------------------
# Trigonometrische und Umkehr-Funktionen - Gradmaß
# ------------------------------------------------

def sing(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nSinus für Gradwerte - Funktion\n")
        print("Aufruf      sing( winkel )\n")
        print("                winkel   Winkel in Grad\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben")                     
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = sin(number * pi /180)
    if kwargs.get("d"):
        return N(wert)
    return wert	
	
def cosg(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nKosinus für Gradwerte - Funktion\n")
        print("Aufruf      cosg( winkel )\n")
        print("                winkel   Winkel in Grad\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben") 
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")
        return		
    wert = cos(number * pi /180)
    if kwargs.get("d"):
        return N(wert)
    return wert	

def tang(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nTangens für Gradwerte - Funktion\n")
        print("Aufruf      tang( winkel )\n")
        print("                winkel   Winkel in Grad\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben") 
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")
        return		
    wert = tan(number * pi /180)
    if kwargs.get("d"):
        return N(wert)
    return wert	

def cotg(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nKotangens für Gradwerte - Funktion\n")
        print("Aufruf      cotg( winkel )\n")
        print("                winkel   Winkel in Grad\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben") 
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")
        return		
    wert = 1 / tan(number * pi /180)
    if kwargs.get("d"):
        return N(wert)
    return wert	

	
def asing(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nArkussinus in Grad - Funktion\n")
        print("Aufruf      arcsing( x )")
        print("oder        asing( x )\n")
        print("                x   Zahl \n")
        print("Rückgabe einer reellen Zahl bei x in [-1, 1]\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    try:		
        if len(number) != 1:
            raise AglaError("eine Zahl angeben")      
        number = sympify(number[0])
        if not is_zahl(number):
            raise AglaError("eine Zahl angeben")      
    except AglaError as e:
        print('agla:', str(e))
        return	
    try:		
        number = nsimplify(number)
    except RecursionError:
        pass	
    wert = asin(number)*180/pi
    if kwargs.get("d"):
        return N(wert)
    return wert	

arcsing = asing	
	
def acosg(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nArkuskosinus in Grad - Funktion\n")
        print("Aufruf      arccosg( x )")
        print("oder        acosg( x )\n")
        print("                zahl   Zahl \n")
        print("Rückgabe einer reellen Zahl bei x in [-1, 1]\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    try:		
        if len(number) != 1:
            raise AglaError("eine Zahl angeben")      
        number = sympify(number[0])
        if not is_zahl(number):
            raise AglaError("eine Zahl angeben") 
        number = re(number)
    except AglaError as e:
        print('agla:', str(e))
        return			
    try:		
        number = nsimplify(number)
    except RecursionError:
        pass		
    wert = acos(number)*180/pi
    if kwargs.get("d"):
        return N(wert)
    return wert	

arccosg = acosg
	
def atang(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nArkustangens in Grad - Funktion\n")
        print("Aufruf      arctang( x )")
        print("oder        atang( x )\n")
        print("                x   Zahl\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben") 
        return		
    number = sympify(number[0])
    if not is_zahl(number):
        print("agla:  eine Zahl angeben") 
        return		
    number = nsimplify(number)
    try:		
        number = nsimplify(number)
    except RecursionError:
        pass		
    wert = atan(number) * 180 / pi
    if kwargs.get("d"):
        return N(wert)
    return wert	

arctang = atang

def acotg(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nArkuskotangens in Grad - Funktion\n")
        print("Aufruf      arccotg( x )")
        print("oder        acotg( x )\n")
        print("                x   Zahl\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben") 
        return		
    number = sympify(number[0])
    if not is_zahl(number):
        print("agla:  eine Zahl angeben") 
        return		
    number = nsimplify(number)
    try:		
        number = nsimplify(number)
    except RecursionError:
        pass		
    wert = acot(number) * 180 / pi
    if kwargs.get("d"):
        return N(wert)
    return wert	

arccotg = acotg


# -----------------------------------
# Hyperbolische und Umkehr-Funktionen 
# -----------------------------------

def sinh(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nSinus hyperbolikus - Funktion\n")
        print("Aufruf      sinh( x )\n")
        print("                x   Zahl\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben")                     
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = Sinh(number)
    if kwargs.get("d"):
        return N(wert)
    return wert	

def cosh(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nKosinus hyperbolikus - Funktion\n")
        print("Aufruf      cosh( x )\n")
        print("                x   Zahl\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben")                     
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = Cosh(number)
    if kwargs.get("d"):
        return N(wert)
    return wert	
	
def tanh(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nTangens hyperbolikus - Funktion\n")
        print("Aufruf      tanh( x )\n")
        print("                x   Zahl\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben")                     
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = Tanh(number)
    if kwargs.get("d"):
        return N(wert)
    return wert	

def asinh(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nAreasinus - Funktion\n")
        print("Aufruf      asinh( x )")
        print("  oder     arsinh( x )\n")
        print("                x   Zahl\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben")                     
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = Asinh(number)
    if kwargs.get("d"):
        return N(wert)
    return wert	

arsinh = asinh
	
def acosh(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nAreakosinus - Funktion\n")
        print("Aufruf      acosh( x )")
        print("  oder     arcosh( x )\n")
        print("                x   Zahl\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben")                     
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = Acosh(number)
    if kwargs.get("d"):
        return N(wert)
    return wert	
	
arcosh = acosh
	
def atanh(*number, **kwargs):                                   
    if kwargs.get("h"):
        print("\nAreatangens - Funktion\n")
        print("Aufruf     atanh( x )")
        print("  oder    artanh( x )\n")
        print("                x   Zahl\n")
        print("Zusatz      d=1   Dezimaldarstellung\n")     
        return
    if len(number) != 1:
        print("agla:  eine Zahl angeben")                     
        return		
    number = number[0]
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = Atanh(number)
    if kwargs.get("d"):
        return N(wert)
    return wert	

artanh = atanh

		
		
# Test auf eine zufall-zahl
# -------------------------
		
def is_zahl(x):	
    if isinstance(x, str):
        return False
    x = sympify(x)
    try:
        if x.is_number:
            return True
        elif x.is_Function:
            return True
    except AttributeError:
        pass
    zahlen = (Integer, int, Float, float, Symbol, One, Zero, NegativeOne, Half, 
             sin, cos, tan, sinh, cosh, tanh, asin, acos, atan, exp, log,
			   Mul, Add, Pow)
    return type(x) in zahlen 
	
isZahl = is_zahl	

		
# ------------------------
# Test auf freie Parameter
# ------------------------
		
def mit_param(obj):
    nv = importlib.import_module('zufall.lib.objekte.normal_verteilung')
    NormalVerteilung = nv.NormalVerteilung
    if iterable(obj):
        test = [mit_param(el) for el in obj]
        return any(test)
    obj = sympify(obj)
    if is_zahl(obj):
        try:
            return bool(obj.free_symbols)	
        except SyntaxError:
            return False
    elif isinstance(obj, NormalVerteilung):
        return mit_param(obj.mu) or mit_param(obj.sigma) 	
			
mitParam = mit_param
			
	
# --------------------------
# Ausgabe nummerischer Werte
# --------------------------

def wert_ausgabe(wert, d=None):   # interne Funktion
    if not isinstance(d, (Integer, int)):
        d = None
    else:
        if d <= 0:
            d = None  
    if not d:	
        if mit_param(wert):
            return N(wert)
        else:
            return eval(format(float(wert)))
    else:
        if mit_param(wert):
            return N(wert, d)
        else:
            return eval(format(float(wert), ".%df" %d ))
       
wertAusgabe = wert_ausgabe	   


# ---------
# Fakultaet
# ---------
		
def fakultaet(*args, **kwargs):
    """Fakultätsfunktion"""
	
    if kwargs.get('h'):
        print("\nfakultät - Fakultätsfunktion\n")	
        print("Kurzform    fak\n")		
        print("Aufruf      fak( n )\n")	
        print("                 n   ganze Zahl >= 0\n")
        return	

    if len(args) != 1:
        print('zufall: ein Argument angeben')
        return
    n = args[0]
    if mit_param(n):
        return	 factorial(n)	
    if not (isinstance(n, (int, Integer)) and n >= 0):	
        print ('zufall: ganze nichtnegative Zahl angeben')
        return		
    return factorial(n)

fak = fakultaet


# -------------------
# Binomialkoeffizient
# -------------------
		
def binomial(*args, **kwargs):
    """Binomialkoeffizient"""
	
    if kwargs.get('h'):
        print("\nbinomial - Binomialkoeffizient\n")	
        print("Kurzform    B\n")		
        print("Aufruf      B( n, k )\n")	
        print("               n, k   ganze Zahl >= 0\n")
        print("Achtung - der Bezeichner B kann überschrieben werden\n")
        return	
    if len(args) != 2:
        print('zufall: zwei Argumente angeben')
        return
    n, k = args
    if mit_param(n):
        if mit_param(k):
            return Binomial(n, k)
        else:
            if isinstance(k, (int, Integer)) and k >= 0:
                return Binomial(n, k)
            print('zufall: positive ganze Zahlen angeben')
            return				 
    else:
        if isinstance(n, (int, Integer)) and n >= 0:
            return Binomial(n, k)
        print('zufall: positive ganze Zahlen angeben')
        return				 
        			
B = binomial


# -------------
# Permutationen
# -------------
		
def permutationen(*args, **kwargs):
    """Permutationen einer Menge von Elementen"""
	
    if kwargs.get('h'):
        print("\nPermutationen der Elemente einer Menge\n")	
        print("Kurzform    perm\n")		
        print("Aufruf      perm( menge | n )\n")		                     
        print("                  menge    Liste/Tupel/Menge von Elementen | dictionary ")
        print("                           Elemente sind Zahlen, Symbole, Zeichenketten")
        print("                           ein dictionary enthält (element:anzahl)-Paare")
        print("                  n        bei Angabe einer ganzen Zahl >0 wird die Menge")
        print("                           {1, 2,...,n} verwendet\n")	
        print("Zusatz   k=ja    Ausgabe der Permutationen in Kurzform")			
        print("         l=ja    Ausgabe der Permutationen in Listenform")			
        print("         f=ja    Formeln\n")
        print("Beispiele")
        print("perm( [a, b, c, d], k=ja)")		
        print("perm( { 0:3, 1:2 }, l=ja)")		
        print("perm( 5)\n")		
        return	

    if kwargs.get('f'):
        i = Symbol('i')
        print(' ')		
        display(Math('Anzahl\; der\; Permutationen\; ohne\; Wiederholungen = n!'))	
        display(Math('Anzahl\; der\; Permutationen\; mit\; Wiederholungen = \\frac{n!}{n_1!\: n_2!\: ... \:n_p!}'))	
        display(Math('n - Anzahl\; der\; Elemente \; der\; Grundgesamtheit'))	
        display(Math('n_i - Anzahl\; des\; Auftretens \; des\;' + latex(i) + \
                   '.\; Elementes\; in\; der\; Grundgesamtheit, \\quad \\sum\limits_{i=1}^{p}n_i = n'))	
        print(' ')				   
        return
		
    if len(args) != 1:
        print('zufall: ein Argument angeben')
        return
    menge = args[0]			
    if not menge:
        return []		
    if not isinstance(menge, (list, tuple, set, dict, int, Integer)):	
        raise ZufallError('Liste/Tupel/Menge von Elementen oder ganze positive Zahl angeben')
    if isinstance(menge, (list, tuple, set)) and not all(map(lambda x: isinstance(x, \
        (int, Integer, Symbol, str)), menge)):
        raise ZufallError("Listenelemente können ganze Zahlen, Symbole oder Zeichenketten sein")			
    if isinstance(menge, dict):
        if not all(map(lambda x: isinstance(x, (int, Integer)) and x > 0, menge.values())):
            raise ZufallError("im dictionary als Werte Anzahlen angeben")
        m = []	
        for it in menge:
            m += [it for i in range(menge[it])]
        menge = m				
    if isinstance(menge, (int, Integer)):
        if menge <= 0:	
            raise ZufallError('ganze positive Zahl angeben')
        else:
            menge = range(1, menge+1)	
    menge = list(menge)
    menge.sort(key=str)
    di = {menge[0]:1}	
    wiederh = False		
    for it in menge[1:]:
        try:
            di[it] += 1
            wiederh = True				
        except KeyError:
            di[it] = 1
    kwl = kwargs.get('l')
    kwk = kwargs.get('k')
    if not(kwl or kwk):
        if not wiederh:
            return factorial(len(menge))          
        else:
            N = factorial(len(menge))
            for it in di:
                N = N / factorial(di[it])
            return nsimplify(N)
    if not wiederh:
        pp = list(permutations(menge))
    else:
        def pmw(iterable):     
            L = [iterable[0]]
            for i, it in enumerate(iterable):
                if i == 0 or it not in L:
                    L += [it]
                    yield it
        pp = list(pmw(list(permutations(menge))))
		
    if kwl:
        return pp
    elif kwk:
        return [kurz_form(x) for x in pp]
    	
perm = permutationen
		


# -------------
# Kombinationen
# -------------
		
def kombinationen(*args, **kwargs):
    """k-Kombinationen aus einer Menge von Elementen"""
	
    if kwargs.get('h'):
        print("\nKombinationen - k-Kombinationen aus einer Menge von n Objekten\n")	
        print("Kurzform    komb\n")		
        print("Aufruf      komb( menge, k, wiederh, anordn )\n")		                     
        print("                  menge    Liste/Tupel/Menge von Elementen | dictionary |")
        print("                           ganze positive Zahl") 		
        print("                           Listenelemente sind Zahlen, Symbole, strings,")
        print("                           aber keine Listen")
        print("                           ein dictionary enthält (Objekt:Anzahl)-Paare")
        print("                           bei Angabe einer Zahl n wird die Menge")
        print("                           {1,2,...,n} verwendet")	
        print("                  k        Anzahl Elemente einer Kombination")
        print("                  wiederh  Wiederholungen von Elementen in einer Kombina-") 
        print("                           tion möglich (ja/nein)")
        print("                  anordn   Beachtung der Anordnung/Reihenfolge der Elemen- ")
        print("                           te in einer Kombination (ja/nein)\n")
        print("Zusatz   k=ja     Ausgabe der Kombinationen in Kurzform")			
        print("         l=ja     Ausgabe der Kombinationen in Listenform")			
        print("         f=ja     Formeln")
        print("         b=ja     Begriffe\n")
        print("Beispiele")
        print("komb( [a, b, c, d], 2, ja, nein)")		
        print("komb( { 0:3, 1:2 }, 4, ja, ja, k=ja)")		
        print("komb( 5, 2, nein, nein)\n")		
        return	

    if kwargs.get('b'):
        print("\nMitunter werden Kombinationen mit Berücksichtigung der Anordnung Varia-")
        print("tionen genannt, die ohne Berücksichtigung der Anordnung heißen dann Kom-")
        print("binationen\n")
        return		

    try:
        if len(args) != 4:
            raise ZufallError('vier Argumente angeben')
        menge, k, wiederh, anordn = args		
        if not isinstance(menge, (list, tuple, set, dict, int, Integer)):	
            raise ZufallError('Liste/Tupel/Menge von Elementen oder ganze positive Zahl angeben')
        if isinstance(menge, (list, tuple, set)) and not all(map(lambda x: isinstance(x, \
            (int, Integer, Symbol, str)), menge)):
            raise ZufallError("Listenelemente können Zahlen, Symbole eoder Zeichenketten sein")			
        if isinstance(menge, dict):
            if not all(map(lambda x: isinstance(x, (int, Integer)) and x > 0, menge.values())):
                raise ZufallError("im dictionary als Werte Anzahlen angeben")
            m = []	
            for it in menge:
                m += [it for i in range(menge[it])]
            menge = m				
        if isinstance(menge, (int, Integer)):
            if menge <= 0:	
                raise ZufallError('ganze positive Zahl angeben')
            else:
                menge = range(1, menge+1)	
        if not isinstance(k, (int, Integer)) and k > 0:	
            raise ZufallError('für Anzahl Elemente ganze Zahl > 0 angeben')
        if not isinstance(wiederh, bool):	
            raise ZufallError('Zulassen Wiederholungen mit ja/mit oder nein/ohne angeben')
        if not isinstance(anordn, bool):	
            raise ZufallError('Beachten der Anordnung mit ja/mit oder nein/ohne angeben')		
    except ZufallError as e:
        print('zufall:', str(e))
        return
			
    if kwargs.get('f'):
        print(' ')	
        if wiederh and anordn:
            display(Math('Anzahl\; der\; Kombinationen\; mit\; Wiederholungen, \; mit\; Anordnung = n^k'))	
        elif wiederh and not anordn:
            display(Math('Anzahl\; der\; Kombinationen\; mit\; Wiederholungen, \; ohne\; Anordnung'))
            display(Math('\\qquad {n+k-1 \\choose k} = \\frac{(k+n-1)!}{k!\,(n-1)!}'))	
        elif not wiederh and anordn:
            display(Math('Anzahl\; der\; Kombinationen\; ohne\; Wiederholungen, \; mit\; Anordnung = ' + \
                       '\\frac{n!}{(n-k)! }'))	
        elif not wiederh and not anordn:
            display(Math('Anzahl\; der\; Kombinationen\; ohne\; Wiederholungen, \; ohne\; Anordnung'))
            display(Math('\\qquad {n \\choose k} = \\frac{n!}{k!\,(n-k)! }'))	
        display(Math('n - Anzahl\; der\; Elemente \; der\; Grundgesamtheit'))	
        display(Math('k - Anzahl\; der\; ausgewählten \; Elemente'))	
        print(' ')		
        return
		
    if not menge:
        return []		
 	
    menge = list(menge)	
    menge.sort(key=str)	
    if not anordn and not wiederh:
        kk = list(combinations(menge, k))
    elif not anordn and wiederh:
        kk = list(combinations_with_replacement(menge, k))
    elif anordn and not wiederh:
        kk = list(permutations(menge, k))	
    elif anordn and wiederh:
        kk = list(product(menge, repeat=k))	
	
    kwl = kwargs.get('l')
    kwk = kwargs.get('k')
    n = len(menge)	
    if not(kwl or kwk):
        if wiederh and anordn:
            return n**k          
        elif wiederh and not anordn:
            N = factorial(k+n-1) / (factorial(k) * factorial(n-1))
            return nsimplify(N)
        elif not wiederh and anordn:
            N = factorial(n) / factorial(n-k)         
            return nsimplify(N)		
        elif not wiederh and not anordn:
            N = factorial(n) / (factorial(k) * factorial(n-k))         
            return nsimplify(N)		
    if kwl:
        return kk
    elif kwk:
        return [kurz_form(x) for x in kk]

komb = kombinationen	



# -----------
# Variationen
# -----------
		
def variationen(*args, **kwargs):
    """k-Variationen aus einer Menge von Elementen"""
    
    if kwargs.get('h'):
        print("\nVariationen - k-Variationen aus einer Menge von n Objekten\n")	
        print("Aufruf      variationen( menge, k, wiederh )\n")		                     
        print("                  menge    Liste/Tupel/Menge von Elementen | dictionary |")
        print("                           ganze positive Zahl") 		
        print("                           Listenelemente sind Zahlen, Symbole, strings,") 
        print("                           aber keine Listen")
        print("                           ein dictionary enthält (Objekt:Anzahl)-Paare")
        print("                           bei Angabe einer Zahl n wird die Menge") 
        print("                           {1,2,...,n} verwendet")	
        print("                  k        Anzahl Elemente einer Variation")
        print("                  wiederh  Wiederholungen von Elementen in einer Variation") 
        print("                           möglich (ja/nein)\n")
        print("Zusatz   k=ja     Ausgabe der Variationen in Kurzform")			
        print("         l=ja     Ausgabe der Variationen in Listenform")			
        print("         f=ja     Formeln")
        print("         b=ja     Begriffe\n")
        print("Beispiele")
        print("variationen( [a, b, c, d], 2, ja)")		
        print("variationen( { 0:3, 1:2 }, 4, ja, k=ja)")		
        print("variationen( 5, 2, nein)\n")		
        return	

    if kwargs.get('b'):
        print("\nVariationen sind Kombinationen mit Berücksichtigung der Anordnung/Reihenfolge")
        print("der Elemente; wird der Begriff verwendet, heißen Kombinationen nur diejenigen ")
        print("ohne Berücksichtigung der Anordnung\n")
        return		

    try:
        if len(args) != 3:
            raise ZufallError('drei Argumente angeben')
        menge, k, wiederh = args		
        if not isinstance(menge, (list, tuple, set, dict, int, Integer)):	
            raise ZufallError('Liste/Tupel/Menge von Elementen oder ganze positive Zahl angeben')
        if isinstance(menge, (list, tuple, set)) and not all(map(lambda x: isinstance(x, \
            (int, Integer, Symbol, str)), menge)):
            raise ZufallError("Listenelemente können Zahlen, Symbole eoder Zeichenketten sein")			
        if isinstance(menge, dict):
            if not all(map(lambda x: isinstance(x, (int, Integer)) and x > 0, menge.values())):
                raise ZufallError("im dictionary als Werte Anzahlen angeben")
            m = []	
            for it in menge:
                m += [it for i in range(menge[it])]
            menge = m				
        if isinstance(menge, (int, Integer)):
            if menge <= 0:	
                raise ZufallError('ganze positive Zahl angeben')
            else:
                menge = range(1, menge+1)	
        if not isinstance(k, (int, Integer)) and k > 0:	
            raise ZufallError('für Anzahl Elemente ganze Zahl > 0 angeben')
        if not isinstance(wiederh, bool):	
            raise ZufallError('Zulassen Wiederholungen mit ja/mit oder nein/ohne angeben')
    except ZufallError as e:
        print('zufall:', str(e))
        return
			
    return kombinationen(menge, k, wiederh, True, **kwargs)			


	
# -------------
# Zufallszahlen
# -------------
		
def zuf_zahl(*args, **kwargs):
    """Erzeuung von Zufallszahlen"""
    
    if kwargs.get('h'):
        print("\nzuf_zahl - Erzeugung von ganzzahligen Pseudo-Zufallszahlen\n")	
        print("Aufruf      zuf_zahl( bereich1  /[, bereich2, ... ]  /[, anzahl ] )\n")	
        print("                 bereich   Bereichsangabe  z.B. (0, 9);  [1, 6]")
        print("                 anzahl    Anzahl der erzeugten Zahlen; Standard = 1\n")
        print("Zusatz      w=nein  keine Wiederholung von Zahlen; Standard=ja")
        print("            s=ja    sortierte Ausgabe mehrerer Zufallszahlen; ") 
        print("                    Standard=nein\n")
        print("Rückgabe    eine einzelne Zahl oder eine Liste mit anzahl Elementen")
        print("            ist die Anzahl der Bereiche > 1, so ist jedes Element ein")
        print("             Tupel, dessen i. Element aus dem i. Bereich ist\n")
        print("Beispiele   zuf_zahl( (0, 9) ) - eine Zufallsziffer 0, 1, ... oder 9")
        print("            zuf_zahl( (1, 365), 6, w=nein ) - 6 Tage eines Jahres, ohne") 
        print("                     Wiederh.")		
        print("            zuf_zahl( [0, 1], 3 ) - zur Simulation des 3-maligen Werfens") 
        print("                     einer Münze")		
        print("            zuf_zahl( [1, 6], [1, 6], 100 ) - zur Simulation des 100-ma-")
        print("                     ligen Werfens zweier Würfel\n")		
        return	
	
    if not args:
        print('zufall: Mindestens ein Argument angeben')
        return
    if not iterable(args[0]):
        print('zufall: Mindestens einen Bereich angeben')   
        return
    if iterable(args[-1]):
        anzahl = 1
        bereich = [*args]
    else:
        anzahl = args[-1]    
        bereich = [*args[:-1]]
    for ber in bereich:
        if not (iterable(ber) and len(ber) == 2):
            print('zufall: Bereiche der Länge 2 und eventuell Anzahl angeben')
            return
        if not (isinstance(ber[0], (int, Integer)) and isinstance(ber[1], (int, Integer))):
            print('zufall: die Bereichsgrenzen müssen ganzzahlig sein')
            return        
        if ber[0] >= ber[1]:
            print('zufall: es muss 1.Bereichsgrenze < 2.Bereichsgranze sein')
            return  
        w = kwargs.get('w')
        if w == None:
            w = True        
        s = kwargs.get('s')        
        if anzahl == 1:
            if len(bereich) == 1:
                return randint(*bereich[0])
            else:
                return [randint(*b) for b in bereich]
        else:
            if len(bereich) == 1:
                b = bereich[0]
                if w:
                    if not s:				
                        return [randint(*b) for i in range(anzahl)]
                    return sorted([randint(*b) for i in range(anzahl)])
                if anzahl > len(range(b[0], b[1]+1)):
                    print('zufall: es muss Anzahl <= Bereichsgröße sein')
                    return
                if not s:					
                    return sample(range(b[0], b[1]+1), anzahl)
                return sorted(sample(range(b[0], b[1]+1), anzahl))
            else:
                if w is None:
                    samp = [[randint(*b) for b in bereich] for i in range(anzahl)]
                    if s is None:				
                        return samp
                    return sorted(samp)						
                anz = 1					
                for b in bereich:
                    g = b[1] - b[0] + 1
                    anz *= g
                if anz < anzahl and not w:
                    print('zufall: die angegebene Anzahl ist größer als die Vorratsmenge')
                    return					
                samp, i = [], 0
                while i < anzahl:
                    sa = []
                    for b in bereich:
                        sa += [randint(*b)]
                    samp += [tuple(sa)]
                    i += 1
                if not s:					
                    return samp					
                return sorted(samp)					
	
zufZahl = zuf_zahl
	
	
# -------------------------------------
# Anzahl des Vorkommens eines Elementes 
# in einer DatenReihe / Liste
# -------------------------------------
    	
def anzahl(*args, **kwargs):
    """Anzahl von Elementen"""
	
    if kwargs.get('h'):	
        print("\nanzahl - Anzahl des Vorkommens eines Elementes in einer DatenReihe /") 
        print("         Liste\n")
        print("Aufruf      anzahl( daten /[, elem ] )\n")		                     
        print("                    daten    Liste von Elementen | DatenReihe")
        print("                    elem     Listen- / Datenelement") 	
        print("                             bei Fehlen wird die Anzahl der Elemente")
        print("                             von daten zurückgegeben")
        print("   oder     anzahl( elem )\n")
        print("                    es wird eine Funktion zurückgegeben, die die Anzahl")
        print("                    des Vorkommens des Elementes elem in einer Liste /") 
        print("                    DatenReihe zählt")
        print("                    bei deren Aufruf ist die Liste / DatenReihe  als")
        print("                    Argument anzugeben; ist elem selbst eine Liste, ist") 
        print("                    der Zusatz el=ja anzugeben\n")
        print("Beispiele")
        print("anzahl( [ 1, 0, 0, 1, 1, 1 ], 1 )   ergibt 4")
        print("anzahl( [ a, b, c ] )   ergibt 3")
        print("anzahl(sp, W) ergibt die Anzahl der W[appen] in der Stichprobe sp beim")
        print("              Münzwurf-ZufallsExperiment)")
        print("anzahl( el )  ergibt eine Funktion zum Zählen des Elements el")
        print("              anzahl(0)( [0,1,1,0,0] ) ergibt 3")
        print("              ist el eine Liste, wird der Zusatz el=ja angegeben")
        print("              anzahl([a, b], el=ja)( [[a, a], [a, b], [a, c], [a, b]]") 
        print("              ergibt 2\n")		
        return		

    dr = importlib.import_module('zufall.lib.objekte.datenreihe')
    DatenReihe = dr.DatenReihe
			
    if len(args) == 1:
        a = args[0]	
        if isinstance(a, list) and not kwargs.get('el'):		
            return len(a)
        elif isinstance(a, DatenReihe):			
            return a.n
        else:
            def fkt(*li):
                liste = li[0]					
                if not liste or not isinstance(liste, (list, DatenReihe, \
                       tuple, Tuple)):			
                    print('zufall: Liste oder DatenReihe angeben')
                    return
                if isinstance(liste, DatenReihe):	
                    liste = liste.daten				
                return len([x for x in liste if x == a])				
            return fkt		
    elif len(args) == 2:
        liste, elem = args
        if not isinstance(liste, (list, DatenReihe)):			
            print('zufall: als 1. Argument Liste oder DatenReihe angeben')
            return
        if isinstance(liste, DatenReihe):	
            liste = liste.daten				
        return len([x for x in liste if x == elem])				
    else:
        print('zufall: ein oder zwei Argumente angeben')
        return		



# --------------
# Anzahl Treffer 
# --------------
    	
def anzahl_treffer(*args, **kwargs):
    """Anzahl Treffer"""
	
    if kwargs.get('h'):	
        print("\nanzahl_treffer - Anzahl des Treffer\n")
        print("Aufruf      anzahl_treffer( treffer )\n")		                     
        print("                  treffer   Element, das als Treffer / Erfolg angesehen")
        print("                            wird (etwa Wappen oder W beim Münzwurf)\n")
        print("Die Funktion ist nur als ZG-Funktion beim Erzeugen von ZufallsGröße-Ob-")
        print("jekten verwendbar\n")
        return
    if len(args) != 1:
        print('zufall: ein Element als Treffer angeben')
        return		
    return anzahl(args[0])

anzahlTreffer = anzahl_treffer
	
	
# -----
# Summe 
# -----
    	
def summe(*args, **kwargs):
    """Summe der Elemente"""
	
    if kwargs.get('h'):	
        print("\nsumme - Summe der Elemente  einer Liste mit Daten / DatenReihe\n")
        print("Aufruf      summe( daten )\n")		                     
        print("                  daten    Liste mit Daten | DatenReihe\n")
        print("Synonyme    augen_summe, augenSumme\n")		
        print("Beispiel")
        print("summe( [ 1, 0, 0, 1, 1, 1 ] )   ergibt 4\n")
        return	
		
    dr = importlib.import_module('zufall.lib.objekte.datenreihe')
    DatenReihe = dr.DatenReihe
    if len(args) != 1 or not isinstance(args[0], (list, tuple, Tuple, DatenReihe)):	
        print('zufall: Liste oder Datenreihe angeben')
        return
    liste = args[0]		
    if isinstance(liste, DatenReihe):
        liste = liste.daten
    if not all([isinstance(x, (int, Integer, Rational, float, Float)) for x in liste]):
        print('zufall: in der Liste nur Zahlen angeben')
        return		
    return Add(*liste)		
	
augen_summe = summe    		
augenSumme = summe    		
	
	

# ------------------
# Allgemeiner solver                 		
# ------------------	

def loese(*args, **kwargs):
    if kwargs.get("h") == 1:
        print("\nlöse - Funktion\n")
        print("Zum Lösen von Gleichungen sowie von Ungleichungen\n")
        print("   Aufruf   löse( gleich /[, variable ] )\n")
        print("                  gleich    linke Seite einer Gleichung der Form")
        print("                            ausdruck = 0 oder Liste mit solchen")
        print("                            Elementen (Gleichungssystem)")
        print("                  variable  einzelne oder Liste von Variablen")                           
        print("                  ausdruck  Ausdruck in den Variablen\n")
        print("   oder     löse( ungleich /[, variable ] )\n")
        print("                  ungleich  Ungleichung der Form ausdruck rel ausdruck1")
        print("                  rel       Relation  '<' | '<=' | '>' | '>='\n")
        print("Zusatz   set=ja   Verwendung von solveset; standardmäßig wird solve ver-")
        print("                  wendet (siehe SymPy-Dokumentation)\n")		
        print("Beispiele")	
        print("löse( 3*x^2 + 5*x - 3 )          - einzelne Gleichung")
        print("löse( 3*x^2 + 5*x - 3, set=ja )")
        print("löse( (1-1/3)^n > 0.01, set=ja ) - Ungleichung")        		
        print("löse( [2*x-4*y-2, 3*x+5*y+1] )   - Gleichungssystem\n")
        return	
		
    ve = importlib.import_module('agla.lib.objekte.vektor')
    Vektor = ve.Vektor
	
    if len(args) == 1:
        gleich = args[0]
        var = []
    elif len(args) == 2:		
        gleich = sympify(args[0])
        var = args[1]
    else:
        print('zufall:  ein oder  zwei Argumente angeben')
        return		
    if not type(var) in (Symbol, list, tuple, Tuple):
        print('zufall:  einzelne Variable als Symbol, mehrere in einer' + 
                                         ' Liste angeben')
        return	
		
    se = kwargs.get('set')    		
    if is_zahl(gleich):
        if se:
            if not var:
                return solveset(gleich, domain=S.Reals)                				
            return solveset(gleich, var, domain=S.Reals)
        if not var:
            res = solve(gleich, dict=True, rational=True)
        else:
            res = solve(gleich, var, dict=True, rational=True)
        if isinstance(res, list) and len(res) == 1:
            return res[0]
        if not res:
            return set()
        return res			
    elif isinstance(gleich, _Gleichung):
        gleich = gleich.lhs - gleich.rhs
        if se:
            if not var:
                return solveset(gleich, domain=S.Reals)
            return solveset(gleich, var, domain=S.Reals)
        if not var:
            res = solve(gleich, dict=True, rational=True)
        else:
            res = solve(gleich, var, dict=True, rational=True)	
        if isinstance(res, list) and len(res) == 1:
            return res[0]
        if not res:
            return set()
        return res			
    elif isinstance(gleich, Vektor):
        gleich = [gleich.komp[i] for i in range(gleich.dim)]	
        if not var:			
            res = solve(gleich, dict=True, rational=True)
        else:
            res = solve(gleich, var, dict=True, rational=True)
        if isinstance(res, list) and len(res) == 1:
            return res[0]
        if not res:
            return set()
        return res			
    elif isinstance(gleich, (list, tuple, Tuple)):
        res = solve(gleich, rational=True)
        if not res:
            return set()
        return res			
    elif '<' in str(gleich) or '>' in str(gleich):
        if se:
            if not var:
                return solveset(gleich, domain=S.Reals)			
            return solveset(gleich, var, domain=S.Reals)
        if not var:
            res = solve(gleich)
        else:
            res = solve(gleich, var)
        if isinstance(res, list) and len(res) == 1:
            return res[0]
        if not res:
            return set()
        return res		
    else:
        print('zufall: linke Seite einer Gleichung oder einer ' +
             'Vektorgleichung oder Gleichungssystem angeben')
									  
									 
# -------------
# Vereinfachung	
# -------------	

from zufall.lib.objekte.umgebung import UMG 

def einfach(*x, **kwargs):	
    if kwargs.get('h') == 1:
        print("\neinfach - Funktion\n")
        print("Vereinfachung von Objekten\n")
        print("Aufruf      einfach( objekt )\n")
        print("                objekt   numm. Ausdruck, Vektor, Matrix\n")
        print("Zusatz   rad=ja    Einsatz von radsimp")
        print("         trig=ja   Einsatz von trigsimp")
        print("         num=ja    Einsatz von nsimplify")  
        print("         sign=ja   Einsatz von signsimp")  
        print("                   (siehe SymPy-Dokumentation)\n")		
        return
		
    Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
    if len(x) != 1:
        print('zufall:  ein Objekt angeben')
        return	
    x = x[0]		
    if not UMG.SIMPL:
        return x
    if not (is_zahl(x) or isinstance(x, (Vektor, SympyMatrix))):
        print('zufall:  nummerischen Wert, Vektor oder Matrix angeben')
        return		
    if isinstance(x, Vektor):
        li = [einfach(k, **kwargs) for k in x.komp]
        return Vektor(li)
    if isinstance(x, SympyMatrix):
        Matrix = importlib.import_module('zufall.lib.objekte.matrix').Matrix		
        return Matrix(*[einfach(v, **kwargs) for v in x.vekt])
    elif is_zahl(x):
        if not kwargs:
            return simplify(x)	
        elif kwargs.get('rad'):
            return radsimp(x)
        elif kwargs.get('trig'):
            return trigsimp(x)
        elif kwargs.get('num'):
            try:	
                return nsimplify(x)
            except RecursionError:
                return x		
        elif kwargs.get('sign'):
            return signsimp(x)
        else:
            return x		
  					 
  													  
# --------------------------
# k-Auswahlen aus n Objekten
# --------------------------

def auswahlen(**kwargs):
    """k-Auswahlen aus n Objekten; Übericht"""

    if kwargs.get('h'):		
        print("\nk-Auswahlen aus n Objekten (Übersicht)\n")	
        print("Aufruf     auswahlen( )\n")
        print("Zusatz  a=ja  Algorithmus als Pseudocode\n")	
        return

    if not kwargs.get('a'):

        dm = lambda x: display(Math(x))		

        print(' ')		
        dm('\\text{Tabelle der $k$-Auswahlen aus $n$ Objekten}')
        print(' ')		
        dm('\\text{Bezeichnung $\\qquad\qquad\\quad$ Eigenschaften \
            $\\qquad\\quad$ Formel $\\qquad\\quad$ Beispiel}')
        dm('\\text{$k$-Kombination oW mA } \\quad\:\, k \\lt n \\qquad\\quad \
		    \\qquad\quad\; \\dfrac{n!}{(n-k)!} \\qquad\\quad\, \\text{Pakplatzbelegung}')
        dm('\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad \
     		\\qquad\\qquad\;\, \\text{15 Autos, 6 Plätze}')
        dm('\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad \
     		\\qquad\\qquad\; \, \\Rightarrow n=15, k=6')			
        dm('\\text{$k$-Kombination  mW mA} \\quad\:\,  k, n \; \\text{beliebig} \\qquad\\quad \
		    \,\quad n^k \\qquad\\qquad\\quad\, \\text{Fußballtoto}')
        dm('\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad \
     		\\qquad\\qquad\; \, \\Rightarrow n=3, k=11')
        dm('\\text{$k$-Permutation  oW } \\qquad\\quad\:\, \\text{mA; jedes Element} \\quad\:\;\, \
             n! \\qquad\\qquad\\quad\, \\text{Startaufstellung}')	
        dm('\\qquad\\qquad\\qquad\\qquad\\qquad\\text{wird benutzt} \
     		\\qquad\\qquad\\qquad\\qquad\\quad\:\;\; \, \\text{8 Läufer auf 8 Bahnen}')
        dm('\\qquad\\qquad\\qquad\\qquad\\qquad\, k=n \\qquad\\qquad \
     		\\qquad\\qquad\\qquad\\quad\:\:\:\; \, \\Rightarrow n=k=8')			
        dm('\\text{$k$-Permutation  mW } \\qquad\\quad\:\, \\text{mA; jedes Element} \\quad\:\;\, \
             \\dfrac{n!}{n_1!\cdot \dots \cdot n_p}\\quad\, \\text{Anagramm}')	
        dm('\\qquad\\qquad\\qquad\\qquad\\qquad\\text{wird benutzt} \
     		\\qquad\\qquad\\qquad\\qquad\\quad\:\;\; \, \\text{RENNEN}')
        dm('\\qquad\\qquad\\qquad\\qquad\\qquad\, k>n \\qquad\\qquad \
     		\\qquad\\qquad\\qquad\\quad\:\:\:\; \, \\Rightarrow p=3,n=6')
        dm('\\text{$k$-Kombination oW oA } \\quad\:\,\:\; k \\lt n \\qquad\\quad \
		    \\qquad\quad\;\; \\dfrac{n!}{(n-k)! \cdot k!} \\quad\, \\text{Zahlenlotto}')
        dm('\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad \
     		\\qquad\\qquad\;\, \\text{6 aus 49}')
        dm('\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad \
     		\\qquad\\qquad\; \, \\Rightarrow n=49, k=6')			
        dm('\\text{$k$-Kombination mW oA } \\quad\:\,\: k, n \\text{beliebig} \\qquad\\quad \
		    \\quad \;\; {n+k-1 \choose k} \\quad \\text{Flaschenträger}')
        dm('\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad \
     		\\qquad\\qquad\;\, \\text{12 Flaschen aus 3 Sorten}')
        dm('\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad \
     		\\qquad\\qquad\; \, \\Rightarrow n=3, k=12')			
        print(' ')		
        dm('\\text{(mW/oW - mit/ohne Wiederholung,   mA/oA - mit/ohne Anordnung)}')
        print(' ')
        dm('\\text{Oft werden Kombinationen mit Berücksichtigung der Anordnung Variationen genannt}')		
        dm('\\text{die ohne Berücksichtigung der Anordnung heißen dann Kombinationen}')
        print(' ')		
        return

    # Algorithmus		
    print(""" \
 
Algorithmus zur Berechnug der k-Auswahlen aus n Objekten (Python-ähn- 
licher Pseudocode)

Analyse der Aufgabenstellung
WENN die Elemente 'angeordnet' sind:
    WENN einzelne Elemente wiederholt werden dürfen:
        WENN jedes Element mindestens einmal benutzt wird:
            Permutation mW  mit n > p
                / Aus n > p ergibt sich die Zuordnung von p und n:
                / Die Länge n der Anordnung ist größer als die Größe p 
                / der Vorratsmenge ]
        SONST:
            Kombination mW mA
                / Zuordnung von k und n:
                / Das, was 'wiederholt' werden kann, gehört zur Vorrats-
                / menge 
    SONST:
        WENN jedes Element genau einmal benutzt wird:
            WENN k = n ist:
                Permutation oW
            SONST:
                ES WURDE ETWAS ÜBERSEHEN
                neu beginnen
        SONST:  
            Kombination oW mA  mit k < n
                / Aus k < n ergibt sich die Zuordnung von n und k:
                / Die Länge k der Anordnung ist kleiner als die Größe n 
                / der Vorratsmenge 
SONST:
    WENN Elemente wiederholt werden dürfen:
        Kombination mW oA
            / Zuordnung von n und k:
            / Das, was 'wiederholt' werden kann, gehört zur Vorratsmenge         
    SONST:
        Kombination oW oA  mit k < n
            / Aus k < n ergibt sich die Zuordnung von n und k:
            / Die Größe  k der Teilmenge ist kleiner als die Größe n 
            / der Vorratsmenge 

			  
Oft werden Kombinationen mit Berücksichtigung der Anordnung Variationen 
genannt, die ohne Berücksichtigung der Anordnung heißen dann Kombinationen

Grundlage:
Wolfdieter Feix
mentor Abiturhilfe
Mathematik Oberstufe
Stochastik
mentor Verlag 2000
""")		
    return



# ---------------------------------------
# Gesetze der Wahrscheinlichkeitsrechnung
# ---------------------------------------

def gesetze(**kwargs):
    """Gesetze der Wahrscheinlichkeitsrechnung"""

    if kwargs.get('h'):		
        print("\nEinige Gesetze der Wahrscheinlichkeitsrechnung\n")	
        print("Aufruf     gesetze( )\n")
        return

    dm = lambda x: display(Math(x)) 	
	
    print(' ')	
    dm('\\text{Einige Gesetze der Wahrscheinlichkeitsrechnung}')
    print(' ')	
    dm('\\text{Additionssatz}')
    dm('\\qquad\\text{Für beliebige Ereignisse} \; A \\text{ und } B \\text{ gilt } P( \\cup B) = \
       P(A)+P(B)-P(A \\cap B)')	
	
    dm('\\text{Satz von Bayes}')
    dm('\\qquad\\text{Sei } A \\text{ ein Ereignis und } B \\text{ eine Bedingung, \
        unter der das Ereignis betrachtet}')
    dm('\qquad\\text{wird. Dann berechnet sich die Wahrscheinlichkeit } P_B(A) \
       \\text{ für } A \\text{ unter der Be-}')
    dm('\\qquad \\text{dingung } B \\text{nach der Formel }\;  P_B(A) = \\dfrac{P(A \\cap B)}{P(B)}')	
	   
    dm('\\text{Multiplikationssatz}')
    dm('\\qquad\\text{Ist } P(A) \\neq 0 \\text{, so gilt } P(A \\cap B) = P(A) \cdot \
       P_A(B)')	
	   
    dm('\\text{Satz von der totalen Wahrscheinlichkeit}')
    dm('\\qquad\\text{Für beliebige Ereignisse }A \\text{ und }B \\text{ gilt }  P(B) = \
        P(A \\cap B) + P(\\overline{A} \\cap B) = ')
    dm('\\qquad P(A) \\cdot P_A(B) + P(\\overline{A}) \\cdot P_\\overline{A}(B)') 		
    dm('\\qquad\\text{oder allgemeiner}')	
    dm('\\qquad\\text{Wenn } A_1 \\cup A_2 \\cup \\dots \\cup A_n = \\Omega, \; A_i\\cap A_j = \
        \\emptyset \\text{ für } i,j=1\dots n, i \\neq j \\text{ gilt, dann ist}')
    dm('\\qquad P(B) = \\sum_{i=1}^n P(A_i)\\cdot P_{A_i}(B)') 		
    dm('\\text{Empirisches Gesetz der großen Zahlen}')
    dm('\\qquad\\text{Bei langen Versuchsreihen, also bei häufiger Wiederholung eines Zufallsex-}')
    dm('\\qquad\\text{perimentes verändern sich die relativen Häufigkeiten eines Ergebnisses in }')
    dm('\\qquad\\text{der Regel nur noch wenig. Sie stabilisieren sich in der Nähe der Wahrschein-}')
    dm('\\qquad\\text{lichkeit des Ergebnisses.}')
    dm('\\text{Bernoullisches Gesetz der großen Zahlen}')
    dm('\\qquad\\text{Gegeben sei ein } n \\text{-stufiges Bernoulli-Experiment mit der Trefferwahrschein-}')
    dm('\\qquad\\text{lichkeit }p. X  \\text{ sei die Zufallsgröße \'Anzahl der Treffer\'. Für jedes beliebige}') 
    dm('\\qquad\\text{positive } \\epsilon \\text{ gilt dann }\\lim\\limits_{n \\rightarrow \\infty} P \left( \
       \left| \\frac{X}{n} - p \\right| \\le \
       \\epsilon \\right)  = 1')
    dm('\\text{Tschebyschew - Ungleichung}')
    dm('\\qquad\\text{Sei } X \\text{ eine beliebige Zufallsgröße mit Erwartungswert } \\mu \\text{ und Standardabwei-}')
    dm('\\qquad\\text{chung }\\sigma. \\text{ Für die Wahrscheinlichkeit, dass } X \\text{ einen Wert annimmt, der um}') 
    dm('\\qquad\\text{mindestens } c\; (c \\gt 0) \\text{ vom Erwartungswert abweicht, gilt}')
    dm('\\qquad P\\left(\\left|X - \\mu\\right| \\ge c \\right) \\le \\dfrac{\\sigma^2}{c^2}. \
	   \\qquad \\text{Daraus folgt}')	
    dm('\\qquad P(\\mu - \\sigma\cdot c \\le X \\le \\mu + \\sigma\\cdot c ) \\ge 1 -\\dfrac{1}{c^2}')	
    dm('\\dfrac{1}{\\sqrt{n}} \\text{ - Gesetz}')
    dm('\\qquad X_1, X_2, \\dots , X_n \\text{ seien identisch verteilte unabhängige Zufallsgrößen mit dem }')	
    dm('\\qquad\\text{Erwartungswert } \\mu \\text{ und der Standardabweichung } \\sigma. \\text{ Für die Zufallsgröße }')
    dm('\\qquad\\overline{X} = \\dfrac{1}{n} \, (X_1 + X_2 + \\dots + X_n) \ \\text{ gilt dann:} ')
    dm('\\qquad\\text{Sie hat den Erwartungswert } \\mu \\text{ und die Standardabweichung } \
        \\dfrac{\\sigma}{\\sqrt{n}}')	
    dm('\\text{Zentraler Grenzwertsatz}')		
    dm('\\qquad X_1, X_2, \\dots , X_n \\text{ seien unabhängige Zufallsgrößen. Die Zufallsgröße } \
        \;X = X_1+')
    dm('\\qquad \\dots + X_n \\text{ habe den Erwartungswert } \\mu \\text{ und die Standardabweichung } \\sigma. \
       \\text{Dann}')
    dm('\\qquad\\text{gilt unter gewissen Bedingungen, die fast immer erfüllt sind (insbesondere}') 
    dm('\\qquad\\text{für großes } n \\text{): }')
    dm('\\qquad\\text{Die Zufallsgröße $X$ ist näherungsweise nomalverteilt mit } \\mu \\text{ und } \\sigma')
    print(' ')

	
# ------------------
# ja-nein - Funktion
# ------------------
		
def ja_nein(*args, **kwargs):
    """Bewertung eines logischen Ausdruckes"""
	
    if kwargs.get('h'):
        print("\nja_nein - Bewertung eines logischen Ausdruckes\n")	
        print("Aufruf     ja_nein( ausdruck )\n")		                     
        print("                    ausdruck  Ausdruck mit dem Wert True oder False\n")
        print("Rückgabe   1, wenn ausdruck==True")			
        print("           0, wenn ausdruck==False\n")		
        return
		
    if len(args) != 1:
        print('zufall: ein Argument angeben')	
        return
    ausdruck = args[0]		
    if not isinstance(bool(ausdruck), bool):
        print('zufall: der Ausdruck hat nicht den Wert True oder False')
        return		
    if ausdruck:
        return 1
    return 0		
	
jaNein = ja_nein
	
	
# --------------------------------------------------------
# stochastisch - Test auf stochastische(n) Vektor / Matrix
# --------------------------------------------------------
	
def stochastisch(*args, **kwargs):
    """Test auf stochastischen Vektor / Matrix"""
	
    if kwargs.get('h'):
        print("\nstochastisch - Test auf stochastische(n) Vektor / Matrix\n")	
        print("Aufruf     stochastisch( objekt )\n")		                     
        print("                 objekt   Vektor, Matrix\n")
        print("Ein Vektor ist stochastisch, wenn alle Komponenten in [0, 1] liegen")		
        print("und ihre Summe 1 ist\n")
        print("Eine quadratische Matrix ist stochastisch, wenn alle Spaltenvektoren") 
        print("stochastisch sind\n")		
        return

    if len(args) != 1:
        print('zufall: Vektor oder Matrix angeben')
        return		
    obj = args[0]	
    ve = importlib.import_module('agla.lib.objekte.vektor')
    Vektor = ve.Vektor
    if not isinstance(obj, (Vektor, SympyMatrix)):
        print('zufall: Vektor oder Matrix angeben')
        return		
    if isinstance(obj, Vektor):
        if not all(k >= 0 for k in obj.komp):
            return False
        s = 0
        for k in obj.komp:
            s += k	
        if s != 1:
            return False
        return True			
    else:	
        if obj.shape[0] != obj.shape[1]:
            return False		
        for i in range(obj.shape[0]):
            col =  Vektor(*[obj[j, i] for j in range(obj.shape[1])])
            if not stochastisch(col):
                return False
        return True    	
	
	
	
# ------------------
# Kurzform für Tupel
# ------------------

def kurz_form(iterable):
    menge = list(iterable)
    symbole = all(map(lambda x: isinstance(x, Symbol), menge))
    ziffern = all(map(lambda x: isinstance(x, (int, Integer)), menge))	
    if symbole or ziffern:
        kf = ''
        for el in menge:
            kf += str(el)
        return Symbol(kf)	
    return None    				
	
	
# ------------------------------------------
# Erzeugen der Baumstruktur einer Tupelmenge
# ------------------------------------------	
	
def tupel2baum(liste):
	
    def kopf(liste):
        if not isinstance(liste, list):
            return liste
        elif len(liste) == 0:
            return None
        return liste[0]  
			
    def rest(liste):
        if not isinstance(liste, list):
            return []
        elif len(liste) == 1:
            return []
        return liste[1:]      
    	
    def ibaum(liste):
        rliste = []
        if liste:
            rliste = ['o']
            #li = map(lambda x: not isinstance(x, list), liste)
            li = [not isinstance(x, list) for x in liste]
            if all(li):
                rliste += [[x] for x in liste]
            else:                
                nam = set([kopf(x) for x in liste if kopf(x) is not None])
                nam = list(nam)
                nam.sort(key=str)				
                for nm in nam:
                    nm_liste = [ nm ]
                    nm_rest_liste = [x for x in liste if kopf(x) == nm]
                    nm_rest_liste = [rest(x) for x in nm_rest_liste]
                    nm_rest_baum = ibaum(nm_rest_liste)
                    nm_liste += rest(nm_rest_baum) 
                    rliste += [nm_liste]
        return rliste

    return ibaum(liste)		
			
			
			
# --------------
# Hilfe-Funktion
# --------------

def Hilfe(**kwargs):
    h = kwargs.get('h')
    if not h:
        h = 1	
    if h == 1:
        print("h=2  - Einleitung")
        print("h=3  - Online-Hilfeinformationen")
        print("h=4  - Bezeichner")
        print("h=5  - Zugriff auf Eigenschaften und Methoden")
        print("h=6  - Klassen")		
        print("h=7  - Funktionen")
        print("h=8  - Operatoren")		
        print("h=9  - Jupyter-Notebook")
        print("h=10 - Nutzung von SymPy-Anweisungen")		
        print("h=11 - Griechische Buchstaben")		
        print("h=12 - Kleiner Python-Exkurs")		
        print("h=13 - Bemerkungen für Programmierer/Entwickler")		
        return
		
    if h == 2:
        print(
        """		
Einleitung

Python ist ein leistungsfähiger konventioneller Taschenrechner. Durch das CAS
SymPy werden seine Fähigkeiten vor allem um das symbolische Rechnen erwei-
tert. Mit dem Paket zufall sollen Berechnungen auf dem Gebiet der Stochastik 
unterstützt werden, wobei es für den Gebrauch in der Schule vorgesehen ist
	
zufall ist ein Python-Paket und kann innerhalb von Jupyter-Notebooks benutzt 
werden

In zufall werden die Objekte der Stochastik, wie Zufallsexperiment, Bernoul-,
likette, Urne, Binomialverteilung usw. mit entsprechenden Python-Klassen dar-
gestellt. Über eine Konstruktor-/Erzeugerfunktion gleichen Namens können In-  
stanzen dieser Klassen (Objekte), erzeugt werden. Mit diesen und ihren Eigen-
schaften + Methoden wird  dann interaktiv gearbeitet. Weiterhin unterstützen 
einige Funktionen die Arbeit
		
Das Paket basiert auf dem vollständig in Python geschriebenen CAS SymPy und 
ist selbst ebenfalls (mit leichten Modifizierungen) in reinem Python ge- 
schrieben. Für Grafiken wird das matplotlib-Paket benutzt
		
Die Programme von zufall werden im Quellcode für die Benutzung bereitgestellt\n 
Die Syntax zur Handhabung von zufall ist so gestaltet, dass sie leicht er-  
lernbar ist. Es sind nur geringe Python-Kenntnisse sowie Fähigkeiten zum  
Bedienen eines Jupyter-Notebooks notwendig
 
Bei der Arbeit mit zufall kann auf den gesamten Leistungsumfang von Python 	
zugegriffen werden, der vor allem duch eine Vielzahl weiterer Pakete reali-
siert wird		
        """)		
        return		
		
    if h == 3:		
        print(
        """		
Erhalten von Hilfe-Informationen

Unter dem Namen Hilfe steht eine Funktion zur Verfügung, über die zentrale
Hilfeinformationen erhalten werden können. Mit der Eingabe

   In [..]: Hilfe()  oder  Hilfe(h=1)
   
in eine Zelle des Notebooks wird man auf einzelne Seiten geleitet

Weitere Hilfeinformationen können zu jedem zufall-Objekt und zu den Metho-
den eines Objektes gewonnen werden, indem bei der Erzeugung des Objektes 
mit Hilfe seiner Erzeugerfunktion oder beim Aufruf der Methode als letzter 
Eintrag in der Argumentenliste h=1 geschrieben wird. Man erhält dann unmit-
telbar die gewünschte Information oder wird auf eine andere Hilfeseite ge-
leitet

Analoges gilt für die Funktionen, die von zufall zur Verfügung gestellt wer-
den

Weiterhin ist für jedes Objekt eine Eigenschaft mit dem Namen h (Kurzform 
von hilfe) vorhanden, bei deren Aufruf die verfügbaren Eigenschaften und 
Methoden aufgelistet werden
	
Tritt in einer Syntaxdarstellung die Konstruktion /[...] auf, kann die Anga- 
be zwischen den eckigen Klammern entfallen. Ein |-Zeichen bedeutet i.A., 	
dass zwischen zwei Angaben ausgewählt werden kann	
        """)		
        return
		
    if h == 4:
        print(
        """		
Bezeichner (Namen)

Die erzeugten zufall-Objekte können einem Bezeichner zugewiesen werden, 
z.B. wird mit der Anweisung

   In [..]: bv = BV(12, 0.3)
   
dem Bezeichner bv als Wert ein BinomialVerteilung-Objekt zugewiesen ('=' ist 
in Python für Zuweisungen vorgesehen)

Ein Bezeichner kann in zufall aus allen Buchstaben des englischen Alphabets,
allen Ziffern 0, 1, ..., 9 und dem Unterstrich '_' bestehen, wobei er mit
einem Buchstaben beginnen muß. Der Name kann beliebig lang sein, es wird
zwischen großen und kleinen Buchstaben unterschieden. Auf diese Art gebil-
deten Namen kann jederzeit ein Objekt (zufall-Objekt oder anderes, z.B. ei-
ne Zahl) zugewiesen werden. Dabei darf es sich nicht um einen geschützten 
Namen handeln (s.u.)

Anders verhält es sich bei den 'freien' Bezeichnern, denen unmittelbar kein
Wert zugewiesen wird und die als Variablen oder als Parameter u.a. in Glei-
chungen auftreten. Im Unterschied zu anderen CAS werden in dem von zufall 
benutzten SymPy solche Bezeichner nicht einfach durch Hinschreiben erkannt 
und akzeptiert, sondern sie müssen explizit als Symbole deklariert werden. 
Für Buchstaben und kleine griechische Buchstaben wird das bereits innerhalb
von zufall erledigt, so dass Bezeichner wie r, g, b, A, X usw. jederzeit 
frei verwendet werden können. Soll ein freier Bezeichner länger als ein 
Zeichen sein, muss er mittels einer entsprechenden SymPy-Anweisung dekla-
riert werden, etwa durch

   In [..]: xyz = Symbol('xyz')
   
Es gibt eine Reihe von Bezeichnern, die in zufall eine feste Bedeutung ha-
ben und nicht anderweitig verwendet werden können, indem sie einen anderen 
Wert bekommen. Beim Versuch, einen anderen Wert an einen solchen Bezeichner
zu binden, warnt zufall mit einem Hinweis und verhindert das Überschreiben. 
Ebenfalls in das Warnsystem aufgenommen wurden die Elemente der SymPy-Spra-
che, die innerhalb von zufall zur Verfüung des Nutzers gestellt werden\n
Besondere Beachtung erfordern die Bezeichner E N und I, denen Konstanten zu-
gewiesen sind. Sie werden kommentarlos überschrieben werden, wenn ihnen ein
anderer Wert zugewiesen wird
		
Viele Eigenschaften/Methoden haben synonyme Bezeichner, die folgendermaßen
gebildet werden:

   - ein '_' (Unterstrich) innerhalb des Bezeichners einer Eigenschaft oder 
     Methode wird eliminiert, indem der nächste Buchstabe groß geschrieben  
     wird, z.B. sch_el -> schEl ('Kamelschreibweise'; Methode
     'Scharelement')
   - ein '_' am Ende eines Bezeichners wird elimimiert, indem das erste Zei-
     chen groß geschrieben wird, z.B: umfang_ -> Umfang (Methode 'Umfang')
	 
In einem zufall-Notebook kann explizit mit anderen Python-Paketen gearbeitet 
werden, speziell mit SymPy, von dem einige Anweisungen dem System bereits 
bekannt sind. Soll ein weiteres SymPy-Element benutzt werden, z.B. die Funk-
tion ceiling, so ist dieses mit der üblichen import-Anweisung zu importieren 
und kann danach aufgerufen werden
	
   In [..]: from sympy import ceiling
            ...
   In [..]: ceiling(3.12)    #  das Ergebnis ist 4		
        """)		
        return		
		
    if h == 5:
        print(
        """			
Zugriff auf Eigenschaften und Methoden von Objekten

Die zufall-Objekte haben verschiedene Eigenschaften und Methoden (die letz-
teren erwarten für ihre Ausführung Argumente - ein weiteres Objekt, einen 
Parameterwert o.ä.). Die implementierten Eigenschaften und Methoden eines 
Objektes können über seine Hilfeseite wie etwa

   In [..]: BV(h=1)
   
ermittelt werden. Ein BV-Objekt (BV ist der Kurzname von BinomialVerteilung) 
hat z.B. die Eigenschaft erw (Erwartungswert) und die Methode P (zur Berech-
nung von Wahrscheinlichkeiten). Der Zugriff erfolgt mittels des '.' - Ope-
rators, der allgemein in der Objektorientierten Programmierung Verwendung 
findet. Sei etwa dem Bezeichner bv ein BV-Objekt zugewiesen, etwa mit der 
Anweisung

   In [..]: bv = BV(50, 1/3))
   
so sind die Anweisungen für den Zugriff zu seinem Erwartungswert
		
   In [..]: bv.erw
   
und zu der Methode für die Berechnung von Wahrscheinlichkeiten
		
   In [..]: bv.P(25)
   
Eine Methode wird generell über einen Funktionsaufruf realisiert, der Argu-
mente erwartet, die in Klammern eingeschlossen werden. Hier wurde das Argu-
ment 25 angegeben, es soll die Wahrscheinlichkeit dafür berechnet werden, 
dass eine Zufallsgröße mit der betrachteten Verteilung diesen Wert annimmt

Zu einer Reihe von Eigenschaften existiert eine Methode mit gleichem Namen, 
der auf einen Unterstrich '_' endet. Damit besteht die Möglichkeit, mittels 
des entsprechenden Funktionsaufrufes zusätzliche Informationen/Leistungen 
anzufordern. Welche das sind, kann über die Hilfeanforderung (h=1 als letz-
ter Eintrag in der Argumentliste) erfahren werden. Diese zu Eigenschaften 
gehörenden Methoden können auch über den Namen der Eigenschaft mit großem 	
Anfangsbuchstaben aufgerufen werden, also z.B. für die Eigenschaft erw von
bv
		
   In [..]: bv.erw_(...)   oder
   In [..]: bv.Erw(...)
   
Das Ergebnis eines Eigenschafts-/Methodenaufrufes kann ein Tupel oder eine 
Liste sein, etwa die Daten einer DatenReihe dr, die als Liste dr.daten vor-
liegen. Um auf ein einzelnes Element zuzugreifen, wird der Indexzugriff ver-
wendet, etwa

   In [..]: dr.daten[3]
   
für das 4. Element der Liste (gemäß der Python-Konvention beginnt die Zählung 
bei 0) oder

   In [..]: dr.daten[:3] 
   
für den Zugriff auf die ersten 3 Elemente

Wahrscheinlichkeits- und Häufigkeits-Verteilungen und anderes werden als 
dictionary bereitgestellt (Schlüssel/Wert-Paare). Hier erfolgt der Zugriff 
auf einen einzelnen Wert über den Schlüssel, z.B. bei der Methode vert 
(Wahrscheinlichkeitsverteilung) der betrachteten BinomialVerteilung

   In [..]: bv.vert[4]		
        """)		
        return		
		
    if h == 6:
        print(
        """		
Klassen in zufall
	
Kurz-     Langname

ZE        ZufallsExperiment
             = ZV  ZufallsVersuch
ZG        ZufallsGröße
BK        BernoulliKette

BV        BinomialVerteilung		
HGV       HyperGeometrischeVerteilung		
GLV       GleichVerteilung
GV        GeometrischeVerteilung
PV        PoissonVerteilung\n		
NV        NormalVerteilung
EV        ExponentialVerteilung

DR        DatenReihe

EA        EreignisAlgebra		
VT        VierFelderTafel
HB        HäufigkeitsBaum

KI        KonfidenzIntervall		
AT        AlternativTest		
STP       SignifikanzTestP
		
Urne		
Münze		
Würfel		
Rad       GlücksRad
		
MK        MarkoffKette
		
Roulette		
Chuck     ChuckALuck		
Craps		
Toto      FussballToto		
Lotto		
Skat      SkatBlatt
		
Vektor    analog zu agla		
Matrix    analog zu agla			
        """)		
        return
		
    if h == 7:        
        print(
        """		
Funktionen in zufall
		
Allgemeine Funktionen
		
Hilfe                  Hilfefunktion
fakultät = fak         Fakultät
binomial = B           Binomialkoeffizient 
perm = permutationen   Permutationen	
komb = kombinationen   Kombinationen	
variationen            Variationen	
auswahlen              Berechnung von k-Auswahlen	
zuf_zahl = zufZahl     Erzeugen von (Pseudo)-Zufallszahlen	
anzahl                 Anzahl des Vorkommens eines Elementes in einer 
                       Liste/DatenReihe
anzahl_treffer         Anzahl Treffer in einer Liste 
     = anzahlTreffer        
summe                  Summe der Elemente einer Liste/DatenReihe 
gesetze                Einige Gesetze der Wahrscheinlichkeitsrechnung	
löse                   Allgemeiner Gleichungs-/Ungleichungs-Löser		
ja_nein = jaNein       Bewertung logischer Ausdrücke
stochastisch           Test auf stochastische(n) Vektor/Matrix
einfach                Vereinfachen von Objekten
ja, nein, mit, ohne,   Hilfsgrößen
Ja, Nein, Mit, Ohne    für True/False

Mathematische Funktionen

sqrt, exp, log, ln, lg, abs
sin, arcsin (= asin), sing, arcsing (= asing)     / ...g: 
cos, arccos (= acos), cosg, arccosg (= acosg)     / Funktionen
tan, arctan (= atan), tang, arctang (= atang)     / mit Grad-
cot, arccot (= acot), cotg, arccotg (= acotg)     / werten
sinh, arsinh (= asinh)	
cosh, arcosh (= acosh)	
tanh, artanh (= atanh)
deg = grad                Umrechnung Bogen- in Gradmaß		
rad = bog                 Umrechnung Grad- in Bogenmaß	
kug_koord (= kugKoord)    Umrechnung in Kugelkoordinaten			
min, max - Minimum bzw. Maximum von zwei oder mehr Zahlen		
N oder Methode n - Umwandlung SymPy- in Dezimal-Ausdruck    
re - Realteil einer komplexen Zahl
im - Imaginärteil einer komplexen Zahl
conjugate (= konjugiert) - Konjugiert-komplexe Zahl

Konstanten

pi - Zahl Pi (3.1415...)
E  - Eulersche Zahl e (2.7182...)
I - imaginäre Einheit

ACHTUNG!  B, E, N, I sind kommentarlos überschreibbar
        """)		
        return
				
    if h == 8:
        print(
        """		
Operatoren

Folgende Operatoren stehen zusätzlich zu den Python-Operatoren zur		
Verfügung bzw. ersetzen diese
	
   ^    Potenzierung; zusätzlich zum Operator **; Umdefinition des
        Python-Operators ^		
   °    Skalarprodukt von Vektoren; zusätzlich zum Operator *		
   |    Verkettung von Vektoren; Umdefinition des Python-Operators |			
        """)		
        return
		
    if h == 9:  
        print(
        """		
Jupyter-Notebook

+==================================================================+
| Um in einem Notebook mit zufall arbeiten zu können, muss zu      | 
| Beginn der Sitzung die (Jupyter-) Anweisung                      |
|                                                                  |
|    In [..]: %run zufall/start                                    |
|                                                                  |
| in einer Codezelle ausgeführt werden                             |
+==================================================================+
		
zufall benutzt als Bedienoberfläche Jupyter. Dieses wurde unter dem 
Namen IPython ursprünglich als Entwicklungsumgebung für Python- 
Anwendungen bereitgestellt, unterstützt aber inzwischen eine Vielzahl  
weiterer Programmiersprachen. Der Name setzt sich aus den Namen von 
drei Sprachen zusammen - Julia (eine Sprache, die sehr schnellen Code 
erzeugt), Python und R (inzwischen ein leistungsfähiges Statistikpaket)

Ausschlaggebend für die Wahl dieser Plattform war das hier realisierte 
Notebook-Konzept, wie es auch in kommerziellen CAS (z.B. Mathematica) 
Verwendung findet

Jupyter läuft als lokale Anwendung auf dem Standardbrowser des 
Computers, Kern (kernel) ist der Python-Interpreter

Ein Jupyer-Notebook ist in Zellen (cells) unterteilt, wobei drei 
Zelltypen auftreten, die hier interessieren:

   - Code-Zellen   Kennzeichnung:  In [..] 
	 
      In diese Zellen werden Anweisungen in der benutzten  
      Programmiersprache (hier Python) geschrieben, also auch   
      Anweisungen zur Benutzung von zufall; die Zellen sind analog zu 
      einem Texteditor editierbar; beim Ausführen (run) einer solchen 
      Zelle wird ihr Inhalt an den Python-Interpreter übergeben, der 
      für seine Verarbeitung sorgt
	  
      Eine neue Zelle wird standardmäßig als Code-Zelle erzeugt; die 
      Umwandlung einer Markdown-Zelle in eine Code-Zelle ist über das 
      Code-Menü oder die Platzierung des Cursors im vorderen 
      Zellbereich und Drücken der Y-Taste erreichbar
	  
   -Ausgabe-Zellen   Kennzeichnung:  Out [..]
	 
      Die Zellen entstehen, wenn nach der Auswertung einer Codezelle 
      durch den Python-Interpreter eine Ausgabe erforderlich ist; in 
      diese Zellen kann der Benutzer nicht direkt schreiben	 
	 
   - Markdown-Zellen	Ohne Kennzeichnung
	 
      Die Zellen dienen vor allem zur Aufnahme von Texten, wobei diese 
      mit Markdown- (eine einfache Auszeichnungssprache) oder HTML-  
      Anweisungen formatiert werden können; sie können auch   
      mathematische Formeln enthalten (Nutzung von LATEX), außerdem 
      können in solchen Zellen Grafiken und Bilder dargestellt und/
      oder Audio- und Video-Dateien aktiv sein; beim Ausführen einer 
      solchen Zelle werden eventuell vorhandene Formatierungs-
      Anweisungen ausgeführt und der Inhalt auf dem Ausgabemedium 
      präsentiert

      Die Umwandlung einer Code-Zelle in eine Markdown-Zelle ist über 
      das entsprechende Menü oder die Platzierung des Cursors im  
      vorderen Zellbereich und Drücken der M-Taste erreichbar 
	  
Code- und Markdown-Zellen können beliebig erzeugt, gelöscht, kopiert, 
eingefügt und verschoben werden	 

Es kann zu jeder dieser Zellen gesprungen werden, um sie zu verändern 
und/oder erneut auszuführen 

In einem Notebook kann in zwei Modi gearbeitet werden

- Editier-Modus: Einschalten mit Enter; oben rechts ist ein Stift 
                 dargestellt 
	 
     In diesem Modus kann der Inhalt der aktuellen Zelle editiert 
     werden 

     Das Editieren einer bestehenden Markdown-Zelle kann auch mit 
     einem Doppel-Klick eingeleitet werden
	   
- Kommando-Modus: Einschalten mit ESC; der Stift rechts oben fehlt
	 
     in diesem Modus können Aktionen durchgeführt werden, die das   
     Notebook als Ganzes betreffen (Zellen erzeugen/kopieren/
     löschen/verschieben, zwischen ihnen navigieren, Dateien öffnen 
     und speichern usw.)

Wenn der Kern beschäftigt ist, ist der schwarze Kreis rechts oben 
gefüllt; auch in dieser Zeit kann editiert werden, die Ausführung 
weiterer Zellen kann aber erst erfolgen, wenn der Kern wieder frei 
ist 

Eine Datei, in die der Inhalt eines Notebooks gespeichert wird, 
erhält die Endung .ipynb

Für den Export eines Notebooks, z.B. in das .html- oder .pdf-
Format, ist das separat zu nutzende Werkzeug nbconvert vorgesehen
 

Die Bedienung eines Notebooks kann über das Menü und/oder über die Tastatur 
erfolgen
		
Einige Tastatur-Kürzel für das Jupyter-Notebook

   Umsch+Enter    Zelle ausführen, zur nächsten gehen (diese wird even-
                  tuell neu angefügt)		
   Strg+Enter     Zelle ausführen, in der Zelle verbleiben		
   Strg+M B       Zelle unterhalb einfügen		
   Strg+M A       Zelle oberhalb einfügen	
   Strg+M DD      Zelle löschen (D 2-mal drücken)		
   Esc X          Zelle löschen		
   Strg+Z         Zurücksetzen beim Editieren\n		
   Esc            Einschalten des Kommando-Modus
   Enter          Einschalten des Editier-Modus
   Strg+M H       Anzeigen aller Tastatur-Kürzel für die beiden Modi
   
   Ausführen:  (z.B. Strg-M B)
   
      Strg-Taste drücken, dann M-Taste, Strg loslassen, dann B-Taste	
      durch mehrmaliges Drücken der B-Taste können mehrere Zellen eingefügt
      werden	
        """)  
        return
			
    if h == 10:		
        print(
        """		
Nutzung von SymPy-Anweisungen

In zufall sind folgende Elemente von SymPy integriert:
		
Symbol, symbols - zur Definition von (mehrstelligen) Bezeichnern
Rational - zur Erzeugung von rationalen Zahlen (wird in zufall weitgehend  
automatisch erledigt)

solve, solveset, expand, collect, factor, simplify, nsimplify 

N [der Wert ist überschreibbar]

pi - die Kreiszahl
E - die Basis der natürlichen Logarithmen (e) [der Wert ist überschreibbar]
I - die imaginäre Einheit (i) [der Wert ist überschreibbar]
		
Sollen weitere Elemente benutzt werden, sind diese zu importieren, z.B.

   In [..]: from sympy import Piecewise
   
(eventuell ist der Pfad im  SymPy-Verzeichnis-Baum anzugeben)	
        """)		
        return
 
    if h == 11:
        print("\nGriechische Buchstaben\n")
        print("Es werden die kleinen griechischen Buchstaben\n")	  
        print("alpha, beta, gamma, delta, epsilon, zeta, eta, theta, iota, kappa ")
        display(Math("\\alpha \qquad \\beta \qquad \\gamma \qquad \\delta \qquad \\epsilon \qquad \
		         \\zeta \qquad \\eta \qquad \\theta \qquad \\iota \qquad \\kappa "))		
        print("lamda (Schreibweise!), mu, nu, xi, omicron, pi, rho, sigma, tau ")
        display(Math("\\lambda \qquad \\mu \qquad \\nu \qquad \\xi \qquad \\omicron \qquad \\pi \
                 \qquad \\rho \qquad \\sigma \qquad \\tau"))		
        print("upsilon, phi, chi, psi, omega\n")
        display(Math("\\upsilon \qquad \\phi \qquad \\chi \qquad \\psi \qquad \\omega"))		
        print("bereitgestellt. Die Namen sind nicht überschreibbar\n")
        return
		
    if h == 12:
        print(
        """
Kleiner Python-Exkurs

Eingabe von Code (in eine Code-Zelle des Jupyter-Notebooks):

    Die Ausführung einer Zelle wird durch Umsch+Enter bzw. Strg+Enter 
    veranlaßt		
	
    Eine Zuweisung (eines Wertes an einen Bezeichner) wird mittels '=' 
    realisiert:
	
        In [..]: a = 4
		
    Der Wert eines Bezeichners kann über eine Abfrage ermittelt werden
	
        In [..]: a
		
    Mehrere Zuweisungen in einer Zeile sind durch ';' zu trennen
	
        In [..]: a = 4; b = 34; c = -8
		
    Mehrere Abfrageanweisungen in einer Zeile sind durch ',' zu trennen				
    (ein ';' unterdrückt die Anzeige der vorausgehenden Elemente)	
	
        In [..]: a, b, c
		
    Eine neue Zeile (innerhalb einer Zelle des Notebooks) wird über die
    Enter-Taste erzeugt; in der neuen Zeile ist ab derselben Stelle zu 
    schreiben wie in der vorangehenden Zeile, wenn nicht ein eingerückter 
    Block entstehen soll (bzw. wenn nicht durch ein '\\' am Zeilenende ei-
    ne Verlängerung der Zeile erreicht werden soll) 
    Das ist Teil der Python-Syntax und führt bei Nichtbeachten zu einem
    Syntaxfehler   		
	
    Eingerückte Blöcke sind z.B. bei Kontrollstrukturen (vor allem in Pro-
    grammen benutzt) erforderlich. Dabei müssen alle Einrückungen die glei-
    che Stellenanzahl (standardmäßig 4 Stellen) haben
    Bei der if-else-Anweisung sieht das z.B. folgendermaßen aus:
	
        In [..]: if a < 1: 
                     b = 0        # 4 Stellen eingerückt
                     c = 3        # ebenso		
                 else:
                     b = 1        # ebenso	
					 
    oder bei einer Funktions-Definition:	
	
        In [..]: def summe(x):
                     sum = 0		
                     for y in x:
                         sum += y     # weitere Einrückung		
                     return sum			
					 
        Die Funktion berechnet die Summe der Elemente des Zahlen-Containers 
        x (eine Liste, ein Tupel oder eine Menge)
		
    Mittels '#' können in Codezellen Kommentare geschrieben werden, sie wer-
    den bei der Ausführung ignoriert
	
Einige Datentypen:

    Zeichenkette (string)   z.B.:  'Tab23' oder \"Tab23\"#
	
    Tupel (tuple)   z.B.:  
	
        In [..]: t = ( 1, 2, 3 ); t1 = ( 'a', a, Rational(1, 2), 2.7 )
        Zugriff auf Elemente  t[0], t1[-1], Slicing   (Zählung ab 0)
		
    Liste (list)   z.B.:  
	
        In [..]: L = [ 1, 2, 3 ]; L1 = [ 'a', a, Rational(1, 2), 2.7 ] 		
        Zugriff auf Elemente  L[0], L1[-1], Slicing   (Zählung ab 0)
		
    Schlüssel-Wert-Liste (dictionary, dict)   z.B.:
	
        In [..]: d = { a:4, b:34, c:-8 }
        Zugriff auf Elemente  d[a], d[c]
		
    Menge (set)   z.B.:  
	
        In [..]: m = { a, b, c };  m1 = set() (leere Menge)
        Zugriff auf Elemente  m.pop(), Indexzugriff mit list(m)[index] mög-
        lich		
		
Weitere nützliche Python-Elemente:

    Mittels type(obj) kann der Datentyp eines Objektes obj erfragt werden	
	
    List-Comprehension
	
        In [..]: tup = 1, 2, 3, 4, 5, 6    # oder anderer Datencontainer
        In [..]: [ x^2 for x in tup ]      # sehr mächtige Anweisung	
        Out[..]: [1, 4, 9, 16, 25, 36] 	
		
    Funktionsdefinition mit anonymer Funktion
	
        lambda arg1, arg2, ... : ausdruck in arg1, arg2, ...
		
    Klasse Rational: da p/q in Python (und damit auch in SymPy) eine float-
        Zahl ergibt, kann bei Bedarf eine rationale Zahl Rational(p, q) ver-
        wendet werden (in zufall erfolgt das an den meisten Stellen automa-
        tisch) 		
		
    *liste als Argument einer Funktion packt den Container liste aus   
	
    Ersetzen des Wertes eines Bezeichners in einem Ausdruck durch
        einen anderen Wert  (eine SymPy-Anweisung)  
		
        ausdruck.subs(bez, wert) 
		
        In [..]: (x+y).subs(x, 2)		
        Out[..]: y+2
		
    Die Ausgabe '<bound method ...>' weist auf eine an ein Objekt gebundene 
    Methode (eine Funktion) hin, die zu ihrer Ausführung in Klammern ein-
    gefasste Parameter erwartet		
        """)
        return

    if h == 13:
        print(
        """	
Bemerkungen für Programmierer / Entwickler

Zur Unterstützung der Fehlersuche ist im Hauptprogramm die Variable _TEST
vorgesehen, die im Quelltext geändert werden kann; bei _TEST = True werden
bei Fehlern die vollständigen Python-Fehlermeldungen angezeigt	
Durch das zufall-Paket wird die Python-Sprache an einigen Stellen modifiziert
(Umdefinition der Operatoren '^' und '|', Unterbinden der Zuweisung eines
Wertes an die Eigenschaft/Methode eines Objektes ('objekt.eigenschaft = wert'-
Konstrukt), Verwenden der deutschen Umlaute in Bezeichnern u.a.m.). Bei Ände-
rungen oder Ergänzungen der zufall-Quelltexte dürfen diese Modifizierungen nicht
benutzt werden. Ebenso ist es nicht ratsam, innerhalb eines zufall-Notebooks
eine allgemeine Python-Programmierung durchzuführen

Aus der Sicht des Autors sollten die Schwerpunkte der weiteren Entwicklung 
des Paketes sein:		

   - Konfiguration der Jupyter-Oberfläche entsprechend den Bedürfnissen von 
     Lehrern und Schülern\n
   - Vereinheitlichung der Schriftart und -größe für Ausgaben\n	 
   - Aufnahme weiterer statistischer Tests in das Paket\n
   - Gestaltung der EreignisAlgebra-Klasse auf der Basis von logischen Aus-
     drücken\n
   - Verbesserung der Fehlererkennung und -mitteilung\n	 
   - Bessere Verknüpfung der Dokumentation mit den Programmen\n	 
   - Eventuelle Anpassung an die SymEngine (nach deren Fertigstellung durch  
     die Entwickler)	 
        """)
        return
			
			
# ------------------------------
# Hilfsgroessen für True / False
# ------------------------------

Ja = ja = Mit = mit = True
Nein = nein = Ohne = ohne = False
		

		
# ---------------------------              
# Hilfsklasse für Gleichungen 
# ---------------------------              

class _Gleichung(ZufallsObjekt):   

    def __new__(cls, *args):    

        printmethod = '_latex'
    
        try:
            if not args:
                raise ZufallError("mindestens die linke Seite der Gleichung angeben")	
            if len(args) > 2:
                raise ZufallError("nur die beiden Seiten der Gleichung angeben")		
            lhs = args[0]
            rhs = 0
            if len(args) > 1:
                rhs = args[1]
            ve = importlib.import_module('agla.lib.objekte.vektor')
            Vektor = ve.Vektor
            if not ((is_zahl(lhs) or isinstance(lhs, Vektor)) and 
		         (is_zahl(rhs) or isinstance(rhs, Vektor))):	
                raise ZufallError("nur arithmetische Ausdrücke oder Vektoren angeben")		
            return ZufallObjekt.__new__(cls, lhs, rhs)
        except ZufallError as e:
            print('zufall', str(e))
            return
			
    def __str__(self):
        return str(self.lhs) + " = " + str(self.rhs)
		
    def __repr__(self):
        return 'gleichung(' + repr(self.lhs) + ',' + repr(self.rhs) + ')'
		
    def _latex(self, printer):	                          
        return latex(self.lhs) + '=' + latex(self.rhs)		
		
    @property
    def lhs(self):
        return self.args[0]
    @property		
    def rhs(self):
        return self.args[1]
		
    def __mul__(self, other):
        if not is_zahl(other):
            print('zufall: Zahlenwert als Faktor angeben')
            return			
        return gleichung(other * self.lhs, other * self.rhs)
		
    def __rmul__(self, other):
        if not is_zahl(other):
            print('zufall: Zahlenwert als Faktor angeben')
            return			
        return gleichung(other * self.lhs, other * self.rhs)

    def __truediv__(self, other):
        if not is_zahl(other):
            print('zufall: Zahlenwert angeben')
            return			
        return gleichung(self.lhs / other, self.rhs / other)
		
    def __add__(self, other):
        if not is_zahl(other):
            print('zufall: Zahlenwert als Summand angeben')
            return			
        return gleichung(other + self.lhs, other + self.rhs)

    def __radd__(self, other):
        if not is_zahl(other):
            print('zufall: Zahlenwert als Summand angeben')
            return			
        return gleichung(other + self.lhs, other + self.rhs)

    def __neg__(self):
        return gleichung(-self.lhs, -self.rhs)

    def __pow__(self, other):
        if not is_zahl(other):
            print('zufall: Zahlenwert als Exponent angeben')
            return			
        return gleichung(self.lhs**other, self.rhs**other)

    def __sub__(self, other):
        if not is_zahl(other):
            print('zufall: Zahlenwert angeben')
            return			
        return gleichung(self.lhs - other, self.rhs - other)

		
			
