#!/usr/bin/python
# -*- coding utf-8 -*-


#                                                 
#  Start-Programm von agla           
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



# -----------------------------------------------------------------------------
# Variable zur Steuerung des Testbetriebes
# -----------------------------------------------------------------------------
#
# zur Verwendung durch den Programmierer; hier im Quelltext ein-/ausschalten
# _TEST = True:  es werden die vollständigen Python-Fehlermitteilungen angezeigt 
# _TEST = False: es werden teilweise agla-eigene Fehlermitteilungen angezeigt

_TEST = False


# -----------------------------------------------------------------------------
# Zurücksetzen
# -----------------------------------------------------------------------------

_ip = get_ipython()
_ip.magic('reset -sf')


# -----------------------------------------------------------------------------
# Importe
# -----------------------------------------------------------------------------

import importlib
import copy

from IPython.core.inputtransformer import InputTransformer
from IPython.display import display, Math

from sympy.core.expr import Expr
from sympy.matrices import Matrix as SympyMatrix  
from sympy.core.compatibility import iterable
from sympy.core.containers import Tuple

# ausgewählte SymPy-Objekte und -funktionen zur unmittelbaren Verfügung 
# des Nutzers
#
from sympy.abc import *    
from sympy.core.numbers import Rational, Integer, Float, pi, E, I   
from sympy.core.symbol import Symbol, symbols
from sympy import (sympify, solve, solveset, expand, collect, factor, simplify,  
     nsimplify, radsimp, trigsimp, nsolve, diff, N)
				
# Initialisierung der Latex-Ausgabe	
#
from sympy.interactive.printing import init_printing
init_printing()	
from sympy.printing.latex import LatexPrinter
LatexPrinter._default_settings["mat_delim"] = "(" 

# Import ausgewählter agla-Elemente	
#
from agla.lib.objekte.vektor import v   
from agla.lib.objekte.umgebung import UMG, sicht_box, sichtBox 
from agla.lib.objekte.ausnahmen import AglaError		

# Alle anderen Objekte und Funktionen werden dynamisch nachgeladen (s.u.)


# -----------------------------------------------------------------------------
# Variable zur Steuerung von internen Vereinfachungen
# -----------------------------------------------------------------------------
#
# Systemvariable, zur interaktiven Benutzung durch den Anwender
# UMG.SIMPL = True:  in den Programmen vorgesehene Vereinfachungen werden  
#                    automatisch durchgeführt
# UMG.SIMPL = False: es werden keine automatischen Vereinfachungen durch-
#                    geführt 

UMG.SIMPL = True

# -----------------------------------------------------------------------------
# Variable zur Steuerung der Berechnung von hyperbolischen Objekten
# -----------------------------------------------------------------------------
#
# Systemvariable, zur interaktiven Benutzung durch den Anwender
# UMG.EXAKT = True:  die Berechnungen werden exakt (mit SymPY / SympyEngine) 
#                    durchgeführt
# UMG.EXAKT = False: die Berechnungen werden mit float-Werten durchgeführt 

UMG.EXAKT = False

		
# -----------------------------------------------------------------------------
# Dynamisches Importieren	
# -----------------------------------------------------------------------------

_attr = 'agla.lib.objekte.'
_fkt = 'agla.lib.funktionen.funktionen'
_abb_fkt = 'agla.lib.funktionen.abb_funktionen'
_graf_fkt = 'agla.lib.funktionen.graf_funktionen'
_verf = 'agla.lib.funktionen.verfahren'


