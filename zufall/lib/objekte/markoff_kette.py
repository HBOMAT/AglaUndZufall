#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  MarkoffKette - Klasse  von zufall           
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



import copy
import importlib

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib as mpl

from sympy.matrices import Matrix as SympyMatrix
from sympy import Symbol, Tuple, simplify, nsimplify, N 
from sympy.abc import lamda
from sympy.core.numbers import Integer, Float
from sympy.matrices import Matrix as SympyMatrix
from sympy.core.compatibility import iterable

from zufall.lib.objekte.basis import ZufallsObjekt
#from zufall.lib.objekte.matrix import Matrix 
from zufall.lib.objekte.ausnahmen import ZufallError
from zufall.lib.funktionen.funktionen import stochastisch, loese

from agla.lib.objekte.vektor import  v, Vektor



# -----------------------------------------------------------------------------
#
# Bereitstellung der Matrix-'Klasse'
#
#     (Kopie des Quelltextes aus agla/start)
#  
# -----------------------------------------------------------------------------

"""

agla hat keine eigene Matrix-Klasse (es ist nicht gelungen, die elegantere
Methode, diese durch Vererbung  von einer SymPy-Klasse bereitzustellen, 
zu realisieren). Stattdessen wird direkt die MutableDenseMatrix-Klasse von 
SymPy verwendet, die entsprechend angepasst wird. Somit sind alle Eigen-
schaften und Methoden für diese Matrizen automatisch verfügbar (siehe Sym-
PyDokumentation)

Zur Erzeugung einer Matrix dient die agla-Funktion 'Matrix', die neben der 
in SymPy verwendeten Art auch die Erzeugung über die (Spalten-) Vektoren 
gestattet

Aus Gründen der Kompatibilität mit den anderen agla-Klassen wurden einige 
wenige Eigenschaften/Methoden ergänzt und andere deutsch benannt

Die Multiplikation einer Matrix mit einem Vektor wird mittels Überschreiben 
der __mul__-Methode realisiert, die Verkettung einer Matrix mit einem Vektor 
(Operator '|') mittels  einer dazu definierten __or__-Methode 

Die Anbindung der überschriebenen und eigenen Methoden an die Matrix-Objekte 
erfolgt mittels der Funktion '_einrichten_matrix', die bei Bedarf aufgerufen 
werden kann 

Der Quellcode wurde aus Parformace-Gründen nicht in ein eigenes Modul 
ausgegliedert

"""


# Erzeuger-Funktion für Matrix in agla
# -------------------------------------

def Matrix(*args, **kwargs):  
    """*Funktion zur Erzeugung von Matrizen mit beliebiger Dimension"""
	
    h = kwargs.get("h")		
    if h in (1, 2, 3):                          
        matrix_hilfe(h)		
        return
    elif 	isinstance(h, (Integer, int)):
        matrix_hilfe(1)		
        return
		
    Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor

    # Erzeugen einer SymPy-Matrix auf die übliche Art		
    if iterable(args) and not isinstance(args[0], Vektor):
        m = SympyMatrix(*args, **kwargs)
        for i in range(m.rows):
            for j in range(m.cols):
                try:		
                    m[i, j] = nsimplify(m[i, j])
                except RecursionError:
                    pass				
        return m
		
    # Erzeugen einer SymPy-Matrix anhand der Spaltenvektoren	
    try:		
        if not args:
            raise AglaError('mindestens zwei Vektoren angeben')		
        if isinstance(args[0], (tuple, Tuple, list, set)):
            vektoren = args[0]
            if not type(vektoren) == list:
                vektoren = list(vektoren)
        else: 
            vektoren = list(args) 
        if not all(isinstance(v, Vektor) for v in vektoren):
            raise AglaError('Vektoren angeben')
        if not all(v.dim == vektoren[0].dim for v in vektoren):
            raise AglaError('die Vektoren haben unterschiedliche Dimension')
    except AglaError as e:
        print('agla:', str(e)) 
	
    liste  = [ [k for k in v.komp] for v in vektoren ]
    m, n = vektoren[0].dim, len(vektoren)
    zeilen = [ [liste[i][j] for i in range(n)] for j in range(m) ]	
    M = SympyMatrix(zeilen)
		
    return M						


