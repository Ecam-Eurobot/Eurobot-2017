# Elaboration des fonctionnalités.

======

## Actions à réaliser :

Dans le cahier des charges il y avait plusieurs actions possibles donnant chacune d’elles un nombre de points différents nécessaire à la victoire.

Possibilité de ramasser des plots monochrome ou polychrome et de les mettre dans des rails ou dans la zone de départ (le nombre de points en fonction de la zone change également).Pour les polychrome, il convient de les orienter de façon a masquer le coté n’étant pas notre couleur.

Possibilité de ramasser des balles et de les mettre dans un filet ou dans la zone de départ.
possibilité de lancer un projectile ressemblant a une fusée, après le temps réglementaire, cette action est considéré comme étant bonus.

Avant de commencer la conception il a fallu dresser un cahier des charges des actions qu’on veut réaliser pour notre robot.
Les autres actions doivent êtres assuré par un robot auxiliaire.

Les actions retenues étant la récolte de plots ainsi que la funny action.
Chaque fonctionnalité faisaient partie d’un bundle comprenant plusieurs actions a effectuer pour arriver au but escompté.

## Action bonus (funny action)
La funny action consistait simplement au lancement d’un projectile devant vaguement rappeler une fusée.

### Voici les contraintes:

	⋅⋅* Le robot doit lancer l’engin spatial à la verticale, après la fin du temps⋅⋅
	⋅⋅⋅ réglementaire dans un délai de 5 secondes.
	⋅⋅*  La masse de l’engin spatial ne devra pas excéder 50 g.  
	⋅⋅*  Durant le match, l’engin spatial ne doit pas dépasser des 350mm du robot.  
	⋅⋅* L’engin spatial devra, visiblement et de n’importe quel point de vue, se séparer du robot⋅⋅
	⋅⋅⋅ qui l’a lancé (environ 10 cm au-dessus du⋅⋅
 	⋅⋅⋅ point le plus haut du robot excepté le mat) et ne devra pas excéder 2 mètres de hauteur.
	⋅⋅* Une seule action de lancer sera comptabilisée par équipe.
	⋅⋅* Réussir cette action nous octroiera 20 points. 
### Le mécanisme de lancement se compose de plusieurs éléments :

	⋅⋅* Un tube, servant à abriter la fusée.
	⋅⋅* La fusée, qui est le projectile qui sera lancé et est le seul élément imprimé en⋅⋅
	⋅⋅⋅ 3D de ce bundle.
	⋅⋅* Un plateau accroché par des ressorts qui va fournir la poussée nécessaire à la⋅⋅
	⋅⋅⋅ fusée pour qu’elle décolle.
	⋅⋅* En position chargé, le plateau est attaché au fond par le biais d’un crochet qui⋅⋅
	⋅⋅⋅ sert de goupille.
	⋅⋅*	Un servomoteur servant à tirer ce crochet.
	⋅⋅* Un fente a été creusé afin de pouvoir inclure facilement le module qui est collé⋅⋅
	⋅⋅⋅ un étage en dessous.

### Cinématique :

*toute la partie programmation est expliqué dans la partie code.*

	⋅⋅* La première étape est de maintenir le plateau au fond avec les ressorts tendus.⋅⋅
	⋅⋅⋅ On doit, pour ce faire venir insérer le crochet dans les espaces prévus afin de⋅⋅
	⋅⋅⋅ retenir le plateau.⋅⋅
	⋅⋅⋅ Une fois chargé, on peut mettre la fusée.⋅⋅
	⋅⋅⋅ Une fois l’ordre donné, le servomoteur est actionné, tirant le crochet et⋅⋅
	⋅⋅⋅ désolidarisant le plateau de sa fixation, celui ci est violemment⋅⋅
	⋅⋅⋅ propulsé vers le haut , transférant l’énergie dans la fusée qui peut s’élever par⋅⋅
	⋅⋅⋅ effet d’inertie.

