
Jupyter-Notebook
================

|

.. note::

   Um in einem Notebook mit *zufall* arbeiten zu können, muss zu Beginn 
   der Sitzung die (Jupyter-) Anweisung

   .. code-block:: python

      In [..]: %run zufall/start
   
   in einer Codezelle ausgeführt werden

|
   
*zufall* benutzt als Bedienoberfläche **Jupyter**. Dieses wurde unter dem Namen
**IPython** ursprünglich als Entwicklungsumgebung für Python-Anwendungen 
bereitgestellt, unterstützt aber inzwischen eine Vielzahl weiterer 
Programmiersprachen. Der Name setzt sich aus den Namen von drei Sprachen
zusammen - **Julia** (eine Sprache, die sehr schnellen Code erzeugt), 
**Python** und **R** (inzwischen ein leistungsfähiges Statistikpaket)

Ausschlaggebend für die Wahl dieser Plattform war das hier realisierte 
Notebook-Konzept, wie es auch in kommerziellen CAS (z.B. Mathematica) 
Verwendung findet

Die Oberfläche ist in englischer Sprache verfasst, erfordert also das
Verständnis beim Lesen

Jupyter läuft als lokale Anwendung auf dem Standardbrowser des Computers, Kern
(*kernel* ) ist der Python-Interpreter

Ein Jupyer-Notebook ist in Zellen (*cells*) unterteilt, wobei drei Zelltypen 
auftreten, die hier interessieren:

- **Code**-Zellen
     | Kennzeichnung: ``In [..]`` 
	 
     | In diese Zellen werden Anweisungen in der benutzten Programmiersprache 
      (hier Python) geschrieben, also auch Anweisungen zur Benutzung von  
      *zufall*; die Zellen sind analog zu einem Texteditor editierbar; beim  
      Ausführen (*run*) einer solchen Zelle wird ihr Inhalt an den 
      Python-Interpreter übergeben, der für seine Verarbeitung sorgt
	  
     | Eine neue Zelle wird standardmäßig als Code-Zelle erzeugt; die 
      Umwandlung einer Markdown-Zelle in eine Code-Zelle ist über das 
      ``Code``-Menü oder die Platzierung des Cursors im vorderen Zellbereich  
      und Drücken der ``Y``-Taste erreichbar
	  
- **Ausgabe**-Zellen
     | Kennzeichnung: ``Out [..]``
	 
     | Die Zellen entstehen, wenn nach der Auswertung einer Codezelle durch  
      den Python-Interpreter eine Ausgabe erforderlich ist; in diese Zellen 
      kann vom Benutzer nicht direkt geschrieben werden	 
	 
- **Markdown**-Zellen	 
     | Ohne Kennzeichnung
	 
     | Die Zellen dienen vor allem zur Aufnahme von Texten, wobei diese mit 
      Markdown- (eine einfache Auszeichnungssprache) oder HTML-Anweisungen  
      formatiert werden können; sie können auch mathematische Formeln 
      enthalten (Nutzung von :math:`\LaTeX`), außerdem können in solchen 
      Zellen Grafiken und Bilder dargestellt sowie Audio- und  
      Video-Dateien aktiv sein; beim Ausführen einer solchen Zelle werden  
      eventuell vorhandene Formatierungs-Anweisungen ausgeführt und der  
	  Inhalt auf dem Ausgabemedium präsentiert

     | Die Umwandlung einer Code-Zelle in eine Markdown-Zelle ist über das 
       entsprechende Menü oder die Platzierung des Cursors im vorderen 
       Zellbereich und Drücken der ``M``-Taste erreichbar 
	  
Code- und Markdown-Zellen können beliebig erzeugt, gelöscht, kopiert, 
eingefügt und verschoben werden	 

Es kann zu jeder dieser Zellen gesprungen werden, um sie zu verändern 
und/oder (erneut) auszuführen 

In einem Notebook kann in zwei Modi gearbeitet werden

- **Editier**-Modus
     | Einschalten mit ``Enter``; oben rechts ist ein Stift dargestellt 
	 
     | in diesem Modus kann der Inhalt der aktuellen Zelle editiert werden 

     | das Editieren einer vorhandenen Markdown-Zelle kann auch mit einem
       Doppel-Klick eingeleitet werden
	   
- **Kommando**-Modus
     | Einschalten mit ``ESC``; der Stift rechts oben fehlt
	 
     | in diesem Modus können Aktionen durchgeführt werden, die das Notebook  
       als Ganzes betreffen (Zellen erzeugen, kopieren, löschen, verschieben,   
       zwischen ihnen navigieren, Dateien öffnen und speichern usw.)

Wenn der Kern beschäftigt ist, ist der schwarze Kreis rechts oben gefüllt;  
auch in dieser Zeit kann editiert werden, die Ausführung weiterer Zellen
kann aber erst erfolgen, wenn der Kern wieder frei ist 

Eine Datei, in die der Inhalt eines Notebooks gespeichert wird, erhält die 
Endung ``.ipynb``

Für den Export eines Notebooks, z.B. in das ``.html``- oder ``.pdf``-Format, 
ist das separat zu nutzende Werkzeug **nbconvert** vorgesehen
  
|

Die Bedienung eines Notebooks kann über das Menü und/oder über die Tastatur 
erfolgen
  
Einige Tastatur-Kürzel zur Arbeit mit einem Jupyter-Notebook:

+-----------------------+------------------------------------------+
| Kürzel                | Bedeutung                                |                                      
+=======================+==========================================+
| ``Umsch+Enter``       | Zelle ausführen, zur nächsten gehen      |
|                       | (diese wird eventuell neu angefügt)      |            
+-----------------------+------------------------------------------+
| ``Strg+Enter``        | Zelle ausführen, in der Zelle verbleiben |            
+-----------------------+------------------------------------------+
| ``Strg+M B``          | Zelle unterhalb einfügen                 |            
+-----------------------+------------------------------------------+
| ``Strg+M A``          | Zelle oberhalb einfügen                  |            
+-----------------------+------------------------------------------+
| ``Strg+M DD``         | Zelle löschen (``D`` 2-mal drücken)      |            
+-----------------------+------------------------------------------+
| ``Esc X``             | Zelle löschen                            |            
+-----------------------+------------------------------------------+
| ``Strg+Z``            | Zurücksetzen beim Editieren              |            
+-----------------------+------------------------------------------+
| ``Esc``               | Einschalten des Kommando-Modus           |            
+-----------------------+------------------------------------------+
| ``Enter``             | Einschalten des Editier-Modus            |            
+-----------------------+------------------------------------------+
| ``Strg+M H``          | Anzeigen aller Tastatur-Kürzel           |            
+-----------------------+------------------------------------------+

Ausführen:  (z.B. ``Strg-M B``)

``Strg``-Taste drücken, dann ``M``-Taste, ``Strg`` loslassen, dann ``B``-
Taste
	
Durch mehrmaliges Drücken der ``B``-Taste können mehrere Zellen eingefügt
werden	
 
|
