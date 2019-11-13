
Matrix
======

   Das Paket *agla* besitzt keine eigene Matrix-Klasse, es wird direkt die 
   (angepaßte) **MutableDenseMatrix**-Klasse von SymPy verwendet 

   Matrizen können eine beliebige Dimension *mxn* haben, *m*, *n* > 1
   
|   
	
**Erzeugung** 

   Matrix ( *vektor1, vektor2,* ... )
   
   *oder*

   vektor1 | vektor2 | ... 
   
      *vektor* : (Spalten-)Vektor; alle Vektoren müssen die gleiche Dimension 
      haben
	  
      ``|`` : Verkettungsoperator	  
	
   *oder*

   Erzeugung auf die in SymPy verwendete Art (siehe SymPy-Dokumentation)
   
|
   
   **Zugriff** auf das Element in Zeile *i* und Spalte *j* der *mxn* - Matrix *M*:
   
      *M[i, j], i=0...m-1, j=0...n-1*
	  
      mittels Zuweisung können so auch einzelne Elemente verändert werden
     
|

**Operatoren**

   +--------+------------------------------------------------+   
   | ``+``  | Addition von zwei Matrizen                     |
   +--------+------------------------------------------------+   
   | ``-``  | Negation / Subtraktion von Matrizen            |
   +--------+------------------------------------------------+   
   | ``*``  | Multiplikation mit Skalar, Vektor, Matrix      |
   +--------+------------------------------------------------+   
   | ``^``  | Potenzieren einer Matrix mit einer ganzen Zahl |
   +--------+------------------------------------------------+   
   | ``**`` | ebenso                                         |
   +--------+------------------------------------------------+   
   | ``|``  | Verketten einer Matrix mit einem Vektor        |
   +--------+------------------------------------------------+   
   
|
   
**Vordefinierte Matrizen** im Raum und in der Ebene

   ``NullMat``   : Nullmatrix im Raum

   ``EinhMat``   :	Einheitsmatrix im Raum

   ``NullMat2``  : Nullmatrix in der Ebene

   ``EinhMat2``  :	Einheitsmatrix in der Ebene
   
|
   
Die unten aufgeführten **Eigenschaften und Methoden** betreffen Matrizen mit 
einer Zeilenanzahl < 4. Für höhere Dimensionen siehe 
:ref:`Andere Klassen  <andere_klassen>`
      
.. currentmodule:: None
	  
.. attribute:: hilfe

      Bezeichner der Eigenschaften und Methoden           
   
      Synonym: **h**

.. attribute:: anz_spalt
                  
      Anzahl Spalten
	  
      SymPy-Zugriff: **cols**		 

.. attribute:: anz_zeil
                  
      Anzahl Zeilen
	  
      SymPy-Zugriff: **rows**		 

.. attribute:: char_poly
                  
      Charakteristisches Polynom; nur für *2x2*- und *3x3*-Matrizen
	  
      SymPy-Zugriff: **charpoly()**		 

.. attribute:: D
                  
      Determinante; nur für *2x2*- und *3x3*-Matrizen
	  
      SymPy-Zugriff: **det()**		 
	  
.. attribute:: dim
                  
      Dimension
	  
      SymPy-Zugriff: **shape**	

.. attribute:: eig_wert
                  
      Eigenvwerte; nur für *2x2*- und *3x3*-Matrizen
	  
      SymPy-Zugriff: **eigenvects()**	

.. attribute:: eig_vekt
                  
      Eigenvektoren; nur für *2x2*- und *3x3*-Matrizen
	  
      SymPy-Zugriff: **eigenvects()**

.. attribute:: einfach
                  
      Vereinfachung
	  
      SymPy-Zugriff: **simplify** (*matrix*)		

.. attribute:: inverse
                  
      Inverse; nur für *2x2*- und *3x3*-Matrizen
	  
      SymPy-Zugriff: **inv()**	

      Es kann auch ``m^-1`` benutzt werden, *m* - Matrix	  
	  
.. attribute:: is_schar
                  
      Test auf Schar

.. method:: sch_el(/[wert])
                  
      Element einer Schar
	  
      *wert* : Wert des  Scharparameters	  

.. attribute:: sch_par
                  
      Scharparameter

.. attribute:: transp
                  
      Transponierte
	  
      SymPy-Zugriff: **T** *oder*	**transpose()**

.. attribute:: vekt
                  
      Spaltenvektoren

|
	  
**Synonyme Bezeichner**
   
   ``anz_spalt :  anzSpalt``
   
   ``anz_zeil  :  anzZeil``
   
   ``char_poly :  charPoly``
   
   ``eig_wert  :  eigWert``
   
   ``eig_vekt  :  eigVekt``
   
   ``is_schar  :  isSchar``
   
   ``sch_el    :  schEl``
   
   ``sch_par   :  schPar``	

   
   