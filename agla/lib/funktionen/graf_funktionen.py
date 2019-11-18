#!/usr/bin/python
# -*- coding utf-8 -*-

               
			   
#                                                 
#  agla-Funktionen für Grafik                    
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



# Inhalt:
#
#   _klassen_mit_grafik     Klassen mit graf-Methode
#	_klassen_ohne_anim		Klassen ohne Animationsmöglichkeit
#	_funkt_sympy2numpy      Transformation mathematischer Funktionen 
#   farben					Farben
#   Grafik					Zeichnen einer Grafik
#   sicht_box               s. agla.lib.objekte.umgebung.sicht_box 
#   _spezifikation			Spezifikations-Kontrolle
#
#   Mayavi - Funktionen
#   _Grafik_mit_mayavi		3D-Grafik
#   _box_mayavi				Zeichnen der Sichtbox
#   _axes_mayavi			Zeichnen der Achsen
#   _x_skala_mayavi         Zeichnen der x-Skala
#   _y_skala_mayavi         ebenso, y
#   _z_skala_mayavi         ebenso, z				
#   _gitter_xy_mayavi		Zeichnen eines Gitters in der xy-Ebene
#   _gitter_xyz_mayavi		ebenso, 3-seitiges Gitter
#   _arrow_mayavi			Zeichnen eines Pfeils
#   _implicit_plot_mayavi   Implizites plotten
#   _many_lines_mayavi      Zeichnen vieler Linien
#
#   VisPy - Funktionen
#   _Grafik_mit_vispy		3D-Grafik
#   _box_vispy				Zeichnen der Sichtbox
#   _axes_vispy			    Zeichnen der Achsen
#   _x_skala_vispy          Zeichnen der x-Skala
#   _y_skala_vispy          ebenso, y
#   _z_skala_vispy          ebenso, z				
#   _gitter_xy_vispy		Zeichnen eines Gitters in der xy-Ebene
#   _gitter_xyz_vispy		ebenso, 3-seitiges Gitter
#   _arrow_vispy			Zeichnen eines Pfeils
#
#   2D - Funktionen (matplotlib)
#   _Grafik_mit_matplotlib	2D-Grafik 
#   _gitter2		        Zeichnen eines Gitters
#   _x_skala2			    Zeichnen der x-Skala
#   _y_skala2			    ebenso, y



#from __future__ import (absolute_import, division, print_function,
#                       unicode_literals)

import six
import re
import time
import importlib
from copy import deepcopy

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import colors

from IPython.display import display, Math   

from sympy.core.compatibility import iterable
from sympy.core.numbers import Integer, Rational, Float
from sympy.core.containers import Tuple
from sympy.core.sympify import sympify
from sympy.core.symbol import Symbol, symbols
from sympy import (sqrt, Abs, sin, cos, tan, asin, acos, atan, 
    exp, log, sinh, cosh, tanh, asinh, acosh, atanh, pi)
from sympy.printing import latex	
from sympy.utilities.lambdify import lambdify

from agla.lib.funktionen.funktionen import (mit_param, ja, Ja, nein, Nein, 
    mit, ohne, is_zahl)
	
from agla.lib.objekte.umgebung import UMG, sicht_box
if UMG.grafik_3d == 'mayavi':						
    from tvtk.tools import visual
    from mayavi import mlab	
else:
    from vispy import app, scene
    from vispy.scene import visuals
    from vispy.geometry import create_arrow
    from vispy.scene import STTransform, AffineTransform, ChainTransform

from agla.lib.objekte.ausnahmen import *
import agla
			
	
	
# --------------------------------------------------
# Klassen, für die graf-Methoden implementiert sind
# --------------------------------------------------

_klassen_mit_grafik = [

    "Vektor",
    "Gerade",
    "Ebene",
    "Kugel", 
    "Parallelogramm",
    "Spat",
    "Strecke",
    "Dreieck",
    "Viereck",
    "Kreis",
    "Pyramide",
    "Prisma",
    "Kegel",
    "Zylinder",
	 "Figur",
    "Koerper",
    "Kurve",
    "Kurve2terOrdnung",
    "Flaeche2terOrdnung",
    "Ellipsoid",
    "Paraboloid",
    "EinSchaligesHyperboloid",
    "ZweiSchaligesHyperboloid",
    "ElliptischesParaboloid",
    "HyperbolischesParaboloid",
    "DoppelKegel",
    "ElliptischerZylinder",
    "HyperbolischerZylinder",
    "ParabolischerZylinder",
    "Flaeche",
    "Ellipse",
    "Hyperbel",
    "Parabel",
    "Piecewise",	
    "hPunkt",
    "hGerade",
    "hStrahl",
    "hStrecke",
    "hKreis",
    "hDreieck",
    "sPunkt",
    "sGerade",
    "sStrecke",
    "sKreis",
    "sDreieck",
    "sZweieck"	 ]
			
# ------------------------------------------------------
# Klassen in R^3, für die keine Animationen möglich sind
# ------------------------------------------------------
	
_klassen_ohne_anim = [

    "Parallelogramm",
    "Spat",
    "sPunkt",
    "sGerade",
    "sStrecke",
    "sDreieck",
    "sZweieck",                                            
    "sKreis",
    "hPunkt",
    "hGerade",
    "hStrecke",
    "hDreieck",
    "hKreis" ]                             

# ---------------------------------------------------------------
# Transformation mathematischer Funktionen (SymPy/agla --> NumPy)
# ---------------------------------------------------------------

_funkt_sympy2numpy = {

	  'Abs'   : 'abs',	
     'ln'    : 'log',
     'lg'    : '1/log(10)*log',
     'asin'  : 'arcsin',					 
     'acos'  : 'arccos',					 
     'atan'  : 'arctan',	
     'asinh' : 'arcsinh',				   
     'acosh' : 'arccosh',		 		   
     'atanh' : 'arctanh' }

	
# =====================
# Allgemeine Funktionen
# =====================

# -------
# Farben
# -------

# vordefinierte Farbnamen, deutsch
rot		= (1, 0, 0)
gruen	= (0, 1, 0)
blau 	= (0, 0, 1)
schwarz	= (0, 0, 0)
weiss	= (1, 1, 1)
gelb	= (1, 1, 0) 
magenta	= (1, 0, 1) 
cyan	= (0, 1, 1) 

_zu_farben = \
    {  # deutsche Farbnamen als Zeichenkette
      'rot' 	: u'#FF0000',		
      'gruen' 	: u'#00FF00', 
      'blau' 	: u'#0000FF',
      'schwarz': u'#000000',     	
      'weiss' 	: u'#FFFFFF',  
      'gelb' 	: u'#FFFF00',
      'ge'		: u'#FFFF00',	
      # einstellige Namen
      'c' : u'#00bfbf',
      'b' : u'#0000ff',
      'w' : u'#ffffff',
      'g' : u'#008000',
      'y' : u'#bfbf00',
      'k' : u'#000000',
      'r' : u'#ff0000',
      's' : u'#000000',
      'm' : u'#bf00bf'   } 


def farben(**kwargs):

	# aus der Dokumentation von matplotlib entnommen und modifiziert
	
    if kwargs.get('h'):
        print("\nfarben - Funktion\n")
        print("Ausgabe einer Liste mit den zulässigen Farbnamen\n")	
        print("Aufruf   farben()\n")	
        return
		
    import six
    import matplotlib.pyplot as plt
    from matplotlib import colors	
    print("\nEine beliebige Farbe kann als RGB-Tripel (z.B. (1, 0, 0) für rot) oder durch")         
    print("das hexadezimale Äquivalent ('#ff0000' oder '#FF0000' für rot) angegeben wer-") 
    print("den, für eine Reihe von Farben stehen vordefinierte Namen zur Verfügung")	
    print("\nDeutsche Farbnamen:  rot, gruen, blau, schwarz, weiss, gelb, cyan, magenta")
    print("                     (Angabe ohne ' ' möglich)")
    print("\nWeitere Farbnamen    (Angabe mit ' '):")
	
    colors__ = colors.cnames
    for n in _zu_farben:
        colors__[n] = _zu_farben[n]
    colors_ = list(six.iteritems(colors__))

    # Transform to hex color values.
    hex_ = [color[1] for color in colors_]
    # Get the rgb equivalent.
    rgb = [colors.hex2color(color) for color in hex_]
    # Get the hsv equivalent.
    hsv = [colors.rgb_to_hsv(color) for color in rgb]

    # Split the hsv values to sort.
    hue = [color[0] for color in hsv]
    sat = [color[1] for color in hsv]
    val = [color[2] for color in hsv]

    # Sort by hue, saturation and value.
    ind = np.lexsort((val, sat, hue))
    sorted_colors = [colors_[i] for i in ind]

    n = len(sorted_colors)
    ncols = 4
    nrows = int(np.ceil(1. * n / ncols))

    fig = plt.figure(figsize=(15, 10), dpi=110)
    ax = fig.add_subplot(111)

    X, Y = fig.get_dpi() * fig.get_size_inches()
    # row height
    h = Y / (nrows + 1)
    # col width
    w = X / ncols

    for i, (name, color) in enumerate(sorted_colors):
        col = i % ncols
        row = int(i / ncols)
        y = Y - (row * h) - h

        xi_line = w * (col + 0.05)
        xf_line = w * (col + 0.25)
        xi_text = w * (col + 0.3)

        ax.text(xi_text, y, name, fontsize=(h * 0.5),
                horizontalalignment='left',
                verticalalignment='center')

        ax.hlines(y + h * 0.1, xi_line, xf_line, color=color, linewidth=(h * 0.8))

    ax.set_xlim(0, X)
    ax.set_ylim(0, Y)
    ax.set_axis_off()

    fig.subplots_adjust(left=0, right=1,
                    top=1, bottom=0,
                    hspace=0, wspace=0)
    plt.show()


# aus matplotlib.colors

def rgb2hex(rgb):
    'Given an rgb or rgba sequence of 0-1 floats, return the hex string'
    a = '#%02x%02x%02x' % tuple([int(np.round(val * 255)) for val in rgb[:3]])
    return a
	
def hex2color(s):
    """
    Take a hex string *s* and return the corresponding rgb 3-tuple
    Example: #efefef -> (0.93725, 0.93725, 0.93725)
    """
    if not isinstance(s, six.string_types):
        return s
    return tuple([int(n, 16) / 255.0 for n in (s[1:3], s[3:5], s[5:7])])
	

# ------------------	
# Grafik - Funktion	
# ------------------
	
def Grafik(*args, **kwargs):    
    """Funktion zum Herstellen von 3D- und 2D-Grafiken"""

    if kwargs.get('h'):
        print("\nGrafik - Funktion\n")
        print("Synonym    zeichne\n")
        print("Zeichnen einer Grafik in 3D oder 2D\n")
        print("Aufruf   Grafik( eintrag1 eintrag2, ... /[, gestalt ] )\n")		                     
        print("             eintrag   obj | [ obj, spez ]")
        print("             obj       Objekt")
        print("             spez      Spezifikationsangaben")
        print("             gestalt   ein oder mehrere Zusatzangaben zur ")
        print("                       Gestaltung der Grafik\n")
        print("Zu den Spezifikationsangaben für die einzelnen Objekte sowie ")
        print("zu Animationen siehe die entsprechenden Seiten der Hilfe-")
        print("Funktion\n")
        print("Beispiele")
        print("(A - Punkt, g - Gerade, e - Ebene, d - Dreieck)")		
        print("Grafik(A, g, e)")		
        print("Grafik(A, [g, blau, 2], [e, 'r'])")
        print("zeichne(Kugel(A, 4), box=nein, achsen=nein)")		
        print("zeichne([d, rot, 'füll=ja'])\n")		
        return		
	
    if not args:
       print('agla: Objekt/e zum Zeichnen angeben')
       return
    obj = args[0]
    if isinstance(obj, (tuple, Tuple, list)):
        obj = obj[0]
    try:			
        d = obj.dim	
    except AttributeError:
        print('agla: nur zeichenbare Objekte angeben')
        return		
	
    for arg in args:
        if isinstance(arg, (tuple, Tuple, list)):
            arg = arg[0]	
        try:			
            d = arg.dim	
        except AttributeError:
            print('agla: nur zeichenbare Objekte angeben')
            return			
        if arg.dim != obj.dim:
            print('agla: alle Objekte müssen die gleiche Dimension haben')	
            return
	
    if not hasattr(obj, 'graf'):
        print('agla: 1. Eintrag - zeichenbares Objekt angeben')	
        return
    if obj.dim == 3:
        if UMG.grafik_3d == 'mayavi':	
            _Grafik_mit_mayavi(*args, **kwargs)
        else:
            _Grafik_mit_vispy(*args, **kwargs)			
    elif obj.dim == 2:
        _Grafik_mit_matplotlib(*args, **kwargs)