# Definition eigener Eigenschaften und Methoden
# ---------------------------------------------
#
# die Bindung an die Objekte erfolgt mit der Funktion
# _einrichten_matrix_klasse

@property				
def _anz_zeil(self):   
    """Zeilenanzahl"""
    return self.rows

@property				
def _anz_spalt(self):   
    """Spaltenanzahl"""
    return self.cols

@property				
def _char_poly(self):   
    """Charakteristisches Polynom"""
    if self.cols != self.rows:
        print('agla: keine quadratische Matrix')
        return
    la = Symbol('lamda')
    cp = self.charpoly(x=la)  
    cp = str(cp)
    cp = cp[9 : cp.find(",")]	
    try:	
        return nsimplify(eval(cp))	
    except RecursionError:
        return eval(cp)	
	
@property		
def _D(self):
    """Determinante"""
    if self.cols == self.rows:
        return simplify(self.det())
    print('agla: keine quadratische Matrix')
		
@property		
def _eig_wert(self):
    """Eigenwerte; für 2x2- und 3x3-Matrizen"""
    if self.rows in (2, 3) and self.cols == self.rows:
        loese = importlib.import_module('agla.lib.funktionen.funktionen').loese
	
        L = loese(self.char_poly, lamda)
    else:		
        print('agla: keine 2x2- bzw. 3x3-Matrix')
        return		
    if len(L) == 1:
        return L[lamda]
    else:
        return [l[lamda] for l in L]
		
@property		
def _eig_vekt(self):
    """Eigenvektoren; für 2x2- und 3x3-Matrizen"""
    Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor			
    if self.rows in (2, 3) and self.cols == self.rows:
        L = self.eigenvects()
        if 	not L:
            print("agla: nicht implementiert")
            return			
        ev = []
        for el in L:
            par = el[1]
            vekt = el[2]
            i = 0
            while par:
               ev.append(matrix2vektor(vekt[i]))
               par -= 1
               i += 1
        l = len(str(ev))
        if l > 250:    # Verhinderung der komplexen Ausgabe
                      # Übergang zu nummerischen Werten	
            print('agla: Übergang zur nummerischen Berechnung wegen komplexer Ausgabe')					  
            from sympy import N
            simpl = UMG.SIMPL			
            UMG.SIMPL = False			
            if self.dim[0] == 2:
                ev = [Vektor(N(el.x, 12), N(el.y, 12)) for el in ev]	
            else:
                ev = [Vektor(N(el.x, 12), N(el.y, 12), N(el.z, 12)) for el in ev]			
            UMG.SIMPL = simpl			
        return ev			
    print('agla: keine 2x2- bzw. 3x3-Matrix')

@property		
def _einfach(self):
    """Vereinfachung"""
    m = Matrix(*[v.einfach for v in self.vekt])
    return m
		
@property		
def _inverse(self):
    """Inverse"""
    if self.cols != self.rows:
        print('agla: keine quadratische Matrix')
        return 
    if self.det() == 0:
        print('agla: die Inverse existiert nicht (die Determinante ist = 0)')
        return
    return self.inv()
		
@property		
def _vekt(self):
    """Spaltenvektoren"""
    vekt = []
    Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor			
    for j in range(self.shape[1]):
        vekt.append(Vektor([self[i, j] for i in range(self.shape[0])]))
    return vekt

@property		
def _dez(self):
    """Dezimalausgabe"""
    Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor			
    vekt = []
    for j in range(self.shape[1]):
        vekt.append(Vektor([N(self[i, j]) for i in range(self.shape[0])], simpl=False))
    return Matrix(*vekt)
		
@property		
def _is_schar(self):    
    """Test auf Schar"""
    return len(self.sch_par) == 1
	
