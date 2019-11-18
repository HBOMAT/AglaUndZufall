#!/usr/bin/python
# -*- coding utf-8 -*-



#                                                 
# Umgebung - Klasse  von agla           
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



import numpy as np

from IPython.display import display, Math

from sympy.core.numbers import Integer, Rational, Float, Mul
from sympy.core.sympify import sympify
from sympy.printing import latex	

from agla.lib.objekte.basis import AglaObjekt



class Umgebung(AglaObjekt):
    """Umgebung von agla"""
             
    def __new__(cls, *args, **kwargs): 
	
        # Variable zur Steuerung der Eingabe von Vektoren
        #    bei UMG.SIMPL == False erfolgen keine Umwandlung von 
        #    Vektor-float-Komponenten in rationale sowie Vereinfachungen 
        #    mit einfach    
        cls.SIMPL = True
	
        # Variable zur Steuerung der Berechnung von Objekten
        #    bei UMG.EXAKT == True wird mit SymPy/SYmEngine exakt gerechnet
        #    bei UMG.EXAKT == False wird mit float-Zahlen und numpy-Funktionen 
        #                     gerechnet
        #    mit einfach    
        cls.EXAKT = True
	
        # Sicht-Box
        g = np.float(10)
        cls._sicht_box = np.array([-g, g, -g, g, -g, g])
		
        # default-Farben	
        cls._default_lin_farbe = (0, 0, 0)
        cls._default_pkt_farbe = (0, 0, 0)
        cls._default_flaech_farbe = (0, 1, 0)
        cls._default_lin_farbe2 = (0, 0, 0)
        cls._default_pkt_farbe2 = (0, 0, 0)

        # 3D-Grafik (mayavi / vispy)   durch den Entwickler hier einzustellen
        cls.grafik_3d = 'mayavi'		
		
        return AglaObjekt.__new__(cls)				
				
				
    # Maß zur Skalierung der Grafiken
    def _mass(self):
        return max(abs(self._sicht_box)) / 10
		
    @property		
    def _staerke(self):
        # Einträge im dict: key-Werte 1, 2, 3
        # je key: ( Punkte in R^3, Linien in R^3, Punkte in R^2, Linien in R^2 ) 	
        m = self._mass()
        return {	1 : (0.3*m, 0.5, 4.0, 0.5),    
					2 : (0.5*m, 2.1, 5.0, 1.2), 
					3 : (0.75*m, 4.0, 8.0, 2.5) }  
					
    @property		
    def _default_lin_staerke(self):
        return self._staerke[1][1]
		
    @property		
    def _default_pkt_staerke(self):
        return self._staerke[1][0]

    @property		
    def _default_lin_staerke2(self):
        return self._staerke[1][3]
		
    @property		
    def _default_pkt_staerke2(self):
        return self._staerke[1][2]

    # Sichtbox	- Funktion	
    def sicht_box(self, *args, **kwargs):

        if kwargs.get('h'):
            print("\nsicht_box - Funktion\n")
            print("Einstellen des Sichtbereiches für eine Grafik\n")
            print("Aufruf    sicht_box( x )\n")		                     
            print("   oder   sicht_box( /[ xu, xo /[, yu, yo /[, zu, zo ] ] ] )\n")		                     
            print("             xu, xo    untere und obere Grenze auf der x-Achse")
            print("             yu, yo    analog für die y-Achse")
            print("             zu, zo    analog für die z-Achse")
            print("             Der Wert 0 muss in jedem dieser Bereiche enthalten sein\n")			
            print("Ist nur ein Argument x angegeben, wird ein Bereich bestimmt, indem der")
            print("Wert -x dazugenommen wird; dieser Bereich wird für alle Achsen angenommen")		
            print("Sind zwei Argumente angegeben, wird der Bereich aus diesen für alle")
            print("Achsen angenommen")		
            print("Ist kein Argument angegeben, wird die aktuelle Einstellung angezeigt\n")
            return		
		
        def bereichs_kontrolle(a, b):
            a, b = sympify(a), sympify(b)
            if not (isinstance(a, (Integer, Rational, Float)) and \
	                isinstance(b, (Integer, Rational, Float))):
                print("agla: für Bereichsgrenzen Zahlen angeben")
                return
            if a >= b:
                print("agla: es muss untere Grenze < obere Grenze sein")
                return
            if not (a < 0 and  b > 0):
                print("agla: Null muß im Bereich enthalten sein")
                return
            if max(-a, b) > 10000:
                print("der Bereich muß im Intervall [-10000, 10000] liegen")
                return
            return a, b
			
        if not args:
            xl, xr, yl, yr, zl, zr = self._sicht_box
            str0 = lambda s: str(s).strip('0') if \
                  isinstance(s, (Float, float)) else str(s)
            display(Math(latex('('+str0(xl)+',\:'+str0(xr)+',\:\:\: '+str0(yl)+ \
                  ',\:'+str0(yr)+',\:\:\: '+str0(zl)+',\:'+str0(zr)+')')))	
            return 
        elif len(args) == 1:
            a = sympify(args[0])				
            if not isinstance(a, (Integer, Rational, Float)):
                print("agla: für Bereichsgrenzen Zahlen angeben")
                return				
            a = abs(a)				
            ber = bereichs_kontrolle(-a, a)
            if ber is None:
                return
            a, b = float(ber[0]), float(ber[1])
            self._sicht_box = np.array([a, b, a, b, a, b])
        elif len(args) == 2:
            ber = bereichs_kontrolle(args[0], args[1])
            if ber is None:
                return
            a, b = np.float(ber[0]), np.float(ber[1])
            self._sicht_box = np.array([a, b, a, b, a, b])
        elif len(args) in (4,  6):
            berx = bereichs_kontrolle(args[0], args[1])
            if berx is None:
                return		
            ax, bx = float(berx[0]), float(berx[1])
            bery = bereichs_kontrolle(args[2], args[3])
            if bery is None:
                return		
            ay, by = float(bery[0]), float(bery[1])
            if len(args) == 6:
                berz = bereichs_kontrolle(args[4], args[5])
                if berz is None:
                    return		
                az, bz = float(berz[0]), float(berz[1])
            else:
                az, bz = ax, bx		
            self._sicht_box = np.array([ax, bx, ay, by, az, bz])		
        else:
            print("agla: 1, 2, 4 oder 6 Argumente angeben")
            return
		
				
UMG = Umgebung()
sicht_box = UMG.sicht_box	
sichtBox = sicht_box	


