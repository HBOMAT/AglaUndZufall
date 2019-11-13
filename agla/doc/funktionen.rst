
Funktionen
==========

Als Zahl ist auch jeder Audruck zu verstehen, dessen Evaluierung (nach 
einer eventuellen Substitution von Variablen durch Zahlen) eine Zahl ergibt

*/statt* ``oe`` *kann* ``ö`` *geschrieben werden/*

.. _allg:

Allgemeine Funktionen
---------------------

   .. function:: Hilfe()
   
         Hilfefunktion 

         Zusatz: `h=n`, *n* = 1, 2, ...		 

   .. function:: Determinante(vektor1, vektor2 /[, vektor3])
   
         Determinante von drei Vektoren des Raumes oder von zwei Vektoren der
         Ebene 
		 
         Synonym:   **det**
   
         *vekor* : Vektor
		 
         Zusatz: `d=1`  Dezimaldarstellung
 
   .. function:: linear_abh(vektor1, vektor2, ...)
   
         Test auf lineare Abhängigkeit von Vektoren im Raum und
         in der Ebene 
		 
         Synonym:   **linearAbh**
   
         *vekor* : Vektor
		 
   .. function:: kollinear(vektor1, vektor2) 
   
         *oder*
   
   .. function:: kollinear(punkt1, punkt2, punkt3)

        Test auf Kollinearität von zwei Vektoren oder drei Punkten im Raum
        und in der Ebene 
		 
        *vekor* : Vektor

        *punkt* : Punkt
		 
        Zusatz: `d=1`  Darstellung des einen Vektors durch den anderen

   .. function:: komplanar(vektor1, vektor2, vektor3) 
   
         *oder*
   
   .. function:: komplanar(punkt1, punkt2, punkt3, punkt4)

        Test auf Komplanarität von drei Vektoren oder vier Punkten im Raum
		 
        *vekor* : Vektor

        *punkt* : Punkt
		 
        Zusatz:
           `l=1`  Verschwindende Linearkombination (bei Komplanarität)
		
           `d=1`  Darstellung jedes Vektors durch die beiden anderen (bei Komplanarität)
		   
   .. function:: parallel(objekt1, objekt2)
		   
         Test auf Parallelität von Objekten im Raum und in der Ebene

         *objekt* im Raum:   Vektor, Gerade, Ebene, Strecke
		 
         *objekt* in der Ebene:   Vektor, Gerade, Strecke

   .. function:: orthogonal(objekt1, objekt2)
   
         Test auf Parallelität von Objekten im Raum und in der Ebene

         Synonym: **senkrecht** 
  
         *objekt* im Raum:   Vektor, Gerade, Ebene, Strecke
		 
         *objekt* in der Ebene:   Vektor, Gerade, Strecke

   .. function:: identisch(objekt1, objekt2)
     
        Test auf Identität von zwei Geraden oder zwei Ebenen

        *objekt* :   Gerade, Ebene
		 
   .. function:: Abstand(objekt1, objekt2)
     
        Abstand zweier Objekte voneinander
		
        *objekt* im Raum:   Punkt, Gerade, Ebene, Kugel

        *objekt* in der Ebene:   Punkt, Gerade
		 
        Zusatz: `d=n`   Dezimaldarstellung, *n* - Anzahl der Nachkommastellen
		
   .. function:: Winkel(objekt1, objekt2)
     
        Winkel zwischen zwei Objekten (in Grad)
		
        *objekt* im Raum:   Vektor, Gerade, Ebene

        *objekt* in der Ebene:   Vektor, Gerade
		 
        Zusatz: 
           `d=n`   Dezimaldarstellung mit *n* Nachkommastellen
	
           `b=1`   Ausgabe in Bogenmaß
	
           `d=n`   ebenso, Dezimaldarstellung mit *n* Nachkommastellen
		
   .. function:: Lage(objekt1, objekt2)
     
        Lage zweier Objekte zueinander
		
        *objekt* im Raum:   Vektor/Punkt, Gerade, Ebene, Strecke, Kugel, Dreieck, Viereck

        *objekt* in der Ebene:   Vektor/Punkt, Gerade, Strecke, Kreis, Dreieck, Viereck
		 
        Für die beiden Objekte muss eine passende schnitt-Methode definiert sein
		 
        Zusatz: `l=1`   Lageinformationen
		

   .. function:: loese(gleich /[, variable])
	   
        *oder*

   .. function:: loese(ungleich /[, variable])
			 
        Lösen von normalen und Vektor-Gleichungen sowie von Ungleichungen
		
        *gleich* : linke Seite einer Gleichung der Form ``ausdruck = 0`` 
        oder Liste mit solchen Elementen (Gleichungssystem)	
	
        *variable* : einzelne oder Liste von Variablen
		
        *ausdruck*: Ausdruck in den Variablen; bei einer einzelnen Gleichung
        kann es auch ein Vektor-Ausdruck sein; rechts steht dann der Nullvektor		
		
        *ungleich*:  Ungleichung der Form ``ausdruck1`` *rel* ``ausdruck2``
		
        *rel* : Relation  < | <= | > | >=		
		
        Zusatz: `set=ja`   Verwendung von solveset; standardmäßig wird 
        solve verwendet (siehe SymPy-Dokumentation)		
		
   .. function:: einfach(objekt)

        Vereinfachung von Objekten

        *objekt* : nummerischer Ausdruck, Vektor, Matrix

        Falls ``UMG.SIMPL`` gleich ``False`` ist, wird nicht vereinfacht
		 
        Zusatz: 
           `rad=ja` Einsatz von radsimp
		   
           `trig=ja`  Einsatz von trigsimp	

           `num=ja` Einsatz von nsimplify

           `sign=ja`  Einsatz von signsimp
		   
           (siehe SymPy-Dokumentation)		   
		 
   .. _Grafik:		 
 		 
   .. function:: Grafik(eintrag1, eintrag2, ... /[, gestalt])
 
         Zeichnen einer Grafik in 3D oder 2D 
		 
         Synonym: **zeichne**
            		
         *eintrag* : objekt | [objekt, spez]
		 
         *objekt* : grafikfähiges Objekt
		 
         *spez* : Spezifikationsangaben
		 
         *gestalt* : ein oder mehrere Zusatzangaben zur 
         Gestaltung der Grafik		

         Zu den möglichen Spezifikations- und Zusatzangaben 
         :ref:`siehe hier <grafik_spezifikationen>`	 
 		  
   .. function:: sicht_box(/[xu, xo /[, yu, yo /[, zu, zo]]])

        Einstellen des Sichtbereiches für eine Grafik
		
        Synonym: **sichtBox**   
		  
        *xu, xo* : untere und obere Grenze auf der *x* -Achse
		 
        *yu, yo* : analog für die *y* -Achse
		 
        *zu, zo* : analog für die *z* -Achse
		 
        Der Wert 0 muss in jedem dieser Bereiche enthalten sein
		 
        Sind nur zwei Argumente angegeben, werden diese für alle Achsen 
        angenommen
		 
        Ist kein Argument angegeben, wird die aktuelle Einstellung angezeigt
		 
   .. function:: farben()
            
        Überblick über die Farben in Grafiken
		
   |
   
Abbildungen der Modelle der hyperbolischen Geometrie
----------------------------------------------------
	
   .. function:: D2H(hPunkt)
   
      *D*-Modell :math:`\rightarrow` *H*-Modell   
   
   .. function:: D2D3(hPunkt)
   
      *D*-Modell :math:`\rightarrow` *D3*-Modell
	  
   .. function:: H2D(hPunkt)
   
      *H*-Modell :math:`\rightarrow` *D*-Modell
	  
   .. function:: H2D3(hPunkt)
   
      *H*-Modell :math:`\rightarrow` *D3*-Modell
	  
   .. function:: D32D(hPunkt)
   
      *D3*-Modell :math:`\rightarrow` *D*-Modell
	  
   .. function:: D32H(hPunkt)
   
      *D3*-Modell :math:`\rightarrow` *H*-Modell   
	
        *hPunkt* : hyperbolischer Punkt im jeweiligen Modell	

.. _mathe:
	
   |
   		
Mathematische Funktionen
------------------------
   
   .. function:: sqrt( x )
   
         (Quadrat-) Wurzel -  Funktion

         *x* : Zahl	

         Rückgabe einer reellen Zahl bei *x* > 0
		 
         Zusatz: `d=1` Dezimaldarstellung		 

   .. function:: exp( x )
   
         Exponential - Funktion   

         *x* : Zahl		

         Zusatz: `d=1` Dezimaldarstellung		 
		 
   .. function:: ln( x )
   
         Logarithmus - Funktion (natürlicher Logarithmus) 

         Synonym: **log**
		 
         *x* : Zahl		

         Rückgabe einer reellen Zahl bei *x* > 0
		 
         Zusatz: `d=1` Dezimaldarstellung		 

   .. function:: lg( x )
   
         Logarithmus - Funktion (dekadischer Logarithmus) 

         *x* : Zahl		

         Rückgabe einer reellen Zahl bei *x* > 0
		 
         Zusatz: `d=1` Dezimaldarstellung		 
		 
   .. function:: abs( x )
   
         Betrags - Funktion   

         *x* : Zahl		

         Zusatz: `d=1` Dezimaldarstellung		 
		 
   .. function:: sin( x )
   
         Sinus - Funktion (Winkel in Bogenmaß) 
		 
         *x* : Zahl		

         Zusatz: `d=1` Dezimaldarstellung		 
		 
   .. function:: arcsin( x )
   
         Arkussinus -Funktion (Winkel in Bogenmaß)   
		 
         Synonym: **asin**

         *x* : Zahl		

         Rückgabe einer reellen Zahl bei *x* :math:`\in [-1, 1]`
		 
         Zusatz: `d=1` Dezimaldarstellung		 
   
   .. function:: sing( x )
   
         Sinus - Funktion (Winkel in Grad) 
		 
         *x* : Zahl		

         Zusatz: `d=1` Dezimaldarstellung		 

   .. function:: arcsing( x )
   
         Arkussinus - Funktion (Winkel in Grad)   
		 
         Synonym: **asing**		 

         Rückgabe einer reellen Zahl bei *x* :math:`\in [-1, 1]`
		 
         *x* : Zahl		

         Zusatz: `d=1` Dezimaldarstellung		 

   .. function:: cos( x )
   
         Kosinus - Funktion (Winkel in Bogenmaß) 
		 
         *x* : Zahl		

         Zusatz: `d=1` Dezimaldarstellung		 

   .. function:: arccos( x )
   
         Arkuskosinus - Funktion (Winkel in Bogenmaß)   
		 
         Synonym: **acos**		 
   
         *x* : Zahl		

         Rückgabe einer reellen Zahl bei *x* :math:`\in [-1, 1]`
		 
         Zusatz: `d=1` Dezimaldarstellung		 
   
   .. function:: cosg( x )
   
         Kosinus - Funktion (Winkel in Grad) 
		 
         *x* : Zahl		
		 
         Zusatz: `d=1` Dezimaldarstellung		 
   		 
   .. function:: arccosg( x )
   
         Arkuskosinus - Funktion (Winkel in Grad)   
		 
         Synonym: **acosg**		 
   
         *x* : Zahl		

         Rückgabe einer reellen Zahl bei *x* :math:`\in [-1, 1]`
		 
         Zusatz: `d=1` Dezimaldarstellung		 
   
   .. function:: tan( x )
   
         Tangens - Funktion (Winkel in Bogenmaß) 
		 
         *x* : Zahl		
		 
         Zusatz: `d=1` Dezimaldarstellung		 
   
   .. function:: arctan( x )
   
         Arkustangens - Funktion (Winkel in Bogenmaß)   
		 
         Synonym: **atan**		 
   
         *x* : Zahl		
		 
         Zusatz: `d=1` Dezimaldarstellung		 
      
   .. function:: tang( x )
   
         Tangens  - Funktion (Winkel in Grad) 
		 
         *x* : Zahl		
		 
         Zusatz: `d=1` Dezimaldarstellung		 
   		 
   .. function:: arctang( x )
   
         Arkustangens - Funktion (Winkel in Grad)   
		 
         Synonym: **atang**		 
   
         *x* : Zahl		
   
         Zusatz: `d=1` Dezimaldarstellung		 
   
   .. function:: sinh( x )
   
         Sinus hyperbolikus - Funktion  
		    	
         *x* : Zahl		
   
         Zusatz: `d=1` Dezimaldarstellung		 
				
   .. function:: arsinh( x )
   
         Areasinus hyperbolikus - Funktion    
		 
         Synonym: **asinh**		 
      
         *x* : Zahl		
   
         Zusatz: `d=1` Dezimaldarstellung	
		 
   .. function:: cosh( x )
   
         Kosinus hyperbolikus  - Funktion  
		    		 
         *x* : Zahl		
   
         Zusatz: `d=1` Dezimaldarstellung	
		 
   .. function:: arcosh( x )
   
         Areakosinus hyperbolikus - Funktion    
		 
         Synonym: **acosh**		 
      
         *x* : Zahl		
   
         Zusatz: `d=1` Dezimaldarstellung	
		 
   .. function:: tanh( x )
   
         Tangens hyperbolikus - Funktion    
		    
         *x* : Zahl		
   
         Zusatz: `d=1` Dezimaldarstellung	
			
   .. function:: artanh( x ) 
   
         Areatangens hyperbolikus - Funktion    
		 
         Synonym: **atanh**		 
      
         *x* : Zahl		
   
         Zusatz: `d=1` Dezimaldarstellung	
	  
   .. function:: deg(winkel)
   
         Umrechnung Bogen- in Gradmaß   
		 
         Synonym: **grad**	
		 
         *winkel* : Winkel in Radian		 

         Rückgabe: *Winkel in Grad*		 
		 
         Zusatz: `d=n` Dezimaldarstellung mit *n* Kommastellen		 
   
   .. function:: rad(winkel)
   
         Umrechnung Grad- in Bogenmaß   
		 
         Synonym: **bog**		 
   
         *winkel* : Winkel in Grad		 
   
         Rückgabe: *Winkel in Radian*		 
   
         Zusatz: `d=n` Dezimaldarstellung mit *n* Kommastellen		 
      
   .. function:: kug_koord(punkt)
   
         Umrechnung in Kugelkoordinaten   
		 
         Synonym: **kugKoord**	

         *punkt* : Punkt der Einheitssphäre oder sPunkt	 
		 
         Rückgabe: *Länge, Breite*		 
   
         Zusatz: `g=1` Ausgaben in Grad		 
   
   .. function:: min(zahl1, zahl2, ...)
   
         Kleinste Zahl in einer Folge von zwei oder mehr Zahlen  
		 
         *zahl* : Zahl	 
		 
         Rückgabe: *kleinste Zahl*		 
   
   .. function:: max(zahl1, zahl2, ...)
   
         Größte Zahl in einer Folge von zwei oder mehr Zahlen  
		 
         *zahl* : Zahl	 
		 
         Rückgabe: *größte Zahl*		 
   
.. _konst:
		
   |
   
Konstanten
----------

   .. attribute:: pi 

         Zahl :math:`\pi` (3.1415...)
	  
   .. attribute:: E

         Eulersche Zahl :math:`e` (2.7182...)

   .. attribute:: I

         Imaginäre Einheit :math:`i`
	  
   .. attribute:: ja, nein, mit, ohne, Ja, Nein, Mit, Ohne

         Hilfsgrößen für True/False
		 
   |
   
.. warning::

   Die Namen **E, I** können kommentarlos überschrieben werden		
		 	  
.. _sympy:
		
   |
   
SymPy - Funktionen
------------------

   .. function:: N(ausdruck, /[, m])
   
         Umwandlung von SymPy-Zahlen / -Ausdrücken in Dezimal-Zahlen 
         / -Ausdrücke  
		 
         *ausdruck* : nummerischer Ausdruck
		 
         *m* : Anzahl der Stellen	 

         Es kann auch die entsprechende **n**-Methode eines SymPy-Ausdruckes 
         verwendet werden: ``ausdruck.n(/[m])``
		 
   Weiterhin sind die SymPy-Funktionen **solve, solveset, expand, collect, 
   factor, simplify, nsimplify, radsimp, trigsimp, nsolve, re, im, diff**
   sowie die Klasse **Rational** direkt verwendbar
   
   Werden weitere SymPy-Elemente benötigt, können sie importiert werden
		
   |
   
.. warning::

   Der Name **N** kann kommentarlos überschrieben werden		
		
		
		