zeichne = Grafik	

		
# ------------------------		
# Spezifikations-Kontrolle 
# ------------------------

def _spezifikation(args, **kwargs):                
    """Spezifiktionskontrolle für Grafikelemente"""
    
    # es sind bis zu 5 Angaben möglich
    # - Punkt [ für Aufpunkt eines Vektor-Pfeils ]
    # - Stärke [ in (1, 2, 3) ]
    # - Farbe [ (farbe ist (r, g, b) mit 0 <= r,g, b <= 1 oder
    #            farbe ist Kurzname (s. farben()) ]
    # - Bereich (für Parameter) [ ist ( /[name,> unten, oben ), 
    #                             oder (/[name,> unten, oben, anzahl),
    #                                   name - Paramtername
    #                                   unten, oben - Grenzen des Bereiches	
    #                                   anzahl - Anzahl der Unterteilungen ]
    # - 'kwarg' [ wie kwarg, aber als string ]
    # die Reihenfolge ist beliebig
    #	
    # Rückgabewert ist das Tupel (vektor, farbe, staerke, bereich) bzw. 
    #                            (vektor, farbe, staerke, bereich, kwarg's)
	
    _en_farben = colors.cnames
    Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
	
    def eine_spez(sp):
        if isinstance(sp, Vektor):
            return('vektor', sp)
        if isinstance(sp, (int, Integer)):
            if sp in (1, 2, 3):
                return ('staerke', UMG._staerke[sp])
            return AglaError('ungültige Angabe für Stärke')
        elif isinstance(sp, str):
            if sp.find('=') > 0:
                return ('kwarg', sp)			
            if sp in _zu_farben:
                return ('farbe', _zu_farben[sp])
            if sp in _en_farben:
                return ('farbe', colors.hex2color(_en_farben[sp]))
            else:
                try:			
                    colors.hex2color(sp)
                    return ('farbe', sp)
                except:
                    pass		
            return AglaError('ungültige Farbangabe')
        elif isinstance(sp, (tuple, Tuple, list)): 
            if len(sp) == 3: 
                if isinstance(sp[0], Symbol):
                    pass
                else:
                    if is_zahl(sp[0]) and is_zahl(sp[1]) and is_zahl(sp[2]): 
                        if (0<=sp[0]<=1) and (0<=sp[1]<=1) and (0<=sp[2]<=1):
                            return ('farbe', sp)
            if len(sp) in (2, 3, 4):
                if len(sp) == 3:		
                    if isinstance(sp[0], Symbol):
                        sp = sp[1:]	
                if len(sp) == 4:
                    sp = sp[1:]					
                try:
                    float(sp[0]), float(sp[1])
                except: 					  
                    raise AglaError('ungültige Bereichsangabe')
                if sp[0] == sp[1]:
                    raise AglaError('die Bereichsgrenzen müssen verschieden sein')				
                if len(sp) == 3:
                    if not isinstance(sp[2], (int, Integer)) and sp[2] > 1:
                        raise AglaError('die Anzahl Unterteilungen muss ganz und > 1 sein')
                return ('bereich', sp)
        raise AglaError('Spezifikation überprüfen') 
        		
    if not args:
        return (None, 'default', 'default', None) # vektor, farbe, staerke, bereich
    if len(args) == 1:
        spe = [eine_spez(args[0])]
    elif len(args) == 2:
        spe = [eine_spez(args[0]), eine_spez(args[1])]
    if len(args) == 3:
        spe = [eine_spez(args[0]), eine_spez(args[1]), eine_spez(args[2])]	
		
    vektor = None		
    farbe = 'default'
    staerke = 'default'
    bereich = None
    kwarg = []
    for s in spe:	
        if s[0] == 'kwarg':
            kwarg.append(s[1])
        if s[0] == 'vektor':
            vektor = s[1]
        if s[0] == 'farbe':
            farbe = s[1]
        if s[0] == 'staerke':
            staerke = s[1]
        if s[0] == 'bereich':
            bereich = s[1]
        if isinstance(s, AglaError):
            return s	
    if farbe != 'default':
        farbe = hex2color(farbe)	
    if kwarg:			
        return (vektor, farbe, staerke, bereich, tuple(kwarg))
    return (vektor, farbe, staerke, bereich)
		

		
# ==========================	
# Funktionen für 3D - Grafik
# ==========================	
	
# ------------------
# Grafik mit Mayavi
# ------------------

def _Grafik_mit_mayavi(*args, **kwargs):    
    """Funktion zum Erzeugen von 3D-Grafiken mit Mayavi"""
		
    mlab.close(all=True)
	
    x, y, z = symbols("x y z")			
	
    achsen = True if kwargs.get('achsen') is None else kwargs.get('achsen')
    box = True if kwargs.get('box') is None else kwargs.get('box')
    xy_gitter = False if kwargs.get('xy_gitter') is None else \
               kwargs.get('xy_gitter')
    xyz_gitter = False if kwargs.get('xyz_gitter') is None else \
               kwargs.get('xyz_gitter')
    skalen = True if kwargs.get('skalen') is None else kwargs.get('skalen') 
    x_skala = True if kwargs.get('x_skala') is None else kwargs.get('x_skala') 
    y_skala = True if kwargs.get('y_skala') is None else kwargs.get('y_skala')		
    z_skala = True if kwargs.get('z_skala') is None else kwargs.get('z_skala')	
    text = kwargs.get('text')
    bez = kwargs.get('bez')
	
	# string-Angaben in Eingabe sichten
    i = 0	
    for arg in args:
        i += 1	
        if isinstance(arg, str):
            if arg.find('=') > 0:
                exec(arg)
                continue
            else:
                print("agla: %s. Eintrag: '=' ist nicht angegeben" % i)
                return			
				
    if xyz_gitter:
        achsen = False	
    if not skalen:
        x_skala = False
        y_skala = False		
        z_skala = False	

    if isinstance(achsen, bool):
        x_bez, y_bez, z_bez = 'x', 'y', 'z'	
    else:	
        a = achsen
        if not isinstance(a, (tuple, Tuple, list)) or len(achsen) != 3:
            print('agla: Liste/Tupel mit drei Bezeichnern für die Achsen angeben')
            return
        x_bez = str(a[0]) if isinstance(a[0], Symbol) else a[0]	 	
        y_bez = str(a[1]) if isinstance(a[1], Symbol) else a[1]	 	
        z_bez = str(a[2]) if isinstance(a[2], Symbol) else a[2]
        if not (isinstance(x_bez, str) and isinstance(y_bez, str) and 
              isinstance(z_bez, str))	:
            print('agla: die Bezeichner als Symbole oder Zeichenketten angeben')
            return
			
    if bez:          # Textangabe: (Vektor/Punkt, 'text' /[,text_groesse>)
        text = bez
    if text:
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor						
        meld = 'agla: Textangaben sind als Tupel/Liste mit Elementen der \nLänge 2 oder 3 zu schreiben'
        if not iterable(text): 
            print(meld)				
            return
        if not all([iterable(el) and len(el) in (2, 3) for el in text]):        
            print(meld)		
            return
        if not all([isinstance(el[0], Vektor) and isinstance(el[1], str) 
               for el in text]):
            print('agla: Textelemente müssen die Form (Vektor/Punkt, \'text\' /[, text_größe]) haben')
            return
        tg = [el for el in text if len(el) == 3]			
        if tg:		
            if not all([el[2] in (1, 2) for el in tg]):
                print('agla: Textgrößen sind  1:kleiner, 2:größer')
                return
			
    # Einträge kontrollieren und sammeln		
    eintraege = []		# [Objekt, Spezifikation]
    i = 1	
    for arg in args:	
        if isinstance(arg, str):
            if arg.find('=') > 0:
                exec(arg)
                continue
            else:
                print("agla: %s. Eintrag: '=' ist nicht angegeben" % i)
                return			
        spez = tuple()
        if isinstance(arg, (list, tuple, Tuple)):
            obj = arg[0]
            if len(arg) > 1:
                spez = tuple(arg[1:])
        else:
            obj = arg
        if not hasattr(obj, 'graf'):
            s = str(type(obj))
            print("agla: %s. Eintrag: ein Objekt zum Zeichnen angeben" % i)
            return
        try:
            if mit_param(obj) and not obj.is_schar:	
                raise AglaError('Parameteranzahl > 1, die Darstellung ist nicht implementiert')			
            spez = _spezifikation(spez)
            if isinstance(spez, AglaError): 
                raise AglaError(spez[0])	
            if not obj.is_schar and spez[3]:
                raise AglaError('keine Schar, die Bereichsangabe ist ungültig')	
            if obj.is_schar and not spez[3]:
                raise AglaError('Schar, eine Bereichsangabe machen')
        except AglaError as e:
            print("agla: " + str(i) + ". Eintrag:", e.args[0])
            return 
        except Exception:
            print("agla: %s. Eintrag: die Eingaben sind fehlerhaft" % i)	
            return			
					
        eintraege += [[obj, spez]]  
        i += 1
    
    # auf Animationsfähigkeit untersuchen	
    animation = None	
    for i, ein in enumerate(eintraege): 
        obj, spez = ein
        txt = 'agla: ' + str(i+1) + '. Eintrag: ' + \
             'die animierte Darstellung des Objektes ist nicht implementiert'		
        if spez[3]:
            in_klassen = False
            ss = str(type(obj))		
            for k in _klassen_ohne_anim:
                if k in ss:
                    in_klassen = True
                    break	
            if in_klassen or len(spez) > 4:
                raise AglaError(txt)
        if ('Vektor' in str(type(obj)) and 'Vektor' in str(type(spez[0]))) and \
            (mit_param(obj) or mit_param(spez[0])):				 
            raise AglaError(txt)
        if obj.is_schar:   
            animation = True
			
    fig = mlab.figure(bgcolor=(1, 1, 1), size=(600, 600))  
    visual.set_viewer(fig)		
    dist = 100 * UMG._mass()
    mlab.view(azimuth=15, elevation=70, distance=dist)
    mlab.yaw(10)	
		
    if achsen:
        _axes_mayavi(x_bez=x_bez, y_bez=y_bez, z_bez=z_bez)
    if box:
        _box_mayavi()
    else:
       x_skala = False 		
       y_skala = False 		
       z_skala = False 		
    if xy_gitter:
	     _xy_gitter_mayavi()
    if xyz_gitter:
	     _xyz_gitter_mayavi()
    if x_skala:
        if not box and not achsen and not xy_gitter and not xyz_gitter:
            _x_skala_mayavi(None)
        elif xy_gitter:
            _x_skala_mayavi(0)		        			
        elif xyz_gitter:
            _x_skala_mayavi(1)
        elif box and achsen:
            _x_skala_mayavi(1)		
        elif box and not achsen:
            _x_skala_mayavi(1)
        else:
            _x_skala_mayavi(0)		
    if y_skala:
        if not box and not achsen and not xy_gitter and not xyz_gitter:
            _y_skala_mayavi(None)
        elif xy_gitter:
            _y_skala_mayavi(0)		        			
        elif xyz_gitter:
            _y_skala_mayavi(1)
        elif box and achsen:
            _y_skala_mayavi(1)		
        elif box and not achsen:
            _y_skala_mayavi(1)
        else:
            _y_skala_mayavi(0)		
    if z_skala:
        if not box and not achsen and not xy_gitter and not xyz_gitter:
            _z_skala_mayavi(None)
        elif xy_gitter:
            _z_skala_mayavi(None)		        			
        elif xyz_gitter:
            _z_skala_mayavi(1)
        elif box and achsen:
            _z_skala_mayavi(1)		
        elif box and not achsen:
            _z_skala_mayavi(1)
        else:
            _z_skala_mayavi(0)	
				
    # (Dreieck, Viereck) -> (Strecke, Strecke, ...)	
    # (Prisma, Pyramide) -> Koerper; Koerper -> (Strecke, Strecke, ...)			
    Koerper = importlib.import_module('agla.lib.objekte.koerper').Koerper		
    Prisma = importlib.import_module('agla.lib.objekte.prisma').Prisma		
    Pyramide = importlib.import_module('agla.lib.objekte.pyramide').Pyramide	
    Strecke = importlib.import_module('agla.lib.objekte.strecke').Strecke	
	
    for i, ein in enumerate(eintraege):
        if not ein[1][3]:
            continue		
        sein0 = str(ein[0])
        if not ('Dreieck' in sein0 or 'Viereck' in sein0 or 'Koerper' in sein0
               or 'Körper' in sein0 or 'Prism' in sein0 or 'Pyramide' in sein0):
            continue
        oo = ein[0]			
        if 'Dreieck' in sein0 or 'Viereck' in sein0 or 'Prism' in sein0 \
            or 'Pyramide' in sein0:
            oo = ein[0].in_koerper
        ein1 = []
        for k in oo.kanten:
            ss = Strecke(oo.ecken[k[0]], oo.ecken[k[1]])
            ein2 = ein[1]			
            if not ss.is_schar:			
                ein2 = ein[1][0], ein[1][1], ein[1][2], None			
            ein1 += [[ss, ein2]]
        eintraege = eintraege[:i] + ein1 + eintraege[i+1:]

    # Erzeugen der Grafikelemente
    animations_liste = []
    for ein in eintraege: 
        obj, spez = ein
        if not obj.is_schar:   
            res = obj.graf(spez, figure=fig)
            if isinstance(res, AglaError):
                print('agla:', res.args[0])
                return
        else:
            res = obj.graf(spez, figure=fig)
            if isinstance(res, AglaError):
                print('agla:', res.args[0])
                return
            animations_liste += [[type(obj), res[0], res[1], res[2]]]
		
    if animations_liste:	
        anim_mayavi(animations_liste)    # Funktion wird außerhalb definiert			
			
    if text:
        _mass = UMG._mass()
        f = (0.5, 0.5, 0.5)		
        for t in text:
            if len(t) < 3:		
                mlab.text3d(t[0].x, t[0].y, t[0].z, t[1], scale=0.5*_mass, color=f) 								
            else:			
                scale = {1:0.4, 2:0.6} # default 0.5			
                mlab.text3d(t[0].x, t[0].y, t[0].z, t[1], scale=scale[t[2]]*_mass, color=f)
						
    mlab.show()
	
    return	True	
	
	