_to_load = {           

    'v'             : _attr + 'vektor', 
    'Vektor'        : _attr + 'vektor', 
	'Punkt'         : _attr + 'vektor', 
	'O'             : _attr + 'vektor', 
    'O2'            : _attr + 'vektor', 
	'X'             : _attr + 'vektor', 
	'X2'            : _attr + 'vektor',
    '_ZeilenVektor' : _attr + 'vektor',	


    'Abbildung' : _attr + 'abbildung',
	
	'Gerade'   : _attr + 'gerade', 
	'x_achse'  : _attr + 'gerade', 
	'y_achse'  : _attr + 'gerade', 
	'z_achse'  : _attr + 'gerade',
    'xAchse'   : _attr + 'gerade', 
	'yAchse'   : _attr + 'gerade', 
	'zAchse'   : _attr + 'gerade', 
	'x_achse2' : _attr + 'gerade', 
	'y_achse2' : _attr + 'gerade', 
	'xAchse2'  : _attr + 'gerade', 
	'yAchse2'  : _attr + 'gerade',

    'Ebene'    : _attr + 'ebene', 
	'xy_ebene' : _attr + 'ebene',
	'xz_ebene' : _attr + 'ebene',
	'yz_ebene' : _attr + 'ebene',
    'xyEbene'  : _attr + 'ebene', 
	'xzEbene'  : _attr + 'ebene', 
	'yzEbene'  : _attr + 'ebene',

    'Parallelogramm' : _attr + 'parallelogramm', 
	'ParGramm'       : _attr + 'parallelogramm',
	
	'Kreis'      : _attr + 'kreis', 
	'EinhKreis'  : _attr + 'kreis', 
	'EinhKreis2' : _attr + 'kreis',
	
	'Flaeche'          : _attr + 'flaeche',  
	'Sphaere'          : _attr + 'flaeche',
	'KugelOberFlaeche' : _attr + 'flaeche', 
	'EinhSphaere'      : _attr + 'flaeche', 
    'HypSchale'        : _attr + 'flaeche',
	
	'K2O'              : _attr + 'k2o', 
	'Kurve2terOrdnung' : _attr + 'k2o', 
	'KegelSchnitt'     : _attr + 'k2o',
	
	'F2O'                      : _attr + 'f2o', 
	'Flaeche2terOrdnung'       : _attr + 'f2o', 
	'Ellipsoid'                : _attr + 'f2o',               
    'EinSchaligesHyperboloid'  : _attr + 'f2o', 
	'ZweiSchaligesHyperboloid' : _attr + 'f2o',
    'ElliptischesParaboloid'   : _attr + 'f2o', 
	'HyperbolischesParaboloid' : _attr + 'f2o', 	
    'ElliptischerZylinder'     : _attr + 'f2o', 
	'HyperbolischerZylinder'   : _attr + 'f2o',     
    'ParabolischerZylinder'    : _attr + 'f2o', 
	'DoppelKegel'              : _attr + 'f2o',
	
	'hPunkt'      : _attr + 'hyp_geometrie', 
	'hGerade'     : _attr + 'hyp_geometrie', 
	'hStrahl'     : _attr + 'hyp_geometrie', 
	'hHalbGerade' : _attr + 'hyp_geometrie', 
	'hStrecke'    : _attr + 'hyp_geometrie', 
    'hDreieck'    : _attr + 'hyp_geometrie', 
	'hKreis'      : _attr + 'hyp_geometrie', 
	'D2H'         : _attr + 'hyp_geometrie', 
	'D2D3'        : _attr + 'hyp_geometrie', 
	'D32H'        : _attr + 'hyp_geometrie', 
	'D32D'        : _attr + 'hyp_geometrie', 
	'H2D'         : _attr + 'hyp_geometrie', 
	'H2D3'        : _attr + 'hyp_geometrie',
	
	'sPunkt'   : _attr + 'sphaer_geometrie', 
	'sGerade'  : _attr + 'sphaer_geometrie', 
	'sStrecke' : _attr + 'sphaer_geometrie', 
	'sDreieck' : _attr + 'sphaer_geometrie', 
	'sKreis'   : _attr + 'sphaer_geometrie', 
    'sZweieck' : _attr + 'sphaer_geometrie',
	
	'LGS'                      : _attr + 'lgs', 
	'LinearesGleichungsSystem' : _attr + 'lgs',
	
	'Spat'     : _attr + 'spat', 	
	'Strecke'  : _attr + 'strecke', 	
	'Dreieck'  : _attr + 'dreieck', 	
	'Viereck'  : _attr + 'viereck', 			    
	'Pyramide' : _attr + 'pyramide', 	
	'Prisma'   : _attr + 'prisma', 
	'Kugel'    : _attr + 'kugel', 
	'Kegel'    : _attr + 'kegel', 
	'Zylinder' : _attr + 'zylinder', 
	'Figur'    : _attr + 'figur',
	'Koerper'  : _attr + 'koerper', 
	'Kurve'    : _attr + 'kurve', 
	'Ellipse'  : _attr + 'ellipse', 
	'Hyperbel' : _attr + 'hyperbel', 
	'Parabel'  : _attr + 'parabel',
	
    'Lage'         : _fkt, 
    'Abstand'      : _fkt, 
    'Winkel'       : _fkt, 
	'Hilfe'        : _fkt, 
	'determinante' : _fkt, 
	'det'          : _fkt, 
	'loese'        : _fkt, 
	'einfach'      : _fkt, 
	'kollinear'    : _fkt, 
	'komplanar'    : _fkt, 
    'linear_abh'   : _fkt, 
	'linearAbh'    : _fkt, 
	'parallel'     : _fkt, 
	'orthogonal'   : _fkt, 
	'senkrecht'    : _fkt, 
	'identisch'    : _fkt, 
	'is_zahl'      : _fkt, 
    'isZahl'       : _fkt, 
	'mit_param'    : _fkt, 
	'mitParam'     : _fkt, 
	'kug_koord'    : _fkt, 
	'kugKoord'     : _fkt, 
	'Gleichung'    : _fkt, 
	'ja'           : _fkt, 
	'Ja'           : _fkt, 
	'nein'         : _fkt, 
	'Nein'         : _fkt, 
	'mit'          : _fkt, 
	'Mit'          : _fkt, 
	'ohne'         : _fkt, 
	'Ohne'         : _fkt,
	
    'abs'          : _fkt, 
	'sqrt'         : _fkt, 
	'exp'          : _fkt, 
	'ln'           : _fkt, 
	'lg'           : _fkt, 
	'log'          : _fkt, 
    'sin'          : _fkt, 
	'cos'          : _fkt, 
	'tan'          : _fkt, 
	'cot'          : _fkt, 
	'sing'         : _fkt, 
	'cosg'         : _fkt, 
	'tang'         : _fkt, 
	'cotg'         : _fkt, 
    'arcsin'       : _fkt, 
	'arccos'       : _fkt, 
	'arctan'       : _fkt, 
	'arccot'       : _fkt, 
	'asin'         : _fkt, 
	'acos'         : _fkt, 
	'atan'         : _fkt, 
	'acot'         : _fkt,
    'arcsing'      : _fkt, 
	'arccosg'      : _fkt, 
	'arctang'      : _fkt, 
	'arccotg'      : _fkt, 
	'asing'        : _fkt, 
	'acosg'        : _fkt, 
	'atang'        : _fkt, 
	'acotg'        : _fkt, 	
    'sinh'         : _fkt, 
	'cosh'         : _fkt, 
	'tanh'         : _fkt, 
	'arsinh'       : _fkt, 
	'arcosh'       : _fkt, 
	'artanh'       : _fkt, 
	'asinh'        : _fkt, 
	'acosh'        : _fkt, 
	'atanh'        : _fkt,
    're'           : _fkt, 
	'im'           : _fkt, 
	'conjugate'    : _fkt, 
	'konjugiert'   : _fkt, 
	'max'          : _fkt, 
	'min'          : _fkt, 
	'deg'          : _fkt, 
	'grad'         : _fkt, 
	'rad'          : _fkt, 
	'bog'          : _fkt,	
	
    'Grafik'  : _graf_fkt, 
	'zeichne' : _graf_fkt, 
	'farben'  : _graf_fkt, 
	'rot'     : _graf_fkt, 
    'gruen'   : _graf_fkt, 
	'blau'    : _graf_fkt, 
	'schwarz' : _graf_fkt, 
	'gelb'    : _graf_fkt, 
	'magenta' : _graf_fkt, 
	'cyan'    : _graf_fkt, 
	'weiss'   : _graf_fkt,	
	
	'verschiebung' : _abb_fkt, 
	'versch'       : _abb_fkt, 
	'translation'  : _abb_fkt, 
	'trans'        : _abb_fkt, 
	'parallel_projektion' : _abb_fkt, 
	'proj'         : _abb_fkt,
	'drehung'      : _abb_fkt, 
	'dreh'         : _abb_fkt, 
	'drehx'        : _abb_fkt, 
	'drehy'        : _abb_fkt, 
	'drehz'        : _abb_fkt, 
	'drehO2'       : _abb_fkt,
    'spiegelung'   : _abb_fkt, 
	'spieg'        : _abb_fkt, 
	'spiegxy'      : _abb_fkt, 
	'spiegxz'      : _abb_fkt, 
	'spiegyz'      : _abb_fkt, 
	'spiegx'       : _abb_fkt, 
    'spiegy'       : _abb_fkt, 
	'spiegz'       : _abb_fkt, 
	'spiegx2'      : _abb_fkt, 
	'spiegy2'      : _abb_fkt, 
	'spiegO'       : _abb_fkt, 
	'spiegO2'      : _abb_fkt, 
    'streckung'    : _abb_fkt, 
	'streck'       : _abb_fkt, 
	'scherung'     : _abb_fkt, 
	'scher'        : _abb_fkt, 
	'projektion'   : _abb_fkt, 
	'kavalier'     : _abb_fkt, 
    'kabinett'     : _abb_fkt, 
	'schraegbild'  : _abb_fkt, 
	'militaer'     : _abb_fkt, 
	'isometrie'    : _abb_fkt, 
	'dimetrie'     : _abb_fkt,
	'grundriss'    : _abb_fkt,
	'aufriss'      : _abb_fkt,
	'seitenriss'   : _abb_fkt,	
	
    'AEE'   : _verf, 
	'LEE'   : _verf, 
	'WEE'   : _verf, 
	'AGE'   : _verf, 
	'AGG'   : _verf, 
	'AGG1'  : _verf, 
    'AGG2'  : _verf, 
	'APP'   : _verf, 
	'APE'   : _verf, 
	'APE1'  : _verf, 
	'APE2'  : _verf, 
	'APG'   : _verf, 
	'APG1'  : _verf, 
	'APG2'  : _verf, 
	'APG3'  : _verf, 
	'LGE'   : _verf, 
	'LGE1'  : _verf, 
	'LGG'   : _verf,
    'LGG1'  : _verf, 
	'LPD'   : _verf, 
	'LPD1'  : _verf, 
	'LPE'   : _verf, 
	'LPG'   : _verf, 
	'LPV'   : _verf, 
	'WGE'   : _verf, 
	'WVV'   : _verf, 
	'EK2P'  : _verf, 
	'EK2P1' : _verf, 
	'EN2P'  : _verf, 
	'EP2K'  : _verf, 
	'EP2K1' : _verf,
    'EP2N'  : _verf, 
	'ERV'   : _verf, 
	'RV'    : _verf, 
	'ENV'   : _verf, 
	'NV'    : _verf, 
	'ENV1'  : _verf, 
	'NV1'   : _verf, 
	'LPK'   : _verf, 
	'LGK'   : _verf, 
	'LEK'   : _verf	
	
	}		

