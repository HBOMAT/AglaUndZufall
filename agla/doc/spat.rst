
Spat
====

.. currentmodule:: agla.lib.objekte.spat

.. autoclass:: Spat
   
   **Eigenschaften und Methoden**

   */statt* ``ae``, ``oe`` *kann* ``ä``, ``ö`` *geschrieben werden/*
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   
 	
   .. autoattribute:: dim
   
   .. autoattribute:: in_koerper
   
   .. autoattribute:: in_prisma
      
   .. autoattribute:: is_schar
   
   .. autoattribute:: laengen
   
   .. method:: laengen_()
   
         Seitenlängen; Dezimaldarstellung
		 
         Zusatz : `d=n` - mit *n* Nachkomma-/Stellen    
		 
   .. autoattribute:: punkte

   .. method:: punkte_()

         zu punkte zugehörig; Erläuterung der Ausgabe	  
   
   .. autoattribute:: sch_par
   
   .. autoattribute:: spann
   
   .. autoattribute:: stuetz
   
   .. autoattribute:: volumen

   .. method:: volumen_()
   
         Volumen; Dezimaldarstellung
		 
         Zusatz : 
		 
            `d=n` - mit *n* Nachkomma-/Stellen 
			
            `f=1` - Formel		 
   	    	 
   .. autoattribute:: winkel

   .. method:: winkel_()
		 
         Winkel zwischen den Spannvektoren; Dezimaldarstellung
		 
         Zusatz : `d=n`  - mit *n* Nachkomma-/Stellen       
   	 
   .. method:: bild(abbildung)
   
         Bild bei einer Abbildung
		 
         *abbildung* : Abbildung des Raumes
   
   .. method:: sch_el(wert)
   
         Element einer Spatschar mit einem Parameter
			
         *wert* : Wert des Scharparameters
		       
   |
  
   **Synonyme Bezeichner**
  	  	  
      ``in_körper :  inKörper``
	
      ``in_prisma :  inPrisma``
	
      ``is_schar  :  isSchar``
	
      ``längen_   :  Längen``
	
      ``punkte_   :  Punkte``
	
      ``sch_el    :  schEl``
	  
      ``sch_par   :  schPar``
	
      ``volumen_  :  Volumen``
 
 		 