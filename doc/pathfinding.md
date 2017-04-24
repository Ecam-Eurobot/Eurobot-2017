# PathFinding

## Solutions possibles

[Plusieurs solutions](http://theory.stanford.edu/%7Eamitp/GameProgramming/MapRepresentations.html#navigation-meshes)
sont possibles pour implémenter un pathfinding. Ayant une régulation seulement en position, le
*navigation mesh* m'a paru la solution la plus adapté à notre cas (moins couteux en mémoire/calcul
qu'une grille de cases).

## Navigation mesh

Le navigation mesh consiste en deux étapes:

- La création d'un mesh (suite d'arêtes et de sommets) représentant le terrain disponible pour le
  robot
- La convertion du mesh en un graphe pour appliquer l'algorithme de recherche (dijkstra, A\*, ...)

### Creation du mesh

Notre programme principal étant programmé en Python, nous devions trouver des librairies
compatibles. Plusieurs libraires ont été considérées:

- [PyMesh](https://pymesh.readthedocs.io/en/latest/)
    - Aucune API pour créer un mesh facilement
- [MeshPy](https://documen.tician.de/meshpy/)
    - Segfault lors de la création de mesh plus compliqués
- [The fenics projects tools](https://fenicsproject.org/)
    - Constitué de plusieurs outils pour la création de mesh
        - Dolfin permet de créer des meshes.
        - Mshr permet de créer facilement des meshs Dolfin.
    - *Pain in the ass* installation
    - Relativement bonne performance sur un ordinateur normal (5-10 min pour la création de meshs
      (parfois moins)(possibilité d'ajouter de la cache)) par contre inutilisable sur la raspberrypi
      (3h de création de mesh!).

Pour des raisons évidente, nous sommes partis sur la solution Dolfin+Mshr. Pour simplifier le
developpement, je conseille d'activer VTK par defaut pour visualiser le mesh créer. Une bonne source
pour les scripts de compilation sont les PKGBUILDs des AUR packages d'ArchLinux genre
[celui-ci](https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=python-dolfin-git).

### Création du graphe

## Autres solutions

- *Potential field* pourrait être très bon système de pathfinding si une régulation en vitesse était
  implémenter.
