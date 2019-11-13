
Matrix (Zeilen-, Spaltenanzahl > 3)
===================================

   Das Paket *agla* besitzt keine eigene Matrix-Klasse, es wird direkt die 
   (angepaßte) **MutableDenseMatrix**-Klasse von SymPy verwendet 

   Matrizen können eine beliebige Dimension *mxn* haben, *m*, *n* > 1
	
|

**Erzeugung** 

   **Matrix** ( *vektor1, vektor2,*, ... )
   
   *oder*

   vektor1 | vektor2 | ... 
   
      *vektor* :    (Spalten-)Vektor; alle Vektoren müssen die gleiche 
      Dimension haben
	  
      ``|`` : Verkettungsoperator	  
	
   *oder*

   Erzeugung auf die in SymPy verwendete Art (siehe SymPy-Dokumentation)
   
|

   **Zugriff** auf das Element in Zeile *i* und Spalte *j* der *mxn* - 
   Matrix *M*:
   
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
   
**Eigenschaften und Methoden**
	  
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
                  
      Charakteristisches Polynom; nur für *nxn*-Matrizen
	  
      SymPy-Zugriff: **charpoly()**		 

.. attribute:: D
                  
      Determinante; nur für *nxn*-Matrizen
	  
      SymPy-Zugriff: **det()**		 
	  
.. attribute:: dim
                  
      Dimension
	  
      SymPy-Zugriff: **shape**	

.. attribute:: einfach
                  
      Vereinfachung
	  
      SymPy-Zugriff: **simplify** (*matrix*)		

.. attribute:: inverse
                  
      Inverse; nur für *nxn*-Matrizen
	  
      SymPy-Zugriff: **inv()**	

      Es kann auch *m^-1* benutzt werden, *m* - Matrix	  
	  
.. attribute:: is_schar
                  
      Test auf Schar

.. attribute:: sch_el
                  
      Element einer Schar

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
   
   ``is_schar  :  isSchar``
   
   ``sch_el    :  schEl``
   
   ``sch_par   :  schPar``	

   
   
      

