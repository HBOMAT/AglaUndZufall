#!/usr/bin/python
# -*- coding utf-8 -*-



#                                                 
#  Funktionen für agla-Abbildungen               
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
# Inhalt:
#
#   parallel_projektion    Erzeugung von Parallelprojektionen des R^3
#      spez. Parallelprojektionen   kavalier, kabinett, militaer, isometrie, dimetrie 		
#   verschiebung           Erzeugen von Verschiebungen in R^3 und R^2
#   drehung                Erzeugen von Drehungen in R^3 und R^2
#   spiegelung             Erzeugen von Spiegelungen in R^3 und R^2
#   streckung              Erzeugen von Zentr. Streckungen in R^3 und R^2
#   scherung               Erzeugen von Scherungen in R^2
#   spez. Projektionen (Risse) im R^3   grundriss, aufriss, seitenriss



from IPython.display import display, Math

from sympy.core.symbol import Symbol
from sympy.core.sympify  import sympify
from sympy.core.numbers import pi
from sympy.functions.elementary.miscellaneous import sqrt
from sympy import sin, cos, tan, atan
from sympy.abc import alpha, beta

from agla.lib.objekte.vektor import Vektor
from agla.lib.objekte.gerade import Gerade
from agla.lib.objekte.ebene import Ebene
from agla.lib.objekte.matrix import Matrix
from agla.lib.objekte.abbildung import Abbildung	

from agla.lib.objekte.gerade import (x_achse, y_achse, z_achse, x_achse2, 
   y_achse2)
from agla.lib.objekte.ebene import xy_ebene, xz_ebene, yz_ebene
from agla.lib.funktionen.funktionen import is_zahl, cosg, sing, mit_param



# -------------------
# Parallelprojektion
# -------------------

def parallel_projektion(*args, **kwargs):
    a, b = Symbol('a'), Symbol('b')
    m = Vektor(0, -a*cos(alpha), -a*sin(alpha)).kette(
        Vektor(0, b*cos(beta), -b*sin(beta)),
        Vektor(0, 0, 1))	
    if kwargs.get('h') == 1:
        print("\nparallel_projektion - Funktion\n") 
        print("Erzeugung von Parallel-Projektionen des Raumes R^3 in die " +
		                                       "yz-Ebene")
        print("mittels einer allgemeinen Projektions-Matrix\n")
        print("Aufruf      parallel_projektion(a, b, alpha, beta)\n")
        print("                a, b, alpha, beta   Parameter der Projektion\n")
        print("Es sind auch die Bezeichner proj, projektion erlaubt\n")
        print("Projektionsmatrix")
        s = repr(m).replace(',', '')
        print(s[8:-2])	
        print("\na - Streckfaktor der x-Achse,  b, - Streckfaktor der y-Achse")		
        print("alpha - Winkel der x-Achse mit der negativen y-Achse des yz-Systems")
        print("beta  - Winkel der y-Achse mit der positiven y-Achse des yz-Systems\n")
        print("Vordefinierte Projektionen")
        print("kavalier   = projektion(1/2*sqrt(2), 1, 45, 0)")
        print("schrägbild = kavalier")
        print("kabinett   = projektion(1/2, 1, 45, 0)")
        print("militär    = projektion(1, 1, 60, 30)")
        print("isometrie  = projektion(1, 1, 30, 30)")
        print("dimetrie   = projektion(1/2, 1, 42, 7)\n")
        return
    if len(args) != 4:
        print("agla: vier Argumente angeben")
        return
    for el in args:
        if not is_zahl(el):
            print("agla: es sind nur Zahlenangaben erlaubt")
            return
    aa, bb, al, be = (sympify(args[0]), sympify(args[1]), sympify(args[2]), 
                    sympify(args[3]))
    m = Vektor(0, -aa*cosg(al), -aa*sing(al)).kette(
        Vektor(0, bb*cosg(be), -bb*sing(be)),
        Vektor(0, 0, 1))
    vv = Vektor(0, 0, 0)
    return Abbildung(m, vv)

parallelProjektion = parallel_projektion
proj      = parallel_projektion
projektion = parallel_projektion

