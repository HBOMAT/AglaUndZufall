
Vektor
======

.. currentmodule:: agla.lib.objekte.vektor

.. autoclass:: Vektor

   Der **lesende Zugriff** auf die *i*. Komponente eines Vektors *a* der
   
      Dimension *3* erfolgt neben ``a.x``, ``a.y`` und ``a.z`` auch mittels

      ``a[i]``   *oder*   ``a.komp[i]``, *i = 0, 1, 2*
   
      Eine Änderung einzelner Komponenten ist nicht implementiert

   |

   Die unten aufgeführten **Eigenschaften und Methoden** betreffen Vektoren 
   in der Ebene und im Raum. Für :ref:`höhere Dimensionen <hoehDim>` sind 
   nicht alle verfügbar
     
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
		 
         Zusatz : `d=n`  - mit *n* Nachkomma-/Stellen   
      
   .. autoattribute:: dim
   
   .. autoattribute:: einfach
   
   .. autoattribute:: einh_vekt
   
   .. autoattribute:: is_schar
   
   .. autoattribute:: komp
   
         Synonym: **koord**
   
   .. autoattribute:: O
      
   .. autoattribute:: punkt_ausg
      
   .. autoattribute:: sch_par
	  
   .. autoattribute:: vektor2sympy
   
   .. autoattribute:: x
   
   .. autoattribute:: y
   
   .. autoattribute:: z
   
   .. autoattribute:: zeil
   
         Synonym: **T**   
      
   .. method:: abstand(objekt)
         
         Abstand des Punktes zu einem anderen Objekt
      
         *objekt* im Raum: Punkt, Gerade, Ebene, Kugel
		 
         *objekt* in der Ebene: Punkt, Gerade 
		 					 
         Zusatz : `d=n` - mit *n* Nachkomma-/Stellen 
			
         Rückgabe : 0, wenn der Punkt in *objekt* enthalten bzw. mit diesem 
         identisch ist	

   .. method:: bild(abbildung)
   
         Bildvektor/-punkt bei einer Abbildung
		 
         *abbildung* : Abbildung des Raumes oder der Ebene
   
   .. method:: diff(variable)

         Partielle Ableitung eines Vektors mit mehreren Variablen nach 
         einer der Variablen	
		 
         *variable* : Variable, nach der abgeleitet wird
		   
   .. method:: kette(vektor1, vektor2, ...)
   
         Verketten von Vektoren zu einer Matrix
			   
         *vektor* : Vektor

         Mit dem Operator ``|`` kann die Verkettung auch so erfolgen
		 
            *vektor* | *vektor1* | *vektor2* ...
			
   .. method:: kollinear(vektor)
   		
         *oder*
   
   .. method:: kollinear(punkt1, punkt2)
   
         Test auf Kollinearität für 2 Vektoren bzw. 3 Punkte
		 
         *vektor* : Vektor
		 
         *punkt* : Punkt		 
   
   .. method:: komplanar(vektor1, vektor2) 
      
         *oder*
   
   .. method:: komplanar(punkt1, punkt2, punkt3) 

         Test auf Komplanararität für 3 Vektoren bzw. 4 Punkte
		 
         *vektor* : Vektor
		 
         *punkt* : Punkt		 
		
         Nur im Raum verfügbar			
   
   .. method:: sch_el(wert)
   
         Element einer Schar mit einem Parameter
			
         *wert* : Wert des Scharparameters
		    
   .. method:: schnitt(objekt)
   
         Schnittmenge des Punktes mit einem anderen Objekt
		 
         *objekt* im Raum: Punkt, Gerade, Ebene, Kugel, Strecke, Dreieck, Viereck
		 
         *objekt* in der Ebene: Punkt, Gerade, Strecke, Dreieck, Viereck
		 
         Zusatz : `l=1` - Lageinformationen
   
   .. method:: sp(vektor)
   
         Skalarprodukt mit einem anderen Vektor

         *vektor* : Vektor
		 
         Mit den Operatoren ``*`` oder ``°`` kann das Skalarprodukt zweier

         Vektoren auch so erhalten werden:

            ``vektor1 * vektor2`` *oder*

            ``vektor1 ° vektor2``
   
   .. method:: vp(vektor)
   
         Vektorprodukt mit einem anderen Vektor

         *vektor* : Vektor
		 
         Mit dem Operator ``><`` kann das Vektorprodukt zweier Vektoren auch
         so erhalten werden:

            ``vektor1 >< vektor2`` 
			
         Nur im Raum verfügbar			
   
   .. method:: winkel(objekt)
   
         Winkel des Vektors mit einem anderen Objekt (in Grad)

         *objekt* im Raum: Vektor, Gerade, Ebene
		 
         *objekt* in der Ebene: Vektor, Gerade
		 
         Zusatz : `d=n` - Dezimaldarstellung mit *n* Nachkomma-/Stellen 
      
|
   
   **Synonyme Bezeichner**
	  
      ``betrag_     :  Betrag``
	  
      ``dez_        :  Dez``
	  
      ``einh_vekt   :  einhVekt``
	  
      ``is_schar    :  isSchar``
	  
      ``länge_      :  Länge``
	  
      ``punkt_ausg  :  punktAusg``
	  
      ``sch_el      :  schEl``
	  
      ``sch_par     :  schPar``
	  	  
	  
	  
   
   
   
