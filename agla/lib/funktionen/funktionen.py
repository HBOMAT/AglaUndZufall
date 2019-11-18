#!/usr/bin/python
# -*- coding utf-8 -*-


                                  
#                                                 
#  agla - Funktionen                    
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



#
#  Inhalt:
#
#   Mathematische Funktionen
#   Abstand-Funktion
#   Winkel-Funktion
#   Lage-Funktion
#   Trigonometrische und Umkehr-Funktionen - Gradmaß
#   Determinante-Funktion - determinante
#   allgemeiner Gleichungslöser - löse
#   Vereinfachung - einfach
#   Test auf Kollinearität - kollinear
#   Test auf Komplanarität - komplanar
#   Test auf Lineare Abhängigkeit - linear_abh
#   Test auf Parallelität - parallel
#   Test auf Orthogonalität - orthogonal
#   Test auf Identität - identisch
#   Umrechnung in Kugelkoordinaten      
#   Test auf agla-Zahl - is_zahl
#   Test auf freien Parameter - mit_param
#   Ausgabe nummerischer Werte - wert_ausgabe
#   Hilfe-Funktion
#   Abbildungen der Modelle der hyperbolischen Geometrie
#   Hilfsklasse für Gleichungen - Gleichung
#   Hilfsgrössen für True / False	
	
	
	
import importlib

from IPython.display import display, Math

from sympy.core import Expr
from sympy.simplify import simplify, nsimplify, radsimp, trigsimp, signsimp

from sympy.core.add import  Add
from sympy.core.mul import  Mul
from sympy.core.power import  Pow
from sympy.core.symbol import Symbol
from sympy.core.evalf import  N
from sympy import Mod, Piecewise, S
from sympy.core.numbers import (Integer, Rational, Float, Zero, One, 
     NegativeOne, Half, pi, E)
from sympy.core.sympify  import sympify, SympifyError
from sympy.core.containers import Tuple
from sympy import (
    Abs, sqrt as Sqrt, exp as Exp, log as Log, 
    sin as Sin, cos as Cos, tan as Tan, cot as Cot,
	asin as Asin, acos as Acos, atan as Atan, acot as Acot,
	sinh as Sinh, cosh as Cosh, tanh as Tanh, 
	asinh as Asinh, acosh as Acosh, atanh as Atanh,
	re as Re, im as Im, conjugate as Conjugate)
from sympy.functions.elementary.miscellaneous import Max, Min
from sympy.core.compatibility import iterable
from sympy.solvers.solvers import solve
import sympy

from sympy.abc import alpha, beta
from sympy.printing import latex
from sympy.matrices import Matrix as SympyMatrix

from agla.lib.objekte.basis import AglaObjekt
from agla.lib.objekte.ausnahmen import *
from agla.lib.objekte.umgebung import UMG 
import agla



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

	
# ----------------
# Abstand-Funktion
# ----------------

def Abstand(*obj, **kwargs):
    if kwargs.get("h"):
        print("\nAbstand - Funktion\n")
        print("Abstand zweier Objekte voneinander\n")
        print("Aufruf      Abstand( objekt1, objekt2 )\n")
        print("                objekt   Punkt, Gerade, Ebene, Kugel (im Raum R^3)")
        print("                         Punkt Gerade (in der Ebene R^2)\n")
        print("Zusatz          d=n   Dezimaldarstellung")
        print("                n<=12 - Anzahl der Nachkommastellen\n") 		
        return	
    try:
        if len(obj) != 2:
            raise AglaError("zwei Objekte angeben")
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
        Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
        Ebene = importlib.import_module('agla.lib.objekte.ebene').Ebene	
        Kugel = importlib.import_module('agla.lib.objekte.kugel').Kugel	
        Kreis = importlib.import_module('agla.lib.objekte.kreis').Kreis	
        o1, o2 = obj
        if o2.dim != o1.dim:
            raise AglaError("die Objekte haben unterschiedliche Dimension")
        if o1.dim == 2:
            objekte = [Vektor, Gerade, Kreis]
        elif o1.dim == 3:
            objekte = [Vektor, Gerade, Ebene, Kugel]
        else:
            objekte = [Vektor]		
        if not (type(o1) in objekte and type(o2) in objekte):
            raise AglaError("siehe Hilfe [ Abstand(h=1) ]")
        ab = o1.abstand(o2)
        if kwargs.get("d"):
            d = kwargs.get('d')
            wert = N(ab)
            if isinstance(d, (Integer, int)):
                if 0 <= d <= 12:
                    return N(wert, d)
            return N(wert)		
        else:
            return ab	
    except AglaError as e:
        print('agla:', str(e))
        return

			
# ---------------
# Winkel-Funktion
# ---------------

def Winkel(*obj, **kwargs):
    if kwargs.get("h"):
        print("\nWinkel - Funktion\n")
        print("Winkel zwischen zwei Objekten (in Grad)\n")
        print("Aufruf      Winkel( objekt1, objekt2 )\n")
        print("                objekt   Vektor, Gerade, Ebene (im Raum R^3)")
        print("                         Vektor, Gerade (in der Ebene R^2)\n")
        print("Zusatz          d=n    Dezimaldarstellung mit n Nachkommastellen")
        print("Zusatz          b=1    Ausgabe in Bogenmaß")
        print("                bd=n   Bogenmass, Dezimaldarstellung")
        print("                       n<=12 - Anzahl der Nachkommastellen\n")		
        return	
    try:
        if len(obj) != 2:
            print("agla: zwei Objekte angeben")
            return
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
        Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
        Ebene = importlib.import_module('agla.lib.objekte.ebene').Ebene	
        o1, o2 = obj
        if o2.dim != o1.dim:
            raise AglaError("die Objekte haben unterschiedliche Dimension")
        if o1.dim == 2:
            objekte = [Vektor, Gerade]
        elif o1.dim == 3:			
            objekte = [Vektor, Gerade, Ebene]
        else:
            raise AglaError("die Objekte müssen Dimension 2 oder 3 haben")		
        if not (type(o1) in objekte and type(o2) in objekte):
            raise AglaError("siehe Hilfe [ Winkel(h=1) ]")
        wi = o1.winkel(o2)
		
        if kwargs.get("d"):
            d = kwargs.get('d')
            if not isinstance(d, (Integer, int)) or d < 0:
                return wi
            return wert_ausgabe(wi, d)		
        if kwargs.get("b"):
            wi = wi / 180 * pi
            try:
                wi = nsimplify(wi, [pi])
            except RecursionError:
                pass             			 
            return wi
        elif kwargs.get("bd"):
            d = kwargs.get('bd')
            wert = float(wi * pi/180)
            if isinstance(d, (Integer, int)):
                if 0 <= d <= 12:
                    return eval(format(wert, ".%df" % d))
                return eval(format(wert))
            return wert	
        else:
            return wi	
    except AglaError as e:
        print('agla:', str(e))
        return
	
			
# -------------
# Lage-Funktion
# -------------

def Lage(*obj, **kwargs):
    if kwargs.get("h"):
        print("\nLage - Funktion\n")
        print("Lage zweier Objekte zueinander\n")
        print("Aufruf      Lage( objekt1, objekt2 )\n")
        print("                objekt   im Raum R^3: Punkt, Gerade,")
        print("                         Ebene, Strecke, Kugel, Dreieck,") 
        print("                         Viereck")
        print("                         in der Ebene R^2: Punkt, ")
        print("                         Gerade, Strecke, Dreieck, Kreis,")
        print("                         Viereck\n")		
        print("Für die beiden Objekte muss eine passende schnitt-Methode")
        print("definiert sein\n")
        print("Zusatz          l=1    Lageinformationen\n")
        return	
		
    try:		
        if len(obj) != 2:
            raise AglaError("zwei Objekte angeben")
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
        Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
        Ebene = importlib.import_module('agla.lib.objekte.ebene').Ebene	
        Strecke = importlib.import_module('agla.lib.objekte.strecke').Strecke	
        Kreis = importlib.import_module('agla.lib.objekte.kreis').Kreis	
        Kugel = importlib.import_module('agla.lib.objekte.kugel').Kugel	
        Dreieck = importlib.import_module('agla.lib.objekte.dreieck').Dreieck	
        Viereck = importlib.import_module('agla.lib.objekte.viereck').Viereck	
        o1, o2 = obj
        if o1.dim != o2.dim:
            raise AglaError("die Objekte haben unterschiedliche Dimension")
        if o1.dim == 2:
            objekte = [Vektor, Gerade, Strecke, Kreis, Dreieck, Viereck] 
            schnitte = { Vektor : objekte,
                       Gerade : objekte,
                       Strecke : (Vektor, Gerade, Strecke),
                       Kreis : (Vektor, Gerade, Kreis),
                       Dreieck : (Vektor,),
                       Viereck : (Vektor,) }					  
        elif o1.dim == 3:			
            objekte = [Vektor, Gerade, Ebene, Strecke, Kugel, Dreieck, Viereck] 
            schnitte = { Vektor : objekte,
                       Gerade : objekte,
                       Ebene : (Vektor, Gerade, Ebene, Kugel),
                       Strecke : (Vektor, Gerade, Ebene, Strecke),
                       Kugel : (Vektor, Gerade, Ebene, Kugel),					   
                       Dreieck : (Vektor, Gerade),
                       Viereck : (Vektor, Gerade) }					  
        else:
            raise AglaError("die Objekte müssen Dimension 2 oder 3 haben")
        if not (type(o1) in objekte and type(o2) in objekte):
            raise AglaError("siehe Hilfe [ Lage(h=1) ]")
        if type(o2) in schnitte[type(o1)]:
            ss = o1.schnitt(o2)
        else:			 
            raise AglaError('keine schnitt-Methode implementiert')
    except AglaError as e:
        print('agla:', str(e))
        return		
    if kwargs.get('l'):
        return o1.schnitt(o2, l=1)
    return ss
	

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
    number = sympify(number[0])
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
    number = sympify(number[0])
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = Asin(nsimplify(number))
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
    number = sympify(number[0])
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
    number = sympify(number[0])
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = Acos(nsimplify(number))
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
    number = sympify(number[0])
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
    number = sympify(number[0])
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = Atan((number))
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
    number = sympify(number[0])
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
    number = sympify(number[0])
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = Acot(nsimplify(number))
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
    number = sympify(number[0])
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
    number = sympify(number[0])
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
    number = sympify(number[0])
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
    number = sympify(number[0])
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
    number = sympify(number[0])
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
    number = sympify(number[0])
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
    number = sympify(number[0])
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
    number = sympify(number[0])
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
    number = sympify(number[0])
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
    number = sympify(number[0])
    if not is_zahl(number):
        print("agla:  eine Zahl angeben")          
        return		
    wert = Atanh(number)
    if kwargs.get("d"):
        return N(wert)
    return wert	

artanh = atanh


# ---------------------------
# Berechnung der Determinante
# ---------------------------