kavalier  = parallel_projektion(1/2*sqrt(2), 1, 45, 0)
kabinett  = parallel_projektion(1/2, 1, 45, 0)
schraegbild = kabinett
militaer  = parallel_projektion(1, 1, 60, 30)
isometrie = parallel_projektion(1, 1, 30, 30)
dimetrie  = parallel_projektion(1/2, 1, 42, 7)		


# ------------
# Verschiebung
# ------------
	
def verschiebung(*args, **kwargs):
    if kwargs.get('h') == 1:
        print("\nverschiebung - Funktion\n")
        print("Erzeugung einer Verschiebung um einen Vektor " +
		                           "im Raum R^3 und") 
        print("in der Ebene R^2\n")
        print("Aufruf      verschiebung( vektor )\n")
        print("               vektor   Verschiebungsvektor\n")
        print("Es sind auch die Bezeichner versch, translation, trans erlaubt\n")
        return	
    if len(args) != 1:
        print("agla: ein Argument angeben")
        return		
    vv = args[0]
    if not isinstance(vv, Vektor) and vv.dim in (2, 3):
        print("agla: einen Vektor der Dimension 2 oder 3 angeben")
        return		
    if vv.dim == 3:
        m = Matrix(Vektor(1, 0, 0), Vektor(0, 1, 0), Vektor(0, 0, 1))
    else:
        m = Matrix(Vektor(1, 0), Vektor(0, 1))
    return Abbildung(m, vv)

versch = verschiebung	
translation = verschiebung
trans = verschiebung
	

# --------
# Drehung 
# --------

def drehung(*args, **kwargs):
    if kwargs.get('h') == 1:
        print("\ndrehung - Funktion\n")
        print("Erzeugung von Drehungen des Raumes R^3 und der Ebene R^2\n")
        print("Aufruf      drehung( objekt, winkel )\n")
        print("                objekt   Gerade - Drehachse (im Raum)")
        print("                         Punkt  - Drehzentrum (in der Ebene)")
        print("                winkel   Drehwinkel in Grad\n")
		# intern: exakt=False - nummerische Berechnung
        print("Spezielle Drehungen")
        print("drehx( winkel )   Drehung um die x-Achse (im Raum)")
        print("drehy( winkel )   Drehung um die y-Achse (im Raum)")
        print("drehz( winkel )   Drehung um die z-Achse (im Raum)")
        print("drehO2( winkel )  Drehung um den Ursprung (in der Ebene)\n")
        return
    if len(args) != 2:
        print("agla: zwei Argumente angeben")
        return
    fix, wi = args[0], sympify(args[1])
    if not is_zahl(wi):
        print("agla: für den Winkel eine Zahl angeben")
        return
    wi = wi * pi / 180
    if isinstance(fix, Gerade):
        ev = fix.richt.einh_vekt
        v1, v2, v3 = ev.x, ev.y, ev.z
        d = 1 - cos(wi)		
        # fuer Ursprungsgerade; nach Wikipedia
        if kwargs.get('exakt')==False and not mit_param(wi) and not ev.is_schar:
            m = (Vektor(float(cos(wi)+v1**2*d), float(v2*v1*d+v3*sin(wi)), 
                                                float(v3*v1*d-v2*sin(wi)), simpl=False) |
                 Vektor(float(v1*v2*d-v3*sin(wi)), float(cos(wi)+v2**2*d), 
                                                float(v2*v3*d+v1*sin(wi)), simpl=False) |
                 Vektor(float(v1*v3*d+v2*sin(wi)), float(v2*v3*d-v1*sin(wi)), 
                                                 float(cos(wi)+v3**2*d), simpl=False))
        else:		
            m = (Vektor(cos(wi)+v1**2*d, v2*v1*d+v3*sin(wi), v3*v1*d-v2*sin(wi)) |
                 Vektor(v1*v2*d-v3*sin(wi), cos(wi)+v2**2*d, v2*v3*d+v1*sin(wi)) |
                 Vektor(v1*v3*d+v2*sin(wi), v2*v3*d-v1*sin(wi), cos(wi)+v3**2*d))
        st = fix.stuetz
        vv = Vektor(0, 0, 0)
        abb1 = Abbildung(m, vv)		
        abb = verschiebung(st)._kett(abb1)._kett(verschiebung(-st))
        return abb
    elif isinstance(fix, Vektor) and fix.dim == 2: 
        if kwargs.get('exakt')==False and not mit_param(wi):	
            m = Vektor(N(cos(wi)), N(sin(wi))) | Vektor(N(-sin(wi)), N(cos(wi)))
        else:			
            m = Vektor(cos(wi), sin(wi)) | Vektor(-sin(wi), cos(wi))
        return Abbildung(m, fix - m*fix) 
    else:
        print("agla: eine Gerade (im Raum) oder einen Punkt (in der Ebene) angeben")
        return
		
