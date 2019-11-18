#!/usr/bin/python
# -*- coding utf-8 -*-


#                                                 
# Abbildung - Klasse  von agla           
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
                                                 


import importlib

from IPython.display import display, Math

from sympy.core.sympify import sympify
from sympy.core.containers import Tuple
from sympy.core.symbol import symbols, Symbol
from sympy.matrices import Matrix as SympyMatrix 
from sympy.printing.latex import latex

from agla.lib.objekte.basis import AglaObjekt
from agla.lib.objekte.vektor import Vektor
from agla.lib.objekte.matrix import Matrix, _einrichten_matrix
from agla.lib.objekte.ausnahmen import *
from agla.lib.funktionen.funktionen import is_zahl, Gleichung, mit_param

_einrichten_matrix()
	
	

# Abbildung - Klasse   
# ------------------

class Abbildung(AglaObjekt):                                      
    """

Abbildung im Raum und in der Ebene
	
**Erzeugung** 
	
   Abbildung (*matrix /[, versch]* ) 
   
**Parameter**

   *matrix* : Matrix der Abbildung (3x3 bzw. 2x2)
   
   *versch* : Verschiebungsvektor; bei Fehlen Nullvektor; zunächst wird eine 
   Abbildung mittels der Matrix durchgeführt, danach die Verschiebung   
	
**Operatoren** 

   ``*``, ``°`` : Verknüpfung zweier Abbildungen
   
      ``abb = abb1 * abb2``  bzw. ``abb = abb1 ° abb2`` ergibt die verknüpfte 
      Abbildung ``abb`` (``abb1`` und ``abb2`` sind Abbildungen; zuerst wird 
      ``abb2`` angewendet, danach ``abb1``)
	
**Vordefinierte Abbildungen**
	
   :ref:`siehe dort <vordefinierte_abbildungen>`
   
    """
		
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            abbildung_hilfe(kwargs["h"])		
            return	
					
        try:         					
            if not 1 <= len(args) <= 2:
                raise AglaError("ein oder zwei Argumente angeben")
            if len(args) == 1:
                matrix = args[0]
                versch = None
            else:
                matrix, versch = args
            if not ( isinstance(matrix, SympyMatrix) and matrix.dim 
                                                in [(2, 2), (3, 3)] ):
                raise AglaError("(2x2)- oder (3x3)-Matrix angeben")
            m0  = Matrix(Vektor(0, 0, 0), Vektor(0, 0, 0), Vektor(0, 0, 0))			
            m02 = Matrix(Vektor(0, 0), Vektor(0, 0))
            if (matrix.dim == (3, 3) and matrix == m0 or
                matrix.dim == (2, 2) and matrix == m02):
                raise AglaError("Null-Matrix ist nicht zulässig")
            if not versch:
                versch = matrix.vekt[0].O
            if not (  isinstance(versch, Vektor) and versch.dim==\
                                                  matrix.anzZeil ):
                raise AglaError("Vektor passender Dimension angeben")
			
        except AglaError as e:
            print('agla:', str(e))
            return
			
        cls.exakt = True			# interne Eigenschaft
        if kwargs.get('exakt') == False:
            matrix = matrix.dez		
            versch = versch.dez			
            cls.exakt = False			
		
        return AglaObjekt.__new__(cls, matrix, versch)
		               			
		
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "Abbildungsschar(" + ss + ")"
        return "Abbildung"			
		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def dim(self):              
        """Dimension"""
        return self.versch.dim
		
    @property
    def matrix(self):
        """Abbildungsmatrix"""
        m = self.args[0]
        spalten = [[m[i,j] for i in range(m.rows)] for j in range(m.cols)]
        if self.exakt:		
            vekt = [Vektor(s) for s in spalten]
        else:			
            vekt = [Vektor(s, simpl=False) for s in spalten]
        return Matrix(*vekt)
					      
    @property			
    def versch(self):              
        """Verschiebungsvektor"""
        a = self.args[1]		
        if self.exakt or mit_param(a):		
            return a
        return a.dez
		
    trans = versch
	
    @property
    def sch_par(self):
        """Parameter einer Schar"""
        m, v = self.matrix, self.versch
        return m.sch_par.union(v.sch_par)
		
    schPar = sch_par
	
    @property		
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) == 1
		
    isSchar = is_schar		

    @property
    def char_poly(self):
        """Charakteristisches Polynom"""
        return self.matrix.char_poly
		
    charPoly = char_poly	
						
    @property
    def eig_wert(self):
        """Eigenwerte"""
        return self.matrix.eig_wert
		
    eigWert = eig_wert
	
    @property
    def eig_vekt(self):
        """Eigenvektoren"""
        return self.matrix.eig_vekt
		
    eigVekt = eig_vekt		
		
    @property
    def inverse(self):
        """Inverse Abbildung"""
        m = self.matrix.inverse
        if not m:
            return		
        vv = -m * self.versch
        return Abbildung(m, vv)

    @property
    def gleich(self):
        """Abbildungsgleichungen"""
        m, v = self.matrix, self.versch
        x, y, z = symbols('x y z')
        xs, ys, zs = symbols("x' y' z'")
        if self.dim == 3:
            glx = m[0,0]*x + m[0,1]*y + m[0,2]*z + v.x
            gly = m[1,0]*x + m[1,1]*y + m[1,2]*z + v.y
            glz = m[2,0]*x + m[2,1]*y + m[2,2]*z + v.z
            return (Gleichung(xs, glx),
                   Gleichung(ys, gly),
                   Gleichung(zs, glz) )			
        glx = m[0,0]*x + m[0,1]*y + v.x
        gly = m[1,0]*x + m[1,1]*y + v.y
        return (Gleichung(xs, glx),
               Gleichung(ys, gly) )
		
    def sch_el(self, *wert, **kwargs):
        """Element einer Schar; für einen Parameter"""
		 
        if not self.is_schar or len(self.sch_par) > 1:
            print("agla: keine Schar mit einem Parameter")
            return			
		
        if kwargs.get('h'):
            print("\nElement einer Abbildungsschar\n")		
            print("Aufruf   abbildung . sch_el( wert )\n")		                     
            print("             abbildung   Abbildung")
            print("             wert        Wert des Scharparameters\n")			
            print("Es ist nur ein Scharparameter zugelassen\n")    
            return 
			
        if len(wert) != 1:
            print("agla: einen Wert für den Scharparameter angeben") 
            return
        p = Tuple(*self.sch_par)[0]
        wert = sympify(*wert)
        if not is_zahl(wert):
            print("agla: Zahlenwert angeben")
            return
        m, vv = self.matrix, self.versch
        if m.has(p):
            m = m.sch_el(wert)
        if vv.has(p):
            vv = vv.sch_el(wert)
        return Abbildung(m, vv)		

    schEl = sch_el

	
    def bild(self, *args, **kwargs):
        """Bild bei der Abbildung"""
		
        if kwargs.get('h'):
            print("\nBild eines Objektes bei der Abbildung\n")		
            print("Aufruf   abb . bild( objekt )\n")		                     
            print("             abb      Abbildung")
            print("             objekt   agla-Objekt mit bild-Mehode\n")
            return 				
			
        if len(args) != 1:
            print("agla: ein Objekt angeben")
            return			
        obj = args[0]
        try:
            ret = obj.bild(self)
        except:
            return None
        return ret			
		
	
    def _kett(self, abb):     
        """Verketten von Abbildungen"""
		
        # Anwendungs-Reihenfolge: 1. self, 2. abb		
		
        if not(type(abb) is Abbildung and abb.dim == self.dim):
            print("agla: eine Abbildung (mit gleicher Dimension) angeben")
            return
        return Abbildung(self.matrix * abb.matrix, self.matrix * abb.versch \
              + self.versch)
	
    # Definition einer Methode zur Realisierung der Operatoren 
    # '*' und '°' zur Verkettung von Abbildungen
    #	
    def __mul__(self, other):   
        if isinstance(other, Abbildung):	
            try:
                if other.dim == self.dim:
                    return self._kett(other) 
                txt = "die Abbildungen haben unterschiedliche Dimension"				
                raise AglaError(txt)
            except AglaError as e:
                print('agla:', str(e))
        else:
            raise AglaError('zwei Abbildungen angeben')
			

    @property					
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        abbildung_hilfe(3)	
		
    h = hilfe		
		
	