@property		
def _sch_par(self):    
    """Scharparameter"""
    p = set()
    for ve in self.vekt:
        p = p.union(ve.sch_par)
    return p					
		
def _sch_el(self, *wert, **kwargs):
    """Element einer Schar; für einen Parameter"""
    if kwargs.get('h'):
        print("\nElement einer Schar von Matrizen\n")		
        print("Aufruf   matrix . sch_el( wert )\n")		                     
        print("             matrix    Matrix")
        print("             wert      Wert des Scharparameters")			
        print("\nEs ist nur ein Scharparameter zugelassen\n")    
        return 			
    schar = any([ve.is_schar for ve in self.vekt])			
    if not schar or len(self.sch_par) > 1:
        print('agla: keine Schar mit einem Parameter')	
        return		
    if not wert or len(wert) != 1:
        print('agla: einen Wert für den Scharparameter angeben') 
        return	
    p = Tuple(*self.sch_par)[0]
    wert = sympify(*wert)
    if not is_zahl(wert):
        print('agla: für den Scharparameter Zahl oder freien Parameter angeben')	
        return		
    try:
        wert = nsimplify(wert)		
    except RecursionError:
        pass	
    vekt = []
    for ve in self.vekt:
        if p in ve.sch_par:
            vekt.append(ve.sch_el(wert))
        else:
            vekt.append(ve)     
    return Matrix(*vekt)
						
@property		
def _hilfe(self):  
    """Bezeichner der Eigenschaften und Methoden"""
    matrix_hilfe(3)	
					
	
# Anbinden der Funktionen an die Matrix-Objekte 
# ---------------------------------------------

def _einrichten_matrix():

    # Überschreiben von Methoden
    #---------------------------

    # Sichern von Original-Methoden:

    matrix_mul = copy.deepcopy(SympyMatrix.__mul__)    
    matrix_rmul	= copy.deepcopy(SympyMatrix.__rmul__)   
    Float_mul 	= copy.deepcopy(Float.__mul__)

    # Definition der Methoden zum Überschreiben:

    def _mul(self, other):  
        """Multiplikation Matrix * Vektor"""
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor		
        if not isinstance(other, Vektor):
            return matrix_mul(self, other)		
        if self.anzSpalt != other.dim:
            print('agla: die Dimensionen sind unverträglich, Multiplikation nicht möglich')
            return
        f = other.vektor2sympy
        m1 = matrix_mul(self, f) 		
        return matrix2vektor(m1)

    def _rmul(self, other):
        """Multiplikation _ZeilenVektor * Matrix"""
        _ZeilenVektor = importlib.import_module('agla.lib.objekte.vektor').\
		                _ZeilenVektor		
        if isinstance(other, _ZeilenVektor):
            m = SympyMatrix(other.args)
            m = m.T
            if m.cols != self.rows:
                print('agla: die Dimensionen sind unverträglich, Multiplikation nicht möglich')
                return
            return matrix_mul(m, self)				
        return matrix_rmul(self, other)            																    

    def _or(self, other):
        """Verkettung einer Matrix mit einem Vektor"""
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor				
        if isinstance(other, Vektor) and other.dim == self.dim[0]:
            vekt = copy.deepcopy(self.vekt)
        else:
            print('agla: Vektor mit passender Dimension angeben')
            return 			
        vekt.append(other)
        return Matrix(*vekt)

		
    # Überschreiben

    SympyMatrix.__mul__ 	= _mul
    SympyMatrix.__rmul__  	= _rmul
    SympyMatrix.__or__		= _or
	
    # Erzeugen eigener Eigenschaften/Methoden
    # ---------------------------------------
    #
    # (Anbinden der Funktionen an die Matrix-Objekte)

    SympyMatrix.hilfe		= _hilfe		
    SympyMatrix.anz_spalt	= _anz_spalt		
    SympyMatrix.anz_zeil	= _anz_zeil		
    SympyMatrix.char_poly	= _char_poly
    SympyMatrix.D			= _D		
    SympyMatrix.dez			= _dez		
    SympyMatrix.dim			= SympyMatrix.shape		
    SympyMatrix.eig_wert	= _eig_wert
    SympyMatrix.eig_vekt	= _eig_vekt
    SympyMatrix.einfach   	= _einfach
    SympyMatrix.inverse		= _inverse
    SympyMatrix.is_schar	= _is_schar
    SympyMatrix.sch_par		= _sch_par
    SympyMatrix.sch_el		= _sch_el
    SympyMatrix.transp		= SympyMatrix.T				
    SympyMatrix.vekt		= _vekt
    SympyMatrix.h			= SympyMatrix.hilfe		
    SympyMatrix.anzZeil		= SympyMatrix.anz_zeil		
    SympyMatrix.anzSpalt	= SympyMatrix.anz_spalt		
    SympyMatrix.charPoly	= SympyMatrix.char_poly		
    SympyMatrix.eigWert		= SympyMatrix.eig_wert
    SympyMatrix.eigVekt		= SympyMatrix.eig_vekt
    SympyMatrix.isSchar		= SympyMatrix.is_schar
    SympyMatrix.schPar		= SympyMatrix.sch_par
    SympyMatrix.schEl		= SympyMatrix.sch_el
				