def determinante(*vekt, **kwargs):
    if kwargs.get("h"):
        print("\ndeterminante - Funktion\n")
        print("Determinante von drei Vektoren des Raumes R^3 oder von")
        print("zwei Vektoren der Ebene R^2\n")
        print("Aufruf      determinante( vektor1, vektor2 /[, vektor3 ] )\n")
        print("                vektor   Vektor\n")
        print("Synonymer Bezeichner   det\n")		
        print("Zusatz      d=1   Dezimaldarstellung\n")
        return
    try:		
        if len(vekt) < 2 or len(vekt) > 3:
            raise AglaError("zwei oder drei Vektoren angeben")
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
        Matrix = importlib.import_module('agla.lib.objekte.matrix').Matrix
        if type(vekt[0]) is Vektor and vekt[0].dim == 2:
            if len(vekt) != 2:
                raise AglaError("zwei Vektoren in der Ebene angeben")		
            if type(vekt[1]) is Vektor and vekt[1].dim == 2:
                m = Matrix(vekt[0], vekt[1])
                d = m.D
                if mit_param(d):
                    return d				
                if kwargs.get("d"):
                    return sympify(float(d))
                return d
            else:
                raise AglaError("zwei Vektoren in der Ebene angeben")		
        elif type(vekt[0]) is Vektor and vekt[0].dim == 3:
            if len(vekt) != 3:
                raise AglaError("drei Vektoren im Raum angeben")		
            if (type(vekt[1]) is Vektor and type(vekt[2]) is Vektor and 
		        vekt[1].dim == 3 and vekt[2].dim == 3):
                m = Matrix(vekt[0], vekt[1], vekt[2])
                d = m.D
                if mit_param(d):
                    return d				
                if kwargs.get("d"):
                    return sympify(float(d))
                return d
            else:
                raise AglaError("drei Vektoren im Raum angeben")	
        else:
            raise AglaError("Eingabe überprüfen")	
    except AglaError as e:
        print('agla:', str(e))	
	
det = determinante
			
			
# ------------------	
# allgemeiner solver
# ------------------	

def loese(*args, **kwargs):
    if kwargs.get("h") == 1:
        print("\nlöse - Funktion\n")
        print("Lösen von normalen und Vektor-Gleichungen sowie von Unglei-")
        print("chungen\n")
        print("   Aufruf   löse( gleich /[, variable ] )\n")
        print("                  gleich    linke Seite einer Gleichung der")
        print("                            Form ausdruck = 0 oder Liste mit")
        print("                            solchen Elementen (Gleichungssys-")
        print("                            tem)")
        print("                  variable  einzelne oder Liste von Variablen")                           
        print("                  ausdruck  Ausdruck in den Variablen")
        print("                            bei einer einzelnen Gleichung kann")
        print("                            es auch ein Vektor-Ausdruck sein,")
        print("                            rechts steht dann der Nullvektor\n")
        print("   oder     löse( ungleich /[, variable ] )\n")
        print("                  ungleich  Ungleichung der Form ausdruck1")
        print("                            rel ausdruck2")
        print("                  rel       Relation  < | <= | > | >=\n")
        print("Zusatz   set=ja   Verwendung von solveset; standardmäßig wird ")
        print("                  solve verwendet (siehe SymPy-Dokumentation)\n")		
        print("Beispiele")	
        print("löse( 3*x-5 )                   - einzelne Gleichung")		
        print("löse( 3*x-5, set=ja )")		
        print("löse( [ 3*x-5*y+2, -2*x+y-4 ] ) - Gleichungssystem")		
        print("A = v(4, 0, 1); B = v(1, 2, -3); C = v(2, -4, 7)")
        print("löse( r*A + s*B + t*C )         - Vektorgleichung")
        print("             (hier: Test auf lineare Abhängigkeit)\n")	
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
        print('agla:  ein oder  zwei Argumente angeben')
        return		
    if not type(var) in (Symbol, list, tuple, Tuple):
        print('agla:  einzelne Variable als Symbol, mehrere in einer' + 
                                         ' Liste angeben')
        return	
    se = kwargs.get('set')
    if se:
        from sympy import solveset	
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
    elif isinstance(gleich, Gleichung):
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
        print('agla: linke Seite einer Gleichung oder einer ' +
             'Vektorgleichung oder \nGleichungssystem angeben')
									  
									 
# -------------	
# Vereinfachung	
# -------------	

from agla.lib.objekte.umgebung import UMG 

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
        print('agla:  ein Objekt angeben')
        return	
    x = x[0]		
    if not UMG.SIMPL:
        return x
    if not (is_zahl(x) or isinstance(x, (Vektor, SympyMatrix))):
        print('agla:  nummerischen Wert, Vektor oder Matrix angeben')
        return		
    if isinstance(x, Vektor):
        li = [einfach(k, **kwargs) for k in x.komp]
        return Vektor(li)
    if isinstance(x, SympyMatrix):
        Matrix = importlib.import_module('agla.lib.objekte.matrix').Matrix		
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
  					 
									  
# ----------------------
# Test auf Kollinearität
# ----------------------

def kollinear(*vekt, **kwargs):                                
    if kwargs.get("h") == 1:
        print("\nkollinear - Funktion\n")
        print("Kollinearität von zwei Vektoren oder drei Punkten im Raum R^3")
        print("oder in der Ebene R^2\n")
        print("Aufruf      kollinear( vektor1, vektor2 )\n")
        print("oder        kollinear( punkt1, punkt2, punkt3 )\n")
        print("                vektor, punkt   Vektor\n")
        print("Zusatz      d=1   Darstellung des einen Vektors durch den")
        print("                  anderen\n")
        return
    Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
    if len(vekt) == 2:
        if not all([isinstance(vekt[i], Vektor) for i in (0, 1)]):
            print("agla:  zwei oder drei Vektoren/Punkte angeben")
            return			
        if not kwargs.get("d"):
            return vekt[0].kollinear(vekt[1])
        else:
            v0, v1 = vekt
            if v0.free_symbols or v1.free_symbols:
                print('agla: nicht implementiert (Parameter)')
                return			
            if v0.kollinear(v1):
                if v0.dim == 2:
                   vv0, vv1 = Vektor(v0.x, v0.y, 0), Vektor(v1.x, v1.y, 0)
                else:
                    vv0, vv1 = v0, v1				
                k = Symbol('k')
                di = solve([vv1.x - k*vv0.x, vv1.y - k*vv0.y, vv1.z - k*vv0.z]) 
                lat = latex(v1) + latex('=') + latex(di[0][k]) + \
				        latex('\cdot') + latex(v0)
                display(Math(lat)) 				
                return
    elif len(vekt) == 3:
        if not all([isinstance(vekt[i], Vektor) for i in (0, 1, 2)]):
            print("agla:  zwei oder drei Vektoren/Punkte angeben")
        return vekt[0].kollinear(vekt[1], vekt[2])
    else:
        print("agla:  zwei oder drei Vektoren/Punkte angeben")

	
	
# ----------------------
# Test auf Komplanarität
# ----------------------

def komplanar(*vekt, **kwargs):                            
    if kwargs.get("h") == 1:
        print("\nkomplanar - Funktion\n")
        print("Komplanarität von drei Vektoren oder vier Punkten im Raum\n")
        print("Aufruf      komplanar( vektor1, vektor2, vektor3 )\n")
        print("oder        komplanar( punkt1, punkt2, punkt3, punkt4 )\n")
        print("                vektor, punkt   Vektor\n")
        print("Zusatz      l=1  Verschwindende Linearkombination")
        print("                 (bei Komplanarität)")
        print("            d=1   Darstellung jedes Vektors durch die beiden")	
        print("                  anderen (bei Komplanarität)\n")
        return
		
    Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
    if len(vekt) == 3:
        if not all([isinstance(vekt[i], Vektor) for i in (0, 1, 2)]):
            print("agla:  3 oder 4 Vektoren/Punkte angeben")
            return					
        v0, v1, v2 = vekt[0], vekt[1], vekt[2]
        if not kwargs.get("l") and not kwargs.get("d"):
             return v0.komplanar(v1, v2)	
        else:
            if not v0.komplanar(v1, v2):
              return False			
        if v0.free_symbols or v1.free_symbols or v2.free_symbols:
            print('agla: nicht implementiert (Parameter)')
            return
			
        if kwargs.get("l"):
            if v0.komplanar(v1, v2):
                r, s, t = Symbol('r'), Symbol('s'), Symbol('t')
                di = solve([r*v0.x + s*v1.x + t*v2.x,
				             r*v0.y + s*v1.y + t*v2.y,
							  r*v0.z + s*v1.z + t*v2.z])                 
                for el in di:
                    if isinstance(di[el], Expr):
                        di[el] = di[el].subs(r, 1).subs(s, 1).subs(t, 1)
                r = di[r] if r in di.keys() else 1	                
                s = di[s] if s in di.keys() else 1			
                t = di[t] if t in di.keys() else 1	
                latr = latex('') if r == 1 else latex(r)
                lats = latex('-') + latex(abs(s)) if s < 0 else \
				         latex('+') + latex(s)
                latt = latex('-') + latex(abs(t)) if t < 0 else \
				         latex('+') + latex(t)				
                lat = latr + latex('\cdot') + latex(v0) + lats + latex('\cdot')\
				        + latex(v1) + latt + latex('\cdot') + latex(v2) \
				        + latex('=') + latex(Vektor(0, 0, 0))
                display(Math(lat))
				
        if kwargs.get("d"):
            r, s, t = Symbol('r'), Symbol('s'), Symbol('t')
			
            # 1. Vektor
            gl = -v0 + r*v1 + s*v2
            di = loese(gl)
            if di:			
                if len(di.keys()) == 2:
                    rr, ss = di[r], di[s]	
                else:
                    rr, ss = di[r].subs(s, 1), 1
                latr = latex('') if rr == 1 else latex(rr)
                lats = latex('-') + latex(abs(ss)) if ss < 0 else \
                       latex('+') + latex(ss)				
                lat = latex(v0) + latex('=') + latr + latex('\cdot') + latex(v1) \
        			    + lats + latex('\cdot') + latex(v2) 
                display(Math(lat))
			
            # 2. Vektor			
            gl = -v1 + r*v0 + s*v2
            di = loese(gl)
            if di:			
                if len(di.keys()) == 2:
                    rr, ss = di[r], di[s]	
                else:
                    rr, ss = di[r].subs(s, 1), 1
                latr = latex('') if rr == 1 else latex(rr)
                lats = latex('-') + latex(abs(ss)) if ss < 0 else \
                       latex('+') + latex(ss)				
                lat = latex(v1) + latex('=') + latr + latex('\cdot') + latex(v0) \
        			    + lats + latex('\cdot') + latex(v2) 
                display(Math(lat))
			
            # 3. Vektor			
            gl = -v2 + r*v0 + s*v1
            di = loese(gl)
            if di:
                if len(di.keys()) == 2:
                    rr, ss = di[r], di[s]	
                else:
                    rr, ss = di[r].subs(s, 1), 1
                latr = latex('') if rr == 1 else latex(rr)
                lats = latex('-') + latex(abs(ss)) if ss < 0 else \
                       latex('+') + latex(ss)				
                lat = latex(v2) + latex('=') + latr + latex('\cdot') + latex(v0) \
        			    + lats + latex('\cdot') + latex(v1) 
                return display(Math(lat))
			
    elif len(vekt) == 4:
        if not all([isinstance(vekt[i], Vektor) for i in range(4)]):
            print("agla:  3 oder 4 Vektoren/Punkte angeben")
            return					
        return vekt[0].komplanar(vekt[1], vekt[2], vekt[3])
    else:
        print("agla:  3 oder 4 Vektoren/Punkte angeben")
        return		
	
	
