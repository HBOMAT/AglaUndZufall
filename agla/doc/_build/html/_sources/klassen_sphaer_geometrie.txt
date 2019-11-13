.. _klassen_sphaer_geometrie:

Klassen der sphärischen Geometrie
=================================

Zu allgemeinen Angaben siehe :ref:`hier <sphaerische_geometrie>`

Es stehen folgende Klassen zur Verfügung:

``sPunkt`` - :ref:`sPunkt` 

``sGerade`` - :ref:`sGerade` 

``sStrecke`` - :ref:`sStrecke` 

``sDreieck`` - :ref:`sDreieck` 

``sKreis`` - :ref:`sKreis` 

``sZweieck`` - :ref:`sZweieck` 
 
.. currentmodule:: agla.lib.objekte.sphaer_geometrie

|

.. _sPunkt:

sphärischer Punkt 
-----------------

.. autoclass:: sPunkt

   **Eigenschaften und Methoden**

   */statt* ``ae`` *kann* ``ä`` *geschrieben werden/*
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   
   
   .. method:: abstand(spunkt)

         Sphärischer Abstand zu einem anderen Punkt

         *spunkt* : sphärischer Punkt		 
   
   .. method:: bild(abbildung)
   
         Bildpunkt bei einer Abbildung
		 
         *abbildung* : Isometrie der Einheitssphäre

   .. autoattribute:: breite
   
         Synonyme: **b**, **phi**   
      		 
   .. autoattribute:: e
   
   .. autoattribute:: diam
   
   .. autoattribute:: dim
   
         Synonym: **gegen**   
		 
   .. autoattribute:: geo_koord
   
   .. autoattribute:: is_schar
   
   .. autoattribute:: laenge
   
         Synonyme: **l**, **lamda** *Schreibweise beachten*  
    
   .. autoattribute:: polare
   
   .. method:: schnitt(sgerade)
   
         Schnitt mit einer sphärischen Geraden  

         *sgerade* : sphärische Gerade		 
   
   .. method:: sch_el(wert)
   
         Element einer Schar von spärischen Punkten
		 
         *wert* : Wert des Scharparameters
   
   .. autoattribute:: sch_par
   
   **Synonyme Bezeichner**
   		
        ``geo_koord :  geoKoord``
		
        ``is_schar  :  isSchar``
		
        ``sch_el    :  schEl``
		
        ``sch_par   :  schPar``
     
|
	 
.. _sGerade:
	 
sphärische Gerade 
-----------------

.. autoclass:: sGerade

   **Eigenschaften und Methoden**

   */statt* ``ae`` *kann* ``ä`` *geschrieben werden/*
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   
   
   .. method:: bild(abbildung)
   
         Bildgerade bei einer Abbildung
		 
         *abbildung* : Isometrie der Einheitssphäre

   .. autoattribute:: dim
   		 
   .. method:: normale(spunkt)
   
         Normale in einem Geradenpunkt
   
         *spunkt* : Punkt der sphärischen Geraden  
		 
   .. method:: pkt(/[wert])
   
         Punkt der sphärischen Geraden
		 
         *wert* : Wert des Geradenparameters  aus :math:`[0, 2 \pi]`		 
   
         Rückgabe : 						 
            bei Angabe eines Parameterwertes: 
               Geradenpunkt, der zu diesem Wert gehört
			   
            bei leerer Argumentliste oder freiem Bezeichner: 
               allgemeiner Punkt der Geraden 
		 
   .. autoattribute:: pol
   
   .. autoattribute:: punkte
   
   .. method:: schnitt(sobjekt)
   
         Schnitt mit einem anderen sphärischen Objekt

         *sobjekt* : sphärische(r) Punkt, Gerade, Kreis
		 
   .. autoattribute:: traeger
   
         Synonym: **e**   
   
   .. method:: winkel(sgerade)
   
         Winkel der sphärischen Geraden mit einer anderen sphärischen 
         Geraden im gemeinsamen Schnittpunkt   

         *sgerade* : sphärische Gerade

|
		 
.. _sStrecke:

sphärische Strecke 
------------------

.. autoclass:: sStrecke
     	 
   **Eigenschaften und Methoden**

   */statt* ``ae`` *kann* ``ä`` *geschrieben werden/*
   
   .. autoattribute:: hilfe
   
          Synonym: **h**
		  
   .. autoattribute:: ber

   .. method:: bild(abbildung)
   
         Bildstrecke bei einer Abbildung
		 
         *abbildung* : Isometrie der Einheitssphäre

   .. autoattribute:: dim
   		 
   .. autoattribute:: gerade
		 
   .. autoattribute:: laenge
   
   .. autoattribute:: mitte
		
   .. autoattribute:: mitt_senkr
		
   .. method:: normale(spunkt)
   
         Normale in einem Streckenpunkt
   
         *spunkt* : Punkt der sphärischen Strecke  
		 
   .. method:: pkt(/[wert])
   
         Punkt der spärischen Strecke
		 
         *wert* : Wert des Streckenparameters aus [0, 1]		 
   
         Rückgabe : 						 
            bei Angabe eines Parameterwertes: 
               Streckenpunkt, der zu diesem Wert gehört
			   
            bei leerer Argumentliste oder freiem Bezeichner: 
               allgemeiner Punkt der Strecke 
		    
   .. autoattribute:: punkte
   		 
   .. autoattribute:: traeger
   
         Synonym: **e**   
   
   .. method:: winkel(sstrecke)
   
         Winkel der sphärischen Strecke mit einer anderen sphärischen 
         Strecke in einem gemeinsamen Endpunkt   

         *sstrecke* : sphärische Strecke

   .. method:: wink_halb(sstrecke)
   
         Winkelhalbierende der sphärischen Strecke mit einer anderen 
         sphärischen Strecke in einem gemeinsamen Endpunkt   

         *sstrecke* : sphärische Strecke
		 
   **Synonyme Bezeichner**
		
        ``mitt_senkr :  mittSenkr``
		
        ``wink_halb  :  winkHalb`` 
		 
|
		 
.. _sDreieck:
	 
sphärisches Dreieck 
-------------------

.. autoclass:: sDreieck

   **Eigenschaften und Methoden**

   */statt* ``ae`` *kann* ``ä`` *geschrieben werden/*
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   
   
   .. method:: bild(abbildung)
   
         Bilddreieck bei einer Abbildung
		 
         *abbildung* : Isometrie der Einheitssphäre

   .. autoattribute:: dim

   .. autoattribute:: flaeche
   
   .. autoattribute:: inkreis
   
   .. autoattribute:: laengen
   
   .. autoattribute:: punkte
   
   .. autoattribute:: seiten
   
   .. autoattribute:: umfang
   
   .. autoattribute:: winkel
   
   .. autoattribute:: wink_summe
   
   **Synonymer Bezeichner**
   		
        ``wink_summe :  winkSumme``		

|

.. _sKreis:

sphärischer Kreis 
-----------------

.. autoclass:: sKreis
     	 
   **Eigenschaften und Methoden**

   */statt* ``ae`` *kann* ``ä`` *geschrieben werden/*
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   
   
   .. method:: bild(abbildung)
   
         Bildkreis bei einer Abbildung
		 
         *abbildung* : Isometrie der Einheitssphäre

   .. autoattribute:: dim
   
   .. autoattribute:: flaeche
   
   .. method:: flaeche_()
   
         Flächeninhalt, Dezimalausgabe

         Zusatz : `f=1` - Formel		 
   
   .. autoattribute:: mitte
   
         Synonyme: **M**, **m**   
   
   .. autoattribute:: radius

         Synonym: **r**   
   
   .. method:: schnitt(sgerade)

         Schnitt mit einer sphärischen Geraden
		 
         *sgerade* : sphärische Gerade  
   
   .. autoattribute:: traeger
   
         Synonym: **e**   
   
   .. autoattribute:: umfang
       
   .. method:: umfang_()
   
         Umfang, Dezimalausgabe

         Zusatz : `f=1` - Formel		 
   
   **Synonyme Bezeichner**
  		
        ``fläche_ :  Fläche``
				
        ``umfang_ :  Umfang``
		 
|
		 
.. _sZweieck:
	 
sphärisches Zweieck 
-------------------

.. autoclass:: sZweieck

   **Eigenschaften und Methoden**

   */statt* ``ae`` *kann* ``ä`` *geschrieben werden/*
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   
      
   .. method:: bild(abbildung)
   
         Bildzweieck bei einer Abbildung
		 
         *abbildung* : Isometrie der Einheitssphäre

   .. autoattribute:: dim

   .. autoattribute:: flaeche
   
   .. autoattribute:: punkte
   
   .. autoattribute:: seiten
   
   .. autoattribute:: umfang
   
   .. autoattribute:: winkel
      


