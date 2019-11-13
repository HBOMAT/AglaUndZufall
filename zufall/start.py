#!/usr/bin/python
# -*- coding utf-8 -*-


#                                                 
#  Start-Programm von zufall           
#                                                 


#
# This file is part of zufall
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
# für den Programmierer; hier im Quelltext ein-/ausschalten
# _TEST = True:  es werden die vollständigen Python-Fehlermitteilungen angezeigt 
# _TEST = False: es werden (teilweise) zufall-eigene Fehlermitteilungen angezeigt

_TEST = False


# -----------------------------------------------------------------------------
# Zurücksetzen
# -----------------------------------------------------------------------------

_ip = get_ipython()
_ip.magic('reset -sf')


# -----------------------------------------------------------------------------
# Importe
# -----------------------------------------------------------------------------

import copy
import importlib

from IPython.core.inputtransformer import InputTransformer

from sympy.core.expr import Expr
from sympy.matrices import Matrix as SympyMatrix

# ausgewählte SymPy-Objekte und -funktionen zur unmittelbaren Verfügung des Nutzers
from sympy.abc import *    
from sympy.core.numbers import Integer, Rational, Float, pi, E, I   
from sympy.core.symbol import Symbol, symbols
from sympy.core.function import Lambda
from sympy import (solve, solveset, S, expand, collect, factor, simplify, 
    nsimplify, N, Not, And, Or, factorial, binomial)
	
# Initialisierung der Latex-Ausgabe	
from sympy.interactive.printing import init_printing
from sympy.printing.latex import LatexPrinter
LatexPrinter._default_settings["mat_delim"] = "("
init_printing(use_latex='mathjax')	
	 
# Import ausgewählter zufall-Elemente	
from zufall.lib.objekte.umgebung import UMG 
from zufall.lib.objekte.ausnahmen import ZufallError
import zufall
		
from agla.lib.objekte.ausnahmen import AglaError
import agla

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

_attr = 'zufall.lib.objekte.'
_fkt = 'zufall.lib.funktionen.funktionen'
_agla = 'agla.lib.objekte.'


