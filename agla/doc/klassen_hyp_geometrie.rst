.. _klassen_hyp_geometrie:

Klassen der hyperbolischen Geometrie
====================================
	
Betrachtete Modelle (:ref:`siehe auch <hyperbolische_geometrie>`):
	
   **D**  - EinheitsKreisScheiben-Modell in der Ebene
   
   **D3** - D-Modell in der *xy* - Ebene des Raumes
   
   **H**  - HyperboloidHalbSchalen-Modell im Raum

Es stehen folgende Klassen zur Verfügung:

``hPunkt`` - :ref:`hPunkt` 
 
``hGerade`` - :ref:`hGerade`

``hStrecke`` - :ref:`hStrecke`

``hStrahl`` - :ref:`hStrahl`

``hDreieck`` - :ref:`hDreieck`

``hKreis`` - :ref:`hKreis`
 
.. currentmodule:: agla.lib.objekte.hyp_geometrie

|

.. _hPunkt:

hyperbolischer Punkt 
--------------------

.. autoclass:: hPunkt

   **Eigenschaften und Methoden**
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   
   
   .. method:: abstand(hpunkt)

         Hyperbolischer Abstand zu einem anderen Punkt

         *hpunkt* : hyperbolischer Punkt		 
   
   .. autoattribute:: dim
   
   .. autoattribute:: exakt

   .. autoattribute:: is_schar
   
   .. autoattribute:: mod
          
   .. method:: schnitt(hgerade)
   
         Schnitt mit einer hyperbolischen Geraden  

         *hgerade* : hyperbolische Gerade		 
   
   .. method:: sch_el(wert)
   
         Element einer Schar von hyperbolischen Punkten
		 
         *wert* : Wert des Scharparameters
   
   .. attribute:: sch_par
   
         Parameter einer Schar hyperbolischer Punkte   
   
   .. autoattribute:: traeger
   
         Synonym: **e**   

   **Synonyme Bezeichner**
   				
        ``is_schar  :  isSchar``
		
        ``sch_el    :  schEl``
		
        ``sch_par   :  schPar``
		
|
		
.. _hGerade:

hyperbolische Gerade 
--------------------