# -----------------------------	
# Animationsfunktion für mayavi
# -----------------------------	
	
@mlab.animate(delay=25000)		
def anim_mayavi(al):
    """Herstellung animierter Grafiken; nur im Raum

    Die 3D-Animation mit Mayavi trägt in agla experimentellen Charakter

	1. Es werden folgende Objekt-Klassen unterstützt: siehe _klassen_mit_animation	
	
	2. Es ist für jedes animierte Objekt nur ein Parameter zugelassen (der Name 
       kann unterschiedlich sein)

	3. Objekte mit Pfeilen sind nicht animierbar, ebenso gefüllte Objekte sowie die 
       Grenzen eines Parameterbereiches
	
	4. Verfeinerte oder als Röhre dargestellte Kurven sowie Fächen mit Gitternetz 
       oder als Drahtdarstellung sind nicht animierbar
       
    5. Es wurden keine Maßnahmen zur Reduzierung der Rechenzeiten bei der
       Herstellung der Grafiken getroffen
	   
    6. Die Bedienung beim Ablaufen einer Animation ist provisorisch	   
	
	Bei der gleichzeitigen Animation mehrerer Objekte ist auf die Über-
	einstimmung der Parameterangaben zu achten
	   
    """
		
    obj = [el[0] for el in al]
    if 'Vektor' in str(obj):	
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor		
    elif 'Gerade' in str(obj):	
        Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
    elif 'Ebene' in str(obj):	
        Ebene = importlib.import_module('agla.lib.objekte.ebene').Ebene	
    elif 'Kugel' in str(obj):	
        Kugel = importlib.import_module('agla.lib.objekte.kugel').Kugel	
    elif 'Strecke' in str(obj):	
        Strecke = importlib.import_module('agla.lib.objekte.strecke').Strecke	
    elif 'Dreieck' in str(obj):	
        Dreieck = importlib.import_module('agla.lib.objekte.dreieck').Dreieck	
    elif 'Viereck' in str(obj):	
        Viereck = importlib.import_module('agla.lib.objekte.viereck').Viereck	
    elif 'Kreis' in str(obj):	
        Kreis = importlib.import_module('agla.lib.objekte.kreis').Kreis
    elif 'Koerper' in str(obj):	
        Koerper = importlib.import_module('agla.lib.objekte.koerper').Koerper
    elif 'Kegel' in str(obj):	
        Kegel = importlib.import_module('agla.lib.objekte.kegel').Kegel	
    elif 'Zylinder' in str(obj):	
        Zylinder = importlib.import_module('agla.lib.objekte.zylinder').Zylinder	
    elif 'Kurve' in str(obj):	
        Kurve = importlib.import_module('agla.lib.objekte.kurve').Kurve	
    elif 'Flaeche' in str(obj):	
        Flaeche = importlib.import_module('agla.lib.objekte.flaeche').Flaeche	
	
    N = al[0][3]
    x, y, z = symbols("x y z")
    	
    for i in range(N):	
	
        for j, o in enumerate(obj):	
		
		     # Die Verwendung von mlab_source.set ergibt einen VTK-Fehler 
            # (fast überall)
            # Es wird stattdessen mlab_source.reset verwendet
            
            if 'Vektor' in str(o):
                al[j][1].mlab_source.reset(x=al[j][2][0][i],    
				          y=al[j][2][1][i], z=al[j][2][2][i])
            elif 'Gerade' in str(o):
                al[j][1].mlab_source.reset(x=al[j][2][0][i], y=al[j][2][1][i],    
                     z=al[j][2][2][i])
            elif 'Ebene' in str(o):
                al[j][1].mlab_source.scalars = al[j][2][i]
            elif 'Kugel' in str(o):
                al[j][1].mlab_source.set(x=al[j][2][0][i], 
                    y=al[j][2][1][i], z=al[j][2][2][i])
            elif 'Strecke' in str(o):
                al[j][1].mlab_source.reset(x=al[j][2][0][i], y=al[j][2][1][i],   
                     z=al[j][2][2][i])
            elif 'Dreieck' in str(o):
                al[j][1].mlab_source.reset(x=al[j][2][0][i], y=al[j][2][1][i],   
                     z=al[j][2][2][i])
            elif 'Viereck' in str(o):                                             
                al[j][1].mlab_source.reset(x=al[j][2][0][i], y=al[j][2][1][i], 
                     z=al[j][2][2][i])
            elif 'Kreis' in str(o):  
                al[j][1].mlab_source.reset(x=al[j][2][0][i], y=al[j][2][1][i], 
                     z=al[j][2][2][i])
            elif 'Koerper' in str(o):
                al[j][1].mlab_source.reset(x=al[j][2][0][i], y=al[j][2][1][i],   
                     z=al[j][2][2][i])					 
            elif 'Kegel' in str(o):
                al[j][1][0].mlab_source.set(x=al[j][2][0][0][i],  # set möglich
                        y=al[j][2][0][1][i], z=al[j][2][0][2][i])
                al[j][1][1].mlab_source.set(x=al[j][2][1][0][i], 
                        y=al[j][2][1][1][i], z=al[j][2][1][2][i])		
            elif 'Zylinder' in str(o):
                al[j][1][0].mlab_source.set(x=al[j][2][0][0][i],  # set möglich
                    y=al[j][2][0][1][i], z=al[j][2][0][2][i])
                al[j][1][1].mlab_source.set(x=al[j][2][1][0][i], 
                    y=al[j][2][1][1][i], z=al[j][2][1][2][i])	
                al[j][1][2].mlab_source.set(x=al[j][2][2][0][i], 
                    y=al[j][2][2][1][i], z=al[j][2][2][2][i])					 					 
            elif 'Kurve' in str(o):			                       
                al[j][1].mlab_source.reset(x=al[j][2][0][i], y=al[j][2][1][i], 
                     z=al[j][2][2][i])
            elif 'Flaeche'in str(o):                              
                if not isinstance(al[j][2], list):
                    al[j][1].mlab_source.set(x=al[j][2][0][i],  # set möglich
                        y=al[j][2][1][i], z=al[j][2][2][i])
                else:                                      
                    al[j][1].mlab_source.scalars = al[j][2][i]
					
        yield
	
	
# -----------------
# Grafik mit VisPy
# -----------------

