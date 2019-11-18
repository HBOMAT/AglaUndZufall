#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  KonfidenzIntervall - Klasse  von zufall           
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



from IPython.display import display, Math

from sympy import Symbol, expand, solve, N, sqrt
from sympy.core.numbers import Integer, Rational, Float 
from sympy.printing.latex import latex

from zufall.lib.objekte.basis import ZufallsObjekt
from zufall.lib.objekte.normal_verteilung import NormalVerteilung
	
from zufall.lib.objekte.ausnahmen import ZufallError



# KonfidenzIntervall - Klasse  
# ---------------------------
	
class KonfidenzIntervall(ZufallsObjekt):                                      
    """
	
Konfidenzintervall

**Kurzname** **KI**
	
**Erzeugung** 

   KI( *umfang, treffer, konf_niveau, verfahren* )

**Parameter**

   *umfang* : Stichprobenumfang
	
   *treffer* : Anzahl Treffer in der Stichprobe
   
   *konf_niveau* :  
   
      Konfidenzniveau/Sicherheitswarscheinlichkei/
      Vertrauenszahl	
                 
   *verfahren* :    
   
      'S' | 'Sigma' - bei Konfidenzniveau aus {0.9, 0.95, 0.99} Benutzung der 
      Sigma-Umgebung des Erwartungswertes
                                             	
      'N' | 'NV' : Benutzung der Approximation durch die Normalverteilung
	  
      'T' | 'Tsch' : Benutzung der Tschebyschew-Ungleichung
                              
    """		
			
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            konfidenz_intervall_hilfe(kwargs["h"])		
            return	
				
        try:
            if len(args) not in (4, 5):
                raise ZufallError('4 oder 5 Argumente angeben')
            n, treffer, konf_niveau, verfahren = args[:4]
            if not (isinstance(n, (int, Integer)) and n > 0):
                raise ZufallError('für Stichprobenumfang ganze Zahl > 0 angeben')
            if not (isinstance(treffer, (int, Integer)) and n > 0):
                raise ZufallError('für Trefferanzahl ganze Zahl > 0 angeben')
            if treffer > n:				
                raise ZufallError('die Trefferanzahl kann nicht größer als der Stichprobenumfang sein')
            if not (isinstance(konf_niveau, (Rational, float, Float)) and \
               (0 < konf_niveau < 1)):
                raise ZufallError('für Konfidenzniveau eine Zahl aus [0,1] angeben')
            if not verfahren in ('S', 'Sigma', 'N', 'NV', 'T', 'Tsch'):
                raise ZufallError("für Verfahren 'S' | 'Sigma', 'N' | 'NV', 'T' | 'Tsch' angeben")
        except ZufallError as e:
            print('zufall:', str(e))
            return

        return ZufallsObjekt.__new__(cls, n, treffer, konf_niveau, verfahren)		
		
			
    def __str__(self):  
        return "KonfidenzIntervall"
		
		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def n(self):
        """Stichprobenumfang"""
        return self.args[0]		

    @property
    def treffer(self):
        """Trefferanzahl"""
        return self.args[1]		

    @property
    def konf_niv(self):
        """Konfidenzniveau"""
        return self.args[2]		

    konfNiv = konf_niv		
		
    @property
    def konf_int(self):
        """Konfidenzintervall"""
        return self._verf(print=False)		
		
    konfInt = konf_int		
		
    @property
    def verf(self):
        """Verfahren"""
        return self._verf(print=True)	
    def _verf(self, **kwargs):
        """Vefahren; interne Methode"""
		
        printen = kwargs.get('print')		
        def dm(x):
            if printen:		
                return display(Math(x))
        def pr(x):
            if printen:		
                return print(x)
		
        pr(' ')		
        v = self.args[3]	
        if v in ('S', 'Sigma'):
            txt = '\mathrm{Benutzung\; der}\;\, \\sigma\mathrm{\,-\,Umgebung\; des\; Erwartungswertes}'
        elif v in ('N', 'NV'):
            txt = '\mathrm{Benutzung\; der\; Approximation\; durch\; die\; Normalverteilung}'
        elif v in ('T', 'Tsch'):
            txt = '\mathrm{Benutzung\; der\; Tschebyschew-Ungleichung}' 	

        dm('\mathrm{Konfidenzintervall\; für\; die\; unbekannte\; Wahrscheinlichkeit\; der\;Binomial-}')
        dm('\mathrm{verteilung;} \;' + txt)
			
        if v in ('S', 'Sigma'):
            #pr(' ')		
            dm('X \,\mathrm{-\, Anzahl\; der\; Treffer\; in\; einer\; Bernoullikette\; der\; Länge}\;' + \
               'n,\; p\,\mathrm{\, -\, unbekannte}')
            dm('\mathrm{Wahrscheinlichkeit}')    		
            alpha = self.konf_niv			   
            kn = {0.9 : 1.64, 0.95 : 1.96, 0.99 : 2.58} 
            if not alpha in list(kn.keys()):
                pr("\mathrm{das Verfahren ist nur bei Konfidenzniveau 0.9, 0.95 oder 0.99 durchführbar}")
                return			   
            dm('\mathrm{Wegen\; der}\;\, \\sigma \mathrm{\,-\,Umgebung\; gilt\; mit\; Wahrscheinlichkeit}\;' + str(alpha))
            dm('\\qquad\\left|\,X-n\,p\,\\right| \\le' + str(kn[alpha]) + '\,\\sigma, \;\mathrm{also' + \
               '\;ist\;mit}\;X=' + str(self.treffer) + ',\;n=' + str(self.n))			
            dm('\\qquad\\left|\,' + str(self.treffer) + '-' + str(self.n) + '\,p\,\\right| \\le' + \
			     str(kn[alpha]) + '\,\\sqrt{' + str(self.n) + '\,p\,(1-p)}' )
            dm('\mathrm{Quadrieren\;führt\;zu\;der\;Ungleichung}')
            p = Symbol('p')			
            li = expand((self.treffer - self.n*p)**2)
            re = expand(kn[alpha]**2 * self.n * p*(1-p))
            dm('\\qquad' + latex(li) + '\\le' + latex(re))
            gl = li - re
            dm('\\qquad' + latex(gl) + '\\le 0')
            dm('\mathrm{Die\; Lösungen\; der\; entsprechenden\; Gleichung\; ergeben\; das\; Intervall}')
            L = solve(gl)
            dm('\mathrm{Konfidenzintervall:} \;[' + '{0:.4}'.format(L[0]) + ',\;' + '{0:.4}'.format(L[1]) + ']' )
            pr(' ')					   			   
            if not printen:
                return [	float('{0:.4}'.format(L[0])), float('{0:.4}'.format(L[1]))]	
        elif v in ('N', 'NV'):
            dm('\mathrm{Vorbetrachtung}')
            dm('X\,\mathrm{-\, Anzahl\; der\; Treffer\; in\; einer\; Bernoullikette\; der\; Länge}\;' + \
               'n,\; p\,\mathrm{ -\, unbekannte}')
            dm('\mathrm{Wahrscheinlichkeit}')    		
            dm('\mathrm{Die\; Zufallsgröße}\;\; \\frac{X-n\,p}{\\sqrt{n\,p\,(1-p)}} = ' + \
               '\\frac{X-n\,p}{\\sigma} \;\;\mathrm{ist\; näherungsweise\;\, (0,1)-nor-}')
            dm('\mathrm{malverteilt, \;es\;ist}' )  
            dm('\\qquad P \\left(-c \\le \\frac{X-n\,p}{\\sigma} \\le c \\right) = \\Phi(c)-\\Phi(-c)' + \
                '= 2 \,\\Phi(c)-1 \;\;\mathrm{mit}')
            dm('\\qquad \\Phi\mathrm{\,-\,Verteilungsfunktion\; der\;\, (0,1)-Normalverteilung}')				
            dm('\mathrm{Eine\; Umformung\; mit}\;\, \\alpha=2 \,\\Phi(c)-1\;\, \mathrm{führt\; zu}') 
            dm('\\qquad P \,\\left( \,\\left| \\frac{X}{n} - p \, \\right| \\le \\frac{\\sigma\, c}{n}' + \
               '\\right) = \\alpha \\quad\\quad  \mathrm{oder}')
            dm('\\qquad P \,\\left( \,\\left| \\frac{X}{n} - p \, \\right| \\le c \,\\sqrt{\\frac{p\, (1-p)}{n}}' + \
               '\\right) = \\alpha')
            dm('\\alpha\; \mathrm{ist\ das\; Konfidenzniveau}')
            dm('\mathrm{Berechnung}')
            aa = 0.5*(1+self.konf_niv)			
            nv = NormalVerteilung(0, 1)
            q = nv.quantil(aa)
            p = Symbol('p')			
            dm('\mathrm{Es\; muß\; gelten}\; \\left| \\frac{X}{n} - p \, \\right| \\le c \,\\sqrt{\\frac{p\,' + \
               '(1-p)}{n}}, \;\mathrm{wobei\; sich}\; c\; \mathrm{aus}\; \\Phi(c) = \\frac{1+\\alpha}{2} = ' + \
               str(aa))
            dm('\mathrm{ergibt; \;die\; Normalverteilung\; liefert}\; ' + 'c = {0:.7}'.format(q) + ',\;\mathrm{mit}\; \
                  X =' + \
               str(self.treffer) + ',\; n =' + str(self.n) + '\;\mathrm{folgt}\;')			
            dm('\\qquad\\left| \\frac{' + str(self.treffer) + '}{' + str(self.n) + '} - p \, \\right|' + \
               '\\le' + '{0:.7}'.format(q) + '\,\\sqrt{\\frac{p\,(1-p)}{' + str(self.n) + '}}' )
            dm('\mathrm{Quadrieren\; führt\; auf\; die\; Ungleichung}')
            pp = expand((Rational(self.treffer, self.n)-p)**2)			
            dm('\\qquad ' + latex(pp) + '\\le' + latex(expand(q**2*p*(1-p)/self.n)))				
            dm('\\qquad ' + latex(N(pp)-expand(q**2*p*(1-p)/self.n)) + '\\le 0')
            dm(latex('\mathrm{Die\; Lösungen\; der\; entsprechenden\; Gleichung\; ergeben\; das\; Konfidenzintervall}'))
            L = solve(N(pp)-expand(q**2*p*(1-p)/self.n))
            dm('[' + '{0:.4}'.format(L[0]) + ',\;' + '{0:.4}'.format(L[1]) + ']')
            pr(' ')					   
            if not printen:
                return [	float('{0:.4}'.format(L[0])), float('{0:.4}'.format(L[1]))]	
        elif v in ('T', 'Tsch'):
            dm('\mathrm{Vorbetrachtung}')
            dm('X\mathrm{\, -\, Anzahl\; der\; Treffer\; in\; einer\; Bernoullikette\; der\; Länge}\;' + \
               'n,\; p\mathrm{\, -\, unbekannte}') 
            dm('\mathrm{Wahrscheinlichkeit}')  
            dm('\\frac{X}{n}\mathrm{\, -\, Zufallsgröße\; mit\; dem\; Erwartungswert}\; p\; \mathrm{und\; der\; Varianz}\;' + \
               '\\frac{p\,(1-p)}{n}')			               		
            dm('\mathrm{Die\;Tschebyschew-Ungleichung\; für\; die\; Zufallsgröße\;lautet}')
            dm('\\qquad P\\left(\ \\left|\, \\frac{X}{n} - p \,\\right| \\ge c \\right) \\le ' + \
                '\\frac{p\,(1-p)}{n\,c^2}')
            dm('\mathrm{Die\;Funktion}\;f(p) = p\,(1-p) \;\mathrm{hat\;bei}\;p=\\frac{1}{2}\;\mathrm{ein\;Maximum,\;deshalb\;ist}')
            dm('\\qquad P\\left(\ \\left|\, \\frac{X}{n} - p \,\\right| \\ge c \\right) \\le ' + \
                '\\frac{1}{4\,n\,c^2}')
            dm('c\;\mathrm{ist\;so\;zu\;wählen,\;daß\;die\;rechte\;Seite}\; \le 1-\\alpha \;\mathrm{wird,\;' + \
               'wobei\;\\alpha\;das\;Konfidenz-}')
            dm('\mathrm{niveau\;ist}')
            dm('\mathrm{Berechnung}')
            aa = self.konf_niv
            cc = sqrt(1/(4*self.n*(1-aa)))	
            hn = self.treffer/self.n			
            dm('\mathrm{Es\;ist}\;\\alpha = ' + str(aa) + ',\;n=' + str(self.n) + ',\;\mathrm{die\;Ungleichung}\; \\frac{1}{' + \
                str(4*self.n) + '\,c^2} \\le' + '{0:.3}'.format(1-aa) + '\;\mathrm{hat\;die\;Lösung}\;c \\ge' + \
                '{0:.3}'.format(cc))
            dm('\mathrm{Ein\;Konfidenzintervall\;ergibt\;sich\;zu}\;\;[h_n-c,\, h_n+c]\;\;mit\;h_n = ' + \
               '\\frac{X}{n}\;\;\mathrm{(relative\;Tref-}')
            dm('\mathrm{ferhäufigkeit)}')
            dm('\mathrm{Mit}\;X='+str(self.treffer)+',\;n=' + str(self.n) + '\;\mathrm{ist}\ h_n=' + \
               '\\frac{'+str(self.treffer)+'}{'+str(self.n)+'} =' + '{0:.4}'.format(hn) + ',\;\mathrm{somit\;ist\;ein\;\
                  Konfidenzintervall}')
            dm('{0:.4}'.format(hn-cc) + ',\;' + '{0:.4}'.format(hn+cc) + ']' )
            pr(' ')	
            if not printen:
                return [	float('{0:.4}'.format(hn-cc)), float('{0:.4}'.format(hn+cc))]	
				
	
    def quantil_nv(self, *args, **kwargs):
        """Quantile der Normalverteilung"""
        if kwargs.get('h'):
            print('\nQuantile der (0,1)-Normalverteilung\n')
            return			
        nv = NormalVerteilung(0, 1)
        q = nv.quantil(*args)	
        if q is None:
            return 		
        return q
		
    quantilNV = quantil_nv		

    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        konfidenz_intervall_hilfe(3)	
		
    h = hilfe					

	
			
