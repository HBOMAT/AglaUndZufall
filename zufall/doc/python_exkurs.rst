
Kleiner Python-Exkurs
=====================

**Eingabe von Code** 

   (in eine Code-Zelle des Jupyter-Notebooks)

   Die Ausführung der aktuellen Zelle wird durch ``Umsch+Enter`` bzw. 
   ``Strg+Enter`` veranlaßt
	
   Eine Zuweisung (eines Wertes an einen Bezeichner) wird mittels ``=`` 
   realisiert::
	
      In [..]: a = 4
		
   Der Wert eines Bezeichners kann über eine Abfrage ermittelt werden::
	
      In [..]: a
		
   Mehrere Zuweisungen in einer Zeile sind durch ``;`` zu trennen::
	
      In [..]: a = 4; b = 34; c = -8
		
   Mehrere Abfrageanweisungen in einer Zeile sind durch ``,`` zu trennen (ein 
   ``;`` unterdrückt die Anzeige der vorausgehenden Elemente)::
	
     In [..]: a, b, c
		
   Eine neue Zeile (innerhalb einer Zelle des Notebooks) wird über die
   ``Enter-Taste`` erzeugt; in der neuen Zeile ist ab derselben Stelle zu 
   schreiben wie in der vorangehenden Zeile, wenn nicht ein eingerückter 
   Block entstehen soll (bzw. wenn nicht durch ein ``\`` am Zeilenende eine
   Verlängerung der Zeile erreicht werden soll)
	
   Das ist **Teil der Python-Syntax** und führt bei Nichtbeachten zu einem
   Syntaxfehler
	
   Eingerückte Blöcke sind z.B. bei Kontrollstrukturen (vor allem in 
   Programmen benutzt) erforderlich. Dabei müssen alle Einrückungen die 
   gleiche Stellenanzahl (standardmäßig 4 Stellen) haben. Bei der ``if-else``-
   Anweisung sieht das z.B. folgendermaßen aus::
	
      In [..]: if a < 1: 
                   b = 0        # 4 Stellen eingerückt
                   c = 3        # ebenso		
               else:
                   b = 1        # ebenso
					 
   oder bei einer Funktions-Definition::
	
      In [..]: def kugel(r):
                   m = v(1, 2, 0)				
                   return Kugel(m, r)
					 
   Die Funktion definiert eine Schar von Kugeln mit festem Mittelpunkt  
   und dem Radius *r* als Parameter, jeder Aufruf erzeugt eine konkrete
   Instanz der Klasse Kugel::
		
      In [..]: k3, k5 = kugel(3), kugel(5)
		
   Mittels ``#`` können in Codezellen Kommentare geschrieben werden, sie 
   werden bei der Ausführung ignoriert
	
**Einige Datentypen**

   **Zeichenkette** (engl. *string*)   z.B.:  ``'Tab23'``; ``"Tab25"``
	
   **Tupel** (engl. *tuple*)   z.B.
	
      .. code-block:: python
	
         In [..]: t = ( 1, 2, 3 )
		 
                  t1 = ( 'a', a, Rational(1, 2), 2.7 )
				  
      Tupel können nicht verändert werden				  
		
      Zugriff auf Elemente  ``t[0]``, ``t1[-1]``, Slicing  (Zählung ab 0)
		
   **Liste** (engl. *list*)   z.B.
	
      .. code-block:: python
	
         In [..]: L = [ 1, 2, 3 ] 
		 
                  L1 = [ 'b', a, Rational(2, 3) ]
				  
      Listen können verändert werden				  
 		
      Zugriff auf Elemente  ``L[0]``, ``L1[-1]``, Slicing  (Zählung ab 0)
		
   **Schlüssel-Wert-Liste** (engl. *dictionary*, *dict*)   z.B.
	
      .. code-block:: python
	
         In [..]: d = { a:4, b:34, c:-8 }
		
      Zugriff auf Elemente  ``d[a]``, ``d[c]``
		
   **Menge** (engl. *set*)   z.B.
	
      .. code-block:: python
	
         In [..]: m = { a, b, c }
		 
                  m1 = set() # leere Menge
		
      Zugriff auf Elemente  ``m.pop()``, Indexzugriff mit 
      ``list(m)[index]`` möglich		
		
**Weitere nützliche Python-Elemente**

   **Funktion** ``type``
   
      Mittels ``type(obj)`` kann der Datentyp eines Objektes ``obj`` 
      erfragt werden
	
   **List-Comprehension**
	
      .. code-block:: python
	
         In [..]: tup = (1, 2, 3, 4, 5, 6)  
		 
         In [..]: [ x^2 for x in tup ]    	
		 
         Out[..]: [1, 4, 9, 16, 25, 36] 
		
   Funktionsdefinition mit **anonymer Funktion**
   
      .. code-block:: python
	
         lambda x, y, ... : ausdruck in x, y, ...
		
   **Klasse** ``Rational``
   
      Da ``p/q`` in Python (und damit auch in SymPy) eine ``float``-Zahl 
      ergibt, kann bei Bedarf eine rationale Zahl ``Rational(p, q)`` 
      verwendet werden (in *zufall* erfolgt das an den meisten Stellen 
      automatisch)
 		
   ``*liste`` **als Argument einer Funktion** packt den Container ``liste`` 
   aus
	
   **Ersetzen** eines Bezeichners in einem Ausdruck durch einen Wert (eine 
   SymPy-Anweisung)
		
      .. code-block:: python
		
	     ausdruck.subs(bezeichner, wert)

      .. code-block:: python
				
         In [..]: (x+y).subs(x, 2)		
         Out[..]: y+2
		
   Die **Ausgabe** ``<bound method ...>``

      weist auf eine an ein Objekt gebundene Methode (eine Funktion) hin, die
      zu ihrer Ausführung in Klammern eingefasste Parameter erwartet	