# -----------------------------------------------------------------------------
# Geschützte Namen
# -----------------------------------------------------------------------------


_protected_names = list(_to_load.keys()) + [

        # Python-Namen
        'and', 'as', 'assert', 'break', 'class', 'continue', 
        'def', 'del', 'elif', 'else', 'except', 'exec', 
        'finally', 'float', 'for', 'from', 'global', 'if', 'import', 
        'in', 'int', 'is', 'lambda', 'not', 'or', 'pass', 'print', 		
		'raise', 'return', 'try', 'while', 'with', 'yield',		

        # SymPy-Namen		  
        'Rational', 'pi', 'Symbol', 'symbols', 'solve', 'solveset', 
        'nsolve', 'expand', 'simplify', 'nsimplify', 'collect', 'diff',
        'factor', 're', 'im', 'min', 'max', 'conjugate', 'sympify',	
		
        # griechische Buchstaben	
        'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 
		 'theta', 'iota', 'kappa', 'lamda', 'mu', 'nu', 'xi', 'omicron', 
		 'pi', 'rho', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 
		 'omega'  
      ]

# -----------------------------------------------------------------------------
# Funktion zum Laden der Moduln	
# -----------------------------------------------------------------------------

def _load_modules(line):

    for obj in _to_load:
        if obj in line and _to_load[obj] != False:
            name = _to_load[obj]
            modul = importlib.import_module(name)
            attribut = getattr(modul, obj)
            _ip.push({obj : attribut})		
            _to_load[obj] = False	
	