_einrichten_matrix()


# Benutzerhilfe für Matrix
# ------------------------

def matrix_hilfe(h):
    """Hilfe-Funktion"""
	
    if h == 1:
        print("h=2 - Erzeugung, Operatoren")
        print("h=3 - Eigenschaften und Methoden")
        return
		
    if h == 2:
        print("\nMatrix - Objekt\n")     
        print("Für mxn - Matrizen mit beliebiger Dimension,  m,n >= 2\n")		
        print("Erzeugung     Matrix( vekt1, vekt2, ... )\n")
        print("                 vekt   (Spalten-)Vektor\n")
        print("     oder     vekt1 | vekt2 | ...\n")                 
        print("Alle Vektoren müssen die gleiche Dimension haben\n")
        print("Zuweisung   M = Matrix(...)  bzw.  M = vekt1 | vekt2 ...")
        print("                             (M - freier Bezeichner)\n")
        print("Zugriff auf das Element in Zeile i und Spalte j:\n")
        print("           M[i, j], i=0...m-1, j=0...n-1\n")
        print("           mittels Zuweisung können so auch einzelne Elemente") 
        print("           verändert werden\n")
        print("Operatoren")
        print("  +  : Addition") 
        print("  -  : Negation/Subtraktion") 
        print("  *  : Multiplikation mit einem Skalar")                  
        print("       Multiplikation mit einer Matrix (mit passender Dimension)")
        print("       Multiplikation mit einem Vektor (mit passender Dimension)")
        print("  ** : Potenzieren mit einer ganzen Zahl")   
        print("  ^  : ebenso")   
        print("  |  : Verketten mit einem Vektor (mit passender Dimension)\n")                        
        print("Beispiele")
        print("m  = Matrix(v(1, 2, 3), v(-1, 0, 4))")
        print("m1 = m | v(3, 1, -2)")
        print("2 * m, sqrt(3) * m1")
        print("m1 * m")
        print("m1 * v(x,y,z)")
        print("m3 = m1**(-1); m4 = m1.inverse")
        print("m3, m4")
        print("m3 * m1, m1 * m4\n")	
        print("Vordefinierte Matrizen")
        print("NullMat    Nullmatrix im Raum R^3")
        print("EinhMat    Einheitsmatrix im Raum R^3")
        print("NullMat2   Nullmatrix in der Ebene R^2")
        print("EinhMat2   Einheitsmatrix in der Ebene R^2\n")
        return
		
    if h == 3:
        print("\nEigenschaften und Methoden für Matrix\n")	
        print("Für ein Matrix-Objekt stehen alle Eigenschaften und Methoden")
        print("eines MutableDenseMatrix-Objektes von SymPy zur Verfügung")
        print("(Näheres ist der SymPy-Dokumentation zu entnehmen)\n")		
        print("Die folgenden ausgewählten Eigenschaften/Methoden wurden aus ")
        print("Kompatibilitätsgründen deutsch benannt bzw. ergänzt\n")
        print("Eig./Meth.      in SymPy")
        print("m.hilfe         -                Bezeichner d. Eig./Meth.")
        print("m.anz_spalt     m.cols           Anzahl Spalten")
        print("m.anz_zeil      m.rows           Anzahl Zeilen")
        print("m.char_poly     m.charpoly()     Charakterist. Polynom   (*)")         
        print("m.D             m.det()          Determinante            (*)")
        print("m.dim           m.shape          Dimension")
        print("m.eig_wert      m.eigenvects()   Eigenwerte             (**)") 
        print("m.eig_vekt      ebenso           Eigenvektoren           (**)") 
        print("m.einfach       simplify(m)      Vereinfachung")
        print("m.inverse       m.inv()          Inverse (= m^-1)        (*)")        
        print("m.is_schar      -                Test auf Schar")
        print("m.sch_el(...)   -                Element einer Schar")		
        print("m.sch_par       -                Scharparameter") 
        print("m.transp        m.T              Transponierte")
        print("                m.transpose()    ebenso")
        print("m.vekt          -                Spaltenvektoren\n")
        print("Synonyme Bezeichner\n")
        print("hilfe     :  h")
        print("anz_spalt :  anzSpalt")
        print("anz_zeil  :  anzZeil")
        print("char_poly :  charPoly")
        print("eig_wert  :  eigWert")
        print("eig_vekt  :  eigVekt")
        print("is_schar  :  isSchar")
        print("sch_el    :  schEl")
        print("sch_par   :  schPar")		
        print("\n(*) für nxn Matrizen")
        print("(**) für 2x2- und 3x3-Matrizen\n")
		