def _Grafik_mit_vispy(*args, **kwargs):    
    """Funktion zum Erzeugen von 3D-Grafiken mit VisPy"""
	
    achsen = True if kwargs.get('achsen') is None else kwargs.get('achsen')
    box = True if kwargs.get('box') is None else kwargs.get('box')
    xy_gitter = False if kwargs.get('xy_gitter') is None else \
               kwargs.get('xy_gitter')
    xyz_gitter = False if kwargs.get('xyz_gitter') is None else \
               kwargs.get('xyz_gitter')
    skalen = True if kwargs.get('skalen') is None else kwargs.get('skalen') 
    x_skala = True if kwargs.get('x_skala') is None else kwargs.get('x_skala') 
    y_skala = True if kwargs.get('y_skala') is None else kwargs.get('y_skala')		
    z_skala = True if kwargs.get('z_skala') is None else kwargs.get('z_skala')	
	
	# string-Angaben in Eingabe sichten
    i = 1	
    for arg in args:	
        if isinstance(arg, str):
            if arg.find('=') > 0:
                exec(arg)
                continue
            else:
                print("agla: %s. Eintrag: '=' ist nicht angegeben" % i)
                return			
				
    if xyz_gitter:
        achsen = False	
    if not skalen:
        x_skala = False
        y_skala = False		
        z_skala = False	

    if isinstance(achsen, bool):
        x_bez, y_bez, z_bez = 'x', 'y', 'z'	
    else:	
        a = achsen
        if not isinstance(a, (tuple, Tuple, list)) or len(achsen) != 3:
            print('agla: Liste/Tupel mit drei Bezeichnern für die Achsen angeben')
            return
        x_bez = str(a[0]) if isinstance(a[0], Symbol) else a[0]	 	
        y_bez = str(a[1]) if isinstance(a[1], Symbol) else a[1]	 	
        z_bez = str(a[2]) if isinstance(a[2], Symbol) else a[2]
        typ = (str, unicode)
        if not (isinstance(x_bez, typ) and isinstance(y_bez, typ) and 
              isinstance(z_bez, typ))	:
            print('agla: die Bezeichner als Symbole oder Zeichenketten angeben')
            return
			
    # Einträge kontrollieren und sammeln		
    eintraege = []		# [Objekt, Spezifikation]
    i = 1	
    for arg in args:	
        if isinstance(arg, str):
            if arg.find('=') > 0:
                exec(arg)
                continue
            else:
                print("agla: %s. Eintrag: '=' ist nicht angegeben" % i)
                return			
        spez = tuple()
        if isinstance(arg, (list, tuple, Tuple)):
            obj = arg[0]
            if len(arg) > 1:
                spez = tuple(arg[1:])
        else:
            obj = arg
        s = str(type(obj))
        if not s[s.rfind('.')+1 : -2] in _klassen_mit_grafik:
            print("agla: %s. Eintrag: ein Objekt zum Zeichnen angeben" % i)
            return
        try:
            if mit_param(obj) and not obj.is_schar:	
                raise AglaError('Parameteranzahl > 1, die Darstellung ist nicht implementiert')			
            spez = _spezifikation(spez)
            if isinstance(spez, AglaError): 
                raise AglaError(spez[0])	
            if not obj.is_schar and spez[3]:
                raise AglaError('keine Schar, die Bereichsangabe ist ungültig')	
            if obj.is_schar and not spez[3]:
                raise AglaError('Schar, eine Bereichsangabe machen')
        except AglaError as e:
            print("agla: " + str(i) + ". Eintrag:", e.args[0])
            return 
        except Exception as e:
            print("agla: %s. Eintrag: die Eingaben sind fehlerhaft" % i)	
            return			
					
        eintraege += [[obj, spez]]  
        i += 1
		
    canvas = scene.SceneCanvas(keys='interactive', bgcolor='white')
    view = canvas.central_widget.add_view()
		
    if achsen:
        _axes_vispy(view, x_bez=x_bez, y_bez=y_bez, z_bez=z_bez)
    if box:
        _box_vispy(view)
    if xy_gitter:
	     _xy_gitter_vispy(view)
    if xyz_gitter:
	     _xyz_gitter_vispy(view)
    if x_skala:
        if not box and not achsen and not xy_gitter and not xyz_gitter:
            _x_skala_vispy(view, None)
        elif xy_gitter:
            _x_skala_vispy(view, 0)		        			
        elif xyz_gitter:
            _x_skala_vispy(view, 1)
        elif box and achsen:
            _x_skala_vispy(view, 1)		
        elif box and not achsen:
            _x_skala_vispy(view, 1)
        else:
            _x_skala(view, 0)	
    if y_skala:
        if not box and not achsen and not xy_gitter and not xyz_gitter:
            _y_skala_vispy(view, None)
        elif xy_gitter:
            _y_skala_vispy(view, 0)		        			
        elif xyz_gitter:
            _y_skala_vispy(view, 1)
        elif box and achsen:
            _y_skala_vispy(view, 1)		
        elif box and not achsen:
            _y_skala_vispy(view, 1)
        else:
            _y_skala_vispy(view, 0)		
    if z_skala:
        if not box and not achsen and not xy_gitter and not xyz_gitter:
            _z_skala_vispy(view, None)
        elif xy_gitter:
            _z_skala_vispy(view, None)		        			
        elif xyz_gitter:
            _z_skala_vispy(view, 1)
        elif box and achsen:
            _z_skala_vispy(view, 1)		
        elif box and not achsen:
            _z_skala_vispy(view, 1)
        else:
            _z_skala_vispy(view, 0)	
						
    for i, ein in enumerate(eintraege): 
        obj, spez = ein	
        res = obj.graf(spez, view=view)
        if isinstance(res, AglaError):
            print('agla:', res.args[0])
            return			 		
			
    cam = scene.TurntableCamera(elevation=10, azimuth=120)	
    view.camera = cam	
    canvas.show()
    app.run()
    canvas.close()
    return	True	
		
		
# -----------------	
# Zeichnen der Box
# -----------------	
	
def _box_mayavi():
    
    xl, xr, yl, yr, zl, zr = UMG._sicht_box
    data = np.array(
           [ [[xl, xl], [yl, yr], [zl, zl]],   
             [[xl, xr], [yl, yl], [zl, zl]],
             [[xl, xr], [yr, yr], [zl, zl]],
             [[xr, xr], [yl, yr], [zl, zl]],
             [[xl, xl], [yl, yr], [zr, zr]],
             [[xl, xr], [yl, yl], [zr, zr]],
             [[xl, xr], [yr, yr], [zr, zr]],
             [[xr, xr], [yl, yr], [zr, zr]],
             [[xl, xl], [yl, yl], [zl, zr]],
             [[xl, xl], [yr, yr], [zl, zr]],
             [[xr, xr], [yl, yl], [zl, zr]],
             [[xr, xr], [yr, yr], [zl, zr]] ])
    for x,y,z in data:
        mlab.plot3d(x, y, z, 
                    tube_radius=None, 
                    color=(0, 0, 0), 
                    line_width=0.01, 
                    opacity=0.3)
    _mass = UMG._mass()					
    x, y, z = [xl, xl], [yr, yr+0.25*_mass], [zl, zl]
    txt = lambda x: str(int(x)) if int(x) == x else format(x, '.1f')	
    x, y, z = [0, 0], [yr, yr+0.25*_mass], [zl, zl]
    mlab.plot3d(x, y, z, tube_radius=None, color=(0, 0, 0), line_width=0.01)
    x, y, z = [xr, xr], [yr, yr+0.25*_mass], [zl, zl]
    x, y, z = [xr, xr+0.25*_mass], [yl, yl], [zl, zl]
    x, y, z = [xr, xr+0.25*_mass], [0, 0], [zl, zl]
    mlab.plot3d(x, y, z, tube_radius=None, color=(0, 0, 0), line_width=0.01)
    x, y, z = [xr, xr+0.25*_mass], [yr, yr], [zl, zl]
    x, y, z = [xr, xr], [yl-0.25*_mass, yl], [zl, zl]
    x, y, z = [xr, xr], [yl-0.25*_mass, yl], [0, 0]
    mlab.plot3d(x, y, z, tube_radius=None, color=(0, 0, 0), line_width=0.01)
    x, y, z = [xr, xr], [yl-0.25*_mass, yl], [zr, zr]
				   
def _box_vispy(view):
    
    xl, xr, yl, yr, zl, zr = UMG._sicht_box
    data = np.array([ 
	          [[xl, yl, zl], [xl, yr, zl]],
             [[xl, yl, zl], [xr, yl, zl]], 
             [[xl, yr, zl], [xr, yr, zl]],               
             [[xr, yl, zl], [xr, yr, zl]],               			 
             [[xl, yl, zr], [xl, yr, zr]],               
             [[xl, yl, zr], [xr, yl, zr]],               
             [[xl, yr, zr], [xr, yr, zr]],               
             [[xr, yl, zr], [xr, yr, zr]],
             [[xl, yl, zl], [xl, yl, zr]],
             [[xl, yr, zl], [xl, yr, zr]],               
             [[xr, yl, zl], [xr, yl, zr]],                 			 
             [[xr, yr, zl], [xr, yr, zr]] 
			 ])
    for pos in data:
        line = scene.visuals.Line(pos=pos, color=(0, 0, 0), parent=view.scene)
        view.add(line)	

		
# -------------------------------	
# Zeichnen der Koordinatenachsen 
# -------------------------------

def _axes_mayavi(**kwargs):
    	
    x_bez = kwargs.get('x_bez')	
    y_bez = kwargs.get('y_bez')	
    z_bez = kwargs.get('z_bez')	
    xl, xr, yl, yr, zl, zr = UMG._sicht_box
    _mass = UMG._mass()
    f = (0.85, 0.85, 0.85)
    f1 = (0.1, 0.1, 0.1)		
    h = min(100., _mass)
    x_achse = _arrow(xl, 0, 0, xr+0.5*_mass, 0, 0, size=2, cone_height=h, 
	               color=f, tube_radius=None)
    y_achse = _arrow(0, yl, 0, 0, yr+0.5*_mass, 0, size=2, cone_height=h, 
	               color=f, tube_radius=None)
    z_achse = _arrow(0, 0, zl, 0, 0, zr+0.5*_mass, size=2, cone_height=h, 
	               color=f, tube_radius=None)
    mlab.text3d(xr*0.9, 0, -1.5*_mass, x_bez, scale=0.5*_mass, color=f1, 
	           opacity=0.8)   
    mlab.text3d(0, yr*0.9, -1.5*_mass, y_bez, scale=0.5*_mass, color=f1, 
	           opacity=0.8) 
    mlab.text3d(0, -1.5*_mass, zr*0.9,  z_bez, scale=0.5*_mass, 
              color=f1, opacity=0.8) 

def _axes_vispy(view, **kwargs):
    
    x_bez = kwargs.get('x_bez')	
    y_bez = kwargs.get('y_bez')	
    z_bez = kwargs.get('z_bez')	
    xl, xr, yl, yr, zl, zr = UMG._sicht_box
    x_achse = scene.visuals.Line(pos=np.array([[xl, 0, 0], [xr, 0, 0]]), 
             color=(1,0,0,1), parent=view.scene)
    view.add(x_achse)	
    y_achse = scene.visuals.Line(pos=np.array([[0, yl, 0], [0, yr, 0]]), 
             color=(0,1,0,1), parent=view.scene)
    view.add(y_achse)	
    z_achse = scene.visuals.Line(pos=np.array([[0, 0, zl], [0, 0, zr]]), 
             color=(0,0,1,1), parent=view.scene)
    view.add(z_achse)	
			  
		
# --------------------
# Zeichnen der Skalen  
# --------------------
     
def _x_skala_mayavi(pos):
    # pos = 0: entlang der x-Achse
    # pos <> 0: entlang der unteren Box-Kante	
    	
    xl, xr, yl, yr, zl, zr = UMG._sicht_box
    if max(abs(xl), xr) < 1.8:
        teiler = [0.25, 0.5]
    elif max(abs(xl), xr) < 3.9:
        teiler = [0.5, 1.]
    elif max(abs(xl), xr) < 10:            
        teiler = [1., 2.]
    else:
        schritt = [1., 2., 5., 10., 20., 50., 100., 200., 500., 1000., 5000.]
        ra = np.ceil(xr)+1 - np.ceil(xl) 
        for i in list(range(len(schritt))):
            if np.ceil(ra/4) < schritt[i]:
                teiler = [schritt[i-1]/2, schritt[i-1]]           
                break
    schritt0, schritt1 = teiler
    txt = lambda x: str(int(x)) if int(x) == x else format(x, '.1f')
    f = (0.1, 0.1, 0.1)	
    xi = 0
    if pos is None:
        return		
    elif pos:	
        yy, zz = yr, zl
    else:
        yy, zz = 0, 0	
    _mass = UMG._mass()
    op = 0.7	
    while xi <= xr:        	
        x, y, z = [xi, xi], [yy, yy+0.25*_mass], [zz, zz]
        mlab.plot3d(x, y, z, tube_radius=None, color=f, line_width=0.01, 
                  opacity=op)
        mlab.text3d(xi, yy+0.6*_mass, zz-0.3*_mass, txt(xi), \
                      scale=0.3*_mass, color=f, opacity=op)
        xi += schritt1  
    xi = 0
    while xi <= xr:
        x, y, z = [xi, xi], [yy, yy+0.25*_mass], [zz, zz]
        mlab.plot3d(x, y, z, tube_radius=None, color=f, line_width=0.01, 
                  opacity=op)
        xi += schritt0
    xi = schritt1
    while xi >= xl:
        x, y, z = [xi, xi], [yy, yy+0.25*_mass], [zz, zz]
        mlab.plot3d(x, y, z, tube_radius=None, color=f, line_width=0.01, 
                  opacity=op)
        mlab.text3d(xi, yy+0.6*_mass, zz-0.3*_mass, txt(xi), 
		           scale=0.3*_mass, color=f, opacity=op)
        xi -= schritt1  
    xi = schritt0
    while xi >= xl:
        x, y, z = [xi, xi], [yy, yy+0.25*_mass], [zz, zz]
        mlab.plot3d(x, y, z, tube_radius=None, color=f, line_width=0.01, 
                  opacity=op)
        xi -= schritt0
   