dreh = drehung	
	
def drehx(winkel):
    return drehung(x_achse, winkel)
def drehy(winkel):
    return drehung(y_achse, winkel)
def drehz(winkel):
    return drehung(z_achse, winkel)	
def drehO2(winkel):
    return drehung(Vektor(0, 0), winkel)	
	

# -----------
# Spiegelung
# -----------

def spiegelung(*args, **kwargs):
    if kwargs.get('h') == 1:
        print("\nspiegelung - Funktion\n")
        print("Erzeugung von Spiegelungen im Raum R^3 und in der Ebene R^2\n")
        print("Aufruf      spiegelung( objekt )\n")
        print("                objekt    Objekt, an dem gespiegelt wird")
        print("                          Punkt, Gerade, Ebene  (im Raum)")
        print("                          Punkt, Gerade (in der Ebene)\n")
        print("Es ist auch der Bezeichner spieg erlaubt\n")
        print("Spezielle Spiegelungen")
        print("spiegxy   Spiegelung an der xy-Ebene (im Raum)")
        print("spiegxz   Spiegelung an der xz-Ebene (im Raum)")
        print("spiegyz   Spiegelung an der yz-Ebene (im Raum)")
        print("spiegx    Spiegelung an der x-Achse (im Raum)")
        print("spiegy    Spiegelung an der y-Achse (im Raum)")
        print("spiegz    Spiegelung an der z-Achse (im Raum)")
        print("spiegO    Spiegelung am Ursprung (im Raum)")		
        print("spiegx2   Spiegelung an der x-Achse (in der Ebene)")
        print("spiegy2   Spiegelung an der y-Achse (in der Ebene)")
        print("spiegO2   Spiegelung am Ursprung (in der Ebene)\n")
        return 
    if len(args) != 1:
        print("agla: ein Objekt angeben")
        return
    obj = args[0]
    if not isinstance(obj, (Vektor, Gerade, Ebene)):
        print("agla: Punkt, Gerade oder Ebene angeben")
        return
    if obj.dim == 3:
        if isinstance(obj, Ebene):
            nv = obj.norm.einh_vekt
            a, b, c = nv.komp
            m = Matrix(Vektor(-a**2+b**2+c**2, -2*a*b, -2*a*c),
                      Vektor(-2*a*b, a**2-b**2+c**2, -2*b*c),
                      Vektor(-2*a*c, -2*b*c, a**2+b**2-c**2))
            abb1 = verschiebung(obj.stuetz)
            abb2 = Abbildung(m, Vektor(0, 0, 0))
            abb3 = verschiebung(-obj.stuetz) 
            return (abb1._kett(abb2))._kett(abb3)
        elif isinstance(obj, Gerade):
            return drehung(obj, 180)			
        elif isinstance(obj, Vektor):
            abb = Abbildung(
                  Matrix(Vektor(-1, 0, 0), Vektor(0, -1, 0), Vektor(0, 0, -1)), 
                  obj * 2)
            return abb
    elif obj.dim == 2:
        if isinstance(obj, Vektor):
            m = Vektor(-1, 0) | Vektor(0, -1)		
            return Abbildung(m, 2 * obj)
        elif isinstance(obj, Gerade):	  # Parallele zur y-Achse		
            if obj.richt.kollinear(Vektor(0, 1)):
                m = Vektor(-1, 0) | Vektor(0, 1)
                ve = Vektor(2*obj.stuetz.x, 0)
                return Abbildung(m, ve) 			
            elif not obj.n:   # Ursprungsgerade
                wi = 2*atan(obj.m)
                m = Vektor(cos(wi), sin(wi)) | Vektor(sin(wi), -cos(wi))
                return Abbildung(m) 
			
            else:   # beliebige Gerade
                if obj.m:
                    abb1 = verschiebung(Vektor(obj.n/obj.m, 0))
                    abb2 = spiegelung(Gerade(obj.m, 0))
                    abb3 = verschiebung(Vektor(-obj.n/obj.m, 0)) 
                else:
                    abb1 = verschiebung(Vektor(0, -obj.n))
                    abb2 = spiegelung(Gerade(0,1,0))
                    abb3 = verschiebung(Vektor(0, obj.n)) 
                abb = abb1._kett(abb2)._kett(abb3)
                return abb			
			
