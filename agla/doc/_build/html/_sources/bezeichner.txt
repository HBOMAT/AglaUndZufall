
Bezeichner
==========

Die erzeugten *agla*-Objekte können einem Bezeichner zugewiesen werden, 
z.B. wird mit der Anweisung

.. code-block:: python

   In [..]: g = Gerade(2, -3)
   
dem Bezeichner ``g`` als Wert ein Gerade-Objekt zugewiesen (``'='`` ist in Python
für Zuweisungen vorgesehen)

Ein Bezeichner kann in *agla* aus allen Buchstaben des englischen Alphabets,
allen Ziffern ``0, 1, ..., 9`` und dem Unterstrich ``'_'`` bestehen, wobei er mit
einem Buchstaben beginnen muß. Weiterhin können die deutschen Umlaute und ``ß``
verwendet werden. Der Name kann beliebig lang sein, es wird zwischen großen und 
kleinen Buchstaben unterschieden. Auf diese Art gebildeten Namen kann jederzeit 
ein Objekt (*agla*-Objekt oder anderes, z.B. eine Zahl) zugewiesen werden. Dabei 
darf es sich nicht um einen geschützten Namen handeln (s.u.)

Anders verhält es sich bei den "freien" Bezeichnern, denen unmittelbar kein
Wert zugewiesen wird und die als Variablen oder als Parameter u.a. in 
Gleichungen auftreten. Im Unterschied zu anderen CAS werden in dem von *agla* 
benutzten SymPy solche Bezeichner nicht einfach durch Hinschreiben erkannt 
und akzeptiert, sondern sie müssen explizit als Symbole deklariert werden. 
Für Buchstaben und kleine griechische Buchstaben wird das bereits innerhalb
von *agla* erledigt, so  dass Bezeichner wie ``r, g, b, A, B`` usw. jederzeit  
frei verwendet werden können

Soll ein freier Bezeichner länger als ein Zeichen sein, muss er mittels einer
entsprechenden SymPy-Anweisung deklariert werden, etwa durch

.. code-block:: python
   
   In [..]: xyz = Symbol('xyz')
   
oder (gleichzeitige Erzeugung mehrerer Bezeichner)   

.. code-block:: python
   
   In [..]: aa, bb, cc = symbols('aa bb cc')
   
Falls in einem Bezeichner ein Umlaut vorkommt, wird er bei der Eingabe 
umgewandelt (z.B. ``ß`` in ``ss``). Deshalb ist zu vermeiden, dass in einer 
Sitzung solche Namenspaare wie ``schoen`` und ``schön`` benutzt werden (beide 
haben intern den Namen ``schoen``)
 
Es gibt eine Reihe von Bezeichnern, die in *agla* eine feste Bedeutung haben 
und nicht anderweitig verwendet werden können, indem sie einen anderen Wert 
bekommen. Beim Versuch, einen anderen Wert an einen solchen Bezeichner zu 
binden, warnt *agla* mit einem Hinweis und verhindert das Überschreiben des 
bisherigen Wertes. Ebenfalls in das Warnsystem aufgenommen wurden die  
Elemente der SymPy-Sprache, die innerhalb von *agla* zur Verfügung des 
Nutzers gestellt werden

Besondere Beachtung erfordern die Bezeichner B, E, N und I, denen Konstanten
zugewiesen sind. Sie werden kommentarlos überschrieben, wenn ihnen ein ande-
rer Wert zugewiesen wird		

Viele Eigenschaften/Methoden haben synonyme Bezeichner, die folgendermaßen
gebildet werden:

- ein '_' (Unterstrich) innerhalb des Bezeichners einer Eigenschaft oder 
  Methode wird eliminiert, indem der nächste Buchstabe groß geschrieben  
  wird, z.B. ``sch_el`` :math:`\rightarrow` ``schEl`` (*Kamelschreibweise*; 
  Methode "Scharelement")
	 
- ein '_' am Ende eines Bezeichners wird eliminiert, indem das erste Zeichen
  groß geschrieben wird, z.B: ``umfang_``:math:`\rightarrow` ``Umfang`` 
  (Eigenschaft "Umfang")	

In einem *agla*-Notebook kann explizit mit anderen Python-Paketen gearbeitet 
werden, speziell mit SymPy, von dem einige Anweisungen dem System bereits 
bekannt sind. Soll ein weiteres SymPy-Element benutzt werden, z.B. die 
Funktion ``ceiling``, so ist dieses mit der üblichen import-Anweisung zu 
importieren und kann danach aufgerufen werden

.. code-block:: python
   	
   In [..]: from sympy import ceiling   # eventuell mit Pfadangabe im SymPy-
                                        # Baum
										
   In [..]: ceiling(3.12)    # das Ergebnis ist 4
   
Die Bezeichner für die Klassen werden oft auch im umgangssprachlichen Sinn 
benutzt, wenn dadurch keine Mißverständnisse entstehen

|


   