def _x_skala_vispy(view, pos):
    # pos = 0: entlang der x-Achse
    # pos <> 0: entlang der unteren Box-Kante	
    
    xl, xr, yl, yr, zl, zr = UMG._sicht_box
    if max(abs(xl), xr) < 1.8:
        teiler = [0.25, 0.5]
    elif max(abs(xl), xr) < 3.9:
        teiler = [0.5, 1.]
    elif max(abs(xl), xr) < 10:            
        teiler = [1., 2.]
    else:
        schritt = [1., 2., 5., 10., 20., 50., 100., 200., 500., 1000., 5000.]
        ra = np.ceil(xr)+1 - np.ceil(xl) 
        for i in list(range(len(schritt))):
            if np.ceil(ra/4) < schritt[i]:
                teiler = [schritt[i-1]/2, schritt[i-1]]           
                break
    schritt0, schritt1 = teiler
    txt = lambda x: str(int(x)) if int(x) == x else format(x, '.1f')
    xi = 0
    if pos is None:
        return		
    elif pos:	
        yy, zz = yr, zl
    else:
        yy, zz = 0, 0	
    _mass = UMG._mass()
    while xi <= xr:        	
        pos = np.array([[xi, yy, zz], [xi, yy+0.25*_mass, zz]])
        line = scene.visuals.Line(pos=pos, color=(0,0,0,1), parent=view.scene)
        view.add(line)
        xi += schritt1  
    xi = 0
    while xi <= xr:
        pos = np.array([[xi, yy, zz], [xi, yy+0.25*_mass, zz]])	
        line = scene.visuals.Line(pos=pos, color=(0,0,0,1), parent=view.scene)
        view.add(line)
        xi += schritt0
    xi = schritt1
    while xi >= xl:
        pos = np.array([[xi, yy, zz], [xi, yy+0.25*_mass, zz]])
        line = scene.visuals.Line(pos=pos, color=(0,0,0,1), parent=view.scene)
        view.add(line)
        xi -= schritt1  
    xi = schritt0
    while xi >= xl:
        pos = np.array([[xi, yy, zz], [xi, yy+0.25*_mass, zz]])
        line = scene.visuals.Line(pos=pos, color=(0,0,0,1), parent=view.scene)
        view.add(line)
        xi -= schritt0
		
    text1 = scene.visuals.Text(txt(0), pos=[0, yy+0.6*_mass, zz-0.3*_mass], 
           color=(0,0,0,1), font_size=12, parent=view.scene)
    text2 = scene.visuals.Text(txt(xl), pos=[xl, yy+0.6*_mass, zz-0.3*_mass], 
           color=(0,0,0,1), font_size=12, parent=view.scene)
    text3 = scene.visuals.Text(txt(xr), pos=[xr, yy+0.6*_mass, zz-0.3*_mass], 
           color=(0,0,0,1), font_size=12, parent=view.scene)
    view.add(text1)		   		
    view.add(text2)		   		
    view.add(text3)		   		

def _y_skala_mayavi(pos):
    # pos = 0: entlang der y-Achse
    # pos <> 0: entlang der unteren Box-Kante	
    	
    xl, xr, yl, yr, zl, zr = UMG._sicht_box   
    if max(abs(yl), yr) < 1.8:
        teiler = [0.25, 0.5]
    elif max(abs(yl), yr) < 3.9:
        teiler = [0.5, 1.]
    elif max(abs(yl), yr) < 10:            
        teiler = [1., 2.]
    else:
        schritt = [1., 2., 5., 10., 20., 50., 100., 200., 500., 1000., 5000.]
        ra = np.ceil(yr)+1 - np.ceil(yl) 
        for i in list(range(len(schritt))):
            if np.ceil(ra/4) < schritt[i]:
                teiler = [schritt[i-1]/2, schritt[i-1]]           
                break
    schritt0, schritt1 = teiler
    txt = lambda x: str(int(x)) if int(x) == x else format(x, '.1f')	
    f = (0.1, 0.1, 0.1)	
    yi = 0
    if pos is None:
        return		
    elif pos:	
        xx, zz = xr, zl
    else:
        xx, zz = 0, 0			
    _mass = UMG._mass()
    op = 0.7	
    mlab.text3d(xx+0.6*_mass, 0, zz-0.8*_mass, 
		   txt(0), scale=0.3*_mass, color=f, opacity=op)
    while yi <= yr:
        x, y, z = [xx, xx+0.25*_mass], [yi, yi], [zz, zz]
        mlab.plot3d(x, y, z, tube_radius=None, color=f, line_width=0.01, 
                  opacity=op)
        if yi != 0:
            mlab.text3d(xx+0.6*_mass, yi-0.3*_mass, zz-0.8*_mass, 
		           txt(yi), scale=0.3*_mass, color=f, opacity=op)
        yi += schritt1  
    yi = 0
    while yi <= yr:
        x, y, z = [xx, xx+0.25*_mass], [yi, yi], [zz, zz]
        mlab.plot3d(x, y, z, tube_radius=None, color=f, line_width=0.01, 
                  opacity=op)
        yi += schritt0
    yi = schritt1
    while yi >= yl:
        x, y, z = [xx, xx+0.25*_mass], [yi, yi], [zz, zz]
        mlab.plot3d(x, y, z, tube_radius=None, color=f, line_width=0.01, 
                  opacity=op)
        if yi != 0:		
            mlab.text3d(xx+0.6*_mass, yi-0.3*_mass, zz-0.8*_mass, 
		            txt(yi), scale=0.3*_mass, color=f, opacity=op)
        yi -= schritt1  
    yi = schritt0
    while yi >= yl:
        x, y, z = [xx, xx+0.25*_mass], [yi, yi], [zz, zz]
        mlab.plot3d(x, y, z, tube_radius=None, color=f, line_width=0.01, 
                  opacity=op)
        yi -= schritt0
         
def _y_skala_vispy(view, pos):
    # pos = 0: entlang der y-Achse
    # pos <> 0: entlang der unteren Box-Kante	
    
    xl, xr, yl, yr, zl, zr = UMG._sicht_box   
    if max(abs(yl), yr) < 1.8:
        teiler = [0.25, 0.5]
    elif max(abs(yl), yr) < 3.9:
        teiler = [0.5, 1.]
    elif max(abs(yl), yr) < 10:            
        teiler = [1., 2.]
    else:
        schritt = [1., 2., 5., 10., 20., 50., 100., 200., 500., 1000., 5000.]
        ra = np.ceil(yr)+1 - np.ceil(yl) 
        for i in list(range(len(schritt))):
            if np.ceil(ra/4) < schritt[i]:
                teiler = [schritt[i-1]/2, schritt[i-1]]           
                break
    schritt0, schritt1 = teiler
    txt = lambda x: str(int(x)) if int(x) == x else format(x, '.1f')	
    f = (0.1, 0.1, 0.1)	
    yi = 0
    if pos is None:
        return		
    elif pos:	
        xx, zz = xr, zl
    else:
        xx, zz = 0, 0			
    _mass = UMG._mass()
    while yi <= yr:
        pos = np.array([[xx, yi, zz], [xx+.25*_mass, yi, zz]])	
        line = scene.visuals.Line(pos=pos, color=(0,0,0,1), parent=view.scene)
        view.add(line)
        yi += schritt1		
    yi = 0
    while yi <= yr:
        x, y, z = [xx, xx+0.25*_mass], [yi, yi], [zz, zz]
        pos = np.array([[xx, yi, zz], [xx+.25*_mass, yi, zz]])	
        line = scene.visuals.Line(pos=pos, color=(0,0,0,1), parent=view.scene)
        view.add(line)
        yi += schritt0
    yi = schritt1
    while yi >= yl:
        pos = np.array([[xx, yi, zz], [xx+.25*_mass, yi, zz]])	
        line = scene.visuals.Line(pos=pos, color=(0,0,0,1), parent=view.scene)
        view.add(line)
        yi -= schritt1  
    yi = schritt0
    while yi >= yl:
        pos = np.array([[xx, yi, zz], [xx+.25*_mass, yi, zz]])	
        line = scene.visuals.Line(pos=pos, color=(0,0,0,1), parent=view.scene)
        view.add(line)
        yi -= schritt0
    text1 = scene.visuals.Text(txt(0), pos=[xx+0.6*_mass, 0, zz-0.8*_mass], 
           color=(0,0,0,1), font_size=12, parent=view.scene)
    text2 = scene.visuals.Text(txt(yl), pos=[xx+0.6*_mass, yl, zz-0.8*_mass], 
           color=(0,0,0,1), font_size=12, parent=view.scene)
    text3 = scene.visuals.Text(txt(yr), pos=[xx+0.6*_mass, yr, zz-0.8*_mass], 
           color=(0,0,0,1), font_size=12, parent=view.scene)
    view.add(text1)		   		
    view.add(text2)		   		
    view.add(text3)		   		
		 
def _z_skala_mayavi(pos):
    # pos = 0: entlang der z-Achse
    # pos <> 0: entlang der linken Box-Kante	
    	
    xl, xr, yl, yr, zl, zr = UMG._sicht_box   
    if max(abs(zl), zr) < 1.8:
        teiler = [0.25, 0.5]
    elif max(abs(zl), zr) < 3.9:
        teiler = [0.5, 1.]
    elif max(abs(zl), zr) < 10:            
        teiler = [1., 2.]
    else:
        schritt = [1., 2., 5., 10., 20., 50., 100., 200., 500., 1000., 5000.]
        ra = np.ceil(zr)+1 - np.ceil(zl) - 2
        for i in list(range(len(schritt))):
            if np.ceil(ra/4) < schritt[i]:
                teiler = [schritt[i-1]/2, schritt[i-1]]           
                break
    schritt0, schritt1 = teiler
    txt = lambda x: str(int(x)) if int(x) == x else format(x, '.1f')	
    f = (0.1, 0.1, 0.1)	
    zi = 0
    if pos is None:
        return		
    elif pos:	
        xx, yy = xr, yl
    else:
        xx, yy = 0, 0			
    _mass = UMG._mass()		
    op = 0.7	
    mlab.text3d(xx, yy-_mass, 0, txt(0), 
	     scale=0.3*_mass, color=f, opacity=op)
    while zi <= zr:
        x, y, z = [xx, xx], [yy-0.25*_mass, yy], [zi, zi]
        mlab.plot3d(x, y, z, tube_radius=None, color=f, line_width=0.01, 
                  opacity=op)
        if zi != 0:		
            mlab.text3d(xx, yy-_mass, zi-0.2*_mass, txt(zi), 
		            scale=0.3*_mass, color=f, opacity=op)
        zi += schritt1  
    zi = 0
    while zi <= zr:
        x, y, z = [xx, xx], [yy-0.25*_mass, yy], [zi, zi]
        mlab.plot3d(x, y, z, tube_radius=None, color=f, line_width=0.01, 
                  opacity=op)
        zi += schritt0      
    zi = schritt1
    while zi >= zl:
        x, y, z = [xx, xx], [yy-0.25*_mass, yy], [zi, zi]
        mlab.plot3d(x, y, z, tube_radius=None, color=f, line_width=0.01, 
                  opacity=op)
        if zi != 0:		
            mlab.text3d(xx, yy-_mass, zi-0.2*_mass, txt(zi), 
		            scale=0.3*_mass, color=f, opacity=op)
        zi -= schritt1  
    zi = schritt0
    while zi >= zl:
        x, y, z = [xx, xx], [yy-0.25*_mass, yy], [zi, zi]
        mlab.plot3d(x, y, z, tube_radius=None, color=f, line_width=0.01, 
                  opacity=op)
        zi -= schritt0
 
