
Vektor (Komponentenanzahl > 3)
==============================

.. currentmodule:: agla.lib.objekte.vektor

.. autoclass:: Vektor

   Der **lesende Zugriff** auf die *i*. Komponente eines Vektors *a* erfolgt 
   
      mittels ``a[i]`` *oder auch* ``a.komp[i]``, *i = 0, 1, 2, ..., a.dim-1*
   
      Eine Änderung einzelner Komponenten ist nicht implementiert

   |
   
   .. _hoehDim:		 
   
   **Eigenschaften und Methoden** für Vektoren mit Komponentenanzahl > 3 
     
   */statt* ``ae`` *kann* ``ä`` *geschrieben werden/*
   
   .. autoattribute:: hilfe
 	
         Synonym: **h**
		 		 
   .. autoattribute:: betrag
   	    
         Synonym: **laenge**
		 
   .. method:: betrag_()
 
         Betrag des Vektors; Dezimaldarstellung
		 
         Synonym: **laenge_**
		 
         Zusatz : `d=n` - mit *n* Nachkomma-/Stellen   

   .. autoattribute:: d   

   .. autoattribute:: dez
   		 
   .. method:: dez_()
 
         Dezimaldarstellung
		 
         Zusatz : `d=n` - mit *n* Nachkomma-/Stellen   
   		    
   .. autoattribute:: dim
   
   .. autoattribute:: einfach
   
   .. autoattribute:: einh_vekt
   
   .. autoattribute:: is_schar
   
   .. autoattribute:: komp
         
         Synonym: **koord**
		 
         Zugriff auf :math:`i`. Komponente mit :math:`\;\text{komp}[i]`, :math:`\;\;i \ge 0`	
		 
   .. autoattribute:: O
      
   .. autoattribute:: sch_par
               
   .. autoattribute:: vektor2sympy
   
   .. autoattribute:: zeil
      
         Synonym: **T**
		 
   .. method:: abstand(punkt)
         
         Abstand des Punktes zu einem anderen Punkt
      		 
         *punkt* : Punkt mit gleicher Dimension
		 					 
         Zusatz : `d=n` - mit *n* Nachkomma-/Stellen 
			
   .. method:: diff(variable)

         Partielle Ableitung eines Vektors mit mehreren Variablen nach 
         einer der Variablen	
		 
         *variable* :       Variable, nach der abgeleitet wird
		   
   .. method:: kette(vektor1, vektor2, ... )
   
         Verketten von Vektoren zu einer Matrix
			   
         *vektor* : Vektor

         Mit dem Operator ``|`` kann die Verkettung auch so erfolgen
		 
            *vektor* | *vektor1* | *vektor2* ...
			
   .. method:: sch_el(wert)
   
         Element einer Schar mit einem Parameter
			
         *wert* : Wert des Scharparameters
		    
   .. method:: sp(vektor)
   
         Skalarprodukt mit einem anderen Vektor

         *vektor* : Vektor
		 
         Mit den Operatoren ``*`` oder ``°`` kann das Skalarprodukt zweier
         Vektoren auch so erhalten werden:

            ``vektor * vektor1`` *oder*

            ``vektor ° vektor1``
			
   |
   
   **Synonyme Bezeichner**
   		
        ``betrag_    :  Betrag``
		
        ``dez_       :  Dez``
		
        ``einh_vekt  :  einhVekt``
		
        ``is_schar   :  isSchar``
		
        ``länge_     :  Länge``
		
        ``sch_el     :  schEl``
		
        ``sch_par    :  schPar``