# Vordefinierte Matrizen
# ----------------------
		
NullMat 	= SympyMatrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
NullMat2 	= SympyMatrix([[0, 0,], [0, 0,]]) 
EinhMat 	= SympyMatrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
EinhMat2 	= SympyMatrix([[1, 0], [0, 1]]) 


# Hilfsfunktion	
# -------------

def matrix2vektor(m):
    """Konvertierung Matrix --> Vektor"""
    Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor			
    if not isinstance(m, SympyMatrix):
        print('agla: Matrix angeben')
        return
    if m.shape[1] != 1:
        print('agla: die Spaltenanzahl ist > 1, Konvertierung nicht möglich')
        return		
    ve = m.vekt
    return Vektor(*ve)


	
# MarkoffKette - Klasse  
# ---------------------
	
class MarkoffKette(ZufallsObjekt):                                      
    """
	
Markoffkette

**Kurzname** **MK**
	
**Erzeugung** 

   MK( *matrix, start /[, bezeichner ]* ) 

**Parameter**
   	
   *matrix* :  Übergangsmatrix
   
   *start* :   Startvektor

   *bezeichner* : Liste mit den Bezeichnern der Zustände 
   (Zeichenketten / Symbole); falls nicht angegeben, werden die Bezeichner
   ``Z0, Z1, Z2,...`` verwendet   
   		 
    """			
		
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            markoff_kette_hilfe(kwargs["h"])		
            return	
				
        try:
            if not 2 <= len(args) <= 3:
                raise ZufallError('2 oder 3 Argumente angeben')
            mm, st = args[:2]
            if not (isinstance(st, Vektor) and isinstance(mm, SympyMatrix)):
                raise ZufallError('Übergangsmatrix und Startvektor angeben')
            if not stochastisch(st) or not stochastisch(mm):
                raise ZufallError('Übergangsmatrix und Startvektor müssen stochastisch sein')
            if st.dim != mm.dim[0]:				
                raise ZufallError('die Dimensionen von Übergangsmatrix und Startvektor '+ \
                     'sind unverträglich')
            dim = st.dim					 
            if len(args) == 3:
                bez = args[2]			
                if not isinstance(bez, (tuple, Tuple, list)):
                    raise ZufallError('Liste oder Tupel mit Bezeichnern angeben')
                if len(bez) != st.dim:
                    raise ZufallError('die Anzahl der Bezeichner stimmt nicht')
                if not all([isinstance(b, (str, Symbol)) for b in bez]):
                    raise ZufallError('die Bezeichner müssen Zeichenketten oder Symbole sein')
                bez = [Symbol(str(b)) for b in bez] 					
            else: 
                bez = [Symbol('Z_'+str(i)) for i in range(dim)]			
        except ZufallError as e:
            print('zufall:', str(e))
            return
			
        return ZufallsObjekt.__new__(cls, mm, st, bez)

		
    def __str__(self):  
        return "MarkoffKette"		
		
		