.. autoclass:: hGerade
	 
   **Eigenschaften und Methoden**
   
   */statt* ``ae`` *kann* ``ä`` *geschrieben werden/*
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   
   
   .. autoattribute:: ber
   
   .. autoattribute:: dim
   
   .. autoattribute:: exakt
   
   .. method:: inv(hobjekt) 
   
         Inversion / Spiegelung eines hyperbolischen Objektes an der Geraden

         Synonym: **spieg**
		 
         *hobjekt* : hyperbolische(r)(s) Punkt, Gerade, Strecke, Dreieck		 
   
   .. method:: inv_f(/[hpunkt])
   
         Abbildungsfunktion zur Inversion eines hyperbolischen Punktes
         an der Geraden

         *hpunkt* : hyperbolischer Punkt	

         Rückgabe: 
            Bei Angabe eines hyperbolischen Punktes wird dessen Bild
            bei der Abbildung ausgegeben, die Funktionsvorschrift
            wird angezeigt

            Wird kein Argument angegeben, wird die Abbildungsfunktion 
            als Funktionsobjekt ausgegeben
			
         Zusatz: `f=1` 
            Ausgabe der Funktionsvorschrift (als komplexe 
            Funktion in der Variablen *z* )	
 		 
   .. method:: lot(hpunkt)
   
         Lot auf die Gerade von einem Punkt aus

         *hpunkt* : hyperbolischer Punkt		 
   
   .. autoattribute:: mod
          
   .. method:: normale(hpunkt)
   
         Normale in einem Punkt der Geraden   
   
         *hpunkt* : hyperbolischer Punkt		 
   
   .. autoattribute:: par
   
   .. autoattribute:: punkte
   
   .. method:: schnitt(hobjekt)
   
            Schnitt mit anderem hyperbolischen Objekt
			
            *hobjekt* : hyperbolische(r) Punkt, Gerade 			
			
   .. autoattribute:: traeger
   
          Synonym: **e**   
  
   .. method:: winkel(hobjekt)
   
         Winkel der Geraden mit einem anderen hyperbolischen Objekt in 
         einem gemeinsamen Punkt   
	 
         *hobjekt* : hyperbolische(r) Punkt, Gerade

         Es wird nicht geprüft, ob der Punkt auf den beiden Objekten
         liegt\n
		 
   **Synonymer Bezeichner**
   
        ``inv_f  :  invF``
		
|
		
.. _hStrecke:

hyperbolische Strecke 
---------------------

.. autoclass:: hStrecke

   **Eigenschaften und Methoden**

   */statt* ``ae`` *kann* ``ä`` *geschrieben werden/*
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   

   .. autoattribute:: ber
   
   .. autoattribute:: dim
   
   .. autoattribute:: exakt
   
   .. autoattribute:: gerade
   
   .. autoattribute:: laenge
   
   .. autoattribute:: mitte

   .. autoattribute:: mitt_senkr
   
   .. autoattribute:: mod
          
   .. method:: normale(hpunkt)
   
         Normale in einem Punkt der Strecke   
   
         *hpunkt* : hyperbolischer Punkt

         Es wird nicht geprüft, ob der Punkt auf der Strecke liegt

   .. autoattribute:: punkte
   
   .. autoattribute:: traeger
   
         Synonym: **e**
		 
   .. method:: winkel(hobjekt, hpunkt)
   
         Winkel der Strecke mit einem anderen hyperbolischen Objekt in einem
         gemeinsamen Punkt

         *hobjekt* : hyperbolische(r) Gerade, Strahl, Strecke
	  
         *hpunkt* : hyperbolischer Punkt - gemeinsamer Punkt
	  
         Es wird nicht geprüft, ob der Punkt zu den beiden Objekten gehört
			
   .. method:: wink_halb(hstrecke, hpunkt)

         Winkelhalbierende Strecke mit einer anderen hyperbolischen Strecke 
         in einem gemeinsamen Endpunkt
		 
         *hstrecke* :  hyperbolische Strecke
		 
         *hpunkt* : hyperbolischer Punkt - gemeinsamer Endpunkt
		 
         Es wird nicht geprüft, ob der Punkt Endpunkt beider Strecken ist
		 
   **Synonyme Bezeichner**
   
        ``mitt_senkr :  mittSenkr``
		
        ``wink_halb  :  winkHalb``

|
		
.. _hStrahl:

hyperbolischer Strahl 
---------------------

.. autoclass:: hStrahl

   **Eigenschaften und Methoden**

   */statt* ``ae`` *kann* ``ä`` *geschrieben werden/*
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   

   .. autoattribute:: ber
   
   .. autoattribute:: dim
   
   .. autoattribute:: exakt
   
   .. autoattribute:: gerade
   
   .. autoattribute:: mod
          
   .. method:: normale(hpunkt)
   
         Normale in einem Strahlpunkt   
   
         *hpunkt* : hyperbolischer Punkt
		 
   .. autoattribute:: punkte

   .. autoattribute:: traeger
   
         Synonym: **e**   
   
   .. method:: winkel(hobjekt, hpunkt)
   
         Winkel mit einem anderen hyperbolischen Objekt in einem gemeinsamen
         Punkt

         *hobjekt* : hyperbolische(r) Gerade, Strahl, Strecke

         *hpunkt* : hyperbolischer Punkt

         Es wird nicht geprüft, ob der Punkt zu den beiden Objekten gehört		 

|

.. _hDreieck:

hyperbolisches Dreieck 
----------------------

.. autoclass:: hDreieck

   **Eigenschaften**

   */statt* ``ae``, ``ss`` *kann* ``ä``, ``ß`` *geschrieben werden/*
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   

   .. autoattribute:: dim

   .. autoattribute:: exakt

   .. autoattribute:: exzess
   
         Synonym: **defekt**   
   
   .. autoattribute:: flaeche
   
   .. autoattribute:: inkreis
   
   .. autoattribute:: laengen
   
   .. autoattribute:: mod
          
   .. autoattribute:: punkte

   .. autoattribute:: seiten
   
   .. autoattribute:: umfang
   
   .. autoattribute:: umkreis
   
   .. autoattribute:: winkel
   
   .. autoattribute:: wink_summe
   
   **Synonymer Bezeichner**
   
        ``wink_summe : winkSumme``

|

.. _hKreis:

hyperbolischer Kreis
--------------------

.. autoclass:: hKreis

   **Eigenschaften und Methoden**

   */statt* ``ae`` *kann* ``ä`` *geschrieben werden/*
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   

   .. autoattribute:: dim
   
   .. autoattribute:: exakt
   
   .. autoattribute:: flaeche

   .. method:: flaeche_()
   
         Flächeninhalt; Dezimalausgabe  
		 
         Zusatz: `f=1` Formel		 
   
   .. autoattribute:: laenge

         Synonym: **umfang**   
   
   .. method:: laenge_()
   
         Länge; Dezimalausgabe  
		 
         Zusatz: `f=1` Formel		 
   
         Synonym: **umfang_**   
   
   .. autoattribute:: mitte
   
         Synonyme: **M**, **m**   
   
   .. autoattribute:: mod
          
   .. autoattribute:: radius
   
         Synonym: **r**   
   
   .. autoattribute:: traeger
   
         Synonym: **e**   
   
   **Synonyme Bezeichner**
   
        ``fläche_  :  Fläche``
		
        ``länge_   :  Länge``
		
        ``umfang_  :  Umfang``