### Problèmes rencontrés :

	⋅⋅* Ce système est simple est efficace mais il comporte certains problèmes qui
	⋅⋅⋅ seraient bon de notifier.⋅⋅
	⋅⋅⋅ les deux fixations étaient collés aux parois du fond et  du plateau, par de⋅⋅
	⋅⋅⋅ l’autocollant double face et de la colle, avec la tension⋅⋅
	⋅⋅⋅ induite par les ressorts en mode tendu, avaient tendance à ce décoller.⋅⋅
	⋅⋅* *On pourrait visser pour assurer la cohésion et la résistance à la traction.*

	⋅⋅* Problèmes de déclenchement, parfois malgré l’action du servomoteur, il ne⋅⋅
	⋅⋅⋅ parvenait pas à dégoupiller le crochet,⋅⋅
	⋅⋅⋅ ne lançant donc pas la funny action.
	⋅⋅* *On pourrait mieux étalonner les longueurs, couper le crochet faisant la⋅⋅
	⋅⋅⋅ liaison.*

	⋅⋅* Le câble de déclenchement avait tendance à se dérober au crochet.
	⋅⋅* *Simplement mettre de la colle pour éviter de faire des fausses manœuvres.*

	⋅⋅* La mise en place du crochet lors du chargement était laborieux et devait se⋅⋅
	⋅⋅⋅ faire avec une pince à épiler.
	⋅⋅* *On pourrait simplement prévoir une ouverture plus grande tout en faisant⋅⋅
	⋅⋅⋅ attention à ne pas entraver  le bon fonctionnement du *déclenchement.*


## Ramassage de plots

*la seconde façon d’engranger des points était par le fait de ramasser et de replacer des plots.*

### Ce module doit réaliser plusieurs actions afin de marquer les points.
⋅⋅* La première étape est ramasser l’objet en tenant compte des obstacles.
⋅⋅* La seconde est de stocker plusieurs objets pour le transport.
⋅⋅* La troisième est la remise de ces objets dans une enceinte prévue a cet effet, dans⋅⋅
⋅⋅⋅ notre dans on doit les mettre entre deux tuteurs de façon aligné.

### Premier mécanisme : attraper et ramener les plots

#### Premières pistes :
Nos premières idées allaient vers un bras déployable faisant tomber et attirant les plots vers la base du robots, d’où ils seront récupérés et stockés.
Les avantages étaient la simplicité de la mise en œuvre, on a simplement à faire basculer les plots.

*Mais cette solution présentait deux défauts majeurs:*

	⋅⋅* La difficulté de stockage: il faut attirer les plots a la base de la structure et les⋅⋅
	⋅⋅⋅ faire basculer dans une enceinte prévue à cet effet,⋅⋅
 	⋅⋅⋅ ensuite, pour optimiser le stockage, il aurait fallu faire monter ces plots. On avait donc un nouveau défi⋅⋅ ⋅⋅⋅ technique mêlé à un facteur aléatoire assez grand lors de la bascule.

	⋅⋅* La disposition des plots dans les tubes "fusées" ne permettait pas au bras de⋅⋅
	⋅⋅⋅ récolter les plots, par manque de prise.

La deuxième piste consistait en un bras préhensile qui allait nous permettre de saisir les plots de façon efficace et de les lève, pour les introduire dans l’enceinte.

La constitution d’une telle pince relève plusieurs défis. La constitution devait être telle que le plot serait naturellement dirigé vers le stockage à l’ouverture.

	⋅⋅* S’assurer des contraintes mécaniques que va subi la pince.
	⋅⋅* Les espaces devront être bien calculés pour aisément prendre le plot.

###Deuxième mécanisme : constitution du réservoir, notre robot devait être capable de maintenir jusqu’à 4 plots :

Nous avons opté pour l’option la plus simple, il sera constitué d’une simple pente allant de la pince en haute à l’endroit de décharge.
Notre principal défi dans cette fonctionnalité est de bien réceptionner les plots et de bien les orienter jusqu’à l’endroit de décharge.

