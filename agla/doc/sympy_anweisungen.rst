
Nutzung von SymPy-Anweisungen
=============================

In *agla* sind folgende Elemente von SymPy integriert:	

``Symbol``, ``symbols`` - zur Definition von (freien) Bezeichnern

``Rational`` - zur Eingaber von rationalen Zahlen 

``solve``, ``solveset``, ``expand``, ``collect``, ``factor``, ``simplify``, 
``nsimplify``, ``sympify``
 
``N`` - zur Umwandlung in Dezimalzahlen; der Wert ist überschreibbar

``pi`` - die Kreiszahl

``E`` - die Basis der natürlichen Logarithmen :math:`e` 
(der Wert ist überschreibbar)

``I`` - die imaginäre Einheit :math:`i` (der Wert ist überschreibbar)	
	
Sollen weitere Elemente benutzt werden, sind diese zu importieren, z.B.::

   In [..]: from sympy import Piecewise
   
(eventuell ist der Pfad im  SymPy-Verzeichnis-Baum anzugeben)			

|
