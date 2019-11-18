#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  SkatBlatt - Klasse  von zufall           
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



from sympy import Symbol, Rational, nsimplify
from sympy.core.compatibility import iterable

from zufall.lib.objekte.basis import ZufallsObjekt
from zufall.lib.objekte.ausnahmen import ZufallError



# SkatBlatt - Klasse  
# ------------------
	
class SkatBlatt(ZufallsObjekt):                                      
    """
	
Skatblatt

**Kurzname** **Skat**
	
**Erzeugung**    

   Skat( )

   Es wird ein Skatblatt erzeugt, womit Wahrscheinlichkeiten für Ereignisse 
   berechnet werden können, die beim Ziehen einer einzelnen Karte eintreten
				 
   Das Objekt ist nicht zum Skatspiel bestimmt; Skat ist kein rein 
   zufälliges Spiel				 
				 
Zuweisung    s = Skat()  :math:`\qquad` (s - freier Bezeichner)

Elemente der Ergebnismenge (das komplette Blatt)

   ``s.KreuzAs`` :math:`\quad`    ``s.PikAs`` :math:`\quad`   ``s.HerzAs`` :math:`\quad`   ``s.KaroAs``  

   ``s.KreuzKönig``  :math:`\quad`     ``s.PikKönig``  :math:`\quad`    ``s.HerzKönig``  :math:`\quad`   ``s.KaroKönig`` 

   ``s.KreuzDame``  :math:`\quad`    ``s.PikDame``  :math:`\quad`  ``s.HerzDame``  :math:`\quad`      ``s.KaroDame``  

   ``s.KreuzBube``  :math:`\quad`  ``s.PikBube``  :math:`\quad`   ``s.HerzBube``  :math:`\quad`  ``s.KaroBube``

   ``s.Kreuz10``  :math:`\quad`   ``s.Pik10``  :math:`\quad`     ``s.Herz10``  :math:`\quad`    ``s.Karo10``
  
   ``s.Kreuz9``   :math:`\quad`    ``s.Pik9``  :math:`\quad`      ``s.Herz9``  :math:`\quad`   ``s.Karo9`` 

   ``s.Kreuz8``  :math:`\quad`    ``s.Pik8``  :math:`\quad`     ``s.Herz8``  :math:`\quad`  ``s.Karo8`` 

   ``s.Kreuz7``  :math:`\quad`   ``s.Pik7``  :math:`\quad`  ``s.Herz7``  :math:`\quad`   ``s.Karo7``

Ereignisse beim Ziehen einer Karte sind alle Elementarereignisse sowie	
	
   ``s.Kreuz``  :math:`\qquad\qquad\:\:`        "Kreuz"  
   
   ``s.Pik``    :math:`\qquad\qquad\quad\:`        "Pik"   
   
   ``s.Herz``   :math:`\qquad\qquad\:\:\:\;`        "Herz"
   
   ``s.Karo``   :math:`\qquad\qquad\:\:\:\,`        "Karo"
   
   ``s.Bube``   :math:`\qquad\qquad\:\:\;\,`        "Bube"
   
   ``s.Dame``   :math:`\qquad\qquad\:\;\:\,`        "Dame"
   
   ``s.König``  :math:`\qquad\qquad\:\,\,`        "König"
   
   ``s.As``     :math:`\qquad\qquad\quad\:\:\;`        "As" 
   
   ``s._7`` = ``s.Sieben``  :math:`\quad\:\:\;` "7"
   
   ``s._8`` = ``s.Acht``  :math:`\qquad\,\,\,` "8"
   
   ``s._9`` = ``s.Neun``  :math:`\qquad\,\,\,` "9"
   
   ``s._10`` = ``s.Zehn`` :math:`\qquad` "10"
   
   ``s.schwarz``   :math:`\qquad\quad\:\:\:\:` "Kreuz oder Pik"
   
   ``s.rot``      :math:`\qquad\quad\quad\:\:\:\:\,\,\,` "Herz oder Karo"
   
   ``s.Bild``    :math:`\qquad\qquad\quad\\,` "Bube, Dame, König oder As"
   
   ``s.Zahl``     :math:`\qquad\qquad\:\:\:\:\;` "7, 8, 9 oder 10"

   (Es gibt jeweils 8 Karten in den Farben Kreuz und Pik (beide schwarz)
   und Herz und Karo (beide rot) 
   
   In jeder Farbe gibt es die Bilder As, König, Dame und Bube  sowie die
   Zahlen 10, 9, 8 und 7)  

    """			
				
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3, 4):                         
            skat_blatt_hilfe(kwargs["h"])		
            return
  
        cls.KreuzAs		= Symbol('KreuzAs')  
        cls.KreuzKoenig	= Symbol('KreuzKoenig')  
        cls.KreuzDame		= Symbol('KreuzDame')  
        cls.KreuzBube		= Symbol('KreuzBube')  
        cls.Kreuz10		= Symbol('Kreuz 10')  
        cls.Kreuz9			= Symbol('Kreuz 9')  
        cls.Kreuz8			= Symbol('Kreuz 8')  
        cls.Kreuz7			= Symbol('Kreuz 7')  
        cls.PikAs			= Symbol('PikAs')  
        cls.PikKoenig		= Symbol('PikKoenig')  
        cls.PikDame		= Symbol('PikDame')  
        cls.PikBube		= Symbol('PikBube')  
        cls.Pik10			= Symbol('Pik 10')  
        cls.Pik9			= Symbol('Pik 9')  
        cls.Pik8			= Symbol('Pik 8')  
        cls.Pik7			= Symbol('Pik 7')  
        cls.HerzAs		 	= Symbol('HerzAs')  
        cls.HerzKoenig	 	= Symbol('HerzKoenig')  
        cls.HerzDame		= Symbol('HerzDame')  
        cls.HerzBube		= Symbol('HerzBube')  
        cls.Herz10			= Symbol('Herz 10')  
        cls.Herz9			= Symbol('Herz 9')  
        cls.Herz8			= Symbol('Herz 8')  
        cls.Herz7			= Symbol('Herz 7')  
        cls.KaroAs			= Symbol('KaroAs')  
        cls.KaroKoenig		= Symbol('KaroKoenig')  
        cls.KaroDame		= Symbol('KaroDame')  
        cls.KaroBube		= Symbol('KaroBube')  
        cls.Karo10			= Symbol('Karo 10')  
        cls.Karo9			= Symbol('Karo 9')  
        cls.Karo8			= Symbol('Karo 8')  
        cls.Karo7			= Symbol('Karo 7') 
        cls.Kreuz = {	cls.KreuzAs,
						cls.KreuzKoenig,  
						cls.KreuzDame,  
						cls.KreuzBube,  
						cls.Kreuz10,  
						cls.Kreuz9,  
                     cls.Kreuz8,  
                     cls.Kreuz7 }  
        cls.Pik =   {	cls.PikAs,
						cls.PikKoenig,  
						cls.PikDame,  
						cls.PikBube,  
						cls.Pik10,  
						cls.Pik9,  
                     cls.Pik8,  
                     cls.Pik7 }  
        cls.Herz = {	cls.HerzAs,
						cls.HerzKoenig,  
						cls.HerzDame,  
						cls.HerzBube,  
						cls.Herz10,  
						cls.Herz9,  
                     cls.Herz8,  
                     cls.Herz7 } 
        cls.Karo = {	cls.KaroAs,
						cls.KaroKoenig,  
						cls.KaroDame,  
						cls.KaroBube,  
						cls.Karo10,  
						cls.Karo9,  
                     cls.Karo8,  
                     cls.Karo7 }  					 
        cls.As 		= {cls.HerzAs, cls.KaroAs, cls.KreuzAs, cls.PikAs}		
        cls.Koenig 	= {cls.HerzKoenig, cls.KaroKoenig, cls.KreuzKoenig, cls.PikKoenig}	
        cls.Dame 	= {cls.HerzDame, cls.KaroDame, cls.KreuzDame, cls.PikDame}	
        cls.Bube 		= {cls.HerzBube, cls.KaroBube, cls.KreuzBube, cls.PikBube}		
        cls._10		= {cls.Herz10, cls.Karo10, cls.Kreuz10, cls.Pik10}
        cls._9		= {cls.Herz9, cls.Karo9, cls.Kreuz9, cls.Pik9}
        cls._8		= {cls.Herz8, cls.Karo8, cls.Kreuz8, cls.Pik8}		
        cls._7		= {cls.Herz7, cls.Karo7, cls.Kreuz7, cls.Pik7}
        cls.Zehn    = cls._10		
        cls.Neun    = cls._9		
        cls.Acht    = cls._8	
        cls.Sieben  = cls._7		
        cls.rot     = cls.Herz.union(cls.Karo)					 
        cls.schwarz = cls.Kreuz.union(cls.Pik)					 
        cls.Bild    = cls.As.union(cls.Koenig).union(cls.Dame).union(cls.Bube)					 
        cls.Zahl    = cls._10.union(cls._9).union(cls._8).union(cls._7)
		
        return ZufallsObjekt.__new__(cls)
					
			
    def __str__(self):  
        return "SkatBlatt"
		
		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def omega(self):
        """Kartenmenge"""	
        return self.Bild.union(self.Zahl)
		
    blatt = omega		

    @property
    def n_omega(self):
        """Anzsahl Karten"""	
        return 32
		
    nOmega = n_omega		


    def P(self, *args, **kwargs):
        """Wahrscheinlichkeit eines Ereignisses"""
		
        if kwargs.get('h'):
            print("\nWahrscheinlichkeit eines Ereignisses\n")
            print("Aufruf   s . P( e )\n")		                     
            print("              s     SkatBlatt")
            print("              e     einzelne Karte | Menge/Liste/Tupel von Karten |")
            print("                    Ereignis beim Ziehen einer Karte (s. Hilfeseite)\n")
            print("  oder   s . P( e, e1)\n")		                     
            print("Bei der Angabe von zwei Ereignissen wird die bedingte Wahrscheinlichkeit")
            print("P( e | e1 ) berechnet\n")
            print("Ereignisse können mit Hilfe der Operatoren 'nicht', 'und' und 'oder' mit-")
            print("tels einfacher Ausdrücke gebildet werden; die Ausdrücke sind als Zeichen-") 
            print("ketten einzugeben\n")			
            print("Beispiele")
            print("s.P( s.König )   s.P( 's.Kreuz und s.Zahl' )   s.P( 'nicht s.Bild' )")
            print("s.P( { s.PikAs, s.HerzBube } ) ")  
            print("s.P( 's.Bild oder s.rot' )     s.P({*s.Bild, *s.rot})") 
            print("s.P( s.rot, s.Karo )   (bedingte Wahrscheinlichkeit)\n")			
            return			
			
        if len(args) not in (1, 2):
            print('zufall: ein oder zwei Ereignisse angeben')
            return	

        def teil(x):
            if isinstance(x, set):
                return all([y in omega for y in x])
            else:
                if x in omega:
                    return True
                return False
			   
        omega = self.omega
        if len(args) == 1:
            e = args[0]
            if not iterable(e) and e in omega:					
                pp = Rational(1, 32)
            elif iterable(e):
                if not all([x in omega for x in e]):
                    print('zufall: Karten des Skatblattes angeben')
                    return
                pp = Rational(len(e), 32)					
            elif isinstance(e, str):
                uu, oo, nn = e.find('und'), e.find('oder'), e.find('nicht')			
                try:
                    if uu >= 0:
                        a, b = e[:uu].strip(), e[uu+3:].strip() 					  
                        ia, ib = a.find('.'), b.find('.')
                        a, b = a[ia+1:], b[ib+1:]
                        a, b = 'self.' + a, 'self.' + b						
                        a, b = eval(a), eval(b)
                        if not (teil(a) and teil(b)):
                            print('zufall: Ereignisse bei Skatblatt angeben')
                            return
                        if isinstance(a, set):							
                            if isinstance(b, set):							
                                ee = a.intersection(b)
                            else:								
                                ee = a.intersection(set([b]))
                        else:	
                            if isinstance(b, set):							
                                ee = set([a]).intersection(b)
                            else:								
                                ee = set([a]).intersection(set([b]))						
                        pp = Rational(len(ee), 32)											
                    elif oo > 0:
                        a, b = e[:oo].strip(), e[oo+3:].strip()					  
                        ia, ib = a.find('.'), b.find('.')
                        a, b = a[ia+1:], b[ib+1:]
                        a, b = 'self.' + a, 'self.' + b						
                        a, b = eval(a), eval(b)
                        if not (teil(a) and teil(b)):
                            print('zufall: Ereignisse bei Skatblatt angeben')
                            return
                        if isinstance(a, set):							
                            if isinstance(b, set):							
                                ee = a.union(b)
                            else:								
                                ee = a.union(set([b]))
                        else:	
                            if isinstance(b, set):
                                ee = set([a]).union(b)
                            else:								
                                ee = set([a]).union(set([b]))						
                        pp = Rational(len(ee), 32)											
                    elif nn >= 0:
                        a = e[nn+5:].strip()				  
                        ia = a.find('.')
                        a = a[ia+1:]
                        a = 'self.' + a						
                        a = eval(a)
                        if not teil(a):
                            print('zufall: Ereignis bei Skatblatt angeben')
                            return
                        if isinstance(a, set):							
                           ee = omega.difference(a)
                        else:
                            ee = omega.difference(set([a]))						
                        pp = Rational(len(ee), 32)											
                    else:
                        ee = eval(e)
                        pp = Rational(len(ee), 32)											
                except:
                    print('zufall:', 'Ausdruck überprüfen')
                    return			
            else:
                print('zufall: Karten des Skatblattes angeben')
                return
							
        elif len(args) == 2: 
            e1, e2 = args	
            if iterable(e1):
                e1 = set(e1)			
            if iterable(e2):
                e2 = set(e2)			
            try:			
                if isinstance(e1, set):
                    if isinstance(e2, set):
                        ee = e1.intersection(e2)
                    else:
                        ee = e1.intersection(set([e2]))
                else:
                    if isinstance(e2, set):
                        ee = set([e1]).intersection(e2)
                    else:
                        ee = set([e1]).intersection(set([e2]))
                pp1, pp2 = self.P(ee), self.P(e2)
                pp = nsimplify(pp1 / pp2, rational=True)
            except:
                print('zufall: die Angaben bitte überprüfen')	
                return
            			
        return pp	
		
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        skat_blatt_hilfe(3)	
		
    h = hilfe					
			
		
		
		
