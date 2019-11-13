
Kurve
=====

.. currentmodule:: agla.lib.objekte.kurve

.. autoclass:: Kurve
   
   **Eigenschaften und Methoden für Kurven im Raum**
   
   */statt* ``ae``, ``ue`` *kann* ``ä``, ``ü`` *geschrieben werden/*   
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   
   
   .. autoattribute:: ber
   
   .. autoattribute:: bog_laenge
   
   .. autoattribute:: dim
   
   .. autoattribute:: evolute
   
   .. autoattribute:: formeln
   
   .. autoattribute:: gleich
   
   .. autoattribute:: is_eben
   
   .. autoattribute:: is_schar
   
   .. autoattribute:: par
   
   .. autoattribute:: pf
   
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
   
   .. method:: bi_normale(/[wert] )
   
         Binormale
	
         *wert* : Wert des Kurvenparameters

         Rückgabe :   
            bei Angabe eines Parameterwertes:
               Binormale im zugehörigen Punkt der Kurve					  
            bei leerer Argumentliste oder freiem Bezeichner:
               Binormale im allgemeinen Punkt der Kurve 			
   
   .. method:: drei_bein(/[wert] )
   
         Begleitendes Dreibein 
   
         *wert* : Wert des Kurvenparameters
		 
         Rückgabe :   
			
            (Tangenteneinheitsvektor, Hauptnormaleneinheitsvektor, Binormaleneinheitsvektor)	
			
            bei Angabe eines Parameterwertes:
               Dreibein im zugehörigen Punkt der Kurve					  
            bei leerer Argumentliste oder freiem Bezeichner:
               Dreibein im allgemeinen Punkt der Kurve 			
   
   .. method:: geschw(/[wert] )
   
        Geschwindigkeits- / Tangentialvektor

        Synonym: **tang_vekt**
		
        *wert* : Wert des Kurvenparameters

        Rückgabe :   
           bei Angabe eines Parameterwertes:
              Geschwindigkeitsvektor im zugehörigen Punkt der Kurve					
           bei leerer Argumentliste oder freiem Bezeichner:
              Geschwindigkeitsvektor im allgemeinen Punkt der Kurve 			
   
   .. method:: h_normale(/[wert] )
   
        Hauptnormale

        *wert* : Wert des Kurvenparameters

        Rückgabe :   
           bei Angabe eines Parameterwertes:
              Hauptnormale im zugehörigen Punkt der Kurve					  
           bei leerer Argumentliste oder freiem Bezeichner:
              Hauptnormale im allgemeinen Punkt der Kurve 			
   
   .. method:: kruemm(/[wert] )
   
         Krümmung

         *wert* : Wert des Kurvenparameters

         Rückgabe :   
            bei Angabe eines Parameterwertes:
               Krümmung im zugehörigen Punkt der Kurve					  
            bei leerer Argumentliste oder freiem Bezeichner:
               Krümmung im allgemeinen Punkt der Kurve 			
   		 
         Zusatz : `d=1` Dezimaldarstellung 		 
		 
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
      
   .. method:: norm_ebene(/[wert] )
   
         Normalebene  
		
         *wert* : Wert des Kurvenparameters

         Rückgabe :   
            bei Angabe eines Parameterwertes:
               Normalebene im zugehörigen Punkt der Kurve
					  
            bei leerer Argumentliste oder freiem Bezeichner:
               Normalebene im allgemeinen Punkt der Kurve 			
   
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

   .. method:: proj(ebene)
   
         Projektion auf eine Ebene   
		 
         *ebene* : *xy* -, *xz* - oder *yz* - Ebene oder eine zu einer von 
         diesen parallele Ebene
   
   .. method:: rekt_ebene(/wert] )
   
         Rektifizierende Ebene   
   
         *wert* : Wert des Kurvenparameters

         Rückgabe :   
            bei Angabe eines Parameterwertes:
               Rektifizierende Ebene im zugehörigen Punkt der Kurve					  
            bei leerer Argumentliste oder freiem Bezeichner:
               Rektifizierende Ebene im allgemeinen Punkt der Kurve 			
   
   .. method:: sch_el(wert)
   
         Element einer Kurvenschar mit einem Parameter
			
         *wert* : Wert des Scharparameters
		    
   .. method:: schm_ebene(/[wert] )
   
         Schmiegebene

         *wert* : Wert des Kurvenparameters

         Rückgabe :   
            bei Angabe eines Parameterwertes:
               Schmiegebene im zugehörigen Punkt der Kurve
            bei leerer Argumentliste oder freiem Bezeichner:
               Schmiegebene im allgemeinen Punkt der Kurve 			
   
   .. method:: schnitt(kurve, start1, start2)
   
         Schnitt mit einer anderen Kurve

         *kurve* :	Kurve	 
		 
         *start* : Startwert des nummerischen Verfahrens
		 
         Rückgabe : (Parameterwert für die gegebene Kurve, Parameterwert für
         die andere Kurve)
		 
         Die beiden Startwerte für die Kurven sind so genau wie möglich 
         anzugeben; die Parameterwerte werden über die Minimierung des 
         Abstandes der Kurvenpunkte zueinander gesucht; es wird :func:`nsolve` 
         verwendet (siehe SymPy-Dokumentation)			 
		 
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
		  
   .. method:: wind(/[wert] )
   
         Windung, Torsion  

         Synonym: **tors**
		 
         *wert* : Wert des Kurvenparameters

         Rückgabe :   
            bei Angabe eines Parameterwertes:
               Windung im zugehörigen Punkt der Kurve					  
            bei leerer Argumentliste oder freien Bezeichnern:
               Windung im allgemeinen Punkt der Kurve 			
		 
         Zusatz : `d=1` - Dezimaldarstellung
		 		 
   .. method:: winkel(objekt, par_wert_kurve /[, par_wert_objekt] )
   
         Winkel mit einem anderen Objekt (in Grad)	  
		 
         *objekt* : Gerade, Kurve, Ebene
		 
         *par_wert* :   Parameterwert des Schnittpunktes 
		 
         *par_wert_objekt* ist nur anzugeben, wenn *objekt* eine Kurve ist, 
         die nicht mit impliziter Gleichung erzeugt wurde	 
		 
         Es wird nicht geprüft, ob die angegebenen Parameterwerte zu einem 
         Schnittpunkt gehören
		 
   |   
   
   **Synonyme Bezeichner**
   		
      ``bi_normale :  biNormale``
		
      ``bog_länge  :  bogLänge``
	  
      ``drei_bein  :  dreiBein``
		
      ``h_normale  :  hNormale``
		
      ``is_eben    :  isEben``
		
      ``is_schar   :  isSchar``
		
      ``kr_kreis   :  krKreis``
		
      ``kr_radius  :  krRadius``
		
      ``norm_ebene :  normEbene``
		
      ``par_wert   :  parWert``
		
      ``rekt_ebene :  rektEbene``
		
      ``sch_el     :  schEl``
		
      ``sch_par    :  schPar``
		
      ``schm_ebene :  schmEbene``
		
      ``tang_vekt  :  tangVekt``
   
