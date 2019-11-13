
Fläche
======

.. currentmodule:: agla.lib.objekte.flaeche

.. autoclass:: Flaeche
   
   **Eigenschaften und Methoden** für **parametrisierte** Flächen

   */statt* ``ae``, ``ss`` *kann* ``ä``, ``ß`` *geschrieben werden/*   
   
   .. autoattribute:: hilfe
   
   .. autoattribute:: ber
   
   .. autoattribute:: dim
   
   .. autoattribute:: fkt
   
   .. autoattribute:: imp
   
   .. autoattribute:: is_schar
   
   .. autoattribute:: par
   
   .. autoattribute:: pf
   
   .. autoattribute:: prg
   
   .. autoattribute:: sch_par
   
   .. method:: bild(abbildung)
   
         Bildfläche bei einer Abbildung
		 
         *abbildung* : Abbildung
   
   .. method:: drei_bein(/[u_wert, w_wert] )
   
         Begleitendes Dreibein
		 
         *wert* : Wert eines Flächenparameters		

         Rückgabe : 
            ( zwei Tangenteneinheitsvektoren, 
			Normaleneinheitsvektor )
						 
            bei Angabe von zwei Parameterwerten: 
               Dreibein in einem bestimmten Punkt der Fläche
            bei leerer Argumentliste oder freien Bezeichnern: 
               Dreibein im allgemeinen Punkt der Fläche 
		 
   .. method:: fund_form1(/[u_wert, w_wert] )
   
         Synonyme: **ff1**, **I**   
   
         Erste Fundamentalform

         *wert* : Wert eines Flächenparameters		
		 
         Rückgabe : 						 
            bei Angabe von zwei Parameterwerten: 
               Koeffizienten der 1. Fundamentalform in einem bestimmten Punkt der Fläche
            bei leerer Argumentliste oder freien Bezeichnern: 
               Koeffizienten der 1. Fundamentalform im allgemeinen Punkt der Fläche 
		 
         Zusatz :
            `d=1` - Dezimaldarstellung
			   
            `df=1` - Darstellung in Differentialen
			   
            `m=1` - Matrix-Darstellung 
		 
   .. method:: fund_form2(/[u_wert, w_wert] )
   
         Synonyme: **ff2**, **II**   
   
         Zweite Fundamentalform

         *wert* : Wert eines Flächenparameters		
		 
         Rückgabe : 						 
            bei Angabe von zwei Parameterwerten: 
               Koeffizienten der 2. Fundamentalform in einem bestimmten Punkt der Fläche   
            bei leerer Argumentliste oder freien Bezeichnern: 
               Koeffizienten der 2. Fundamentalform im allgemeinen Punkt der Fläche 
		 
         Zusatz :
            `d=1` -  Dezimaldarstellung
			   
            `df=1` - Darstellung in Differentialen
			   
            `m=1` -  Matrix-Darstellung 
		 
   .. method:: gauss_kruemm(/[u_wert, w_wert] )
   
         Synonyme: **K**, **k**   
   
         Gauß'sche Krümmung 

         *wert* : Wert eines Flächenparameters		
		 
         Rückgabe : 						 
            bei Angabe von zwei Parameterwerten: 
               Gauß'sche Krümmung in einem bestimmten Punkt der Fläche   
            bei leerer Argumentliste oder freien Bezeichnern: 
               Gauß'sche Krümmung im allgemeinen Punkt der Fläche 
		 
         Zusatz :
            `d=1` -  Dezimaldarstellung
     
   .. method:: haupt_kr_radius(/[u_wert, w_wert] )
   
         Synonyme: **HKR**, **hkr**
   
         Hauptkrümmungsradien

         *wert* : Wert eines Flächenparameters		
		 
         Rückgabe : 						 
            bei Angabe von zwei Parameterwerten: 
               Hauptkrümmungsradien in einem bestimmten Punkt der Fläche   
            bei leerer Argumentliste oder freien Bezeichnern: 
               Hauptkrümmungsradien im allgemeinen Punkt der Fläche 
		 
         Zusatz : `d=1` - Dezimaldarstellung
   
   .. method:: haupt_kr_richt(/[u_wert, w_wert] )

         Synonyme: **HKRicht**, **hkRicht**
   
         Hauptkrümmungsrichtungen  

         *wert* : Wert eines Flächenparameters		
		 
         Rückgabe : 						 
            bei Angabe von zwei Parameterwerten: 
               Hauptkrümmungsrichtungen in einem bestimmten Punkt der Fläche			   
            bei leerer Argumentliste oder freien Bezeichnern: 
               Hauptkrümmungsrichtungen im allgemeinen Punkt der Fläche 
		 
         Zusatz : `d=1` - Dezimaldarstellung
   
   .. method:: haupt_kruemm(/[u_wert, w_wert] )
   
         Synonyme: **HK**, **hk**
		 
         Hauptkrümmungen  

         *wert* : Wert eines Flächenparameters		
		 
         Rückgabe : 						 
            bei Angabe von zwei Parameterwerten: 
               Hauptkrümmungen in einem bestimmten Punkt der Fläche	   
            bei leerer Argumentliste oder freien Bezeichnern: 
               Hauptkrümmungen im allgemeinen Punkt der Fläche 
		 
         Zusatz : `d=1` - Dezimaldarstellung
      
   .. method:: kurve(u_fkt, w_fkt, (par_name, par_unt, par_ob) )
  
         Kurve auf der Fläche
		 		 
         *fkt*    :    Funktion in einem Argument (Parameter)
		 
         *par_name* :  Name des Parameters
		 
         *par_unt, par_ob* : untere und obere Bereichsgrenzen des Parameters		 
		    
   .. method:: mitt_kruemm(/[u_wert, w_wert] )
   
         Synonyme: **H**, **hh**

         Mittlere Krümmung  

         *wert* : Wert eines Flächenparameters		
		 
         Rückgabe : 						 
            bei Angabe von zwei Parameterwerten: 
               Mittlere Krümmung in einem bestimmten Punkt der Fläche
            bei leerer Argumentliste oder freien Bezeichnern: 
               Mittlere Krümmung im allgemeinen Punkt der Fläche 
		 
         Zusatz : `d=1`   Dezimaldarstellung
      
   .. method:: norm(/[u_wert, w_wert] )
   
         Normalenvektor   
   
         *wert* : Wert eines Flächenparameters		
		 
         Rückgabe : 						 
            bei Angabe von zwei Parameterwerten: 
               Normalenvektor in einem bestimmten Punkt der Fläche
            bei leerer Argumentliste oder freien Bezeichnern: 
               Normalenvektor im allgemeinen Punkt der Fläche 
   
   .. method:: par_wert(punkt, start1, start2)
   
         Parameterwerte eines Flächenpunktes
		 
         *start* : Startwert des nummerischen Verfahrens zur Berechnung 
         der Flächenparameter
		 
         Die Startwerte für die beiden Flächenparameter sind so genau wie 
         möglich anzugeben; die Parameterwerte werden über die Minimierung 
         des Abstandes, des gegebenen Punktes zu den Flächenpunkten gesucht; 
         es wird :func:`nsolve` verwendet (siehe SymPy-Dokumentation)	
   
   .. method:: pkt(/[u_wert, w_wert] )
   
         Punkt der Fläche   

         *wert* : Wert eines Flächenparameters		
		 
         Rückgabe : 						 
            bei Angabe von zwei Parameterwerten: 
               zugehöriger Punkt der Fläche   
            bei leerer Argumentliste oder freien Bezeichnern: 
               allgemeiner Punkt der Fläche 
   
   .. method:: sch_el(wert)
   
         Element einer Flächenschar mit einem Parameter
			
         *wert* : Wert des Scharparameters
		       
   .. method:: tang_ebene(/[u_wert, w_wert] )
   
         Tangentialebene    

         *wert* : Wert eines Flächenparameters		
		 
         Rückgabe : 						 
            bei Angabe von zwei Parameterwerten: 
               Tangentialebene in einem bestimmten Punkt der Fläche  
            bei leerer Argumentliste oder freien Bezeichnern: 
               Tangentialebene im allgemeinen Punkt der Fläche 
   
   .. method:: tang_vekt(/[u_wert, w_wert] )
   
         Tangentenvektoren 

         *wert* : Wert eines Flächenparameters		
		 
         Rückgabe : 						 
            bei Angabe von zwei Parameterwerten: 
               Tangentenvektoren in einem bestimmten Punkt der Fläche
            bei leerer Argumentliste oder freien Bezeichnern: 
               Tangentenvektoren im allgemeinen Punkt der Fläche 
   		 
   .. method:: weing_matrix(/[u_wert, w_wert] )

         Weingarten-Matrix
		 
         *wert* : Wert eines Flächenparameters		
		 
         Rückgabe : 						 
            bei Angabe von zwei Parameterwerten: 
               Weingarten-Matrix in einem bestimmten Punkt der Fläche			   
            bei leerer Argumentliste oder freien Bezeichnern: 
               Weingarten-Matrix im allgemeinen Punkt der Fläche 
   
   |
   
   **Synonyme Bezeichner***
   
        ``hilfe           :  h``
		
        ``drei_bein       :  dreiBein``
		
        ``fund_form1      :  fundForm1``
				
        ``fund_form2      :  fundForm2``
		
        ``gauß_krümm      :  gaußKrümm``
				
        ``haupt_kr_radius :  hauptKrRadius``
		
        ``haupt_kr_richt  :  hauptKrRicht``
		
        ``haupt_krümm     :  hauptKrümm``
		
        ``is_schar        :  isSchar``
				
        ``mitt_krümm      :  mittKrümm``
		
        ``par_wert        :  parWert``
		
        ``sch_el          :  schEl``
		
        ``sch_par         :  schPar``
		
        ``tang_ebene      :  tangEbene``
		
        ``tang_vekt       :  tangVekt``
		
        ``weing_matrix    :  weingMatrix``
   
   |
   
   **Eigenschaften und Methoden** für Flächen, die mittels 
   **impliziter Gleichung** erzeugt wurden
   
   .. autoattribute:: hilfe
   
   .. autoattribute:: dim
   
   .. autoattribute:: fkt
   
   .. autoattribute:: imp
   
   .. autoattribute:: is_schar
   
   .. autoattribute:: pf
   
   .. autoattribute:: prg
   
   .. autoattribute:: sch_par
   
   .. method:: bild(abbildung)
   
         Bildfläche bei einer Abbildung
		 
         *abbildung* : Abbildung
      
   .. method:: norm(punkt)
   
         Normalenvektor 

         *punkt* : Punkt der Fläche		 
      
   .. method:: sch_el(wert)
   
         Element einer Flächenschar mit einem Parameter
			
         *wert* : Wert des Scharparameters
   
   .. method:: tang_ebene(punkt)
   
         Tangentialebene   
   
         *punkt* : Punkt der Fläche		    
   
   .. method:: tang_vekt(punkt)
   
         Tangentenvektoren   
   
         *punkt* : Punkt der Fläche	

         Rückgabe : Spannvektoren der Tangentialebene		 
   
   |
   
   **Synonyme Bezeichner**
   
        ``hilfe      :  h``
		
        ``is_schar   :  isSchar``
		
        ``sch_el     :  schEl``
		
        ``sch_par    :  schPar``
		
        ``tang_ebene :  tangEbene``
		
        ``tang_vekt  :  tangVekt``
   
   
   
   
   
   