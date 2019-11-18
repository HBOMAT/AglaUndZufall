#!/usr/bin/python
# -*- coding utf-8 -*-



#                                                 
# LinearesGleichungsSystem - Klasse  von agla           
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

from sympy.abc import *
from sympy.core.symbol import Symbol
from sympy.core.sympify import sympify
from sympy.core.numbers import Rational, Float
from sympy.solvers.solvers import solve
from sympy.polys.polytools import Poly, lcm, gcd
from sympy.core.containers import Tuple
from sympy.simplify.simplify import nsimplify
from sympy.printing import latex

from agla.lib.objekte.basis import AglaObjekt
from agla.lib.objekte.vektor import Vektor
from agla.lib.objekte.ebene import Ebene
from agla.lib.objekte.gerade import Gerade
from agla.lib.funktionen.funktionen import mit_param
from agla.lib.funktionen.graf_funktionen import Grafik
from agla.lib.objekte.umgebung import sicht_box
from agla.lib.objekte.ausnahmen import AglaError
import agla	
	

	
# LinearesGleichungsSystem - Klasse   
# ---------------------------------
	
class LinearesGleichungsSystem(AglaObjekt):                                      
    """
	
LinearesGleichungsSystem 

**Kurzform**

   **LGS**

**Erzeugung** 
	
   LGS ( *[gleich1, gleich2 , ...] /[, var_liste]* ) *oder*
   
   LGS ( *vekt_gleich  /[, var_liste* )
   
**Parameter**

   *gleich* : lineare Gleichung (linke Seite; rechte Seite = 0 angenommen)
		
   *vekt_gleich* : Vektor-Gleichung (linke Seite; rechte Seite als Nullvektor 
   angenommen)
   
   *var_liste* : Liste von Variablen
   				
    """


    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            lgs_hilfe(kwargs["h"])		
            return	
				
        try:
            if len(args) not in (1, 2):
                raise AglaError("ein oder zwei Argumente angeben")
            if isinstance(args[0], (list, tuple, Tuple)):
                gl = list(args[0])
            elif isinstance(args[0], Vektor):
                gl = []
                for k in args[0].komp:
                    gl += [k]
            else:
                raise AglaError("Liste mit Gleichungen oder " +
                                      "Vektorgleichung angeben")
            vars = None		
            if len(args) == 2:
                if isinstance(args[1], (list, tuple, Tuple)):
                    vars = list(args[1])
                else:					
                    raise AglaError("Liste mit Variablennamen angeben")
            if not vars:
               vars = set()
               for g in gl:
                   vars |= g.free_symbols
               vars = list(vars)		
            for v in vars:
                if not isinstance(v, Symbol):	
                    raise yglaError('Variablen müssen Symbole sein')				
                if str(v)[0] == 'c' and len(str(v)) > 1:
                    raise AglaError('Variablennamen dürfen nicht mit c beginnen')				   
            vars = sorted(vars, key=lambda x: str(x))
            if len(vars) > 8:			
                raise AglaError('die Anzahl der Variablen darf höchstens 8 sein')				   
            gleich = []
            for g in gl:
                try:
                    p = Poly(g, vars)
                except:
                    raise AglaError("lineare Gleichungen angeben")
                if p.total_degree() > 1:
                    raise AglaError("lineare Gleichungen in den Variablen angeben")				
                cf = []
                for var in vars:
                    try:				
                        c = nsimplify(p.coeff_monomial(var))
                    except RecursionError:
                        c = p.coeff_monomial(var) 					
                    cf += [c]
                try:					
                    cf += [nsimplify(p.coeff_monomial(1))]	
                except RecursionError:					
                    cf += [p.coeff_monomial(1)]	
                gleich += [cf]					
				
            return AglaObjekt.__new__(cls, gleich, vars)			
							
        except AglaError as e:	
            print('agla:  ', str(e))
            return			
  			
		
    def __str__(self):  
        return 'LGS'		
		
		
		