spieg = spiegelung		
		
spiegxy = spiegelung(xy_ebene)
spiegxz = spiegelung(xz_ebene)
spiegyz = spiegelung(yz_ebene)
spiegx2 = spiegelung(x_achse2)
spiegx = spiegelung(x_achse)
spiegy = spiegelung(y_achse)
spiegz = spiegelung(z_achse)
spiegy2 = spiegelung(y_achse2)
spiegO  = spiegelung(Vektor(0, 0, 0))
spiegO2 = spiegelung(Vektor(0, 0))

	
# ---------------------	
# Zentrische Streckung
# ---------------------

def streckung(*args, **kwargs):
    if kwargs.get('h') == 1:
        print("\nstreckung - Funktion\n")
        print("Erzeugung von Zentrischen Streckungen im Raum R^3 und in der Ebene R^2\n")
        print("Aufruf      streckung( zentrum, faktor )\n")
        print("                zentrum    Streckzentrum (Punkt)")
        print("                faktor     Streckfaktor (Zahl)\n")
        print("Es ist auch der Bezeichner streck erlaubt\n")		
        return
    if len(args) != 2:
        print("agla: zwei Argumente angeben")
        return
    zentrum, faktor = args[0], sympify(args[1])
    if not (isinstance(zentrum, Vektor) and is_zahl(faktor)):
        print("agla: Punkt (Streckzentrum) und Zahl (Streckfaktor) angeben")
        return
    if zentrum.dim == 3:
        m = Matrix(
              Vektor(faktor, 0, 0), Vektor(0, faktor, 0), Vektor(0, 0, faktor))
    elif zentrum.dim == 2:
        m = Matrix(Vektor(faktor, 0), Vektor(0, faktor))
    else:
        print("agla: einen Punkt des Raumes oder der Ebene angeben")
        return
    abb = Abbildung(m, zentrum.O)
    return (verschiebung(-zentrum)._kett(abb))._kett(verschiebung(zentrum))
    
streck = streckung	
	
 		
# ---------		
# Scherung
# ---------

def scherung(*args, **kwargs):
    if kwargs.get('h') == 1:
        print("\nscherung - Funktion\n")
        print("Erzeugung von Scherungen in der Ebene R^2\n")
        print("Aufruf      scherung( winkel )\n")
        print("                winkel   Scherungswinkel in Grad\n")
        print("Es ist auch der Bezeichner scher erlaubt\n")		
        return
    if len(args) != 1:
        print("agla: ein Argument angeben")
        return
    winkel = sympify(args[0])
    if not is_zahl(winkel):
        print("agla: eine Zahl angeben")
        return
    winkel = winkel * pi / 180
    m = Matrix(Vektor(1,0), Vektor(tan(winkel), 1))
    return Abbildung(m)
	
scher = scherung	 
 
 
# -----	
# Risse
# -----
 
grundriss  = Abbildung(Matrix(Vektor(1, 0, 0), Vektor(0, 1, 0), Vektor(0, 0, 0)))
aufriss    = Abbildung(Matrix(Vektor(0, 0, 0), Vektor(0, 1, 0), Vektor(0, 0, 1)))
seitenriss = Abbildung(Matrix(Vektor(1, 0, 0), Vektor(0, 0, 0), Vektor(0, 0, 1)))
  
  