### Dernière fonctionnalité après le stockage : la remise des plots.

Avec l’étape précédente, ceux ci arrivent directement dans une position convenable.
Il suffit de s’assurer de la réception et de l’éjection des plots.

Nous avons opté pour un bélier venant pousser le plot le long de rails afin de les remettre en jeu à la façon d’une balle dans une culasse, sauf qu’ici on utilise simplement la gravité.

### Une fois déterminé, on passe a la conception des pièces.

La première étape est de dessiner les pièces en croquis et de s’assurer que toute l’équipe va dans le même sens.

*Par exemple pour la pince:*
![sketch arm ][assets/img1.PNG]

 **La nécessité de comparer les avis est essentiel, le dessin de pièces 3D et le refactoring de celles-ci est long et fastidieux**

## Modélisation

*Une fois  les pieces constituant le bundle approuvés on peut passer a l’étape de la modélisation a proprement parlé.*

Cette fois ci on doit déterminer les pièces qu’on devra imprimer en 3D, il ne faut pas en abuser et n’utiliser qu’exclusivement ce moyen, comme dit précédemment l’élaboration de celles-ci est longue et l’impression peut l’être d’autant plus.

###Le logiciel:

Tous les fichier 3D ont étés fait sous __Autocad Inventor__, une autre alternative serait __Solidworks__ qui est gratuit à des fins éducatives (voir les conditions sur leur site).

⋅⋅* Le logiciel est simple à prendre en mais souffre de défauts d’ergonomie.