# -----------------------------------------------------------------------------
# Custom InputTransformer
# -----------------------------------------------------------------------------
#
#   Für
#
# - Dynamisches Laden der Moduln
#
# - Ersetzen der deutschen Umlaute und ß
#
#  - Operator '^'   für das Potenzieren (zusätzlich zu '**')
#    Operator '°'   für das Skalarprodukt und die Verknüpfung 
#                   von Abbildungen (zusätzlich zu '*')
#    Operator '><'  für das Kreuzprodukt (Vektorprodukt)
#
# - Schreibwarnung für die agla-, Python- und SymPy-Namen
#
#  (s.a. 'ipython/core/test/test_interactiveshell.py')
		
class AglaInputTransformer(InputTransformer):
	
    def push(self, line):
        """für InputTransformer erforderlich"""
        								            
		# Operatoren, Umlaute
        #		 
        if line.find('^') >= 0:
            line = line.replace('^', '**')			
        if line.find('°') >= 0:
            line = line.replace('°', '*')
        if line.find('><') >= 0:
            line = line.replace('><', '&')
			
        if line.find('ä') >= 0:
            line = line.replace('ä', 'ae')			
        if line.find('ö') >= 0:
            line = line.replace('ö', 'oe')			
        if line.find('ü') >= 0:
            line = line.replace('ü', 'ue')			
        if line.find('ß') >= 0:
            line = line.replace('ß', 'ss')			
		
        # Dynamisches Laden der Moduln
        #   
        _load_modules(line)
		
        # Schreibblockade	
        #
		
        def klammer(line):    # Index der 1. Klammer oder None
            for i, z in enumerate(line):
                if z in '([{':
                    return i
        def gleich(line):   # Indices aller '='-Zeichen vor der 1. Klammer 
            line1 = line.replace('==', 'xx')	 # '==' ausschließen	
            k = klammer(line1)
            g = []
            for i, z in enumerate(line1):
                if i == k:
                    break
                if z == '=':
                    g.append(i)
            return g 
        if '#' in line:
            k = line.find('#')
            kl = False			   	
            for i in range(k): 
                if line[i] in '([{)]}':
                    kl = not kl
            if not kl:		# innere Kommentare bleiben erhalten
               line = line[:k]	
        anw_liste = line.split(';')  # Behandlung von Mehrfachzuweisungen
        anw_liste_neu = []		
        for i, anw in enumerate(anw_liste):
            gl = gleich(anw)
            no1 = anw.find("'")		
            no2 = anw.find('"')   		
            for i, g in enumerate(gl):
                if abs(no1) < gl[i] or abs(no2) < gl[i]:
                    gl = gl[:i]  
                    break								
            if len(gl) <= 1:
                anw_liste_neu.append(anw)
                continue 
            lhs, rhs = anw[:gl[-1]], anw[gl[-1]:]
            ind = ''
            for i in lhs:
                if i == ' ':
                    ind += ' '
                else:
                    break				
            lhs = lhs.split('=') 
            anw_neu = []
            for i, name in enumerate(lhs):
                if i == 0:			
                    anw_liste_neu.append(name + rhs)	
                else:					
                    anw_liste_neu.append(ind + name[1:] + rhs)	
        anw_liste = anw_liste_neu 				
        aus_liste = []  
        for anw in anw_liste:
            anw = anw.rstrip()
            g = anw.find('=')
            if g <= 0:
                aus_liste += [anw] 
                continue 
            try:
                if anw[g+1] == '=':
                    aus_liste += [anw] 
                    continue 				
            except IndexError:
                pass			
            klammer = False			   	
            for i in range(len(anw)):   
                if i == g:
                    break
                if anw[i] in '([{)]}':
                    klammer = not klammer
            if klammer:
                aus_liste += [anw]
                continue 
            if anw[g-1] in ('<', '>', '!'):    
                aus_liste += [anw] 
                continue
            bezeichner = anw[:g].strip() 
            fehler = False   
            if bezeichner in _protected_names:
                print("agla: der Wert von " + bezeichner + " kann nicht überschrieben werden")
                fehler = True
            if anw[0] == '_':
                print("agla: ein Bezeichner darf nicht mit einem Unterstrich beginnen")
                fehler = True
            p = anw.find('.')
            if 0 <= p < g and klammer and not 'UMG.' in anw:
                print("agla: auf der linken Seite einer Zuweisung darf kein '.' auftreten")
                fehler = True
            if not fehler:        
                aus_liste += [anw]
                continue
            else:
                return
        
        return ';'.join(aus_liste)
					  
    def reset(self):
        """für InputTransformer erforderlich"""	
        pass