# Eigenschaften + Methoden
# ------------------------


    @property
    def dim(self):
        """Dimension (Anzahl der Zustände)"""		
        return self.args[1].dim

    @property
    def matrix(self):
        """Übergangsmatrix"""		
        return self.args[0]
    def matrix_(self, **kwargs):
        """Übergangsmatrix; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nÜbergangsmatrix\n")
            print("Aufruf   m . matrix_( )")		                     
            print("             m   MarkoffKette\n")
            print("Zusatz   b=ja    Ausgabe mit Bezeichnungen\n")			
            return 
        m = self.args[0]	
        if kwargs.get('b'):
            bez = self.args[2]		
            n = m.dim[0]
            spalte1 = Vektor(*[[Symbol('.')] + self.args[2]])
            res = spalte1                		
            for i in range(n):
                vv = Vektor([bez[i], *m.vekt[i].komp])
                res |= vv		
            return res            		
        return m

    Matrix = matrix_
		
    @property
    def start(self):
        """Startvektor"""
        return self.args[1]		

    @property
    def bez(self):
        """Zustandsbezeichner"""
        return self.args[2]		
		
    @property
    def is_regulaer(self):
        """Test auf Regularität"""
        m = self.matrix
        M = m**100
        for i in range(M.dim[0]):        
            for j in range(M.dim[0]):		
                if M[i, j] < 1e-8:
                    return False
        return True					

    isRegulaer = is_regulaer
		
    @property
    def fix_vekt(self):
        """Fixvektor der Matrix / Stationäre Verteilung"""
        m = self.matrix  
        n = m.dim[0]
        X = Vektor(*[Symbol('x_'+str(i)) for i in range(n)])
        lgs = []
        for i in range(n):
            gl = 0
            for j in range(n):
                gl += m[i, j] * X.komp[j]
            lgs += [gl-X.komp[i]]
        gl1 = 0
        for j in range(n):
            gl1 += X.komp[j]
        lgs += [gl1-1]		
        L = loese(lgs)
        if not L[0]:
            return None
        try:
            res = Vektor(*[L[0][Symbol('x_'+str(i))] for i in range(n)])
        except KeyError:	
            print('zufall: nicht vorhanden/hier nicht berechnet')
            return None		
        return res		
		
    fixVekt = fix_vekt    
    stat_vert = fix_vekt
    statVert = fix_vekt
	
    @property
    def grenz(self):
        """Grenzmatrix"""
        fv = self.fix_vekt
        if not fv:
            return None		
        n = self.dim		
        mm = [fv for i in range(n)]
        return Matrix(*mm)
		
		
    def zustand(self, *args, **kwargs): 		
        """Zustandsvektor nach n Schritten"""
        if kwargs:
            print("\nZustandsvektor nach n Schritten\n")
            print("Aufruf   m . zustand( n )\n")		                     
            print("             m    MarkoffKette")
            print("             n    Anzahl Schritte, n>=0\n")			
            return 
        if len(args) != 1:
            print('zufall: ein Argument angeben')
            return		
        n = args[0]			
        if not isinstance(n, (int, Integer)):
            print('zufall: Schrittzahl ganzzahlig angeben')
        if n < 0:
            print('zufall: Schrittzahl muss >= 0 sein')
        return self.matrix**n * self.start            

		
    @property
    def diagr(self):
        """Diagramm"""	

        if self.start.dim > 6:
            print('zufall: bei einer Zustandsanzahl > 7 ist das Diagramm eventuell\nwenig brauchbar')	
			
        from numpy import sqrt, abs, sin, cos, arccos, pi, dot

        def f_arrow(x, y, dx, dy, col, hw, hl):
            return patches.FancyArrow(x, y, dx, dy,
                    lw=lw,                        
                    facecolor=col,
                    edgecolor=col,
                    head_width=hw,
                    head_length=hl,
                    alpha=0.6)

        def text(x, y, wert, col):
            ax.text(x, y, '$' + str(wert) + '$', 
                   color=col, 
                   horizontalalignment='center', 
                   verticalalignment='center',
                   fontsize=8)

        def pfeil(i, j, doppel=None):
    
            A = np.array([*zustand[i]])
            B = np.array([*zustand[j]])    
            t = 1/2/sqrt(dot(B-A, B-A))
            AA = A + t*(B-A)
            BB = A + (1-t)*(B-A) 
            MM = BB - AA
            ll = sqrt(dot(MM, MM))
            wi = abs(arccos(dot(MM, np.array([1, 0])) / ll))
            if MM[1] < -1e-6:
                wi = -wi        
            dx, dy = (ll-0.25)*cos(wi), (ll-0.25)*sin(wi) 
    
            if not doppel:   # einfacher Pfeil  
                arr = f_arrow(AA[0], AA[1], 2/5*dx, 2/5*dy, 'b', 0.0, 0.0)
                arr1 = f_arrow(AA[0]+3.25/5*dx, AA[1]+3.25/5*dy, (2/5-0.25/5)*dx, \
				               (2/5-0.25/5)*dy, 'b', 0.15, 0.25)
                ax.add_patch(arr)
                ax.add_patch(arr1)
                MM = AA + 1/2*MM
                text(*MM, mm[i, j], 'b')
        
            else:   # Doppelpfeil
                MM = AA + 1/2*(BB-AA)
                if sqrt(np.dot(BB-AA, BB-AA)) < 2:
                    dx, dy = 0.8*dx, 0.8*dy				
                arr = f_arrow(MM[0]-0.3*dx, MM[1]-0.3*dy, -0.15*dx, -0.15*dy, \
				              'r', 0.15, 0.25) 
                ax.add_patch(arr)
                arr1 = f_arrow(MM[0]-0.1*dx, MM[1]-0.1*dy, 0.2*dx, 0.2*dy, \
				               'g', 0.0, 0.0) 
                ax.add_patch(arr1)
                arr2 = f_arrow(MM[0]+0.3*dx, MM[1]+0.3*dy, 0.15*dx, 0.15*dy, \
				                  'b', 0.15, 0.25)
                ax.add_patch(arr2)
                text(MM[0]-0.22*dx, MM[1]-0.22*dy, mm[j, i], 'r')                
                text(MM[0]+0.22*dx, MM[1]+0.22*dy, mm[i, j], 'b') 
        mm = self.matrix
        n = self.dim
        R = 3
        r = 0.5
        lw = 1
        f = 0.75
        if n >= 5 or max([len(str(x).replace('_', '')) for x in self.bez]) > 2:
            f = 1
        plt.close('all')    
        fig = plt.figure(figsize=((R+3)*f, (R+3)*f))
        ax = fig.add_subplot(1, 1, 1, aspect='equal')
        ax.axis('off')
        plt.xlim(-R-3, R+3)
        plt.ylim(-R-2, R+2)

        zustand = [(R*sin(t), R*cos(t)) for t in [-i*2*pi/n for i in range(n)]]
        bez = self.bez

        for i in range(n):
            k = patches.Circle(zustand[i], r, 
                      facecolor='#ffff11', 
				         edgecolor=(0,0,0), 
				         alpha=0.5)
            ax.add_patch(k)
            ax.text(*zustand[i], '$'+str(bez[i])+'$', 
                   fontsize=11, 
                   horizontalalignment='center',
                   verticalalignment='center')
    
        for i in range(n): 
            if mm[i, i] > 0:
                ell0 = patches.Arc((zustand[0][0], zustand[0][1]+1.5*r), 1.5*r, 3*r,
                                 theta1=-30, 
                                 theta2=200,
                                 lw=lw+0.2,
                                 edgecolor='g', 
                                 alpha=0.6)
                rot = mpl.transforms.Affine2D().rotate_deg(i/n*360) + ax.transData
                ell0.set_transform(rot)
                ax.add_patch(ell0) 
                arr = f_arrow(-0.37, 3.65, 0.0001, -0.0001*3.9, 'g', 0.15, 0.25)
                arr.set_transform(rot)
                ax.add_patch(arr)
                MM = [zustand[0][0], zustand[0][1]+1.8]
                ax.text(*MM, '$' + str(mm[i, i]) + '$', 
                       color='g',                 
                       transform=rot, 
                       horizontalalignment='center', 
                       verticalalignment='center',
                       fontsize=8)

        dp = []
        for i in range(n):
            for j in range(n):
                if j == i:
                    continue
                if mm[i, j] > 0 and mm[j, i] > 0 and [i, j] not in dp:
                    pfeil(i, j, doppel=True) 
                    dp += [[i, j], [j, i]]
                    continue    
                if mm[i, j] > 0 and mm[j, i] == 0:
                    pfeil(i, j)

        plt.show()		
		
		
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        markoff_kette_hilfe(3)	
		
    h = hilfe					
		
			
def markoff_kette_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
MarkoffKette - Objekt     

Kurzname     MK
		
Erzeugung    MarkoffKette( matrix, start /[, bezeichner ] )

                matrix      Übergangsmatrix
                start       Startvektor
                bezeichner  Liste mit den Bezeichnern der Zustände (Zeichen-
                            ketten); falls nicht angegeben, werden die Be-
                            zeichner z0, z1, z2,... verwendet
							
Zuweisung    m = MK(...)   (m - freier Bezeichner)

Beispiele

mk1 = MK(v(0.48, 0.52)|v(0.83, 0.17), v(1, 0))

m2 = v(0.4, 0.4, 0.2)|v(0, 0.5, 0.5)|v(0.3, 0, 0.7); s2 = v(1/3, 0, 2/3)
mk2 = MK(m2, s2, [A, 'B', C])   # B ist binomial

m6 = Matrix(v(0, 0.5, 0.5, 0, 0, 0), 
            v(0.5, 0, 0, 0.5, 0, 0), 
            v(0, 0.5, 0, 0, 0.5, 0), 
            v(0.5, 0, 0, 0, 0, 0.5), 
            v(0, 0, 0, 0, 1, 0),
            v(0, 0, 0, 0, 0, 1))
s6 = v(0.5, 0.5, 0, 0, 0, 0)
b6 = [w, z, 'ww', 'zz', 'www', 'zzz']			
mk6 = MarkoffKette(m6, s6, b6)
	   """)		
        return        
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für MarkoffKette

m.hilfe            Bezeichner der Eigenschaften und Methoden
m.bez              Bezeichner der Zustände 
m.diagr            Übergangsdiagramm 
m.dim              Dimension (Anzahl der Zustände)
m.fix_vekt         Fixvektor 
m.grenz            Grenzmatrix der Übergangsmatrix 
m.is_regulär       Test auf Regularität 
m.matrix           Übergangsmatrix 
m.matrix_(...)  M  ebenso; zugehörige Methode 
m.start            Startvektor 
m.stat_vert        = m.fix_vekt - Stationäre Verteilung 
m.zustand(...)  M  Zustandsvektor

Synonyme Bezeichner

hilfe       h
fix_vekt    fixVekt
is_regulär  isRegulär
matrix_     Matrix
stat_vert   statVert
    """)		
        return
	
	
MK = MarkoffKette