# Benutzerhilfe für SkatBlatt
# ---------------------------

def skat_blatt_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
SkatBlatt - Objekt

Kurzname     Skat	
	
Erzeugung    Skat( )

Es wird ein Skatblatt erzeugt, womit Wahrscheinlichkeiten für Ereignisse 
berechnet werden können, die beim Ziehen einer einzelnen Karte eintreten
				 
Das Objekt ist nicht zum Skatspiel bestimmt; Skat ist kein rein 
zufälliges Spiel				 
				 
Zuweisung    s = Skat()   (s - freier Bezeichner)

Elemente der Ergebnismenge (das komplette Blatt)

s.KreuzAs        s.PikAs        s.HerzAs        s.KaroAs  
s.KreuzKönig     s.PikKönig     s.HerzKönig     s.KaroKönig  
s.KreuzDame      s.PikDame      s.HerzDame      s.KaroDame  
s.KreuzBube      s.PikBube      s.HerzBube      s.KaroBube  
s.Kreuz10        s.Pik10        s.Herz10        s.Karo10  
s.Kreuz9         s.Pik9         s.Herz9         s.Karo9  
s.Kreuz8         s.Pik8         s.Herz8         s.Karo8  
s.Kreuz7         s.Pik7         s.Herz7         s.Karo7