def konfidenz_intervall_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
KonfidenzIntervall - Objekt     Konfidenzintervall für die unbekannte Wahr-
                                scheinlichkeit der Binomialverteilung

Kurzname     KI
		
Erzeugung    KI( umfang, treffer, konf_niveau, verfahren )

                 umfang       Stichprobenumfang
                 treffer      Anzahl Treffer in der Stichprobe
                 konf_niveau  Konfidenzniveau/Sicherheitswarscheinlichkeit/
                              Vertrauenszahl	
                 verfahren    'S' | 'Sigma': bei Konfidenzniveau aus 
                                             {0.9, 0.95, 0.99} Benutzung der 
                                             Sigma-Umgebung des Erwartungswer-
                                             tes	
                              'N' | 'NV'   : Benutzung der Approximation durch 
                                             die Normalverteilung	
                              'T' | 'Tsch' : Benutzung der Tschebyschew-Unglei-
                                             chung	
								 
Zuweisung     k = KI(...)   (k - freier Bezeichner)

Beispiele
KI(500, 273, 0.95, 'Sigma')            KI(500, 273, 0.95, 'T')
	   """)		
        return        
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für KonfidenzIntervall
 
k.hilfe               Bezeichner der Eigenschaften und Methoden
k.konf_niv            Konfidenzniveau / Vertrauenszahl
k.konf_int            Konfidenzintervall
k.n                   Stichprobenumfang
k.quantil_nv(...)  M  Quantile der (0,1)-Normalverteilung
k.treffer             Trefferanzahl in der Stichprobe
k.verf                Berechnungsverfahren

Synonyme Bezeichner

hilfe        h
konf_niv     konfNiv
konf_int     konfInt
quantil_nv   quantilNV
    """)		
        return
	
	
KI = KonfidenzIntervall