# -----------------------------
# Test auf Lineare Abhängigkeit
# -----------------------------

def linear_abh(*vekt, **kwargs):
    if kwargs.get("h"):
        print("\nlinear_abh - Funktion\n")
        print("Test auf lineare Abhängigkeit von Vektoren im Raum R^3 und")
        print("in der Ebene R^2\n")
        print("Aufruf      linear_abh( vektor1, vektor2, ... )\n")
        print("                vektor   Vektor\n")
        return
    try:		
        if not vekt:
            raise AglaError("mindestens einen Vektor angeben")
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
        for el in vekt:
            if not isinstance(el, Vektor):
                raise AglaError("Vektoren angeben")
            if el.dim != vekt[0].dim or not el.dim in (2, 3):
                raise AglaError("die Dimensionen sind ungleich 2,3 oder " + \
                               "unterschiedlich")
    except AglaError as e:
        print('agla:', str(e))
        return		
    if len(vekt) == 1:
        if vekt[0].betrag == 0:
            return True
        return False
    elif len(vekt) == 2:
        return kollinear(vekt[0], vekt[1])
    elif len(vekt) == 3:
        if vekt[0].dim == 2:
            return True
        else:
            return komplanar(vekt[0], vekt[1], vekt[2])
    else:
        return True
	
linearAbh = linear_abh


# ---------------------
# Test auf Parallelität
# ---------------------

def parallel(*obj, **kwargs):
    if kwargs.get("h"):
        print("\nparallel - Funktion\n")
        print("Test auf Parallelität von Objekten im Raum R^3 und")
        print("in der Ebene R^2\n")		
        print("Aufruf      parallel( objekt1, objekt2 )\n")
        print("                objekt   Vektor, Gerade, Ebene, Strecke (im Raum)")
        print("                         Vektor, Gerade, Strecke (in der Ebene)\n")
        return	
    try:	
        if len(obj) != 2:
            raise AglaError("zwei Objekte angeben")
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
        Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
        Ebene = importlib.import_module('agla.lib.objekte.ebene').Ebene	
        Strecke = importlib.import_module('agla.lib.objekte.strecke').Strecke
        o1, o2 = obj
        objekte = (Vektor, Gerade, Ebene, Strecke)
        if not (isinstance(o1, objekte) and isinstance(o2, objekte)):
            raise AglaError("Vektor, Gerade, Ebene oder Strecke angeben")
        if o1.dim != o2.dim:
            raise AglaError("die Objekte haben unterschiedliche Dimension")
    except AglaError as e:
        print('agla:', str(e))
        return		
    if isinstance(o1, Vektor):
        v1 = o1
    elif isinstance(o1, Gerade):
        v1 = o1.richt
    elif isinstance(o1, Ebene):
        v1 = o1.norm
    elif isinstance(o1, Strecke):
        v1 = o1.gerade.richt
    if isinstance(o2, Vektor):
        v2 = o2
    elif isinstance(o2, Gerade):
        v2 = o2.richt
    elif isinstance(o2, Ebene):
        v2 = o2.norm
    elif isinstance(o2, Strecke):
        v2 = o2.gerade.richt
    if isinstance(o1, (Vektor, Gerade, Strecke)):
        if isinstance(o2, (Vektor, Gerade, Strecke)):
            return kollinear(v1, v2)
        else:
            return not bool(v1.sp(v2))
    elif isinstance(o1, Ebene):
        if isinstance(o2, (Vektor, Gerade, Strecke)):
            return not bool(v1.sp(v2))
        else:
            return kollinear(v1, v2)
			
			
# -----------------------
# Test auf Orthogonalität
# -----------------------

def orthogonal(*obj, **kwargs):
    if kwargs.get("h"):
        print("\northogonal - Funktion\n")
        print("Test auf Orthogonalität von Objekten im Raum R^3 und")
        print("in der Ebene R^2\n")		
        print("Synonym     senkrecht\n")		
        print("Aufruf      orthogonal( objekt1, objekt2 )\n")
        print("                objekt   Vektor, Gerade, Ebene, Strecke (im Raum)")
        print("                         Vektor, Gerade, Strecke  (in der Ebene)\n")
        return	
    try:		
        if len(obj) != 2:
            raise AglaError("zwei Objekte angeben")
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
        Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
        Ebene = importlib.import_module('agla.lib.objekte.ebene').Ebene	
        Strecke = importlib.import_module('agla.lib.objekte.strecke').Strecke
        o1, o2 = obj
        objekte = (Vektor, Gerade, Ebene, Strecke)
        if not (isinstance(o1, objekte) and isinstance(o2, objekte)):
            raise AglaError("Vektor, Gerade, Ebene oder Strecke angeben")
        if o1.dim != o2.dim:
            raise AglaError("die Objekte haben unterschiedliche Dimension")
    except AglaError as e:
        print('agla:', str(e))
        return		
    if isinstance(o1, Vektor):
        v1 = o1
    elif isinstance(o1, Gerade):
        v1 = o1.richt
    elif isinstance(o1, Ebene):
        v1 = o1.norm
    elif isinstance(o1, Strecke):
        v1 = o1.gerade.richt
    if isinstance(o2, Vektor):
        v2 = o2
    elif isinstance(o2, Gerade):
        v2 = o2.richt
    elif isinstance(o2, Ebene):
        v2 = o2.norm
    elif isinstance(o2, Strecke):
        v2 = o2.gerade.richt
    if isinstance(o1, (Vektor, Gerade, Strecke)):
        if isinstance(o2, (Vektor, Gerade, Strecke)):
            sp = v1.sp(v2)		
            sp2 = sp**2		
            if  nsimplify(sp) == 0 or simplify(sp) == 0:		
                return True
            if  nsimplify(sp2) == 0 or simplify(sp2) == 0:		
                return True
            return False			
        elif isinstance(o2, Ebene):
            return kollinear(v1, v2)
    elif isinstance(o1, Ebene):
        if isinstance(o2, (Vektor, Gerade, Strecke)):
            return kollinear(v1, v2)
        elif isinstance(o2, Ebene):
            return orthogonal(v1, v2)
			
senkrecht = orthogonal


# ------------------
# Test auf Identität
# ------------------

def identisch(*obj, **kwargs):
    if kwargs.get("h"):
        print("\nidentisch - Funktion\n")
        print("Test auf Identität von zwei Geraden oder zwei Ebenen\n")
        print("Aufruf      identisch( objekt1, objekt2 )\n")
        print("                objekt   Gerade, Ebene\n")
        return	
    try:		
        if len(obj) != 2:
            raise AglaError("zwei Objekte angeben")
        Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
        Ebene = importlib.import_module('agla.lib.objekte.ebene').Ebene	
        o1, o2 = obj
        if not (type(o1) is Gerade and type(o2) is Gerade or
             type(o1) is Ebene and type(o2) is Ebene):
            raise AglaError("zwei Geraden oder zwei Ebenen angeben")
        if o2.dim != o1.dim:
            raise AglaError("die Objekte haben unterschiedliche Dimension")
    except AglaError as e:
        print('agla:', str(e))
        return		
    if parallel(o1, o2) and o2.stuetz.abstand(o1) == 0:
        return True
    else:
        return False	
		
		
# ------------------------------
# Umrechnung in Kugelkoordinaten
# ------------------------------

def kug_koord(*punkt, **kwargs):
    if kwargs.get("h"):
        print("\nkug_koord - Funktion\n")
        print("Umrechnung in Kugelkoordinaten\n")
        print("Aufruf      kug_koord( punkt )\n")
        print("                punkt   Punkt der Einheitssphäre oder sPunkt\n")
        print("Synonymer Bezeichner   kugKoord\n")		
        print("Rückgabe    Länge, Breite\n")		
        print("Zusatz      g=1    Ausgaben in Grad\n")		
        return	
    p = punkt[0]
    Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
    sPunkt = importlib.import_module('agla.lib.objekte.sphaer_geometrie').sPunkt	
    if not isinstance(p, (Vektor, sPunkt)):
        print("agla: Punkt der Einheitssphäre oder sphärischen Punkt angeben")
        return
    if	 isinstance(p, sPunkt):	
        p = p.e
    else:
        if p.dim != 3: 
            print("agla: Punkt der Einheitsphäre angeben")			
        if not mit_param(p):	
            if abs(p.betrag - 1) > 1e-8:
                print("agla: der Punkt liegt nicht in der Sphäre")	
                return
    if kwargs.get('g'):
        l, b = kug_koord(p)
        return N(l*180/pi), N(b*180/pi)		
    if p.x == 0 and p.y == 0:
        if p.z < 0:
            return 0, -pi/2
        else:
            return 0, pi/2	
    l = Piecewise( (2*pi - acos(p.x/sqrt(p.x**2 + p.y**2)), p.y<0), 
	            (acos(p.x/sqrt(p.x**2 + p.y**2)), p.y>=0) )   
    b = pi/2 - acos(p.z/sqrt(p.x**2 + p.y**2 + p.z**2))
    return l, b
  
kugKoord = kug_koord
  
  
# ------------------------
# Test auf eine agla-Zahl
# ------------------------

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
			   Mul, Add, Pow, Abs)
    return type(x) in zahlen 

isZahl = is_zahl
		
# ------------------------
# Test auf freie Parameter
# ------------------------