def _z_skala_vispy(view, pos):
    # pos = 0: entlang der z-Achse
    # pos <> 0: entlang der linken Box-Kante	
    
    xl, xr, yl, yr, zl, zr = UMG._sicht_box   
    if max(abs(zl), zr) < 1.8:
        teiler = [0.25, 0.5]
    elif max(abs(zl), zr) < 3.9:
        teiler = [0.5, 1.]
    elif max(abs(zl), zr) < 10:            
        teiler = [1., 2.]
    else:
        schritt = [1., 2., 5., 10., 20., 50., 100., 200., 500., 1000., 5000.]
        ra = np.ceil(zr)+1 - np.ceil(zl) - 2
        for i in list(range(len(schritt))):
            if np.ceil(ra/4) < schritt[i]:
                teiler = [schritt[i-1]/2, schritt[i-1]]           
                break
    schritt0, schritt1 = teiler
    txt = lambda x: str(int(x)) if int(x) == x else format(x, '.1f')	
    f = (0.1, 0.1, 0.1)	
    zi = 0
    if pos is None:
        return		
    elif pos:	
        xx, yy = xr, yl
    else:
        xx, yy = 0, 0			
    _mass = UMG._mass()		
    while zi <= zr:
        pos = np.array([[xx, yy-0.25*_mass, zi], [xx, yy, zi]])	
        line = scene.visuals.Line(pos=pos, color=(0,0,0,1), parent=view.scene)
        view.add(line)
        zi += schritt1  
    zi = 0
    while zi <= zr:
        pos = np.array([[xx, yy-0.25*_mass, zi], [xx, yy, zi]])	
        line = scene.visuals.Line(pos=pos, color=(0,0,0,1), parent=view.scene)
        view.add(line)
        zi += schritt0      
    zi = schritt1
    while zi >= zl:
        pos = np.array([[xx, yy-0.25*_mass, zi], [xx, yy, zi]])	
        line = scene.visuals.Line(pos=pos, color=(0,0,0,1), parent=view.scene)
        view.add(line)
        zi -= schritt1  
    zi = schritt0
    while zi >= zl:
        pos = np.array([[xx, yy-0.25*_mass, zi], [xx, yy, zi]])	
        line = scene.visuals.Line(pos=pos, color=(0,0,0,1), parent=view.scene)
        view.add(line)
        zi -= schritt0
    text1 = scene.visuals.Text(txt(0), pos=[xx, yy-_mass, 0], 
           color=(0,0,0,1), font_size=12, parent=view.scene)
    text2 = scene.visuals.Text(txt(zl), pos=[xx, yy-_mass, zl], 
           color=(0,0,0,1), font_size=12, parent=view.scene)
    text3 = scene.visuals.Text(txt(zr), pos=[xx, yy-_mass, zr], 
           color=(0,0,0,1), font_size=12, parent=view.scene)
    view.add(text1)		   		
    view.add(text2)		   		
    view.add(text3)		   		
		
 
# --------------------
# Zeichnen von Gittern
# --------------------

def _xy_gitter_mayavi():     # festes Gitter in der xy-Ebene
    	
    sb = UMG._sicht_box
    xl, xr, yl, yr, zl, zr = sb
    if not all([abs(z) == 1 for z in sb]) and \
           not all([abs(z) == 10 for z in sb]):
        print("agla: ein Gitter ist nur bei einer Sichtbox mit (-1, 1) oder \n(-10, 10) vorgesehen\n")	
        return		
    ber = list(range(11))
    if xl == -1 and xr == 1:	
        ber = ber + [-x for x in ber] 
        ber = [x/10 for x in ber]
    elif xl == -10 and xr == 10:	
        ber = ber + [-x for x in ber]

    data = []
    f = (0.1, 0.1, 0.1)
    for b in ber:	
        data += [[[xl, xr], [b, b], [0, 0]]]
        data += [[[b, b], [yl, yr], [0, 0]]]
    for x,y,z in data:
        mlab.plot3d(x, y, z, 
                    tube_radius=None, 
                    color=(0, 0, 0), 
                    line_width=0.001, 
                    opacity=0.1)
 
def _xy_gitter_vispy(view):     # festes Gitter in der xy-Ebene
    
    xl, xr, yl, yr, zl, zr = UMG._sicht_box
    if xl==-10 and xr==10 and yl==-10 and yr==10 and zl==-10 and zr==10:
        ber = list(range(2, 12, 2))
        ber = ber + [-x for x in ber]
    elif -1.2<=xl<= -0.99 and 0.99<=xr<=1.2 and -1.2<=yl<= -0.99 and \
         0.99<=yr<=1.2:
        ber = list(range(2, 10, 2))
        ber = [x/10 for x in ber] + [-x/10 for x in ber]
    else:
        if max(abs(xl), xr) < 1.8:
            teiler = [0.25, 0.5]
        elif max(abs(xl), xr) < 3.9:
            teiler = [0.5, 1.]
        elif max(abs(xl), xr) < 10:            
            teiler = [1., 2.]
        else:
            schritt = [1., 2., 5., 10., 20., 50., 100., 200., 500., 1000., 
                      5000.]
            ra = np.ceil(xr)+1 - np.ceil(xl) 
            for i in list(range(len(schritt))):
                if np.ceil(ra/4) < schritt[i]:
                    teiler = [schritt[i-1]/2, schritt[i-1]]           
                    break
        dd = 2 * teiler[0]
        ber = []
        i = 1		
        while True:
            if xl + i*dd < xr -1/100*(xr-xl):
                ber += [xl + i*dd]
            else:
                break			
            i += 1			
			
    data = []			
    for b in ber:	
        data += [ [[xl, b, 0], [xr, b, 0]],
                [[b, yl, 0], [b, yr, 0]] ]				
    data = np.array(data)		
    for pos in data:
        line = scene.visuals.Line(pos=pos, color=(0,0,0,1), parent=view.scene)
        view.add(line)		
 
def _xyz_gitter_mayavi():     # festes Gitter in allen 3 Koordinatenebenen

    sb = UMG._sicht_box
    xl, xr, yl, yr, zl, zr = sb
    if not all([abs(z) == 1 for z in sb]) and \
           not all([abs(z) == 10 for z in sb]):
        print("agla: ein Gitter ist nur bei einer Sichtbox mit (-1, 1) oder \n(-10, 10) vorgesehen\n")	
        return		
    if xr == 10:		
        dx = dy = dz = 1
    else:		
        dx = dy = dz = 1/10
		
    data = []
    for i in range(11):	
        data += [[[xl, xr], [yl+i*dy, yl+i*dy], [zl, zl]]]
        data += [[[xl, xr], [yr-i*dy, yr-i*dy], [zl, zl]]]
        data += [[[xl+i*dx, xl+i*dx], [yl, yr], [zl, zl]]]
        data += [[[xr-i*dx, xr-i*dx], [yl, yr], [zl, zl]]]
        data += [[[xl, xr], [yl, yl], [zl+i*dz, zl+i*dz]]]
        data += [[[xl, xr], [yl, yl], [zr-i*dz, zr-i*dz]]]
        data += [[[xl+i*dx, xl+i*dx], [yl, yl], [zl, zr]]]
        data += [[[xr-i*dx, xr-i*dx], [yl, yl], [zl, zr]]]
        data += [[[xl, xl], [yl+i*dy, yl+i*dy], [zl, zr]]]
        data += [[[xl, xl], [yr-i*dy, yr-i*dy], [zl, zr]]]
        data += [[[xl, xl], [yl, yr], [zl+i*dz, zl+i*dz]]]	
        data += [[[xl, xl], [yl, yr], [zr-i*dz, zr-i*dz]]]	
    for x,y,z in data:
        mlab.plot3d(x, y, z, 
                    tube_radius=None, 
                    color=(0, 0, 0), 
                    line_width=0.001, 
                    opacity=0.1)
 
def _xyz_gitter_vispy():     # festes Gitter in allen 3 Koordinatenebenen
    xl, xr, yl, yr, zl, zr = UMG._sicht_box
    dx, dy, dz = (xr - xl)/10, (yr - yl)/10, (zr - zl)/10
    data = []
    for i in range(11):	
        data += [[[xl, xr], [yl+i*dy, yl+i*dy], [zl, zl]]]
        data += [[[xl+i*dx, xl+i*dx], [yl, yr], [zl, zl]]]
        data += [[[xl, xr], [yl, yl], [zl+i*dz, zl+i*dz]]]
        data += [[[xl+i*dx, xl+i*dx], [yl, yl], [zl, zr]]]
        data += [[[xl, xl], [yl+i*dy, yl+i*dy], [zl, zr]]]
        data += [[[xl, xl], [yl, yr], [zl+i*dz, zl+i*dz]]]	
 

 
# =====================	 
# Zeichnen eines Pfeils
# =====================	 

# ----------------
# Pfeil für mayavi
# ----------------

def _arrow_mayavi(x1, y1, z1, x2, y2, z2,    # Pfeil von P1 nach P2   
                color=(0, 0, 0),
                size=None,         # die Stärke des Schaftes; Werte: line_widh-Werte
                tube_radius=None,   # für den Schaft
                cone_height=None):  # <= 100 (aus tvtk)
								
    x1, y1, z1 = float(x1), float(y1), float(z1) 				
    x2, y2, z2 = float(x2), float(y2), float(z2) 				
    p1, p2 = np.array([x1, y1, z1]), np.array([x2, y2, z2])
    vv = p2 - p1
    ll = np.sqrt(np.dot(vv, vv))
    if not color:
        f = (0, 0, 0)
    else:
        f = color
    if not size:
        d = UMG._staerke[1][1]
    else:		
        d = size
    _mass = UMG._mass()		
    if not cone_height:
        if ll < 0.1*_mass:
            h = min(100.0, (0.38*_mass) * ll)
        else:
            h = min(100.0, 0.7 * _mass)  
    else:
         h = min(100, cone_height)
    r = min(100., d / (d**2+7.) * 0.9 *_mass)   # kegel_radius; er ist beschränkt
    if size < 0.6:
        r = 2 * r
	
    if not tube_radius:
        tr = None
    else:
        tr = d/50. * _mass
        
    # Ermittlung der Lage der Spitze aus  länge(a(P2-P1)) = h
    a = h / 2. / ll
    kegel_pos = [x2-a*vv[0],  y2-a*vv[1], z2-a*vv[2]]  
    
    # die Spitze  
    cone = visual.Cone(pos=kegel_pos, 
                       axis=vv,
                       color=f, 
                       height=h,
                       radius=r)
					   
    # der Schaft
    x, y, z = [x1, x1+0.95*(x2-x1)], [y1, y1+0.95*(y2-y1)], [z1, z1+0.95*(z2-z1)]             
    line = mlab.plot3d(x, y, z, line_width=d, color=f, tube_radius=tr)      
    
    return cone, line        

	
# ---------------
# Pfeil für vispy
# ---------------
	