_to_load = {           

    'v'             : _agla + 'vektor', 
    'Vektor'        : _agla + 'vektor', 
	'Punkt'         : _agla + 'vektor', 
	'O'             : _agla + 'vektor', 
    'O2'            : _agla + 'vektor', 
	'X2'            : _agla + 'vektor',
    '_ZeilenVektor' : _agla + 'vektor',	

	'SympyMatrix'   : _attr + 'markoff_kette',
	'Matrix'        : _attr + 'markoff_kette',
    'NullMat'       : _attr + 'markoff_kette',
    'NullMat2'      : _attr + 'markoff_kette', 
    'EinhMat'       : _attr + 'markoff_kette',
    'EinhMat2'      : _attr + 'markoff_kette',
		 		 
    'DatenReihe'                  : _attr + 'datenreihe', 
    'DR'                          : _attr + 'datenreihe', 
    'ZufallsGroesse'              : _attr + 'zufalls_groesse', 
	'ZG'                          : _attr + 'zufalls_groesse', 
	'BinomialVerteilung'          : _attr + 'binomial_verteilung', 
	'BV'                          : _attr + 'binomial_verteilung', 
	'HyperGeometrischeVerteilung' : _attr + 'hyper_geometrische_verteilung', 
	'HGV'                         : _attr + 'hyper_geometrische_verteilung',
	'GeometrischeVerteilung'      : _attr + 'geometrische_verteilung', 
	'GV'                          : _attr + 'geometrische_verteilung', 
	'PoissonVerteilung'           : _attr + 'poisson_verteilung', 
	'PV'                          : _attr + 'poisson_verteilung',
	'GleichVerteilung'            : _attr + 'gleich_verteilung', 
	'GLV'                         : _attr + 'gleich_verteilung', 
	'NormalVerteilung'            : _attr + 'normal_verteilung', 
	'NV'                          : _attr + 'normal_verteilung',
	'ExponentialVerteilung'       : _attr + 'exponential_verteilung', 
	'EV'                          : _attr + 'exponential_verteilung', 
	'BernoulliKette'              : _attr + 'bernoulli_kette', 
	'BK'                          : _attr + 'bernoulli_kette',
	'ZufallsExperiment'           : _attr + 'zufalls_experiment', 
	'ZE'                          : _attr + 'zufalls_experiment', 
	'ZufallsVersuch'              : _attr + 'zufalls_experiment', 
	'ZV'                          : _attr + 'zufalls_experiment',
	'Urne'                        : _attr + 'urne', 
	'GluecksRad'                  : _attr + 'gluecks_rad', 
	'Rad'                         : _attr + 'gluecks_rad', 
	'GR'                          : _attr + 'gluecks_rad', 
	'Muenze'                      : _attr + 'muenze', 
	'Wuerfel'                     : _attr + 'wuerfel',
	'HaeufigkeitsBaum'            : _attr + 'haeufigkeits_baum', 
	'HB'                          : _attr + 'haeufigkeits_baum', 
	'VierFelderTafel'             : _attr + 'vier_felder_tafel', 
	'VT'                          : _attr + 'vier_felder_tafel',
    'KonfidenzIntervall'          : _attr + 'konfidenz_intervall', 
	'KI'                          : _attr + 'konfidenz_intervall', 
	'EreignisAlgebra'             : _attr + 'ereignis_algebra', 
	'EA'                          : _attr + 'ereignis_algebra',
    'AlternativTest'              : _attr + 'alternativ_test', 
	'AT'                          : _attr + 'alternativ_test', 
	'SignifikanzTestP'            : _attr + 'signifikanz_test_p', 
	'STP'                         : _attr + 'signifikanz_test_p',
	'SkatBlatt'                   : _attr + 'skat_blatt', 
	'Skat'                        : _attr + 'skat_blatt', 
	'Roulette'                    : _attr + 'roulette', 
	'Craps'                       : _attr + 'craps', 
	'Toto'                        : _attr + 'toto', 
	'Lotto'                       : _attr + 'lotto',
	'Chuck'                       : _attr + 'chuck',
	'ChuckALuck'                  : _attr + 'chuck', 
	'MarkoffKette'                : _attr + 'markoff_kette', 
	'MK'                          : _attr + 'markoff_kette',
        
    'permutationen'  : _fkt, 
    'perm'           : _fkt, 
	'kombinationen'  : _fkt, 
    'komb'           : _fkt, 
    'variationen'    : _fkt, 
	'anzahl'         : _fkt, 
    'anzahl_treffer' : _fkt, 
	'anzahlTreffer'  : _fkt, 
	'summe'          : _fkt, 
	'zuf_zahl'       : _fkt, 
	'zufZahl'        : _fkt, 
	'fakultaet'      : _fkt, 
	'fak'            : _fkt, 
	'binomial'       : _fkt, 
	'B'              : _fkt, 
	'loese'          : _fkt, 
	'Hilfe'          : _fkt, 
	'auswahlen'      : _fkt, 
	'gesetze'        : _fkt, 
	'stochastisch'   : _fkt, 
	'einfach'        : _fkt,	
	'is_zahl'        : _fkt, 
	'isZahl'         : _fkt, 
	'mit_param'   	 : _fkt,
	'mitParam'       : _fkt,
    'jaNein'         : _fkt, 
    'kurz_form'      : _fkt, 
    'kurzForm'       : _fkt, 
	'ja_nein'        : _fkt, 
	'ja'             : _fkt, 
	'Ja'             : _fkt, 
	'nein'           : _fkt, 
	'Nein'           : _fkt, 
	'mit'            : _fkt, 
	'Mit'            : _fkt, 
	'ohne'           : _fkt, 
	'Ohne'           : _fkt,
	
    'abs'            : _fkt, 
	'sqrt'           : _fkt, 
	'exp'            : _fkt, 
	'ln'             : _fkt, 
	'lg'             : _fkt, 
	'log'            : _fkt, 
    'sin'            : _fkt, 
	'cos'            : _fkt, 
	'tan'            : _fkt, 
	'cot'            : _fkt, 
	'sing'           : _fkt, 
	'cosg'           : _fkt, 
	'tang'           : _fkt, 
	'cotg'           : _fkt, 
    'arcsin'         : _fkt, 
	'arccos'         : _fkt, 
	'arctan'         : _fkt, 
	'arccot'         : _fkt, 
	'asin'           : _fkt, 
	'acos'           : _fkt, 
	'atan'           : _fkt, 
	'acot'           : _fkt,
    'arcsing'        : _fkt, 
	'arccosg'        : _fkt, 
	'arctang'        : _fkt, 
	'arccotg'        : _fkt, 
	'asing'          : _fkt, 
	'acosg'          : _fkt, 
	'atang'          : _fkt, 
	'acotg'          : _fkt, 	
    'sinh'           : _fkt, 
	'cosh'           : _fkt, 
	'tanh'           : _fkt, 
	'arsinh'         : _fkt, 
	'arcosh'         : _fkt, 
	'artanh'         : _fkt, 
	'asinh'          : _fkt, 
	'acosh'          : _fkt, 
	'atanh'          : _fkt,
    're'             : _fkt, 
	'im'             : _fkt, 
	'conjugate'      : _fkt, 
	'konjugiert'     : _fkt, 
	'max'            : _fkt, 
	'min'            : _fkt, 
	'deg'            : _fkt, 
	'grad'           : _fkt, 
	'rad'            : _fkt, 
	'bog'            : _fkt	
		
	}		

# -----------------------------------------------------------------------------
# Geschützte Namen
# -----------------------------------------------------------------------------

zufall_namen = list(_to_load.keys())
del zufall_namen[zufall_namen.index('B')]

_protected_names = zufall_namen + [

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
# - Schreibwarnung für die zufall-, Python- und SymPy-Namen
#
#  (s.a. 'ipython/core/test/test_interactiveshell.py')
		
class ZufallInputTransformer(InputTransformer):
	
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
                print("zufall: der Wert von " + bezeichner + " kann nicht überschrieben werden")
                fehler = True
            if anw[0] == '_':
                print("zufall: ein Bezeichner darf nicht mit einem Unterstrich beginnen")
                fehler = True
            p = anw.find('.')
            if 0 <= p < g and klammer and not 'UMG.' in anw:
                print("zufall: auf der linken Seite einer Zuweisung darf kein '.' auftreten")
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

transformer = ZufallInputTransformer()
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
    if 'ZufallError' in stype or 'AglaError' in stype:
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
    _ip.set_custom_exc((ZufallError, AglaError, NameError, KeyError, IndexError, \
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
	

	
	 


