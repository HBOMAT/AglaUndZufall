
Nutzung von SymPy-Anweisungen
=============================

In *zufall* sind folgende Elemente von SymPy integriert:	

``Symbol``, ``symbols`` - zur Definition von (freien) Bezeichnern

``Rational`` - zur Eingabe von rationalen Zahlen 

``solve``, ``solveset``, ``expand``, ``collect``, ``factor``, ``simplify``, 
``nsimplify``
 
``N`` - zur Umwandlung in Dezimalzahlen; der Wert ist überschreibbar

``pi`` - die Kreiszahl

``E`` - die Basis der natürlichen Logarithmen :math:`e` 
(der Wert ist überschreibbar)

``I`` - die imaginäre Einheit :math:`i` (der Wert ist überschreibbar)	
	
Sollen weitere Elemente benutzt werden, sind diese zu importieren, z.B.::

   In [..]: from sympy import ceiling
   
(eventuell ist der Pfad im  SymPy-Verzeichnis-Baum anzugeben)			

|