def _arrow_vispy(view, x1, y1, z1, x2, y2, z2,    # Pfeil von P1 nach P2 
           cols=32,
           rows=32,
           radius=0.1,
           cone_radius=0.15,
           cone_length=0.2,
           color=(0, 0, 0, 1)):  
    x1, y1, z1 = float(x1), float(y1), float(z1)
    x2, y2, z2 = float(x2), float(y2), float(z2)
    p1, p2 = np.array([x1, y1, z1]), np.array([x2, y2, z2])
    vv = p2 - p1
    ll = np.sqrt(np.dot(vv, vv))
    vv = vv / ll
    vz1 = np.array([0.0, 0.0, 1.0])	
    vz2 = np.array([0.0, 0.0, -1.0])
    if np.sqrt(np.dot(vv-vz1, vv-vz1)) < 1e-6:
        alpha = 0.0                         # Winkel mit der xy-Ebene
        dd = np.array([1.0, 0.0, 0.0])         # Drehachse
    elif np.sqrt(np.dot(vv-vz2, vv-vz2)) < 1e-6:
        alpha = np.pi                         
        dd = np.array([1.0, 0.0, 0.0])         		
    else:		
        alpha = np.arccos(vv[2])                      
        dd = np.cross(vv, np.array([0.0, 0.0, 1.0]))    
    arrow = create_arrow(cols, rows, radius=radius, length=ll,   # entlang der positiven z-Achse
                      cone_length=cone_length, cone_radius=cone_radius)
    mesh = scene.visuals.Mesh(meshdata=arrow, color=color)
    rot = AffineTransform()
    mat = _np_rot_matrix(alpha, dd)
    bild = np.dot(mat, [0, 0, 1])
    if np.sqrt(np.dot(bild-vv, bild-vv)) < 1e-3:    # Feststellen der Drehrichtung
        rot.rotate(alpha / np.pi * 180., dd) 
    else:
        rot.rotate(-alpha / np.pi * 180., dd)		
    trans = STTransform(translate=(x1, y1, z1))
    mesh.transform =  ChainTransform([trans, rot])
    return mesh	
	
if UMG.grafik_3d == 'mayavi':
    _arrow = _arrow_mayavi	
else:
    _arrow = _arrow_vispy	
	
	
# --------------------
# Pfeil für matplotlib
# --------------------

def _arrow2(x1, y1, x2, y2,    # Pfeil von P1 nach P2 
                linewidth=0.5,  
                color=(0, 0, 0),
                head_width=0.18,         
                head_length=0.5): 
								
    Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
    _mass = UMG._mass()		
    x1, y1 = float(x1), float(y1) 				
    x2, y2 = float(x2), float(y2) 				
    p1, p2 = Vektor(x1, y1), Vektor(x2, y2)
    vv = Vektor(p1, p2)
    ev = vv.einh_vekt
    if vv.betrag < _mass:
        head_length = 0.5 * vv.betrag
    if linewidth > 2.0:
        head_width = 0.2	
    head_width *= _mass
    head_length *= _mass	
    pp = p2 - head_length * ev
    px, py = float(pp.x), float(pp.y)
    ex, ey = float(ev.x), float(ev.y)	
    line = plt.Line2D([x1, px], [y1, py], color=color, linewidth=linewidth)
    head = patches.FancyArrow(px, py, 0.0001*ex, 0.0001*ey,
                           facecolor=color,
                           edgecolor=color,
                           head_width=head_width,  
                           head_length=head_length,
						       alpha=0.6)
    return line, head	
		
	
	
# =============================
# Implizites plotten mit Mayavi
# =============================

# aus dem Internet angepaßt: 
#
# http://indranilsinharoy.com/2014/03/02/plotting-algebraic-surfaces-using-mayavi/

def _implicit_plot_mayavi(expr, ext_grid, fig_handle=None, Nx=100, Ny=100, Nz=100,
                 col_isurf=(50/255, 199/255, 152/255), 
                 col_osurf=(240/255,36/255,87/255),
                 opa_val=0.8, opaque=True, ori_axis=False, **kwargs):
    """Funktion zum impliziten Plotten in Mayavi"""
 	
    from numpy import (pi, sqrt, sin, cos, tan, exp, log, sinh, cosh, tanh,
             arcsin, arccos, arctan, arcsinh, arccosh, arctanh)				   

    if fig_handle==None: 
        fig = mlab.figure(1, bgcolor=(0.97, 0.97, 0.97), fgcolor=(0, 0, 0), \
                        size=(800, 800))
    else:
        fig = fig_handle
    xl, xr, yl, yr, zl, zr = ext_grid
    x, y, z = np.mgrid[xl:xr:eval('{}j'.format(Nx)),
                       yl:yr:eval('{}j'.format(Ny)),
                       zl:zr:eval('{}j'.format(Nz))]
    scalars = eval(expr)
    src = mlab.pipeline.scalar_field(x, y, z, scalars)
    if opaque:
        delta = 1.e-5
        opa_val=1.0
    else:
        delta = 0.0
    cont1 = mlab.pipeline.iso_surface(src, color=col_isurf, contours=[0-delta],
                                      transparent=False, opacity=opa_val)
    cont1.compute_normals = False 
    if opaque: 
        cont2 = mlab.pipeline.iso_surface(src, color=col_osurf, contours=[0+delta],
                                          transparent=False, opacity=opa_val)
        cont2.compute_normals = False
        cont1.actor.property.backface_culling = True
        cont2.actor.property.frontface_culling = True
        cont2.actor.property.specular = 0.2 #0.4 #0.8
        cont2.actor.property.specular_power = 55.0 #15.0
    else:  
        cont1.actor.property.specular = 0.2 #0.4 #0.8
        cont1.actor.property.specular_power = 55.0 #15.
    return True

if UMG.grafik_3d == 'mayavi':
    _implicit_plot = _implicit_plot_mayavi	
else:
    _implicit_plot = None	
	
	
	
# =================================
# Zeichnen vieler Linien mit Mayavi
# =================================
#
# Anpassung des 'many_lines' - Beispiels aus der Mayavi-Dokumentation       
#	
def _many_lines_mayavi(f, uw, N, n,     # Fläche, u- oder w-Linien, Anzahl 
         color=(0.7, 0.7, 0.7),         # Punkte je Linie, Linienanzahl
		  line_width=1, 
		  opacity=0.5):  
    
    uber, wber = f.ber	
    uu, uo = float(uber[0]), float(uber[1])
    wu, wo = float(wber[0]), float(wber[1])
    lu, lw = uo-uu, wo-wu
    u, w = symbols('u w')
    p = f.pkt(u, w)	  

    i = Symbol('i')
    if uw == Symbol('w'):
        ers = wu + i/n*lw
        sx = str(p.x.subs(Symbol('w'), ers))   
        sy = str(p.y.subs(Symbol('w'), ers))    
        sz = str(p.z.subs(Symbol('w'), ers))
    else:
        ers = uu + i/n*lu   
        sx = str(p.x.subs(Symbol('u'), ers))
        sy = str(p.y.subs(Symbol('u'), ers))    
        sz = str(p.z.subs(Symbol('u'), ers))
    
    u = np.linspace(uu, uo, N)
    w = np.linspace(wu, wo, N)

    x = list()
    y = list()
    z = list()
    s = list()
    connections = list()
    index = 0

    abs=np.abs; pi=np.pi; sqrt=np.sqrt; exp=np.exp; log=np.log
    ln=np.log; sin=np.sin; sinh=np.sinh; Abs=np.abs
    arcsin=np.arcsin; arsinh=np.arcsinh; cos=np.cos; cosh=np.cosh
    arccos=np.arccos; arcosh=np.arccosh; tan=np.tan; tanh=np.tanh 
    arctan=np.arctan; artanh=np.arctanh 
    asin=np.arcsin; acos=np.arccos; atan=np.arctan 
    asinh=np.arcsinh; acosh=np.arccosh; atanh=np.arctanh 			
			       						
    for i in range(n+1):        
        if uw == Symbol('w'):            
            if sx.find('u') >= 0:    
                x.append(eval(sx.replace('Abs', 'np.abs')))
            else:
                sx = str(float(p.x.subs(Symbol('w'), wu + i/n*lw))) 
                x.append([eval(sx) for uu in u])                  
            if sy.find('u') >= 0:    
                y.append(eval(sy.replace('Abs', 'np.abs')))
            else:
                sy = str(float(p.y.subs(Symbol('w'), wu + i/n*lw)))    
                y.append([eval(sy) for uu in u])        
            if sz.find('u') >= 0:
                z.append(eval(sz.replace('Abs', 'np.abs')))
            else:
                sz = str(float(p.z.subs(Symbol('w'), wu + i/n*lw))) 
                z.append([eval(sz) for uu in u])
        else:            
            if sx.find('w') >= 0:    
                x.append(eval(sx))
            else:
                sx = str(float(p.x.subs(Symbol('u'), uu + i/n*lu)))
                x.append([eval(sx) for ww in w])                     
            if sy.find('w') >= 0:    
                y.append(eval(sy))
            else:
                sy = str(float(p.y.subs(Symbol('u'), uu + i/n*lu)))    
                y.append([eval(sy) for ww in w])        
            if sz.find('w') >= 0:
                z.append(eval(sz))
            else:
                sz = str(float(p.z.subs(Symbol('u'), uu + i/n*lu))) 
                z.append([eval(sz) for ww in w])            
        s.append(u)
        connections.append(np.vstack(
                       [np.arange(index,   index + N - 1.5),
                        np.arange(index + 1, index + N - .5)]
                            ).T)
        index += N

    x = np.hstack(x)
    y = np.hstack(y)
    z = np.hstack(z)
    s = np.hstack(s)
    connections = np.vstack(connections)
    src = mlab.pipeline.scalar_scatter(x, y, z, s)
    src.mlab_source.dataset.lines = connections
    src.update()
    lines = mlab.pipeline.stripper(src)
    mlab.pipeline.surface(lines, color=color, line_width=line_width, opacity=opacity)
	
	
	
# ==========================	
# Funktionen für 2D - Grafik
# ==========================	
	
# ----------------------	
# Grafik mit matplotlib
# ----------------------
	
