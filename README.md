
## <i>agla</i> und <i>zufall</i>  
### Zwei Open Source Python-Pakete für die Schule

Die Pakete 

* <b><i>agla</i></b> für das Fachgebiet <b>Analytische Geometrie</b>
* <b><i>zufall</i></b> für das Fachgebiet <b>Stochastik</b>

sind für den Gebrauch durch Lehrer und Schüler im Rahmen der schulischen 
Ausbildung vorgesehen. Sie können sowohl im Unterricht als auch zum 
selbständigen Lernen benutzt werden.

Sie sind durch die Übertragung der MuPAD-Pakete gleichen Namens in die 
Programmiersprache <b>Python</b> enststanden und inhaltlich mit diesen 
im wesentlichen identisch.

Beide Pakete basieren auf dem ebenfalls in Python geschriebenen und 
quelloffen frei verfügbaren <b>CAS SymPy</b>. Für die geometrischen Objekte 
(Vektor/Punkt, Gerade, Ebene, ...) bzw. die Objekte der Stochasik 
(Zufallsexperiment, Zufallsgröße, Datenreihe, ...)  werden Python-Klassen
im Sinne der Objekt-Orientierten-Programmierung bereitgestellt. Damit
können entsprechende Python-Objekte erzeugt werden, mit denen unter 
Verwendung ihrer Eigenschaften und Methoden am Computer gearbeitet wird.

Die Berechnungen werden in einem <b>Jupyter-Notebook</b> (mit englischer
Bedienoberfläche) durchgeführt.

### Einblicke 
in die Arbeit mit den Paketen

<a href="https://hbomat.github.io/AglaUndZufall/agla/demo/html/index.html">agla</a>

<a href="https://hbomat.github.io/AglaUndZufall/zufall/demo/html/index.html">zufall</a>

### Bearbeitungsstand

Die Entwicklung erfolgte durch Holger Böttcher hbomat@posteo.de für
Windows 10 unter Verwendung des Chrome-Browsers. Es liegen 
anwendungsbereite Versionen der beiden Pakete vor.

Gegenwärtig sind die Programme auf die Benutzung der Anaconda-Version
4.2.0 (Python 3.5.2, IPython 5.1.0) eingeschränkt. Am Einsatz höherer 
Versionen wird gearbeitet.

Der Test für Linux und macOS steht noch aus.

### Installation und Einrichten der Arbeit

Für die Benutzung auf einem lokalen Computer wird zunächst die aktuelle 
Version der Pakete heruntergeladen.

Dazu wird auf der Web-Adresse

    https://github.com/hbomat/AglaUndZufall

mit der grünen Schaltfläche rechts oben

    Clone or Download -> Download ZIP

ein ZIP-Archiv geladen, das in einen geeigneten Ordner zu entpacken ist.

Dann sind Python und weitere benötigte Python-Pakete zu laden sowie 
die Arbeit einzurichten. Beide Schritte sind in der Datei 
<b>agla/org/installation_windows</b> beschrieben.

### Fehler und Hinweise

Wenn du auf Fehler oder Unzulänglichkeiten (auch kleine) stößt oder Fragen
hast, wende dich bitte an Holger Böttcher hbomat@posteo.de.

### Mitarbeit am Projekt 

Wenn du aktiv an der Weiterentwicklung mitwirken und z.B. Programm-Code 
einbringen oder die Dokumentation verbessern willst - du bist herzlich 
willkommen. 

Diese Aufforderung richtet sich insbesondere an Python-Kenner, die 
auch dabei mithelfen können, die Quelltexte noch pythonischer zu gestalten.

Mit der grünen Schaltfläche 

    Clone or Download -> Open in Desktop  

		(dazu muss das Programm GitHUB Desktop vorhanden sein)     

oder von der Konsole

    $ git clone https://github.com/hbomat/AglaUndZufall.git 

kannst du eine vollständige Kopie dieses Git-Repository auf deinen Computer
ziehen, wo du dann unter Nutzung von Git an den Paketen arbeiten kannst. 