transformer = AglaInputTransformer()
_ip.input_splitter.python_line_transforms.append(transformer)
_ip.input_transformer_manager.python_line_transforms.append(transformer)
	 
		
# -----------------------------------------------------------------------------
# Eigene Fehlermeldungen
# -----------------------------------------------------------------------------
	
# Extra-Behandlung von SyntaxError (hat kein traceback)	 
#

import linecache 
from IPython.core.ultratb import SyntaxTB
from IPython.utils import py3compat
from IPython.utils import ulinecache
def new_structured_traceback(self, etype, value, elist, tb_offset=None,
                             context=5):
    if isinstance(value, SyntaxError) \
            and isinstance(value.filename, py3compat.string_types) \
            and isinstance(value.lineno, int):
        linecache.checkcache(value.filename)
        newtext = ulinecache.getline(value.filename, value.lineno)
        if newtext:
            value.text = newtext
    nr = value.lineno		
    print('SyntaxError:  ' + value.text[:-1] + (('  /Zeile ' + str(nr) + '/') \
	      if nr > 1 else ''))
    return		

if not _TEST:	
    SyntaxTB.structured_traceback = new_structured_traceback
	

# Custom exc_handler (für ausgewählte Ausnahmen)
#
def exc_handler(shell, etype, value, tb, tb_offset=None):
    stype, sval = str(etype), str(value)
    if 'AglaError' in stype:
        print(sval)
    elif 'NameError' in stype:
        txt = sval[sval.find("'")+1 : sval.rfind("'")]		
        print('NameError: ' + txt + ' ist nicht definiert')		
    elif 'KeyError' in stype:
        print('KeyError: ' + sval)
    elif 'IndexError' in stype:
        print('IndexError: ' + 'der Index ist außerhalb des Bereiches')
    elif 'AttributeError' in stype:
        no = []
        for i, z in enumerate(sval):
            if z == "'":
                no += [i]
        if len(no) != 4:		
            print('AttributeError')
        else:
            obj, eig = sval[no[0]+1:no[1]], sval[no[2]+1:no[3]]		
            print('AttributeError:  ' + 'ein ' + obj + '-Objekt ' + \
                 'hat keine Eigenschaft/Methode \nmit dem Namen ' + eig)
    elif 'TypeError' in stype:
        print('TypeError: ' + 'Funktionsaufruf nicht möglich oder anderer Fehler')
    elif 'MemoryError' in stype:
        print('MemoryError: ' + 'die Zahlen sind zu groß')
    elif 'ImportError' in stype:
        i = sval.find("'")
        j = sval[i+1:].find("'")
        txt = sval[i+1:i+j+1]	
        print('ImportError: ' + txt +  ' kann nicht importiert werden')
    elif 'ZeroDivisionError' in stype:
        print('ZeroDivisionError: ' +	 'Division durch Null ist nicht erlaubt')
    elif 'IndentationError' in stype:
        print('IndentationError: ' +	 'Syntaxfehler - falsche Einrückung')
    elif 'RuntimeError' in stype:
        print('RuntimeError: ' +	    'Ein Laufzeitfehler ist aufgetreten')
    elif 'ValueError' in stype:
        print('ValueError: ' +	    'Ein ValueError ist aufgetreten')
    return	
	