def _Grafik_mit_matplotlib(*args, **kwargs):    
    """Funktion zum Erzeugen von 2D-Grafiken mit matplotlib"""
					
    Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
				
    plt.close('all')		
    mlab.close(all=True)
		
    achsen = True if kwargs.get('achsen') is None else kwargs.get('achsen')
    gitter = False if kwargs.get('gitter') is None else kwargs.get('gitter')
    skalen = True if kwargs.get('skalen') is None else kwargs.get('skalen') 
    x_skala = True if kwargs.get('x_skala') is None else kwargs.get('x_skala') 
    y_skala = True if kwargs.get('y_skala') is None else kwargs.get('y_skala')		
    groesse = kwargs.get('groesse')
    text = kwargs.get('text')
    bez = kwargs.get('bez')
	
	# string-Angaben in Eingabe sichten
    i = 1	
    for arg in args:	
        if isinstance(arg, str):
            if arg.find('=') > 0:
                exec(arg)
                continue
            else:
                print("agla: %s. Eintrag: '=' ist nicht angegeben" % i)
                return	
	
    if not skalen:
        x_skala = False
        y_skala = False	
		
    if isinstance(achsen, bool):
        x_bez, y_bez = 'x', 'y'	
    else:	
        a = achsen
        if not isinstance(a, (tuple, Tuple, list)) or len(achsen) != 2:
            print('agla: Liste/Tupel mit zwei Bezeichnern für die Achsen angeben')
            return
        x_bez = str(a[0]) if isinstance(a[0], Symbol) else a[0]	 	
        y_bez = str(a[1]) if isinstance(a[1], Symbol) else a[1]	 	
        if not (isinstance(x_bez, str) and isinstance(y_bez, str)):
            print('agla: die Bezeichner als Symbole oder Zeichenketten angeben')
            return
			  				
    if x_skala:
        if not achsen and not gitter:
            x_skala = False
    if y_skala:
        if not achsen and not gitter:
            y_skala = False
		
    if groesse:
        if not iterable(groesse) and len(groesse) == 2:        
            print('agla: Größenangaben sind als Tupel/Liste mit 2 Elementen zu schreiben')
            return
        typ = int, Integer, float, Float, Rational			
        if not all([isinstance(el, typ) and isinstance(el, typ) and el > 0 
            for el in groesse]):
            print('agla: Größenangaben müssen die Form (breite, höhe) mit positiven Werten haben')
            return
			
    if bez:
        text = bez	
    if text:
        meld = 'agla: Textangaben sind als Tupel/Liste mit Elementen der \nLänge 3 oder 4 zu schreiben'
        if not iterable(text):
            print(meld)		
            return
        if not all([iterable(el) and len(el) in (2, 3) for el in text]):        
            print(meld)		
            return
        if not all([isinstance(el[0], Vektor)  and isinstance(el[1], str) 
		    for el in text]):
            print('agla: Textelemente müssen die Form (Vektor/Punkt, \'text\' /[, text_größe]) haben')
            return
        tg = [el for el in text if len(el) == 3]			
        if not all([el[2] in (1, 2) for el in tg]):
            print('agla: Textgrößen sind  1:kleiner, 2:größer')
            return
            		   
    # Einträge kontrollieren und sammeln		
    eintraege = []		# [Objekt, Spezifikation]
    i = 1	
    for arg in args:	
        if isinstance(arg, str):
            if arg.find('=') > 0:
                exec(arg)
                continue
            else:
                print("agla: %s. Eintrag: '=' ist nicht angegeben" % i)
                return			
        spez = tuple()
        if isinstance(arg, (list, tuple, Tuple)):
            obj = arg[0]
            if len(arg) > 1:
                spez = tuple(arg[1:])
        else:
            obj = arg
        s = str(type(obj))
        if not s[s.rfind('.')+1 : -2] in _klassen_mit_grafik:
            print("agla: %s. Eintrag: ein Objekt zum Zeichnen angeben" % i)
            return
			
        try:
            if mit_param(obj) and not obj.is_schar:	
                raise AglaError('Parameteranzahl > 1, die Darstellung ist nicht implementiert')			
            spez = _spezifikation(spez)
            if isinstance(spez, AglaError): 
                raise AglaError(spez[0])	
            if not obj.is_schar and spez[3]:
                raise AglaError('keine Schar, die Bereichsangabe ist ungültig')	
            if obj.is_schar and not spez[3]:
                raise AglaError('Schar, eine Bereichsangabe machen')
        except AglaError as e:
            print("agla: " + str(i) + ". Eintrag:", e.args[0])
            return        		
        except Exception:
            print("agla: %s. Eintrag: die Eingaben sind fehlerhaft" % i)	
            return			
						
        eintraege += [[obj, spez]]  
        i += 1

    # auf Animationsfähigkeit untersuchen		
    for i, ein in enumerate(eintraege): 
        obj, spez = ein
        if spez[3]:
            print('agla: ' + str(i+1) + '. Eintrag:', \
                 'die animierte Darstellung von Objekten in der Ebene \n' +\
                 '      ist nicht implementiert')
            return									

    _mass = UMG._mass()				
    fig = plt.figure(figsize=(8, 6))		
    if groesse:
        fig = plt.figure(figsize=(groesse[0], groesse[1]))		
    plt.axes().set_aspect('equal')	
    ax = fig.add_subplot(1, 1, 1)
    ax.axis('off')
	
    xl, xr, yl, yr = UMG._sicht_box[:4]
    d = 0	
    if gitter:
	    d = _mass / 20
    plt.axis([xl-d, xr+d, yl-d, yr+d])     
    f = (0.65, 0.65, 0.65)
    if achsen:
        ax.arrow(xl, 0.0, (xr-xl)-0.6*_mass, 0.0, head_length=0.6*_mass, \
               head_width=0.18*_mass, linewidth=0.5, fc=f, ec=f)
        ax.arrow(0.0, yl, 0.0, (yr-yl)-0.6*_mass, head_length=0.6*_mass, \
               head_width=0.18*_mass, linewidth=0.5, fc=f, ec=f)
        plt.text(xr-0.5*_mass, -1.2*_mass, x_bez, size=9, alpha=0.5)
        plt.text(-1.2*_mass, yr-0.5*_mass, y_bez, size=9, alpha=0.5)
    if gitter:
	     _gitter2(ax, null=(not achsen and gitter))
    if x_skala:
        _x_skala2(ax)
    if y_skala:
        _y_skala2(ax)
	
    if text:	
        for t in text:
            if len(t) < 3:		
                plt.text(t[0].x, t[0].y, t[1], size=10, alpha=0.8)
            else:	
                font = {1:8, 2:12}			
                plt.text(t[0].x, t[0].y, t[1], size=font[t[2]], alpha=0.8)
                				
    # Animation nicht implementiert	
    animations_liste = []
	
    for i, ein in enumerate(eintraege): 
        obj, spez = ein	
        res = obj.graf(spez, figure=fig)
        if isinstance(res, AglaError):
            print('agla:', res.args[0])
            return			 
        #if res is None:
        #    print('agla: ' + str(i+1) + '. Eintrag:', \
        #      'die animierte Darstellung des Objektes ist nicht implementiert')
        #    pass			
        if isinstance(obj, Vektor) and isinstance(spez[0], Vektor):
            plt.gca().add_line(res[0])
            plt.gca().add_patch(res[1])		
        if spez[3]:
            animations_liste += [[type(obj), res[0], res[1]]]            
    if animations_liste:
        anim2(animations_liste)    # Funktion ist außerhalb definiert
				
    plt.show()
	
    return	
	
	
# --------------------------------------
# Zeichnen eines Gitters und der Skalen
# --------------------------------------
	
def _gitter2(ax, **kwargs):

    null = kwargs.get('null')  
    sb = UMG._sicht_box
    xl, xr, yl, yr, zl, zr = sb
    if not all([abs(z) == 1 for z in sb]) and \
           not all([abs(z) == 10 for z in sb]):
        print("agla: ein Gitter ist nur bei einer Sichtbox mit (-1, 1) oder \n(-10, 10) vorgesehen\n")	
        return		
    ber = list(range(1, 11))
    if null:
        ber += [0]			
    if xl == -1 and xr == 1:	
        ber = ber + [-x for x in ber] 
        ber = [x/10 for x in ber]
    elif xl == -10 and xr == 10:	
        ber = ber + [-x for x in ber]	
    f = (0.1, 0.1, 0.1)
    for b in ber:	
        ax.plot([xl, xr], [b, b], color=f, linewidth=0.1)
        ax.plot([b, b], [yl, yr], color=f, linewidth=0.1)	
     
def _x_skala2(ax):

    xl, xr, yl, yr = UMG._sicht_box[:4]
    if max(abs(xl), xr) < 1.8:
        teiler = [0.25, 0.5]
    elif max(abs(xl), xr) < 3.9:
        teiler = [0.5, 1.]
    elif max(abs(xl), xr) < 10:            
        teiler = [1., 2.]
    else:
        schritt = [1., 2., 5., 10., 20., 50., 100., 200., 500., 1000., 5000.]
        ra = np.ceil(xr)+1 - np.ceil(xl) 
        for i in list(range(len(schritt))):
            if np.ceil(ra/4) < schritt[i]:
                teiler = [schritt[i-1]/2, schritt[i-1]]           
                break
    if xl == -10 and xr == 10 and	yl == -10 and yr == 10:
        teiler = [1, 1]
    if -1.2<=xl<= -1.0 and 1.0<=xr<=1.2 and -1.2<=yl<= -1.0 and 1.0<=yr<=1.2:
        teiler = [0.1, 0.2]
				
    schritt0, schritt1 = teiler
    f = (0.35, 0.35, 0.35)	
    _mass = UMG._mass()		
    ax.text(0.05*_mass, -0.6*_mass, '0', color=f, fontsize=6)
    xi = schritt1
    while xi < 0.999*xr:
        x, y = [xi, xi], [-0.1*_mass, 0.1*_mass]
        ax.plot(x, y, color=f, linewidth=0.5)
        if isinstance(xi, (int, Integer)) or xi == int(xi):
            ax.text(xi, -0.6*_mass, str(int(xi)), color=f, \
                   fontsize=6, horizontalalignment='center')
        else:		
            ax.text(xi, -0.6*_mass, format(xi, '.1f'), color=f, \
                   fontsize=6, horizontalalignment='center')
        xi += schritt1 
    if schritt1 != schritt0:		
        xi = schritt0
        while xi < 0.999*xr:
            x, y = [xi, xi], [-0.1*_mass, 0.1*_mass]
            ax.plot(x, y, color=f, linewidth=0.5)
            xi += schritt0
    xi = -schritt1
    while xi > 0.999*xl:
        x, y = [xi, xi], [-0.1*_mass, 0.1*_mass]
        ax.plot(x, y, color=f, linewidth=0.5)
        if isinstance(xi, (int, Integer)) or xi == int(xi):
            ax.text(xi, -0.6*_mass, str(int(xi)), color=f, \
                   fontsize=6, horizontalalignment='center')
        else:		
            ax.text(xi, -0.6*_mass, format(xi, '.1f'), color=f, 
			  fontsize=6, horizontalalignment='center')
        xi -= schritt1  
    if schritt1 != schritt0:		
        xi = -schritt0
        while xi > 0.999*xl:
            x, y = [xi, xi], [-0.1*_mass, 0.1*_mass]
            ax.plot(x, y, color=f, linewidth=0.5)
            xi -= schritt0

def _y_skala2(ax):

    xl, xr, yl, yr = UMG._sicht_box[:4]
    if max(abs(yl), yr) < 1.8:
        teiler = [0.25, 0.5]
    elif max(abs(yl), yr) < 3.9:
        teiler = [0.5, 1.]
    elif max(abs(yl), yr) < 10:            
        teiler = [1., 2.]
    else:
        schritt = [1., 2., 5., 10., 20., 50., 100., 200., 500., 1000., 5000.]
        ra = np.ceil(yr)+1 - np.ceil(yl) 
        for i in list(range(len(schritt))):
            if np.ceil(ra/4) < schritt[i]:
                teiler = [schritt[i-1]/2, schritt[i-1]]           
                break
    if xl == -10 and xr == 10 and	yl == -10 and yr == 10:
        teiler = [1, 1]
    if -1.2<=xl<= -1.0 and 1.0<=xr<=1.2 and -1.2<=yl<= -1.0 and 1.0<=yr<=1.2:
        teiler = [0.1, 0.2]
				
    schritt0, schritt1 = teiler
    f = (0.35, 0.35, 0.35)	
    yi = schritt1
    _mass = UMG._mass()		
    while yi < 0.999*yr:
        x, y = [-0.1*_mass, 0.1*_mass], [yi, yi]
        ax.plot(x, y, color=f, linewidth=0.5)
        if isinstance(yi, (int, Integer)) or yi == int(yi):
            ax.text(-0.3*_mass, yi, str(int(yi)), color=f, horizontalalignment='right',
			        fontsize=6, verticalalignment='center')
        else:		
            ax.text(-0.3*_mass, yi, format(yi, '.1f'), color=f, horizontalalignment='right',
			       fontsize=6, verticalalignment='center')
        yi += schritt1 
    if schritt1 != schritt0:		
        yi = schritt0
        while yi < 0.999*yr:
            x, y = [-0.1*_mass, 0.1*_mass], [yi, yi]
            ax.plot(x, y, color=f, linewidth=0.5)
            yi += schritt0
    yi = -schritt1
    while yi > yl:
        x, y = [-0.1*_mass, 0.1*_mass], [yi, yi]
        ax.plot(x, y, color=f, linewidth=0.5)
        if isinstance(yi, (int, Integer)) or yi == int(yi):
            ax.text(-0.3*_mass, yi, str(int(yi)), color=f, horizontalalignment='right',
			        fontsize=6, verticalalignment='center')
        else:		
            ax.text(-0.3*_mass, yi, format(yi, '.1f'), color=f, horizontalalignment='right',
			        fontsize=6, verticalalignment='center')
        yi -= schritt1  
    if schritt1 != schritt0:		
        yi = -schritt0
        while yi > yl:
            x, y = [-0.1*_mass, 0.1*_mass], [yi, yi]
            ax.plot(x, y, color=f, linewidth=0.5)
            yi -= schritt0
	
	 


