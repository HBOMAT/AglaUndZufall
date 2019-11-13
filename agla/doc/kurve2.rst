
Kurve
=====

.. currentmodule:: agla.lib.objekte.kurve

.. autoclass:: Kurve
      
   **Eigenschaften und Methoden für parametrisierte Kurven in der Ebene**
   
   (die Kurven werden mittels Parameterform/-gleichung, Funktionsgleichung 
   oder Polarkoordinaten erzeugt)   
   
   */statt* ``ae``, ``ue`` *kann* ``ä``, ``ü`` *geschrieben werden/*      
   
   .. autoattribute:: hilfe
   
   .. autoattribute:: ber
   		 
   .. autoattribute:: bog_laenge
      
   .. autoattribute:: dim
   
   .. autoattribute:: evolute
         
   .. autoattribute:: fkt
      
   .. autoattribute:: formeln
   
   .. autoattribute:: gleich
   
   .. autoattribute:: imp
      
   .. autoattribute:: in_raum
      
   .. autoattribute:: is_schar
   
   .. autoattribute:: par
      
   .. autoattribute:: pf
   
   .. autoattribute:: pol
   
   .. autoattribute:: prg
   
   .. autoattribute:: sch_par

   .. method:: beschl(/[wert] )

         Beschleunigungsvektor    
   
         *wert* : Wert des Kurvenparameters

         Rückgabe :   
            bei Angabe eines Parameterwertes:
               Beschleunigungsvektor im zugehörigen Punkt der Kurve	  
            bei leerer Argumentliste oder freiem Bezeichner:
               Beschleunigungsvektor im allgemeinen Punkt der Kurve
			   
   .. method:: bild(abbildung)
   
         Bildkurve bei einer Abbildung
		 
         *abbildung* : Abbildung
   
   .. method:: geschw(/[wert] )
   
        Geschwindigkeits- / Tangentialvektor
		
        Synonym: **tang_vekt**
		
        *wert* : Wert des Kurvenparameters

        Rückgabe :   
           bei Angabe eines Parameterwertes:
              Geschwindigkeitsvektor im zugehörigen Punkt der Kurve	  
           bei leerer Argumentliste oder freiem Bezeichner:
              Geschwindigkeitsvektor im allgemeinen Punkt der Kurve 			
			   
   .. method:: kruemm(/[wert] )
   
         Krümmung 

         *wert* : Wert des Kurvenparameters

         Rückgabe :   
            bei Angabe eines Parameterwertes:
               Krümmung im zugehörigen Punkt der Kurve	  
            bei leerer Argumentliste oder freiem Bezeichner:
               Krümmung im allgemeinen Punkt der Kurve 			
   		 
         Zusatz : `d=1` - Dezimaldarstellung 		 
		 
   .. method:: kr_kreis(/[wert] )
   
         Krümmungskreis  
   
         *wert* : Wert des Kurvenparameters

         Rückgabe :   
            bei Angabe eines Parameterwertes:
               Krümmungskreis im zugehörigen Punkt der Kurve					  
            bei leerer Argumentliste oder freiem Bezeichner:
               Krümmungskreis im allgemeinen Punkt der Kurve 			
      
   .. method:: kr_radius(/[wert] )

         Krümmungsradius    
   
         *wert* : Wert des Kurvenparameters

         Rückgabe :   
            bei Angabe eines Parameterwertes:
               Krümmungsradius im zugehörigen Punkt der Kurve					  
            bei leerer Argumentliste oder freiem Bezeichner:
               Krümmungsradius im allgemeinen Punkt der Kurve 			
      
   .. method:: normale(/[wert])

         Normale
   
         *wert* : Wert des Kurvenparameters

         Rückgabe :   
            bei Angabe eines Parameterwertes:
               Normale im zugehörigen Punkt der Kurve
					  
            bei leerer Argumentliste oder freiem Bezeichner:
               Normale im allgemeinen Punkt der Kurve 			
      
   .. method:: par_wert(punkt, start)
   
         Parameterwert eines Kurvenpunktes

         *punkt* : Punkt

         *start* : Startwert des nummerischen Verfahrens 
						
         Der Parameterwert wird über die Minimierung des Abstandes des Punktes 
         zu einem Kurvenpunkt gesucht; es wird :func:`nsolve` verwendet 
         (siehe SymPy-Dokumentation)
            
         Zusatz : 
            `d=1` - Dezimaldarstellung 
		 
            `g=1` - Grafik der Abstandsfunktion (Abstand des gegebenen  
            Punktes zu den Kurvenpunkten)			
					 
   .. method:: pkt(/[wert] )
   
         Punkt der Kurve			 
   
         *wert* : Wert des Kurvenparameters

         Rückgabe :   
            bei Angabe eines Parameterwertes:
               Kurvenpunkt, der zu diesem Wert gehört					  
            bei leerer Argumentliste oder freien Bezeichnern:
               allgemeiner Punkt der Kurve 			
			   
   .. method:: sch_el(wert)
   
         Element einer Kurvenschar mit einem Parameter
			
         *wert* : Wert des Scharparameters
		    
   .. method:: schnitt(kurve, start1, start2)
   
         Schnitt mit einer anderen Kurve

         *kurve* :	parametrisierte Kurve	 
		 
         *start* : Startwert des nummerischen Verfahrens
		 
         Rückgabe : (Parameterwert für die gegebene Kurve, Parameterwert für 
         die andere Kurve)
		 
         Die beiden Startwerte für die Kurven sind so genau wie möglich anzugeben;
         die Parameterwerte werden über die Minimierung des Abstandes der 
         Kurvenpunkte zueinander gesucht; es wird :func:`nsolve` verwendet 
         (siehe SymPy-Dokumentation)			 
		 
   .. method:: stueck(par_unt, par_ob)
   
         Kurvenstück			 
		 
         *par_unt, par_ob* : untere und obere Bereichsgrenzen des Kurvenparameters		 
		 
   .. method:: tangente(/[wert] )
   
         Tangente

         *wert* : Wert des Kurvenparameters

         Rückgabe :   
            bei Angabe eines Parameterwertes:
               Tangente im zugehörigen Punkt der Kurve		  
            bei leerer Argumentliste oder freien Bezeichnern:
               Tangente im allgemeinen Punkt der Kurve 			
		  
   .. method:: winkel(objekt, par_wert_kurve /[, par_wert_objekt] )
   
         Winkel mit einem anderen Objekt (in Grad)	  
		 
         *objekt* : Gerade, Kurve
		 
         *par_wert* :   Parameterwert des Schnittpunktes 
		 
         *par_wert_objekt* ist nur anzugeben, wenn *objekt* eine Kurve ist, 
         die nicht mit impliziter Gleichung erzeugt wurde	 
		 		 
         Es wird nicht geprüft, ob die angegebenen Parameterwerte zu einem 
         Schnittpunkt gehören 	
		 
   .. method:: zwei_bein(/[wert] )
   
         Begleitendes Zweibein 
   
         *wert* : Wert des Kurvenparameters
		 
         Rückgabe :   
			
            (Tangenteneinheitsvektor, Normaleneinheitsvektor)	
			
            bei Angabe eines Parameterwertes:
               Zweibein im zugehörigen Punkt der Kurve	  
            bei leerer Argumentliste oder freiem Bezeichner:
               Zweibein im allgemeinen Punkt der Kurve 			
   		
   **Eigenschaften und Methoden für Kurven in der Ebene, die mittels 
   impliziter Gleichung erzeugt wurden**
	
   .. autoattribute:: hilfe

   .. autoattribute:: dim
         
   .. autoattribute:: formeln
   
   .. autoattribute:: gleich
   
   .. autoattribute:: imp
   
   .. autoattribute:: is_schar
   
   .. autoattribute:: sch_par
   
   .. method:: bild(abbildung)
   
         Bildkurve bei einer Abbildung
		 
         *abbildung* : Abbildung
   
   .. method:: geschw(punkt)
   
        Geschwindigkeits- / Tangentialvektor
		
        Synonym: **tang_vekt**		

         *punkt* : Punkt der Kurve

   .. method:: kruemm(punkt)
   
         Krümmung 

         *punkt* : Punkt der Kurve
		 
         Zusatz : `d=1` Dezimaldarstellung

   .. method:: kr_kreis(punkt)
   
         Krümmungskreis  
   
         *punkt* : Punkt der Kurve
   
   .. method:: kr_radius(punkt)

         Krümmungsradius   
   
         *punkt* : Punkt der Kurve
   
   .. method:: normale(punkt)

         Normale
   
         *punkt* : Punkt der Kurve

   .. method:: sch_el(wert)
   
         Element einer Kurvenschar mit einem Parameter
			
         *wert* : Wert des Scharparameters

   .. method:: tangente(punkt)
   
         Tangente

         *punkt* : Punkt der Kurve

   .. method:: winkel(objekt, /[, par_wert_objekt] )
   
         Winkel mit einem anderen Objekt (in Grad)	  
		 
         *objekt* : Gerade, Kurve
		 
         *par_wert* :   Parameterwert des Schnittpunktes 
		 
         *par_wert_objekt* ist nur anzugeben, wenn *objekt* eine Kurve ist, 
         die nicht mit impliziter Gleichung erzeugt wurde	 
		 
         Es wird nicht geprüft, ob der angegebene Parameterwert zu einem 
         Schnittpunkt gehören
   
   .. method:: zwei_bein(punkt)
   
         Begleitendes Zweibein 
   
         *punkt* : Punkt der Kurve
		 	
   |
   
   **Synonyme Bezeichner**
   
        ``hilfe     :  h``
		
        ``bog_länge :  bogLänge``
		
        ``in_raum   :  inRaum``	
		
        ``is_schar  :  isSchar``
		
        ``kr_kreis  :  krKreis``
		
        ``kr_radius :  krRadius``
		
        ``par_wert  :  parWert``
		
        ``sch_el    :  schEl``
		
        ``sch_par   :  schPar``
		
        ``tang_vekt :  tangVekt``
		
        ``zwei_bein :  zweiBein``
   