if not _TEST:	
    _ip.set_custom_exc((AglaError, NameError, KeyError, IndexError, \
      AttributeError, TypeError, MemoryError, ImportError, ZeroDivisionError, \
      IndentationError, RuntimeError), exc_handler) 
	
	
# -----------------------------------------------------------------------------
# Ausführung der (linksseitigen) Multiplikation  Zahl * Vektor
# -----------------------------------------------------------------------------

"""
Die rechtsseitige Multiplikation eines Vektors mit einer Zahl 
(Vektor * Zahl) funktioniert für alle infrage kommenden SymPy-Klassen,
das Ergebnis ist ein Vektor-Objekt
Hinsichtlich der linksseitigen Multiplikation (Zahl * Vektor) verhalten
sich die Klassen unterschiedlich. Bei einigen gibt die __mul__-Methode
NotImplemented zurück, sodass automatisch die __rmul__-Methode von Vektor
aufgerufen wird. Für die anderen wird dieses Verhalten mittels Überladen
der __mul__-Methode des Expr-Objektes bzw. ihrer eigenen __mul__-Methode
(Symbol) erreicht
"""

# -----------------------------------------------------------------------------
# Überladen der Expr.__mul__- Methode
# -----------------------------------------------------------------------------

_expr_mul = copy.deepcopy(Expr.__mul__)
def _expr_mul_anpassung(self, other):
    Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor
    if isinstance(other, (Vektor, SympyMatrix)):
        return NotImplemented
    return _expr_mul(self, other)
Expr.__mul__ = _expr_mul_anpassung	
   
   
# -----------------------------------------------------------------------------
# Überladen der Symbol.__mul__- Methode	
# -----------------------------------------------------------------------------

_symbol_mul = copy.deepcopy(Symbol.__mul__)
def _symbol_mul_anpassung(self, other):
    Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor
    if isinstance(other, (Vektor, SympyMatrix)):
        return NotImplemented
    return _symbol_mul(self, other)
Symbol.__mul__ = _symbol_mul_anpassung	   
	
# -----------------------------------------------------------------------------
# Float.__mul__ - Überladung
# -----------------------------------------------------------------------------

_Float_mul = copy.deepcopy(Float.__mul__)

def _Float_mul_anpassung(self, other):
    if isinstance(other, SympyMatrix):
        ve = [self*v for v in other.vekt]
        return Matrix(*ve)
    return _Float_mul(self, other) 
	
Float.__mul__ = _Float_mul_anpassung	
	

	
# -----------------------------------------------------------------------------
# Bereitstellung der Matrix-'Klasse'
# -----------------------------------------------------------------------------

"""

agla hat keine eigene Matrix-Klasse (es ist nicht gelungen, die elegante
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

	