Ereignisse beim Ziehen einer Karte sind alle Elementarereignisse sowie	
	
s.Kreuz          "Kreuz"  		
s.Pik            "Pik"   
s.Herz           "Herz"
s.Karo           "Karo"
s.Bube           "Bube"
s.Dame           "Dame"
s.König          "König"
s.As             "As" 
s._7 = s.Sieben  "7"
s._8 = s.Acht    "8"
s._9 = s.Neun    "9"
s._10 = s.Zehn   "10"
s.schwarz        "Kreuz oder Pik"
s.rot            "Herz oder Karo"
s.Bild           "Bube, Dame, König oder As"
s.Zahl           "7, 8, 9 oder 10"

(Es gibt jeweils 8 Karten in den Farben Kreuz und Pik (beide schwarz)
und Herz und Karo (beide rot) 
In jeder Farbe gibt es die Bilder As, König, Dame und Bube  sowie die
Zahlen 10, 9, 8 und 7)  

	   """)
        return 
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für SkatBlatt
 	
s.hilfe      Bezeichner der Eigenschaften und Methoden
s.omega      Ergebnismenge beim einmaligen Ziehen
s.blatt      = s.omega
s.P(...)  M  Wahrscheinlichkeiten beim einmaligen Ziehen

Synonymer Bezeichner

hilfe    h
""")
        return 
		

        return 


Skat = SkatBlatt		
		
		
	