# Eigenschaften
# -------------

    @property
    def dim(self):              
        """Dimension"""
        return self.A.dim		
				
    @property
    def ausg(self):              
        """Ausgabe"""
		
        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")
            return	
			
        cf, vars = self.args 
        gleich = []
        for c in cf:
            gls = []			
            for j, v in enumerate(vars):
                cc = c[j]
                if not cc:
                    s = ''
                elif abs(cc) == 1:
                    s = str(v)	
                else: 
                    s = str(abs(cc)) + str(v)
                if j == 0 and cc < 0:
                    s = '-' + s				
                gls += [s]					
            ca = c[-1]	
            gls += [' = ' + ('' if ca <= 0 else '-') + str(abs(ca))]            			
            gleich += [gls] 
        maxlen = [0] * (len(vars) + 1)
        for g in gleich:
            for i, t in enumerate(g):
                if len(t) > maxlen[i]:
                    maxlen[i] = len(t)
        for i, g in enumerate(gleich):
            for j in range(len(g)-1):
                g[j] = _leer(maxlen[j] - len(g[j])) + g[j]
        for i, g in enumerate(gleich):				
            for j in range(1, len(g)-1):
                if cf[i][j] < 0:
                    si = ' - '
                elif cf[i][j] > 0:
                    si = ' + '
                else:
                    si = '   '
                if all([bool(cf[i][k]==0) for k in range(j)]):
                    if si == ' - ':
                        si = '  -'
                    else:
                        si = '   '										
                g[j] = si + g[j]	
        for i, g in enumerate(gleich):
            s = ''
            for t in g:
                s += t
            r = _rom()[i+1]
            i = s.find('=')
            if s[:i].lstrip() == '':
                s = s[:i-2] + '0 =' + s[i+1:]		
            elif s[:-5].lstrip() == '':
                pass 		
            s = _leer(5 - len(r)) + r + _leer(5) + s					
            print(s)								
        return 	
			
    @property
    def ausg_ohne_nr(self):              
        """Ausgabe ohne Gleichungsnummern"""
        cf, vars = self.args 
        gleich = []
        for c in cf:
            gls = []			
            for j, v in enumerate(vars):
                cc = c[j]
                if not cc:
                    s = ''
                elif abs(cc) == 1:
                    s = str(v)	
                else: 
                    s = str(abs(cc)) + str(v)
                if j == 0 and cc < 0:
                    s = '-' + s				
                gls += [s]					
            ca = c[-1]	
            gls += [' = ' + ('' if ca <= 0 else '-') + str(abs(ca))]            			
            gleich += [gls] 
        maxlen = [0] * (len(vars) + 1)
        for g in gleich:
            for i, t in enumerate(g):
                if len(t) > maxlen[i]:
                    maxlen[i] = len(t)
        for i, g in enumerate(gleich):
            for j in range(len(g)-1):
                g[j] = _leer(maxlen[j] - len(g[j])) + g[j]
        for i, g in enumerate(gleich):				
            for j in range(1, len(g)-1):
                if cf[i][j] < 0:
                    si = ' - '
                elif cf[i][j] > 0:
                    si = ' + '
                else:
                    si = '   '
                if all([bool(cf[i][k]==0) for k in range(j)]):
                    if si == ' - ':
                        si = '  -'
                    else:
                        si = '   '										
                g[j] = si + g[j]					
        for i, g in enumerate(gleich):
            s = ''
            for t in g:
                s += t
            r = ''
            i = s.find('=')
            if s[:i].lstrip() == '':
                s = s[:i-2] + '0 =' + s[i+1:]		
            elif s[:-5].lstrip() == '':
                pass 		
            s = r + _leer(5) + s					
            print(s)								
        return 	
			
    ausgOhneNr = ausg_ohne_nr
	
    @property
    def kurz_ausg(self):              
        """Ausgabe in Kurzform"""
        cf, vars = self.args                          
        gleich = []
        gl = []
        for v in vars:
            gl += [str(v)]
        gleich += [gl]			
        for c in cf:
            gl = []			
            for j, v in enumerate(vars):
                gl += [str(c[j])]					
            gl += [str(-c[-1])]            			
            gleich += [gl] 
        maxlen = [0] * (len(vars) + 1)
        for g in gleich:
            for i, t in enumerate(g):
                if len(t) > maxlen[i]:
                    maxlen[i] = len(t) + 6					
        for i, g in enumerate(gleich):
            for j in range(len(g)):
                g[j] = _leer(maxlen[j] - len(g[j])) + g[j]
        for i, g in enumerate(gleich):
            s = ''
            for t in g:
                s += t
            r = _rom()[i] if i > 0 else ''
            s = _leer(5 - len(r)) + r + _leer(5) + s					
            print(s)								
        return 
		
    kurzAusg = kurz_ausg		
	
    @property
    def erw_matrix(self):
        """Erweiterte Matrix"""
        aa = self.args	
        AA = Vektor(aa[0][0])
        for i in range(1, len(aa[0])):
            AA = AA | Vektor(aa[0][i])
        return AA.T		

    erwMatrix = erw_matrix		
    aa = erw_matrix		
    AA = erw_matrix		
		
    @property
    def matrix(self):
        """Matrix"""
        AA = self.erw_matrix		
        A = AA.vekt[0] 
        for i in range(1, AA.anz_spalt - 1):
            A = A | AA.vekt[i]		
        return A

    a = matrix		
    A = matrix
	
    @property
    def re_seite(self):
        """Rechte Seite"""
        AA = self.erw_matrix		
        return -AA.vekt[AA.anz_spalt - 1] 
		
    reSeite = re_seite		
    b = re_seite		

    @property
    def cramer(self):
        """Lösung mit der Cramer'schen Regel"""
        A, b = self.A, self.b
        vv = A.vekt
        from sympy import NonSquareMatrixError		  
        try:		
            dd = A.det()	
        except NonSquareMatrixError:
            pass		
        n = A.dim[0]	
        var = self.args[1]
        A_1, A_2, A_3, A_4, A_5 = Symbol('A_1'), Symbol('A_2'), Symbol('A_3'), \
                               Symbol('A_4'), Symbol('A_5') 		
        if not (2 <= n <= 5):
            print("agla: nur für n x n - Systeme mit 2 <= n <= 5 implementiert")	
            return			
        if A.dim[1] != n:
            print("agla: die Regel ist nur für n x n - Systeme anwendbar")		
            return			
        if dd == 0:
            print("agla: die Regel ist nicht anwendbar (Determinante = 0)")	
            return	

        def dm(sym, M, var):
            display(Math(latex(sym) + ' = ' + latex(M) + ', \qquad' \
               + '\det =' + latex(M.D) + ', \qquad ' + latex(var) + \
			     ' = ' + '\\frac{\det(' + latex(sym) + ')}{\det (A)} =' + \
				  '\\frac{' + latex(M.D) + '}{' + latex(dd) + '}' + '=' +\
				  latex(M.D / dd)))		

        print("\nMatrix des Systems, rechte Seite und Determinante\n")			
        display(Math('A = ' + latex(A) + ', \qquad ' + latex(b) + \
           ', \qquad \det = ' + latex(dd)))
        print("\nSukzessives Ersetzen der Spalten durch die rechte Seite und Berechnung")
        print("der Lösung als Quotient der Determinanten\n")			
        if n == 2:
            dm(A_1, b | vv[1], var[0])
            dm(A_2, vv[0] | b, var[1])
        elif n == 3:
            dm(A_1, b | vv[1] | vv[2], var[0])
            dm(A_2, vv[0] | b | vv[2], var[1])
            dm(A_3, vv[0] | vv[1] | b, var[2])
        elif n == 4:
            dm(A_1, b | vv[1] | vv[2] | vv[3], var[0])
            dm(A_2, vv[0] | b | vv[2] | vv[3], var[1])
            dm(A_3, vv[0] | vv[1] | b | vv[3], var[2])
            dm(A_4, vv[0] | vv[1] | vv[2] | b, var[3])
        elif n == 5:
            dm(A_1, b | vv[1] | vv[2] | vv[3] | vv[4], var[0])
            dm(A_2, vv[0] | b | vv[2] | vv[3] | vv[4], var[1])
            dm(A_3, vv[0] | vv[1] | b | vv[3] | vv[4], var[2])
            dm(A_4, vv[0] | vv[1] | vv[2] | b | vv[4], var[3])
            dm(A_5, vv[0] | vv[1] | vv[2] | vv[3] | b, var[4])
        else:
            pass		
        print(' ')
		
    @property		
    def loes(self):              
        """Lösungsmenge"""
        gl, vars = self.args	
        gl1 = []		
        for g in gl:
            gg = sum([g[i]*vars[i] for i in range(len(vars))]) + g[-1]
            gl1 += [gg]					
        L = solve(gl1, vars, rational = True)	
        if not L:
            return set()		
			
        i = 0
        cc = [c1, c2, c3, c4, c5, c6, c7] = symbols('c1, c2, c3, c4, c5, c6, c7')
        for v in vars:
            if v not in L: 
                L[v] = cc[i]		
                i += 1				
        for v in vars:
            for vv in vars:
                L[v] = L[v].subs(vv, L[vv])
        return L
		
    def _gauss(self, kurz=True, erst=True):              
        """Lösung mit dem Gauß-Verfahren"""

        def fakt(a, b):
            if a == b: 
                fo, fu = 1, 1    
            else:
                g = gcd(a, b)
                fo, fu = int(b / g), int(a / g)	
            return fo, fu
			
        piv_ausg = False   # deaktiviert		
        lgs = self			
        gl, vars = self.args[0][:], self.args[1][:]
        m, n = len(gl), len(vars)
		
        if not gl[0][0]:
            aend = False		
            for j in range(1, m):
                if gl[j][0]:
                    [gl[0], gl[j]] = [gl[j], gl[0]]	
                    print("\nVertauschen von Zeile  " + _rom()[1] + \
                         " mit Zeile " + _rom()[j+1] + "\n")
                    aend = True						 
                    break	
            if aend:
                lgs = AglaObjekt.__new__(LGS, gl, vars)
                if not kurz:
                    lgs.ausg
                else:
                    lgs.kurz_ausg		
                erst = False		
				
        if erst:
            if not kurz:
                lgs.ausg
            else:
                lgs.kurz_ausg	
            erst = False				
					
        lgs = self._mult(kurz=kurz)
        for row in range(1, m):
		
            if lgs._keine_loes():
                return
				
            # Pivot-Element suchen				
            gl = lgs.args[0][:]
            gefunden = False
            for col in range(row-1, n):
                pivot = gl[row-1][col]	
                if pivot:
                    gefunden = True				
                    break				
                for i in range(row-1, m):
                    if gl[i][col]:
                        pivot = gl[i][col]	
                        print("\nVertauschen von Zeile  " + _rom()[row] + \
                                          " mit Zeile " + _rom()[i+1] + "\n")
                        [gl[i], gl[row-1]] = [gl[row-1], gl[i]] 
                        lgs = AglaObjekt.__new__(LGS, gl, vars)
                        if kurz:
                            lgs.kurz_ausg
                        else:
                            lgs.ausg		
                        gl = lgs.args[0][:]
                        gefunden = True 
                        break									
                if gefunden:
                    break
									  
            # Zeilen transformieren				  
            if not any([gl[k][col] for k in range(row, m)]):
                continue			
            info = ''
            for j in range(row, m):
                cu = gl[j][col] 
                if cu == 0:
                    continue
                fo, fu = fakt(abs(pivot), abs(cu))				
                cfo = [fo * c for c in gl[row-1]]
                if pivot*cu > 0:
                    cfu = [-fu * c for c in gl[j]]
                else:
                    cfu = [fu * c for c in gl[j]]		
                gl[j] = [x+y for (x,y) in zip(cfo, cfu)]				
                so = '' if abs(fo) == 1 else str(fo) + '*'
                su = '' if abs(fu) == 1 else str(fu) + '*'
                si = '+' if pivot*cu < 0 else '-'
                info += '   ' + 	_rom()[j+1] + ' = ' + so + \
                       _rom()[row] + si + su + _rom()[j+1]
            print('\nÜberführen in Dreieckform, Schritt ' + str(row) + '   ' + \
                  info + '') 
            if piv_ausg:				  
                print('(Pivot-Element  ' \
                      + str(pivot) + '  (Zeile %s, Spalte %s)' % (str(row), \
                      str(col+1)) + ')\n') 
            lgs = AglaObjekt.__new__(LGS, gl, vars)
            if kurz:
                lgs.kurz_ausg
            else:
                lgs.ausg		
            if lgs._keine_loes():
                return
				
        # Streichen von Nullzeilen
        nz = 0
        gl1 = []		
        for g in gl:
            if all([g[k]==0 for k in range(n)]):
                nz += 1
                continue
            gl1 += [g]
        gl = gl1
        if nz:
            print("\nEs lieg" + ("en " if nz > 1 else "t ") + "%s Nullzeile" % nz + \
                ("n" if nz > 1 else "") + " vor, die gestrichen " + ("werden" \
                if nz > 1 else "wird") + "\n")
            lgs = AglaObjekt.__new__(LGS, gl, vars)
            if kurz:
                lgs.kurz_ausg
            else:
                lgs.ausg
								
        if not lgs._dreieck():
            print("\nAnwendung des Verfahrens auf dieses System liefert")		
            lgs._gauss(erst=False)
            return			
			
        # Berechnung der Lösung	
        print("\nBerechnen der Lösung durch Rücksubstitution   " + 
             "( 'von unten nach oben' )\n")
        gl, vars = lgs.args
        loes = dict([v, v] for v in vars)
        ber = list(range(len(gl)))
        ber.reverse() 

        for step in ber:
            vs = [vars[i] for i in range(len(vars)) if gl[step][i] != 0] 
            glstep = sum([gl[step][i]*loes[vars[i]] for i in range(len(vars))])
            L = solve(glstep + gl[step][-1], [vs[0]], rational=True)
            loes[vs[0]] = L[0]
			
            r = ('in ' if step < len(ber)-1 else '  ') + '[' + \
                    _rom()[step+1] + ']:        '   			
            zeile = _leer(8-len(r)) + r			
            zeile +=  str(glstep) + ' = ' + str(-gl[step][-1])
            zeile += '  ->  ' + str(vs[0]) + ' = ' + str(L[0])
            zeile = zeile.replace('*', '')
            print(zeile)
			
        loes1 = dict()
        for l in loes:
            if loes[l] != l:
                loes1[l] = loes[l]

        print("\n\nDie Lösung ist")		
        display(Math(latex(loes1)))	
        if loes1 != loes:		
            print("oder")		
            display(Math(latex(self.loes)))	
        print(' ')			
		
    @property		
    def gauss(self):
        """Lösung mit dem Gauß-Verfahren"""
        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")
            return			
        self._gauss(kurz=True)
        return 
		
    @property		
    def graf_loes(self):
        """Grafische Lösung"""	
        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")
            return			
        UMG = importlib.import_module('agla.lib.objekte.umgebung').UMG	
        sicht_box = importlib.import_module('agla.lib.objekte.umgebung').sicht_box	
        cf, vars = self.args
        if not self.dim in ((3, 3), (2, 2)):
            print('agla:  nur 3x3- und 2x2-LGS grafisch darstellbar')
            return
        gleich = []			
        for c in cf:
            gl = []			
            for j in list(range(len(vars))):
               gl += [c[j]]				
            gl += [c[-1]]            			
            gleich += [gl] 
        if self.dim == (3, 3):
            e = []
            for g in gleich:
                e += [Ebene(*[c for c in g])]
            e1, e2, e3 = e
            g1 = e1.schnitt(e2)
            g2 = e1.schnitt(e3)
            g3 = e2.schnitt(e3)
            sb = UMG._sicht_box
            sicht_box(-100, 100)	
            if g1 and g2 and g3 and self.loes:
                S = g1.schnitt(g2)
                Grafik([e[0], 'bisque'], [e[1], 'khaki'], [e[2], (0.9,0.9,0.9)], \
			        [g1, (1,0,0)], [g2, (1,0,0)], [g3, (1,0,0)], [S, 2, (1,0,0)])						 
            else:				  
                Grafik([e[0], 'bisque'], [e[1], 'khaki'], [e[2], (0.9,0.9,0.9)])	
            sicht_box(*sb)
			
        else:   # dim = 2
            g = []
            for gl in gleich:
                g += [Gerade(*[c for c in gl])]
            g1, g2 = g
            S = g1.schnitt(g2)
            if S:
                Grafik([g1, (0,0,1)], [g2, (0,0,1)], [S, (1,0,0)], gitter=True)	
            else:				  
                Grafik([g1, 2, (0,0,1)], [g2, 2, (0,0,1)], gitter=True)	
				
    grafLoes = graf_loes
	
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften"""
        lgs_hilfe(3)	
		
    h = hilfe					
				
    def _mult(self, kurz=False):
        """Beseitigen der Brüche"""	
        erst = True	
        cf = []
        info = ''
        for i, c in enumerate(self.args[0]):
            kgv = 1
            for j in list(range(len(c))):
                if isinstance(c[j], Rational):
                    kgv = lcm(kgv, c[j].q)
            if kgv > 1:
                if erst:
                    erst = False				   
                cf += [[kgv * t for t in c]]
                info += '   ' + _rom()[i+1] + '*' + str(kgv)
            else:
                cf += [c[:]]
        if info:
            print('\nBeseitigen der Brüche:' + '  ' + info + '\n')
        lgs = AglaObjekt.__new__(LGS, cf, self.args[1])
        if info:		
            if not kurz:
                lgs.ausg
            else:
                lgs.kurz_ausg						
        return lgs		   
           			   
    def _dreieck(self): 
        """Test auf Dreieckform"""	
        cf, vars = self.args
        for i, c in enumerate(cf):
            if not all([bool(cf[i][k]==0) for k in range(i)]):	
                return False			
        return True				
        
    def _tausch(self, i):   
        """Vertauschen von 2 Zeilen; bei Zeile i beginnend"""
        cf = self.args[0][:]
        vars = self.args[1]        			
        def tausch(i, ok):
            if cf[i][i] == 0:
                for j in list(range(i+1, len(cf[i])-1)):
                    if cf[j][i] != 0:
                        cci, ccj = cf[i][:], cf[j][:]
                        cf[i] = ccj
                        cf[j] = cci
                        info = '   ' + _rom()[i+1] + ' <--> ' + \
                              _rom()[j+1]
                        ok = True	
                        print('Zeilen vertauschen:' + '  ' + info + '\n')						
                        return ok
				
        ok = False				
        for j in list(range(i, len(cf)-1)):	
            ok = tausch(j, ok)	
            if ok:
                lgs = AglaObjekt.__new__(LGS, cf, vars)
                lgs.ausg
                return lgs	
        return self				
		
    def _streich(self):
        """Gleichungen streichen"""	
        cf, vars = self.args
        cf1 = []
        info = ''		
        for i, c in enumerate(cf):
            if not any(c):
                info += '   ' + _rom()[i+1]
                continue
            cf1 += [c]
        if info:
            print('\nGleichungen streichen:  ' + info + '\n')
            lgs = AglaObjekt.__new__(LGS, cf1, vars)	
            lgs.ausg	
            return lgs
        else:
            return self		
					
    def _keine_loes(self):
        """Test auf Lösung"""	
        cf = self.args[0]
        for i, c in enumerate(cf):
            if all([c[j]==0 for j in list(range(len(c)-1))]) and c[-1]:
                print('\n' + _rom()[i+1] + ': Widerspruch -> keine Lösung\n')
                return True
        return False
		
	
LGS = LinearesGleichungsSystem
	
	
# Hilfsfunktionen

def _leer(n):
    s = ''
    for i in range(n):
        s += ' '
    return s
	
def _rom():
    return {1:'I', 2:'II', 3:'III', 4:'IV', 5:'V', 6:'VI', 7:'VII', 
          8:'VIII', 9:'IX', 10:'X'}
	
	
			
# Benutzerhilfe für LGS
# ---------------------

def lgs_hilfe(h):

    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften")
        return
		   
    if h == 2:
        print("\nLinearesGleichungsSystem - Objekt\n")
        print("Synonymer Name   LGS\n")
        print("Erzeugung     LGS( [ gleich1, gleich2 , ... ]  /[, var_liste ] )\n")
        print("      oder    LGS( vekt_gleich  /[, var_liste ] ) \n")
        print("                   gleich        lineare Gleichung (linke Seite;") 
        print("                                 rechte Seite = 0 angenommen)")  
        print("                   vekt_gleich   Vektor-Gleichung (linke Seite;") 
        print("                                 rechte Seite als Nullvektor angenommen)")  
        print("                   var_liste     Liste von Variablen\n")
        print("Zuweisung     lgs = LGS(...)   (lgs - freier Bezeichner)\n")
        print("Beispiele\n")
        print("LGS( [2*x+y-5, -x-y+3] )\n") 
        print("LGS( v(2*r+s-5, -r-s+3), [r, s] )\n")
        print("g = Gerade(v(7, -2, 2), v(2, 3, 1))")
        print("h = Gerade(v(4, -6, -1), v(1, 1, 2))")	
        print("LGS( g.pkt(t) - h.pkt(s) )\n")	
        print("A = v(1, -2, 4) | v(3, -1, 2) | v(3, 2, 4)")
        print("vv = v(2, -2, 3)")		
        print("LGS( A*X - vv )\n")		
        return        
		
    if h == 3:   
        print("\nEigenschaften für LGS\n")
        print("lgs.hilfe         Bezeichner der Eigenschaften")
        print("lgs.a             = matrix")
        print("lgs.A             = matrix")
        print("lgs.aa            = erw_matrix")
        print("lgs.AA            = erw_matrix")
        print("lgs.ausg          Ausgabe")
        print("lgs.ausg_ohne_nr  Ausgabe ohne Gleichungsnummern")
        print("lgs.b             = re_seite")	
        print("lgs.cramer        Lösung mittels Cramerscher Regel")	
        print("lgs.dim           Dimension")	
        print("lgs.erw_matrix    Erweiterte Matrix")
        print("lgs.gauß          Lösung mittels Gauß-Verfahren")	
        print("lgs.graf_lös      Grafische Lösung")		
        print("lgs.kurz_ausg     Ausgabe in Kurzform")		
        print("lgs.lös           Lösung")
        print("lgs.matrix        Matrix")
        print("lgs.re_seite      rechte Seite\n")
        print("Synonyme Bezeichner\n")
        print("hilfe        :  h")
        print("ausg_ohne_nr :  ausgOhneNr")
        print("erw_matrix   :  erwMatrix")
        print("graf_lös     :  grafLös")
        print("kurz_ausg    :  kurzAusg")
        print("re_seite     :  reSeite\n")
        return
		
		
		
	 	