# Benutzerhilfe für Abbildung
# ---------------------------

def abbildung_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nAbbildung - Objekt\n")
        print("Erzeugung im Raum R^3 und in der Ebene R^2:\n")
        print("             Abbildung( matrix /[, versch ] )\n")
        print("                 matrix    Matrix der Abbildung (3x3 bzw. 2x2)")
        print("                 versch    Verschiebungsvektor; bei Fehlen Nullvektor")
        print("                           zunächst wird eine Abbildung mittels der Ma-")
        print("                           trix durchgeführt, danach die Verschiebung\n")
        print("Operatoren '*' : Verknüpfung zweier Abbildungen")
        print("           '°' 	 abb = abb1 * abb2  bzw. abb = abb1 ° abb2 ergibt die ver- ")
        print("                 knüpfte Abbildung abb (abb1 und abb2 sind Abbildungen;")
        print("                 zuerst wird abb2 angewendet, danach abb1)\n")
        print("Zuweisung     a = Abbildung(...)   (a - freier Bezeichner)\n")
        print("Beispiel")
        print("m = v(-2, 0, 3) | v(2, -2, 0) | v(5, 2, -1)")
        print("Abbildung(m, v(0, 0, 1))\n")
        return        
		
    if h == 3:   
        print("\nEigenschaften und Methoden (M) für Abbildung\n")
        print("a.hilfe          Bezeichner der Eigenschaften und Methoden")
        print("a.bild(...)   M  Bild eines Objektes")
        print("a.char_poly      Charakteristisches Polynom") 
        print("a.dim            Dimension")
        print("a.eig_vekt       Eigenvektoren") 
        print("a.eig_wert       Eigenwerte")
        print("a.gleich         Abbildungsgleichungen") 
        print("a.inverse        Inverse Abbildung") 
        print("a.is_schar       Test auf Schar")
        print("a.matrix         Abbildungsmatrix") 
        print("a.sch_el(...) M  Element einer Schar")
        print("a.sch_par        Parameter einer Schar")
        print("a.trans          = a.versch")
        print("a.versch         Verschiebungsvektor\n")
        print("Synonyme Bezeichner\n")
        print("hilfe     :  h")
        print("char_poly :  charPoly")
        print("eig_vekt  :  eigVekt")
        print("eig_wert  :  eigWert")
        print("is_schar  :  isSchar")
        print("sch_el    :  schEl")
        print("sch_par   :  schPar\n")
        return
	  		
			
#                  			
# Vordefinierte Abbildungen: siehe lib/funktionen/abb_funktionen 	
#