La documentation officielle fournit beaucoup de ressources pour démarrer ainsi que cette playlist de vidéos qui a l’avantage d’être en français:
[Tutorial’s playlist](https://www.youtube.com/watch?v=Scc0uEEau3w).


###Pour le bundle de récupération des plots:

__L’ensemble des pièces de la pince:__

![sketch arm ][assets/rapport1.JPG]

Cette pièce à donc été conçue de façon a s’adapter aux mieux au contraintes exposés plus tot et a par la suite été imprimé en 3D .

⋅⋅* On a opté pour un étrier dans lequel viendra se fourrer la partie fixe de la pince.

⋅⋅* La pince est composé d’une partie fixe et d’un mord mobile qu’on viendra ⋅⋅
⋅⋅⋅ ouvrir et fermer à  l’aide d’un servomoteur, placé à la base de la pince⋅⋅
⋅⋅⋅ par soucis d’encombrement. La partie mobile s’ouvrira grâce à ce Serov ⋅⋅
⋅⋅⋅ et un système de tendons.La partie mobile est placé du côté  de la pente⋅⋅
⋅⋅⋅ pour libérer le plot du bon coté dans le stockage quand la pince montera.

__Le deuxième système est celui de stockage__ , celui-ci n’incluait pas de pièces imprimés.
Il s’agit simplement d’un réservoir faisant office de pente.
Le réservoir a été conçu avec du treillis de cage a poule, facilement modulable, et recouvert de carton pour que les plots puissent glisser.

__Le dernier système était la remise en place.__

⋅⋅* La base est constitué d’un socle avec deux rails ou vont naturellement tomber les plots.
⋅⋅* Dans ce support nous avons placé une saignée pour pouvoir faire coulisser la⋅⋅
⋅⋅⋅ tête du bélier, derrière la tête est accroché un système d’axe⋅⋅
⋅⋅⋅ permettant à un servomoteur de pousser la tête avec un plot devant tout en⋅⋅
⋅⋅⋅ économisant un maximum de place.

![sketch arm ][assets/rapport2.JPG]
![sketch arm ][assets/rapport3.JPG]


*Une fois tous les éléments en place il ne manque plus que l’impression de ces dernières.*

Lors du design il faut essayer au maximum de rendre la pièce modulaire pour pouvoir facilement l’adapter aux conditions réelles et pouvoir facilement cerner une solution en cas de problème imprévu.
L’idéal est de refactorer les pièces une fois que les tests en conditions réelles avec les prototypes sont validés.


## L’impression 3D à l’ECAM.

Il faut toujours faire attention au sens du filament extrudé, la pièce supportera différemment les efforts de traction selon l’orientation du filament.
Il faut toujours penser a remplir un minium la pièces, un "shell", vide donc supportera très mal les efforts et avec un remplissage minimal on transforme notre pièce en un matériau composite beaucoup plus tenace.

Pour certaines pièces ne nécessitant pas d’être adapté parfaitement a notre usage, qui doivent alors être dessinés par nos soins, il existe une pléiades de sites fournissant des modèles 3D gratuits.
C’est avec un modèle fournit qu’on a imprimé la fusée de la funny action.

![sketch arm ][assets/rapport4.JPG]

### L’ECAM possède deux imprimantes 3D:

------

### UP

C’est une petite imprimante pouvant réaliser toutes sortes de pièces ne dépassant pas 13 cm cube et ne nécessitant pas d’un état de surface optimal. Elle est rapide à l’impression.
⋅⋅* Problèmes: L’imprimante a des soucis au niveau de son plateau chauffant, ⋅⋅
⋅⋅⋅ce qui rend l’impression impossible à cause du retrait trop grand du plastique.
⋅⋅* La première solution est de remplacer la résistance chauffante qui est⋅⋅
⋅⋅⋅ défectueuse en démontant le plateau(attentions aux vis et aux ressorts).
⋅⋅* La deuxième solution est d’utiliser un plateau perforé nous permettant d’y⋅⋅
⋅⋅⋅ injecter les premières couches de plastique afin d’offrir une prise ⋅⋅
⋅⋅⋅ optimales et de supprimer cet effet de retrait du plastique.

__utilisatio:n__ elle est idéale pour des pièces en test ou ne nécessitant pas d’un bon état de surface.

Son logiciel "UP" propose une interface simple pour l’impressions mais manquant de réglages.

![sketch arm ][assets/img2.PNG]


⋅⋅* L’interface Nous propose d’importer des fichiers au format .STL.
⋅⋅* Nous pouvons influer dans les paramètres sur les conditions de remplissage de notre pièce et de son support.
⋅⋅* L’interface propose les transformations simples des pièces sélectionnés.
⋅⋅* Elle nous propose de positionner automatiquement de façon optimal les pièces.
⋅⋅* Attention, la mise à l’échelle ne fonctionne pas avec la version 2.1 du logiciel.

### Ultimaker 2+

Description :
⋅⋅* Elle est idéale pour faire de plus grandes pièces nécessitant des états de surfaces irréprochables.
⋅⋅* Elle est beaucoup plus lente que son homologue car son filament extrudé est beaucoup plus fin.
⋅⋅* Elle peut néanmoins tourner pendant la nuit sans soucis.
⋅⋅* L’imprimante n’est pas aussi potable que la up et est beaucoup plus volumineuse.

__Itilisation:__ elle est idéale pour des pièces volumineuse ou des petites pièces de précision. Nécessitant état de surface excellant.

Le logiciel associé est *"CURA"*, à la base propriétaire, il est maintenant open source et on peut l’utiliser sur des imprimantes "DIY" tel que la gamme des PRUSA.

![sketch arm ][assets/img3.PNG]

L’interface est facile et les réglages sont optimisés en fonction de l’imprimante utilisée.
⋅⋅* On peut choisir son imprimante parmi une liste déroulante.
⋅⋅* On peut aussi définir la densité de remplissage, cela affecte significativement le temps d’impression.
⋅⋅* Les opérations "primaires" sont sur la toolbar à gauche.

Une fois les réglages choisis il faut exporter le fichier crée sur une carte SD qu’on insérera dans l’imprimante.
