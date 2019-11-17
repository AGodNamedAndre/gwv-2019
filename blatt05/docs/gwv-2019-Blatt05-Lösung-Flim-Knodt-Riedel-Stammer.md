# GWV – Übungsgruppe Mo. 14 Uhr

Teilnehmer: **Tobias Flim, Sven Knodt, André Riedel,** **Johannes Stammer**

Abgabe: So., 17.11.2019



> 1. **Implement** the heuristic search strategy "A*" to find a path for the robot. Make sure you choose a suitable heuristic function (disregarding portals for now!) and **motivate** your choice.



Die Implementierung findet sich im Modul *a_star.py*, die interessanten Methoden sind `find_path_rec(..)` und `find_next_step(..)`. Die Implementierung ist in Initialisierung und schrittweise Verarbeitung aufgeteilt, um einfacher Zwischenstände zu speichern und zu debuggen, ohne Algorithmus und Statistik im Code zu vermischen.

Als Heuristik haben wir die Manhattan-Distanz zugrunde gelegt, da sich deren Ergebnisse so verhalten, als wenn zwischen aktuellem Knoten und Ziel keine Hindernisse liegen bzw. keine Umwege genommen werden müssen, was ohne Portale den tatsächlich minimalen Weg beschreibt.



> 2. Write a second heuristic function that works correctly with portals. What do you have to change?

Damit eine Heuristik-Funktion weiterhin korrekt, trotz der Abkürzungen durch Portale funktioniert, muss sie weiterhin unterschätzend bleiben um das Konsistenz-Kriterium zu wahren (damit die erste gefundenen Lösung zwingend optimal ist).

Neben trivialen Lösungen im Sinne von h(x):=1, gibt es die Möglichkeit die möglichen durch Portale eingesparten Kosten von der bisherigen Heuristik abzuziehen. Dies ist aber nicht besonders sinnvoll, da sonst, im Radius von der Summe der Portalreichweiten um das Ziel herum, effektiv nur eine Breitensuche passieren würde. Auch kann die Summe der Einsparungen an Weg durch Portale recht hoch sein.

Der von uns verfolgte Ansatz ist, von den Zielen ausgehend die minimalen Pfade zu allen Portalen zu finden und somit $$\{ cost(G, p_i) \}$$ in einer Vorbereitung der Heuristik zu berechnen. Die von uns angestrebte Heuristik ist dann (bitte die leichten Fehler in der Definition ignorieren, $$cost(G, g_i) = 0$$ müssen noch mit hinein):

 $$h(x):= min(\{ manhatten(x, n) + cost(G,n) | n \in G \cup P \})$$



> 3. The maze above is a slightly modied version of the environment. How does your search react in this case? Can you ensure termination?

Wir haben keine Möglichkeit zu erkennen, dass es keinen validen Weg zur Lösung gibt, außer durch testen aller möglichen Pfade. Früher oder später terminiert unsere Suche auch hier, aber erst, wenn alle begehbaren Koordinaten besucht wurden.

Terminiert wird dann weil die Frontier leer ist und als Lösung wird `None` zurückgegeben.



> 4. For each of the search strategies used so far document the time and memory resources used by the algorithm in terms of expansion operations performed on the frontier of the search and the maximal number of nodes in the frontier.

Tiefensuche:

Breitensuche:

A*-Suche:




> 5. Extend your program so that it can find all paths to the goal.

Hierfür muss lediglich die Abbruchbedingung geändert werden, so dass statt dem returnen einer Lösung, diese in einer Liste gespeichert wird und bei genügend vielen Lösungen (oder per default bei leerer Frontier), der Algorithmus terminiert.



> 6. Extend your program so that it can cope with multiple goals, finding the shortest path to one of them using A*.

Im `environment.py` werden beim Einlesen bereits alle Start- und Endpunkte eingelesen, so dass der Test auf eine Lösung (`env.check_goal`) sich bereits auf eine Menge von Endpunkten bezieht.

Die zweite Anpassung ist, dass die Heuristik auf das Minimum aller Manhattan-Distanzen zu den Zielpunkten erweitert wird.