def mit_param(obj):
    x, y, z = Symbol('x'), Symbol('y'), Symbol('z')
    if iterable(obj):
        test = [mit_param(el) for el in obj]
        return any(test)
    obj = sympify(obj)
    if is_zahl(obj):
        try:
            return bool(obj.free_symbols)	
        except SyntaxError:
            return False		
						
    if not is_zahl(obj):
        pfad = 'agla.lib.objekte.'
        Vektor = importlib.import_module(pfad + 'vektor').Vektor	
        Gerade = importlib.import_module(pfad + 'gerade').Gerade	
        Ebene = importlib.import_module(pfad +'ebene').Ebene	
        Kugel = importlib.import_module(pfad +'kugel').Kugel
        Parallelogramm = importlib.import_module(pfad + 'parallelogramm').Parallelogramm 	
        Spat = importlib.import_module(pfad + 'spat').Spat 
        Strecke = importlib.import_module(pfad + 'strecke').Strecke			 
        Dreieck = importlib.import_module(pfad + 'dreieck').Dreieck	
        Viereck = importlib.import_module(pfad + 'viereck').Viereck	
        Kreis = importlib.import_module(pfad + 'kreis').Kreis	
        Pyramide = importlib.import_module(pfad +'pyramide').Pyramide	
        Prisma = importlib.import_module(pfad +'prisma').Prisma	
        Kegel = importlib.import_module(pfad +'kegel').Kegel			
        Zylinder = importlib.import_module(pfad +'zylinder').Zylinder	
        Koerper = importlib.import_module(pfad +'koerper').Koerper	
        Matrix = importlib.import_module(pfad +'matrix').Matrix	
        Abbildung = importlib.import_module(pfad +'abbildung').Abbildung	
        Kurve = importlib.import_module(pfad +'kurve').Kurve	
        Flaeche = importlib.import_module(pfad +'flaeche').Flaeche	
        Ellipse = importlib.import_module(pfad +'ellipse').Ellipse	
        Hyperbel = importlib.import_module(pfad +'hyperbel').Hyperbel	
        Parabel = importlib.import_module(pfad +'parabel').Parabel	
        K2O = importlib.import_module(pfad +'k2o').Kurve2terOrdnung	
        F2O = importlib.import_module(pfad +'f2o').Flaeche2terOrdnung	
        LGS = importlib.import_module(pfad +'lgs').LGS
        pfad = 'agla.lib.objekte.hyp_geometrie'
        hPunkt = importlib.import_module(pfad).hPunkt	
        hGerade = importlib.import_module(pfad).hGerade	
        hStrecke = importlib.import_module(pfad).hStrecke	
        hKreis = importlib.import_module(pfad).hKreis	
        hDreieck = importlib.import_module(pfad).hDreieck	
        pfad = 'agla.lib.objekte.sphaer_geometrie'
        sPunkt = importlib.import_module(pfad).sPunkt	
        sGerade = importlib.import_module(pfad).sGerade	
        sStrecke = importlib.import_module(pfad).sStrecke	
        sKreis = importlib.import_module(pfad).sKreis	
        sDreieck = importlib.import_module(pfad).sDreieck	
        sZweieck = importlib.import_module(pfad).sZweieck	
        if type(obj) is Vektor:
            return mit_param(obj.args)
        elif type(obj) is Gerade:
            return bool(len(obj.free_symbols) > 1)
        elif type(obj) is Ebene:
            return bool(len(obj.free_symbols) > 3)
        elif type(obj) is Kugel:
            return mit_param(obj.args)
        elif type(obj) is Parallelogramm:
            return mit_param(obj.args)
        elif type(obj) is Spat:
            return mit_param(obj.args)
        elif type(obj) is Strecke:
            return mit_param(obj.args)			
        elif type(obj) is Dreieck:
            return mit_param(obj.args)
        elif type(obj) is Viereck:
            return mit_param(obj.args)
        elif type(obj) is Kreis:
            return mit_param(obj.args)			
        elif type(obj) is Pyramide:
            return mit_param(obj.args)
        elif type(obj) is Prisma:
            return mit_param(obj.args)
        elif type(obj) is Kegel:
            return mit_param(obj.args)
        elif type(obj) is Zylinder:
            return mit_param(obj.args)
        elif type(obj) is Koerper:
            return mit_param(obj.ecken)
        elif type(obj) is Matrix:
            return len(obj.free_symbols) > 0
        elif type(obj) is Abbildung:
            return mit_param(obj.args)
        elif type(obj) is Kurve:
            if obj.dim == 3:			
                return len(obj.free_symbols) > 1
            if str(obj.args[-1]) in ('pol', 'prg', 'fkt'):
                return len(obj.args[0].free_symbols) > 1
            return len(obj.args[0].free_symbols) > 2
        elif type(obj) is Flaeche:
            if obj._typ in ('prg', 'fkt'):		
                sy = obj.args[0].free_symbols.union(obj.args[1].free_symbols). \
                     union(obj.args[2].free_symbols)
                return len(sy) > 2
            else:
                sy = obj.args[0].free_symbols.difference({x, y, z})	
                return len(sy) > 0	
        elif isinstance(obj, (Ellipse, Hyperbel)):
            a = obj.args		
            return mit_param(a[0]) or mit_param(a[1]) or mit_param(a[2])		
        elif isinstance(obj, Parabel):
            return mit_param(obj.args[0])	
        elif isinstance(obj, (K2O, F2O)):
            return mit_param(obj.args[0].free_symbols.difference({x, y, z}))  
			
        elif type(obj) is LGS:
            par = False
            for el in obj.args[:-1]:
                if mit_param(el):
                    par = True 
                    break
            return par					
        elif isinstance(obj, hPunkt): 
            return mit_param(obj.args)
        elif isinstance(obj, (hGerade, hStrecke)):
            A, B = obj.args[1:3]		
            return mit_param(A.e) or mit_param(B.e)
        elif isinstance(obj, hKreis):
            if len(obj.args) == 2:		
                M, r = obj.args		
                return mit_param(M.e) or mit_param(r)
            kurve, M, r = obj.args		
            return mit_param(kurve) or mit_param(M.e) or mit_param(r)
        elif isinstance(obj, hDreieck):
            A, B, C = obj.args[:3]		
            return mit_param(A.e) or mit_param(B.e) or mit_param(C.e)			
        elif type(obj) is sPunkt:
            return mit_param(obj.args)
        elif isinstance(obj, sGerade):
            A, B = obj.args		
            return mit_param(A.e) or mit_param(B.e)
        elif isinstance(obj, sStrecke):
            A, B = obj.args[1:3]	
            return mit_param(A.e) or mit_param(B.e)
        elif isinstance(obj, sKreis):
            M, r = obj.args	
            return mit_param(M) or mit_param(r)
        elif isinstance(obj, (sDreieck, sZweieck)):
            a = obj.args	
            return mit_param(a[0]) or mit_param(a[1]) or mit_param(a[2])
        else:
            return None		
    try:
        float(obj)
        return False
    except TypeError:
        return True

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
        print("h=6  - Klassen im Raum R^3")
        print("h=7  - Klassen in der Ebene R^2")
        print("h=8  - Andere Klassen")		
        print("h=9  - Funktionen")
        print("h=10 - Operatoren")
        print("h=11 - Vordefinierte Abbildungen")
        print("h=12 - Verfahren")
        print("h=13 - Jupyter-Notebook")
        print("h=14 - 3D-Grafiken (Mayavi)")
        print("h=15 - 2D-Grafiken (matplotlib)")
        print("h=16 - Grafik-Spezifikationen")		
        print("h=17 - Animationen")		
        print("h=18 - Nutzung von SymPy-Anweisungen")		
        print("h=19 - Griechische Buchstaben")		
        print("h=20 - Kleiner Python-Exkurs")		
        print("h=21 - Bemerkungen für Programmierer/Entwickler")		
        print("h=22 - Sphärische Geometrie in agla")		
        print("h=23 - Hyperbolische Geometrie in agla\n")			
        return
		
    if h == 2:
        print(
        """		
Einleitung\n
Python ist ein leistungsfähiger konventioneller Taschenrechner. Durch das 
CAS SymPy werden seine Fähigkeiten vor allem um das symbolische Rechnen er-
weitert, mit dem Paket agla ist eine Erweiterung auf das Feld des geometri-
schen Rechnens gegeben\n	
Das Programmpaket agla (Analytische Geometrie und lineare Algebra) ist ein
Python-Paket und kann innerhalb von Jupyter-Notebooks benutzt werden. Es 
ist vor allem für den Gebrauch in der Schule vorgesehen\n
In agla werden	die geometrischen Objekte Vektor, Gerade, Ebene usw. mit  	
entsprechenden Python-Klassen dargestellt. Über eine Konstruktor-/Erzeuger-		
funktion gleichen Namens können Instanzen dieser Klassen (Objekte), erzeugt
werden. Mit diesen und ihren Eigenschaften + Methoden wird dann interaktiv 
gearbeitet. Neben den Klassen zur euklidischen Geometrie werden auch einige 	
Klassen zur sphärischen und zur hyperbolischen Geometrie bereitgestellt. Wei-
terhin unterstützen einige Funktionen die Arbeit\n		
Das Paket basiert auf dem vollständig in Python geschriebenen CAS SymPy und
ist selbst ebenfalls (mit leichten Modifizierungen) in reinem Python ge- 
schrieben. Für 2D-Grafiken wird das matplotlib-Paket benutzt, für 3D Mayavi. 
Zukünftig soll das in der Entwicklung befindliche VisPy zur Anwendung kommen\n		
Die Programme von agla werden im Quellcode für die Benutzung bereitgestellt\n 
Die Syntax zur Handhabung von agla ist so gestaltet, dass sie leicht erlern-  
bar ist. Es sind nur geringe Python-Kenntnisse sowie Fähigkeiten zum Bedie- 
nen eines Jupyter-Notebooks notwendig\n 
Bei der Arbeit mit agla kann auf den gesamten Leistungsumfang von Python zu-	
gegriffen werden, der vor allem duch eine Vielzahl weiterer Pakete reali-
siert wird		
        """)		
        return		
		
    if h == 3:		
        print(
        """		
Erhalten von Hilfe-Informationen\n
Unter dem Namen 'Hilfe' steht eine Funktion zur Verfügung, über die zentrale
Hilfeinformationen erhalten werden können. Mit der Eingabe\n
   In [..]: Hilfe()  oder  Hilfe(h=1)\n
in eine Zelle des Notebooks wird man auf einzelne Seiten geleitet\n
Weitere Hilfeinformationen können zu jedem agla-Objekt und zu den Methoden
eines Objektes gewonnen werden, indem bei der Erzeugung des Objektes mit 
Hilfe seiner Erzeugerfunktion oder beim Aufruf der Methode als letzter Ein-
trag in der Argumentenliste h=1 geschrieben wird. Man erhält dann unmittel-
bar die gewünschte Information oder wird auf eine andere Hilfeseite gelei-
tet\n
Analoges gilt für die Funktionen, die von agla zur Verfügung gestellt wer-
den\n
Weiterhin ist für jedes Objekt eine Eigenschaft mit dem Namen h (Kurzform 
von hilfe) vorhanden, bei deren Aufruf die verfügbaren Eigenschaften und 
Methoden aufgelistet werden\n	
Tritt in einer Syntaxdarstellung die Konstruktion /[...] auf, kann die Anga- 
be zwischen den eckigen Klammern entfallen. Ein |-Zeichen bedeutet i.A., 	
dass zwischen zwei Angaben ausgewählt werden kann	
        """)
        return
		
    if h == 4:
        print(
        """		
Bezeichner (Namen)\n
Die erzeugten agla-Objekte können einem Bezeichner zugewiesen werden, 
z.B. wird mit der Anweisung\n
   In [..]: e = Ebene(2, -3, -1, 3)\n		
dem Bezeichner e als Wert ein Ebene-Objekt zugewiesen ('=' ist in Python
für Zuweisungen vorgesehen)\n
Ein Bezeichner kann in agla aus allen Buchstaben des englischen Alphabets,
allen Ziffern 0, 1, ..., 9 und dem Unterstrich '_' bestehen, wobei er mit
einem Buchstaben beginnen muß.	Der Name kann beliebig lang sein, es wird
zwischen großen und kleinen Buchstaben unterschieden. Auf diese Art gebil-
deten Namen kann jederzeit ein Objekt (agla-Objekt oder anderes, z.B. ei-
ne Zahl) zugewiesen werden. Dabei darf es sich nicht um einen geschützten 
Namen handeln (s.u.)\n
Anders verhält es sich bei den 'freien' Bezeichnern, denen unmittelbar kein
Wert zugewiesen wird und die als Variablen oder als Parameter u.a. in Glei-
chungen auftreten. Im Unterschied zu anderen CAS werden in dem von agla be-
nutzten SymPy solche Bezeichner nicht einfach durch Hinschreiben erkannt 
und akzeptiert, sondern sie müssen explizit als Symbole deklariert werden. 
Für Buchstaben und kleine griechische Buchstaben wird das bereits innerhalb
von agla erledigt, so  dass Bezeichner wie r, g, b, A, B usw. jederzeit  
frei verwendet werden können
Soll ein freier Bezeichner länger als ein Zeichen sein, muss er mittels ei-
ner entsprechenden SymPy-Anweisung deklariert werden, etwa durch\n
   In [..]: xyz = Symbol('xyz')\n
Es gibt eine Reihe von Bezeichnern, die in agla eine feste Bedeutung haben 
und nicht anderweitig verwendet werden können, indem sie einen anderen Wert 
bekommen. Beim Versuch, einen anderen Wert an einen solchen Bezeichner zu 
binden, warnt agla mit einem Hinweis und verhindert das Überschreiben. Eben-
falls in das Warnsystem aufgenommen wurden die Elemente der SymPy-Sprache, 
die innerhalb von agla zur Verfügung des Nutzers gestellt werden\n
Besondere Beachtung erfordern die Bezeichner E, N und I, denen Konstanten zu-
gewiesen sind. Sie werden kommentarlos überschrieben, wenn ihnen ein
anderer Wert zugewiesen wird\n		
Viele Eigenschaften/Methoden haben synonyme Bezeichner, die folgendermaßen
gebildet werden:\n
   - ein '_' (Unterstrich) innerhalb des Bezeichners einer Eigenschaft oder 
     Methode wird eliminiert, indem der nächste Buchstabe groß geschrieben  
     wird, z.B. sch_el -> schEl ('Kamelschreibweise'; Methode
     'Scharelement')
   - ein '_' am Ende eines Bezeichners wird elimimiert, indem das erste Zei-
     chen groß geschrieben wird, z.B: umfang_ -> Umfang (Methode 'Umfang')\n	
In einem agla-Notebook kann explizit mit anderen Python-Paketen gearbeitet 
werden, speziell mit SymPy, von dem einige Anweisungen dem System bereits 
bekannt sind. Soll ein weiteres SymPy-Element benutzt werden, z.B. die Funk-
tion ceiling, so ist dieses mit der üblichen import-Anweisung zu importieren 
und kann danach aufgerufen werden\n	
   In [..]: from sympy import ceiling
            ...
   In [..]: ceiling(3.12)    # das Ergebnis ist 4
        """)		
        return		
		
    if h == 5:
        print(
        """		
Zugriff auf Eigenschaften und Methoden von Objekten\n
Die agla-Objekte haben verschiedene Eigenschaften und Methoden (die letz-
teren erwarten für ihre Ausführung Argumente - ein weiteres Objekt, einen 
Parameterwert o.ä.). Die implementierten Eigenschaften und Methoden eines
Objektes können über die Hilfeseite seiner Klasse, z.B. mit\n
   In [..]: Gerade(h=1)\n
ermittelt werden. Ein Gerade-Objekt g hat z.B. die Eigenschaft richt (Rich-
tungsvektor) und die Methode abstand (Abstand zu einem anderen Objekt). Der 
Zugriff erfogt mittels des '.' - Operators, der allgemein in der Objekt-
orientierten Programmierung Verwendung findet. Sei z.B. e eine Ebene, so 
kann der Zugriff auf die genannte Eigenschaft und die genannte Methode mit
den Anweisungen \n
   In [..]: g.richt \n
und\n		
   In [..]: g.abstand( e ) \n
erfolgen\n		
Eine Methode wird generell über einen Funktionsaufruf realisiert, der Ar-
gumente erwartet, die in Klammern eingeschlossen werden. Hier wurde das Ar- 
gument e angegeben, es soll der Abstand der Geraden g zur Ebene e ermit-
telt werden\n
Zu einigen Eigenschaften existiert eine Methode mit gleichem Namen, der auf 
einen Unterstrich '_' endet. Damit besteht die Möglichkeit, mittels des ent-
sprechenden Funktionsaufrufes zusätzliche Informationen/Leistungen anzufor-
dern. Welche das sind, kann über die Hilfeanforderung (h=1 als letzter Ein-
trag in der Argumentliste) erfahren werden. Diese zu Eigenschaften gehö-
renden Methoden können auch über den Namen der Eigenschaft mit großem An-
fangsbuchstaben aufgerufen werden, also z.B. für die Eigenschaft prg von g\n		
   In [..]: g.prg_(...)       oder
   In [..]: g.Prg(...)\n		
Das Ergebnis eines Eigenschafts-/Methodenaufrufes kann ein Tupel oder eine
Liste sein, etwa die beiden Richtungsvektoren einer Ebene e, die mit\n
   In [..]: e.richt\n
erhalten werden. Um auf ein einzelnes Element zuzugreifen, wird der Index-
zugriff verwendet\n	
   In [..]: e.richt[0]        bzw.
   In [..]: e.richt[1]\n
Zu beachten ist, dass die Zählung gemäß der Python-Konvention bei 0 beginnt		
        """)		
        return		
		 						
    if h == 6:
        print(
        """		
Klassen im Raum R^3\n		
Vektor  / = Punkt
Gerade
Ebene
Kugel
Parallelogramm  / = ParGramm
Spat
Strecke		
Dreieck		
Viereck
Kreis
Pyramide
Prisma
Kegel
Zylinder
Körper		
Matrix		
Abbildung
Kurve
Fläche2terOrdnung  / = F2O
Fläche
\nPunkte werden mit ihren Ortsvektoren identifiziert		
        """)		
        return
     
    if h == 7:
        print(
        """		
Klassen in der Ebene R^2\n		
Vektor  / = Punkt
Gerade
Parallelogramm  / = ParGramm
Strecke		
Dreieck		
Viereck
Figur
Kreis
Matrix		
Abbildung
Ellipse
Hyperbel
Parabel		
Kurve2terOrdnung  / = KegelSchnitt / = K2O
Kurve
\nPunkte werden mit ihren Ortsvektoren identifiziert		
        """)		
        return
	 
    if h == 8:
        print(
        """		
Andere Klassen\n		
Vektor  / = Punkt  (Komponentenanzahl > 3)
Matrix (Zeilenanzahl > 3)
LinearesGleichungssystem  / = LGS
Gleichung
\nKlassen der sphärischen Geometrie		
sPunkt		
sGerade
sStrecke
sDreieck
sZweieck		
sKreis
\nKlassen der hyperbolischen Geometrie
hPunkt
hGerade
hStrahl
hStrecke		
hDreieck
hKreis		
        """)		
        return
		
    if h == 9:
        print(
        """		
Funktionen in agla\n		
Allgemeine Funktionen\n		
Hilfe         Hilfefunktion
determinante  Determinante  / = det
linear_abh    Test auf lineare Abhängigkeit  / = linearAbh
kollinear     Test auf Kollinearität
komplanar     Test auf Komplanarität		
parallel      Test auf Parallelität		
orthogonal    Test auf Orthogonalität  / = senkrecht
identisch     Test auf Identität
Abstand       Abstand zweier Objekte
Winkel        Winkel zwischen zwei Objekten
Lage          Lage zweier Objekte		
löse          Allgemeiner Gleichungs-Löser			
einfach       Vereinfachen von Objekten
Grafik        Zeichnen von Grafiken  / = zeichne
sicht_box     Einstellen des Sichtbereiches einer Grafik  / = sichtBox
farben        Liste der Farben in Grafiken\n
Abbildungen der Modelle der hyperbolischen Geometrie\n
D2H           D-Modell -> H-Modell
D2D3          D-Modell -> D3-Modell
H2D           H-Modell -> D-Modell
H2D3          H-Modell -> D3-Modell
D32D          D3-Modell -> D-Modell
D32H          D3-Modell -> H-Modell\n
Mathematische Funktionen\n
sqrt, exp, log, ln, lg, abs
sin, arcsin /= asin, sing, arcsing /= asing     / ...g: 
cos, arccos /= acos, cosg, arccosg /= acosg     / Funktionen
tan, arctan /= atan, tang, arctang /= atang     / mit Grad-
cot, arccot /= acot, cotg, arccotg /= acotg     / werten
sinh, arsinh /= asinh	
cosh, arcosh /= acosh	
tanh, artanh /= atanh
deg           Umrechnung Bogen- in Gradmaß /= grad		
rad           Umrechnung Grad- in Bogenmaß /= bog	
kug_koord     Umrechnung in Kugelkoordinaten /= kugKoord			
min           Minimum von zwei oder mehr Zahlen
max           Maximum von zwei oder mehr Zahlen
N             Umwandlung SymPy- in Dezimal-Ausdruck (oder Methode n)    
re            Realteil einer komplexen Zahl
im            Imaginärteil einer komplexen Zahl
conjugate     Konjugiert-komplexe Zahl /= konjugiert\n
Konstanten\n
pi            Zahl Pi (3.1415...)
E             Eulersche Zahl e (2.7182...)
I             Imaginäre Einheit
ja, nein, mit, ohne,  - Hilfsgrößen
Ja, Nein, Mit, Ohne   - für True/False\n
ACHTUNG!  N, E, I sind kommentarlos überschreibbar		
        """)		
        return
		
    if h == 10:
        print(
        """		
Operatoren\n
Folgende Operatoren stehen zusätzlich zu den  Python-Operatoren zur		
Verfügung bzw. ersetzen diese\n		
   ^    Potenzierung; zusätzlich zum Operator **; Umdefinition des
        Python-Operators ^		
   °    Skalarprodukt, Verknüpfung von Abbildungen; zusätzlich zum 		
        Operator *		
   ><   Vektorprodukt; Umdefinition des Python-Operators &
   |    Verkettung von Vektoren; Umdefinition des Python-Operators |		
        """)		
        return
		
    if h == 11:
        print(
        """		
Vordefinierte Abbildungen im Raum R^3\n
parallel_projektion / = projektion / = proj  
               - Parallelprojektion  
kavalier       - spezielle Parallelprojektion
kabinett            / = schrägbild
               - spezielle Parallelprojektion
militär        - spezielle Parallelprojektion
isometrie      - spezielle Parallelprojektion
dimetrie       - spezielle Parallelprojektion		
verschiebung        / = versch / = translation / = trans 
               - Verschiebung	
drehung             / = dreh 
               - Drehung 
drehx          - Drehung um die x-Achse
drehy          - Drehung um die y-Achse
drehz          - Drehung um die z-Achse
spiegelung          / = spieg
               - Spiegelung
spiegxy        - Spiegelung an der xy-Ebene
spiegxz        - Spiegelung an der xz-Ebene
spiegyz        - Spiegelung an der yz-Ebene
spiegO         - Spiegelung am Ursprung
streckung           / = streck
               - Zentrische Streckung		
grundriss      - spezielle Projektion
aufriss        - spezielle Projektion
seitenriss     - spezielle Projektion\n
Vordefinierte Abbildungen in der Ebene R^2\n
verschiebung        / = versch 
               - Verschiebung	
drehung             / = dreh
               - Drehung
drehO2         - Drehung um den Ursprung
spiegelung          / = spieg
               -  Spiegelung
spiegx2        - Spiegelung an der x-Achse
spiegy2        - Spiegelung an der y-Achse
spiegO2        - Spiegelung am Ursprung
streckung           / = streck
               - Zentrische Streckung		
scherung            / = scher
               - Scherung
        """)		
        return		
				
    if h == 12:
        print(
        """		
Verfahren\n		
Verfahren sind für wiederkehrende Aufgaben im Raum R^3 vorgesehen und
sollen den Lernvorgang direkt unterstützen\n
Die Verfahren brauchen nicht weiter erläutert zu werden, sie werden
mit einem einprägsamen Kurznamen aktiviert, der auch ihren Inhalt cha-
rakterisiert\n
Zu ihrem Gebrauch wird empfohlen, die entsprechende Hilfeseite einzuse-
hen, etwa mit\n
   In [..]: AGG(h=1)\n		
Es sind folgende Verfahren implementiert:\n	
AEE  Abstand-Ebene-Ebene			   
AGE  Abstand-Gerade-Ebene			
AGG  Abstand-Gerade-Gerade  Version 0		  
AGG1                     ...Version 1		  
AGG2                     ...Version 2		  
APE  Abstand-Punkt-Ebene    Version 0		   
APE1                     ...Version 1		   
APE2                     ...Version 2		   
APG  Abstand-Punkt-Gerade   Version 0  			
APG1                     ...Version 1  		  		
APG2                     ...Version 2  		   		
APG3                     ...Version 3  		   		
APP  Abstand-Punkt-Punkt	
LEE  Lage-Ebene-Ebene			                
LGE  Lage-Gerade-Ebene      Version 0			                
LGE1                     ...Version 1			                
LGG  Lage-Gerade-Gerade     Version 0			
LGG1                     ...Version 1			
LPD  Lage-Punkt-Dreieck     Version 0			 
LPD1                     ...Version 1    		 
LPE  Lage-Punkt-Ebene			
LPG  Lage-Punkt-Gerade			
LPV  Lage-Punkt-Viereck
LPK  Lage-Punkt-Kugel			
LGK  Lage-Gerade-Kugel			
LEK  Lage-Ebene-Kugel			
WEE  Winkel-Ebene-Ebene			
WGE  Winkel-Gerade_Ebene			
WVV  Winkel-Vektor-Vektor\n	
Auf Ebenen bezogene Verfahren
ERV   Richt-Vektor         = RV    Ermittlung von 2 Richtungsvektoren	
ENV   Norm-Vektor-Version0 = NV    Ermittlung eines Normalenvektors 		
ENV1           ...Version1 = NV1   einer Ebene / zu 2 gegebenen Vektoren			
Umformung von Gleichungen			
EK2P  Ebene-Koord-2-Prg Version 0  Koordinatenform -> Parameterform	    
EK2P1                ...Version 1  ebenso		    
EN2P  Ebene-Nf-2-Prg               Normalenform -> Parameterform				  
EP2K  Ebene-Prg-2-Koord Version 0  Parameterform -> Koordinatenform		   
EP2K1                ...Version 1  ebenso		  
EP2N  Ebene-Prg-2-Nf               Parameterform -> Normalenform\n
( '2' = 't(w)o' )
        """)		
        return		
		
    if h == 13:
        print(
        """		
Jupyter-Notebook

+==================================================================+
| Um in einem Notebook mit agla arbeiten zu können, muss zu        | 
| Beginn der Sitzung die (Jupyter-) Anweisung                      |
|                                                                  |
|    In [..]: %run agla/start                                      |
|                                                                  |
| in einer Codezelle ausgeführt werden                             |
+==================================================================+
		
agla benutzt als Bedienoberfläche Jupyter. Dieses wurde unter dem 
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
      Anweisungen zur Benutzung von agla; die Zellen sind analog zu 
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
			
				
    if h == 14:
        print(
        """		
3D-Grafiken (Mayavi)\n	
Grafiken werden mittels der Anweisung\n
   In [..]: Grafik(...)   bzw.   zeichne(...)\n
hergestellt. Siehe dazu Grafik(h=1) und Hilfeseite zu Grafik-Spezifikatio-
nen\n
Das Zeitverhalten ist bei einigen Grafiken nicht akzeptabel. Das wird sich
durch den vorgesehenen Einsatz von VisPy (ein schnelles Python-Grafikpro-
gramm) sowie des schnellen CAS SymEngine (es ist in C++ geschrieben und hat
eine SymPy/Python-Anbindung) mittelfristig ändern. Beide Pakete befinden 
sich seit 2012 bzw. 2013 in der Entwicklung\n\n
Bemerkungen zu Windows-Anwendungen\n		
Es kann immer nur eine Grafik (in einem eigenen Fenster) offen sein\n
Ist eine Grafik offen, werden unter der entsprechenden Zelle des Note-
books liegende Zellen erst dann ausgeführt, wenn das Fenster mit der 
Grafik geschlossen wurde\n
Tastatur- und Maus-Bedienung einer Grafik:\n
   Linke-Maus-Taste gedrückt lassen und ziehen - Drehen der Kamera	
      zusätzlich Umsch-Taste gedrückt lassen - Verschieben der Grafik	
      zusätzlich Strg-Taste gedrückt lassen - Drehen der Grafik um die 
                                              Kameraachse		
      zusätzlich Umsch+Strg-Tasten gedrückt lassen - Ein-/Auszoomen 	
   Rechte-Maus-Taste gedrückt lassen und ziehen - Ein-/Auszoomen 		
   Mittlere-Maus-Taste gedrückt lassen und ziehen - Verschieben der Grafik	
   Mausrad drehen- Ein-/Auszoomen der Grafik 		
        """)		
        return
  
    if h == 15:
        print(
        """		
2D-Grafiken (matplotlib)\n	
Grafiken werden mittels der Anweisung\n
   In [..]: Grafik(...)   bzw.   zeichne(...)\n
hergestellt. Siehe dazu Grafik(h=1) und Hilfeseite zu Grafik-Spezifikatio-
nen\n
Es können beliebig viele Grafiken in einem Notebook (eingebettet) platziert 
werden\n
Die Vergrößerung einer Grafik kann durch das Zoomen des gesamten Notebooks
erreicht werden\n
Beim Drücken der rechten Maus-Taste wid ein Kontext-Menü mit weiteren Ak- 
tionen geöffnet 
        """)
        return

    if h == 16:
        print(
        """		
Grafik-Spezifikationen\n		
Angaben für ein Objekt obj\n		
   obj = Vektor     /[ vekt ] /[, farbe ] /[, stärke ]
                    bei Angabe von vekt Zeichnen des Vektors obj, im
                    Punkt vekt beginnend, sonst Zeichnen des Punktes
                    obj
       = Gerade     /[ farbe ] /[, stärke ]
       = Ebene      /[ farbe ]
       = Kugel      /[ farbe ]
       = Strecke    /[ farbe ] /[, stärke ]
       = Dreieck    /[ farbe ] /[, stärke ] 
                    bei 'füll=ja' Füllen des Dreiecks
       = Viereck    /[ farbe ] /[, stärke ]  
                    bei 'füll=ja' Füllen des Vierecks
       = Kreis      /[ farbe ] /[, stärke ]  
                    bei 'füll=ja' Füllen des Kreises
       = ParGramm   /[ farbe ] /[, stärke ]
       = Spat       /[ farbe ] /[, stärke ]
       = Pyramide   /[ farbe ] /[, stärke ]  
                    bei 'füll=ja' Füllen der Pyramide
                    bei 'kanten=nein' kein Zeichnen der Kanten		
       = Prisma     /[ farbe ] /[, stärke ]  
                    bei 'füll=ja' Füllen des Prismas
                    bei 'kanten=nein' kein Zeichnen der Kanten
       = Kegel      /[ farbe ]
       = Zylinder   /[ farbe ]
       = Körper     /[ farbe ] /[, stärke ]
                    bei 'füll=ja' Füllen des Körpers
                    bei 'kanten=nein' kein Zeichnen der Kanten
       = K2O        /[ farbe ] /[, stärke ]
       = Ellipse    /[ farbe ] /[, stärke ]
                    bei 'füll=ja' Füllen der Ellipse
       = Hyperbel   /[ farbe ] /[, stärke ]
       = Parabel    /[ farbe ] /[, stärke ]
       = Kurve      /[ farbe ] /[, stärke ]
                    für Raumkurven:
                    bei 'fein=ja'   verfeinerte Darstellung
                        'fein=n'    n-Anz. d. Stützst.; Standard 100
                    bei 'radius=ja' Darstellung als Röhre
                        'radius=wert' ebenso; Standard 0.02		
                    für Kurven in der Ebene mit impliziter Gleichung:
                    bei 'punkte=(nx, ny)' 
                                    Festlegen der Punktdichte in x-
                                    und y-Richtung; Standard 300
       = Fläche     /[ farbe ]
                    für Flächen mit Parametergleichung:		
                    bei 'gitter=ja' Zeichnen eines Flächengitters
                        'gitter=(nu, nw)' ebenso; Anz. d. u-,w-Linien 
                                          Standard 12
                    bei 'draht=ja' Zeichnen eines Drahtgitters
                        'draht=(nu, nw)' ebenso; Anz. d. u-,w-Linien
                                         Standard 12
                    für Flächen mit impliziter Gleichung:		
                    bei 'punkte=(nx, ny, nz)' Festlegen der Punktdichte
                                in x-,y- und z-Richtung, Standard 100
       = F2O        /[ farbe ]
       = sPunkt     /[ farbe ] /[, stärke ]
       = sGerade    /[ farbe ] /[, stärke ]
       = sStrecke   /[ farbe ] /[, stärke ]
       = sDreieck   /[ farbe ] /[, stärke ]
       = sZweieck   /[ farbe ] /[, stärke ]
       = sKreis     /[ farbe ] /[, stärke ]
       = hPunkt     /[ farbe ] /[, stärke ]
       = hGerade    /[ farbe ] /[, stärke ]
       = hStrecke   /[ farbe ] /[, stärke ]
       = hStrahl    /[ farbe ] /[, stärke ]
       = hDreieck   /[ farbe ] /[, stärke ]
       = hKreis     /[ farbe ] /[, stärke ]\n
   farbe   zu möglichen Farbangaben siehe farben()
           Standard: Punkte und Linien schwarz,
                     Flächen grün\n
   stärke  1, 2 oder 3  (Punkt-/Linienstärke)
           Standard: 1\n
Zusätzliche Anweisungen zur Gestaltung von 3D-Grafiken\n	
   achsen     = nein - Abschalten der Achsen 
              = (bez_x, bez_y, bez_z) - Bezeichner der Achsen 
   box        = nein - Abschalten der Box
   xy_gitter  = ja   - Anschalten eines Gitters in der xy-Ebene
   xyz_gitter = ja   - Anschalten eines 3-seitigen Gitters
   skalen     = nein - Abschalten der Skalen
   x_skala    = nein - Abschalten der x-Skala
   y_skala    = nein - ebenso y-Skala
   z_skala    = nein - ebenso z-Skala	
   text = Tupel aus Elementen der Form (vekt, 'text' /[, text_größe ])
              vekt - Positions-Vektor/Punkt
              text_größe - {1:kleiner, 2:größer}
   bez - wie text\n
Zusätzliche Anweisungen zur Gestaltung von 2D-Grafiken\n
   achsen     = nein - Abschalten der Achsen 
              = (bez_x, bez_y) - Bezeichner der Achsen 
   gitter     = ja   - Anschalten eines Gitters
   skalen     = nein - Abschalten der Skalen
   x_skala    = nein - Abschalten der x-Skala
   y_skala    = nein - ebenso y-Skala
   größe = (x, y)    - Größe der Grafik; Standard = (8, 6)
   text = Tupel aus Elementen der Form (vekt, 'text' /[, text_größe ])
              vekt - Positions-Vektor/Punkt
              text_größe - {1:kleiner, 2:größer}
   bez - wie text\n
Anstelle von ja kann synonym Ja, mit, Mit oder True verwendet werden,
anstelle von nein - Nein, ohne, Ohne oder False\n	
Zusätzliche Anweisungen können auch in ' ' eingeschlossen werden		
        """)		
        return	
	
    if h == 17:
        print(
        """		
Animationen\n	
Animationen sind gegenwärtig nur in 3D möglich (mit Mayavi), sie befinden   		
sich in einem experimentellen Stadium\n
Animierte Grafiken sind für folgende Klassen im Raum R^3 implementiert:\n	
    Vektor (nur Punktdarstellung)
    Gerade
    Ebene
    Kugel
    Strecke
    Dreieck
    Viereck                                             
    Kreis 
    Kegel
    Zylinder		  
    Körper
    Pyramide
    Prisma		  
    Kurve			                       
    Fläche 
\nEs kann nur ein Parameter (je Objekt) animiert werden. Generell nicht ani-
mierbar sind Pfeile und gefüllte Objekte sowie die Grenzen eines Parameter- 
bereiches. Weitere Einschränkungen sind, dass Kurven nicht verfeinert bzw. 
als Röhre dargestellt und Flächen nicht mit Gitternetz oder als Drahtdar-
stellung animiert werden  können. Des weiteren ist die Bedienung zum Ablau-
fen einer Animation provisorisch\n
Eine Animation wird erzeugt, indem innerhalb einer zeichne-Anweisung in der 
Spezifikation des zu animierenden Objekes eine Angabe zum Parameter in der
Form\n
    ( /[name, ] unten, oben /[, anzahl] )\n
gemacht wird. Hier sind name der Parametername (er kann auch weggelassen 
werden), unten und oben die untere und obere Grenze des Parameterbereiches
 und anzahl die Anzahl der Unterteilungen desselben (bei Weglassen wird der
Standardwert 20 angenommen). Ein Beispiel ist\n
   In [..]: f = Fläche(...)  # mit einem Parameter
   In [..]: zeichne( [ f, gelb, (-3, 3, 200) ] \n		
Das synchrone Ablaufen bei der gleichzeitigen Animation mehrerer Objekte er-
fordert die Übereinstimmung der Angaben zu unten, oben und anzahl\n
Bei der Ausführung öffnen sich zwei Fenster - für die eigentliche Grafik und
ein kleines Bedienfenster, in dem zunächst der 'Delay'-Eintrag von Interesse
ist. Der dort enthaltene große Wert garantiert genügend Zeit, um die beiden 
Fenster in eine günstige Position zu rücken. Die eigentliche Animation wird 
gestartet, indem dieser Wert verringert wird. Dazu wird der Cursor mit der 
Maus am Ende des 'Delay'-Feldes platziert. Dann können mit der Rücktaste ge-
nügend Ziffern gelöscht werden. Eine laufende Animation kann mit den ent-
sprechenden Schaltern gestoppt und wieder gestartet werden. Die Grafik kann 
jederzeit verschoben, gedreht und gezoomt werden\n		
Die Ausführung von weiter unten liegenden Zellen des Notebooks ist erst mög- 
lich, wenn beide Fenster wieder geschlossen wurden
        """)		
        return

    if h == 18:		
        print(
        """		
Nutzung von SymPy-Anweisungen\n
In agla sind folgende Elemente von SymPy integriert:\n		
Symbol, symbols - zur Definition von (mehrstelligen) Bezeichnern
Rational - zur Erzeugung von rationalen Zahlen (wird in agla weitgehend  
automatisch erledigt)\n
solve, solveset, expand, collect, factor, simplify, nsimplify, sympify 
N [der Wert ist überschreibbar]\n
pi - die Kreiszahl
E - die Basis der natürlichen Logarithmen (e) [der Wert ist überschreibbar]
I - die imaginäre Einheit (i) [der Wert ist überschreibbar]\n		
Sollen weitere Elemente benutzt werden, sind diese zu importieren, z.B.\n
   In [..]: from sympy import Piecewise\n
(eventuell ist der Pfad im  SymPy-Verzeichnis-Baum anzugeben)				
        """)		
        return
 
    if h == 19:
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
		
    if h == 20:
        print(
        """		
Kleiner Python-Exkurs\n
Eingabe von Code (in eine Code-Zelle des Jupyter-Notebooks):\n
    Die Ausführung einer Zelle wird u.a. durch Umsch+Enter bzw. 
    Strg+Enter veranlaßt\n		
    Eine Zuweisung (eines Wertes an einen Bezeichner) wird mittels '=' 
    realisiert:\n
        In [..]: a = 4\n
    Der Wert eines Bezeichners kann über eine Abfrage ermittelt werden\n
        In [..]: a\n
    Mehrere Zuweisungen in einer Zeile sind durch ';' zu trennen\n				
        In [..]: a = 4; b = 34; c = -8\n
    Mehrere Abfrageanweisungen in einer Zeile sind durch ',' zu trennen				
    (ein ';' unterdrückt die Anzeige der vorausgehenden Elemente)\n				
        In [..]: a, b, c\n
    Eine neue Zeile (innerhalb einer Zelle des Notebooks) wird über die
    Enter-Taste erzeugt; in der neuen Zeile ist ab derselben Stelle zu 
    schreiben wie in der vorangehenden Zeile, wenn nicht ein eingerückter 
    Block entstehen soll (bzw. wenn nicht durch ein '\\' am Zeilenende ei-
    ne Verlängerung der Zeile erreicht werden soll) 
    Das ist Teil der Python-Syntax und führt bei Nichtbeachten zu einem
    Syntaxfehler\n   		
    Eingerückte Blöcke sind z.B. bei Kontrollstrukturen (vor allem in Pro-
    grammen benutzt) erforderlich. Dabei müssen alle Einrückungen die glei-
    che Stellenanzahl (standardmäßig 4 Stellen) haben\n
    Bei der if-else-Anweisung sieht das z.B. folgendermaßen aus:\n
        In [..]: if a < 1: 
                     b = 0        # 4 Stellen eingerückt
                     c = 3        # ebenso		
                 else:
                     b = 1        # ebenso\n		
    oder bei einer Funktions-Definition:\n				
        In [..]: def kugel(r):
                     m = v(1, 2, 0)				
                     return Kugel(m, r)\n			
        Die Funktion definiert eine Schar von Kugeln mit festem Mittelpunkt  
        und dem Radius r als Parameter, jeder Aufruf erzeugt eine konkrete
        Instanz der Klasse Kugel\n
        In [..]: k3, k5 = kugel(3), kugel(5)\n		
    Mittels '#' können in Codezellen Kommentare geschrieben werden, sie wer-
    den bei der Ausführung ignoriert\n
Einige Datentypen:\n
    Zeichenkette (string)   z.B.:  'Tab23' \n
    Tupel (tuple)   z.B.: \n 
        In [..]: t = ( 1, 2, 3 ); t1 = ( 'a', a, Rational(1, 2), 2.7 )\n
        Zugriff auf Elemente  t[0], t1[-1], Slicing   (Zählung ab 0)\n
    Liste (list)   z.B.:\n  
        In [..]: L = [ 1, 2, 3 ]; L1 = [ 'a', a, Rational(1, 2), 2.7 ]\n 		
        Zugriff auf Elemente  L[0], L1[-1], Slicing   (Zählung ab 0)\n
    Schlüssel-Wert-Liste (dictionary, dict)   z.B.:\n
        In [..]: d = { a:4, b:34, c:-8 }\n
        Zugriff auf Elemente  d[a], d[c]\n
    Menge (set)   z.B.: \n 
        In [..]: m = { a, b, c };  m1 = set() (leere Menge)\n
        Zugriff auf Elemente  m.pop(), Indexzugriff mit list(m)[index] mög-
        lich\n		
Weitere nützliche Python-Elemente:\n
    Mittels type(obj) kann der Datentyp eines Objektes obj erfragt werden\n		
    List-Comprehension\n
        In [..]: tup = 1, 2, 3, 4, 5, 6  # oder anderer Datencontainer\n
        In [..]: [ x^2 for x in tup ]    # sehr mächtige Anweisung	
        Out[..]: [1, 4, 9, 16, 25, 36] \n	
    Funktionsdefinition mit anonymer Funktion\n
        lambda arg1, arg2, ... : ausdruck in arg1, arg2, ...\n
    Klasse Rational: da p/q in Python (und damit auch in SymPy) eine float-
        Zahl ergibt, kann bei Bedarf eine rationale Zahl Rational(p, q) ver-
        wendet werden (in agla erfolgt das an den meisten Stellen automa-
        tisch)\n 		
    *liste als Argument einer Funktion packt den Container liste aus\n        
    Ersetzen des Wertes eines Bezeichners in einem Ausdruck durch
        einen anderen Wert (eine SymPy-Anweisung)\n  
        ausdruck.subs(bez, wert)\n
        In [..]: (x+y).subs(x, 2)		
        Out[..]: y+2\n
    Die Ausgabe '<bound method ...>' weist auf eine an ein Objekt gebundene 
        Methode (eine Funktion) hin, die zu ihrer Ausführung in Klammern ein-
        gefasste Parameter erwartet		
        """)		
        return
 
    if h == 21:
        print(
        """		
Bemerkungen für Programmierer / Entwickler\n
Zur Unterstützung der Fehlersuche ist im Hauptprogramm die Variable _TEST
vorgesehen, die im Quelltext geändert werden kann; bei _TEST = True werden
bei Fehlern die vollständigen Python-Fehlermeldungen angezeigt\n
Durch das agla-Paket wird die Python-Sprache an einigen Stellen modifiziert
(Umdefinition der Operatoren '^' und '|', Unterbinden der Zuweisung eines
Wertes an die Eigenschaft/Methode eines Objektes ('objekt.eigenschaft = wert'-
Konstrukt), Verwenden der deutschen Umlaute in Bezeichnern). Bei Änderungen
oder Ergänzungen der agla-Quelltexte dürfen diese Modifizierungen nicht
benutzt werden. Ebenso ist es nicht ratsam, innerhalb eines agla-Notebooks
eine allgemeine Python-Programmierung durchzuführen\n
Aus der Sicht des Autors sollten die Schwerpunkte der weiteren Entwicklung 
des Paketes sein:\n		
   - Konfiguration der Jupyter-Oberfläche entsprechend den Bedürfnissen von 
     Lehrern und Schülern\n
   - Vereinheitlichung der Schriftart und -größe für Ausgaben\n	 
   - Verbesserung der Fehlermeldungen für die Benutzer\n		
   - Verwendung eines Parsers\n  
   - Konsequente Nutzung der OOP, speziell bei den Grafik-Routinen\n
   - Einsatz von VisPy für 3D nach Vorliegen einer stabilen Version
     Die entsprechenden Grafik-Methoden sind zu entwickeln; ihre Aktivierung
     erfolgt im Quelltext mittels der grafik_3d-Methode des Umgebung-Objektes\n		
   - Einsatz von VisPy für 2D nach Vorliegen einer stabilen Version\n  
   - Animationsfähigkeit aller 3D- und 2D-Objekte (einschließlich sphäri-
     sche und hyperbolische Geometrie) mittels VisPy\n		
   - Einbinden des schnellen C++-Paketes SymEngine; an einer Stelle 
     (Modul hyp_geometrie) ist SymEngine-Code enthalten, der aktuell 
     lediglich Probezwecken dient\n	
   - Bessere Verknüpfung der Dokumentation mit den Programmen	 		
   - Verbesserung der Fehlererkennung und -mitteilung	 
        """)		
        return		

    if h == 22:
        print(
        """		
Sphärische Geometrie in agla\n			
Die agla-Klassen der sphärischen Geometrie tragen experimentellen		
Charakter; die Rechenzeiten sind teilweise sehr lang\n		
Literatur:\n		
I. Agricola, Th. Friedrich, Elementargeometrie, Vieweg+Teubner, 2009		
Ch. Bär, Elementare Differentialgeometrie, De Gruyter, 2010		
        """)		
        return		
		
    if h == 23:		
        print(
        """		
Hyperbolische Geometrie in agla\n
Die agla-Klassen der hyperbolischen Geometrie tragen experimentellen	
Charakter\n		
Sie dienen dazu, hyperbolische Objekte rechnerisch zu erzeugen und sie	
grafisch darzustellen; die Rechenzeiten können relativ lang sein\n		
Es werden folgende Modelle unterstützt (die Bezeichnungen unterscheiden 
sich eventuell von den Bezeichnungen in anderen Quellen)\n	
   D  - EinheitsKreisScheiben-Modell
   H  - HyperboloidHalbSchalen-Modell im R^3
   D3 - D-Modell in der xy-Ebene des R^3 (zur gemeinsamen Betrachtung
        von D- und H-Modell vorgesehen) 
   E  - Halbebenen-Modell in der oberen Halbebene des R^2
        (hier als Hilfsmodell benutzt; bei Berechnungen im E-Modell 
        werden für die Transformationen D <-> E-Modell die Cayley-
        Transformationen benutzt)\n
Außer Punkten sind aktuell keine hyperbolischen Objekte mit Parametern
möglich\n
Die Berechnungen der Objekte erfolgen standardmäßig nummerisch (nicht
exakt), die symbolische Berechnung kann mit einem Schlüsselwortparameter
erreicht werden. Für ihre Methoden ist dieser Parameter nicht vorgesehen\n		
Literatur:\n
I. Agricola, Th. Friedrich, Elementargeometrie, Vieweg+Teubner, 2009
S. Rosebrock, Geometrische Gruppentheorie, Vieweg+Teubner, 2010
Ch. Bär, Elementare Differentialgeometrie, De Gruyter, 2010
C. Augat, Über die Modelle der hyperbolischen Geometrie, 1996
     http://augat.zsg-rottenburg.de/zula.pdf
     (Zugriff 6.3.2018)
U. Zürn, Vergleich der Dreiecksgeometrie in der Euklidischen und 
     Hyperbolischen Ebene
     http://math.uni-tuebingen.de/user/loose/studium/Diplomarbeiten/SA.Zuern.pdf 
     (Zugriff 6.3.2019)
D. Lind, Nichteuklidische Geometrie, Bergische Universität Wuppertal
     ww2.math.uni-wuppertal.de/~lind/NE_Skript.pdf
     (Zugriff 6.3.2019)\n
Gekrümmte Welten
Gruppenleiter:
   Jörg Kramer       Humboldt-Universität zu Berlin
   Anna v. Pippich   Humboldt-Universität zu Berlin					
Teilnehmer:
   6 Schülerinnen und Schüler aus der 
   Andreas-Oberschule, Berlin
   Herder-Oberschule, Berlin
   Heinrich-Hertz-Oberschule, Berlin
   http://didaktik.mathematik.hu-berlin.de/files/2012_pippich.pdf   
   (Zugriff 26.1.2019)
        """)		
        return		 
		
  
# ---------------------------              
# Hilfsklasse für Gleichungen 
# ---------------------------              

class Gleichung(AglaObjekt):   
    """
	
Hilfsklasse für Gleichungen
	
**Erzeugung** 
	
   Gleichung ( *li_seite /[ re_seite, ]* ) 
      
**Parameter**

   *li_seite* : linke Seite; nummerischer oder Vektorausdruck
		
   *re_seite* : rechte Seite; ebenso; bei Weglassen 0 bzw. Nullvektor 

**Operatoren**

   Sie werden auf beide Seiten einer Gleichung angewendet		

   +--------+------------------------------------------------------+   
   | ``+``  | Addition eines Skalars bzw. Vektors                  |
   +--------+------------------------------------------------------+   
   | ``-``  | Negation oder Subtraktion eines Skalars bzw. Vektors |
   +--------+------------------------------------------------------+   
   | ``*``  | Multiplikation mit einem Skalar                      |
   +--------+------------------------------------------------------+   
   | ``/``  | Division durch einen Skalar                          |
   +--------+------------------------------------------------------+   
   | ``^``  | Potenzieren  mit einem Skalar                        |
   +--------+------------------------------------------------------+   
   | ``**`` | ebenso                                               |
   +--------+------------------------------------------------------+  

   Außer bei einer Negation ist ein Operator grundsätzlich nach der 
   Gleichung zu notieren	

    """
	
    def __new__(cls, *args, **kwargs):    

        if kwargs.get("h") in (1, 2, 3):                         
            gleichung_hilfe(kwargs["h"])		
            return	
	
        printmethod = '_latex'
    
        try:
            if not args:
                raise AglaError("mindestens die linke Seite der Gleichung angeben")	
            if len(args) > 2:
                raise AglaError("nur die beiden Seiten der Gleichung angeben")		
            Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
            lhs = args[0]
            rhs = 0
            if isinstance(lhs, Vektor):
                rhs = lhs.O			
            if len(args) > 1:
                rhs = args[1]
            if not ((is_zahl(lhs) and is_zahl(rhs)) or \
               (isinstance(lhs, Vektor) and isinstance(rhs, Vektor) and \
               rhs.dim==lhs.dim)):
                raise AglaError("nur arithmetische Ausdrücke oder nur Vektoren einer Dimension angeben")		
            return AglaObjekt.__new__(cls, lhs, rhs)
        except AglaError as e:
            print('agla', str(e))
            return
			
    def __str__(self):
        return str(self.lhs) + " = " + str(self.rhs)
		
    def _latex(self, printer):	                          
        return latex(self.lhs) + '=' + latex(self.rhs)		
		
    @property
    def ls(self):
        """Linke Seite"""	
        return self.args[0]
		
    lhs = ls
	
    @property		
    def rs(self):
        """Rechte Seite"""	
        return self.args[1]
		
    rhs = rs		
		
    @property
    def r2l(self):
        """Rechte Seite  nach links bringen"""	
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor			
        if isinstance(self.lhs, Vektor):    
            return Gleichung(self.lhs - self.rhs, self.lhs.O)
        return Gleichung(self.lhs - self.rhs, 0)
		
    rechts2links = r2l	
		
    def __mul__(self, other):
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor			
        if not is_zahl(other):
            print('agla: Zahlenwert als Faktor angeben')
            return
        if isinstance(self, Gleichung) and isinstance(self.lhs, Vektor) and \
            isinstance(other, (float, Float)):
            if self.lhs.dim == 2:
                vvl = Vektor(other*self.lhs.x, other*self.lhs.y, simpl=False)
                vvr = Vektor(other*self.rhs.x, other*self.rhs.y, simpl=False)
            elif self.lhs.dim == 3:
                vvl = Vektor(other*self.lhs.x, other*self.lhs.y, \
                      other*self.lhs.z, simpl=False)
                vvr = Vektor(other*self.rhs.x, other*self.rhs.y, \
                      other*self.rhs.z, simpl=False)
            else:
                return			
            return Gleichung(vvl, vvr)
        return Gleichung(other * self.lhs, other * self.rhs)
		
    def __truediv__(self, other):
        if not is_zahl(other):
            print('agla: Zahlenwert als Divisor angeben')
            return	
        if isinstance(other, (int, Rational)):
            return self.__mul__(nsimplify(1/other))
        return self.__mul__(1/other)
		
    def __add__(self, other):
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor			
        if not ((is_zahl(self.lhs) and is_zahl(other)) or \
            (isinstance(self.lhs, Vektor) \
            and isinstance(other, Vektor) and self.lhs.dim==other.dim)):
            print('agla: als Summand Zahlenwert oder Vektor passender Dimension angeben')
            return			
        return Gleichung(other + self.lhs, other + self.rhs)

    def __neg__(self):
        return Gleichung(-self.lhs, -self.rhs)

    def __pow__(self, other):
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor			
        if not is_zahl(other):
            print('agla: Zahlenwert als Exponent angeben')
            return			
        if isinstance(self.lhs, Vektor):
            print('agla: Potenzieren für Vektoren nicht definiert')
            return			
        return Gleichung(self.lhs**other, self.rhs**other)

    def __sub__(self, other):
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor			
        if not ((is_zahl(self.lhs) and is_zahl(other)) or \
            (isinstance(self.lhs, Vektor) \
            and isinstance(other, Vektor) and self.lhs.dim==other.dim)):
            print('agla: als Summand Zahlenwert oder Vektor passender Dimension angeben')
            return			
        return Gleichung(self.lhs - other, self.rhs - other)

    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften"""
        gleichung_hilfe(3)	
		
    h = hilfe		
	
# Benutzerhilfe für Gleichung

def gleichung_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nGleichung - Objekt\n")
        print("Erzeugung    Gleichung( li_seite /[ re_seite, ] )\n")
        print("                li_seite   linke Seite; nummerischer oder Vektor-")
        print("                           Ausdruck ")		
        print("                re_seite   rechte Seite; ebenso; bei Weglassen 0") 
        print("                           bzw. Nullvektor\n")		
        print("Operatoren")
        print("sie werden auf beide Seiten einer Gleichung angewendet")		
        print("  +  : Addition eines Skalars bzw. Vektors") 
        print("  -  : Negation oder Subtraktion eines Skalars bzw. Vektors") 
        print("  *  : Multiplikation mit einem Skalar")                  
        print("  /  : Division durch einen Skalar")                        
        print("  ** : Potenzieren  mit einem Skalar")                                  
        print("  ^  : ebenso")                                  
        print("  Außer bei einer Negation ist ein Operator grundsätzlich nach der ") 
        print("  Gleichung zu notieren\n")                                  
        print("Zuweisung     g = Gleichung(...)   (g - freier Bezeichner)\n")
        print("Beispiele")
        print("Gleichung(5*x -6, 3)")
        print("Gleichung(r*v(2, 3, -1) + s*v(-3, 4, 2)\n")
        return
		
    if h == 3:              
        print("\nEigenschaften für Gleichung\n")
        print("g.hilfe         Bezeichner der Eigenschaften")
        print("g.h             = g.hilfe")
        print("g.ls            linke Seite")       
        print("g.rs            rechte Seite")       
        print("g.r2l           rechte Seite nach links bringen\n")       
		
		
# -----------------------------
# Hilfsgrössen für True / False
# -----------------------------

Ja = ja = Mit = mit = True
Nein = nein = Ohne = ohne = False
		

