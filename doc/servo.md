# Gestion des servo moteurs

Pour le projet nous avons utilisé différents servos moteurs :

* SG-90
* Dynamixel AX12

Les grosses différences sont : Le couple qu'ils peuvent fournir, la
communication à mettre en place pour les controler et éventuellement l'angle qu'
ils peuvent couvrir.

## SG-90

Ceux-ci sont très facile à utiliser, ils sont composés de 3 pinnes : 5v, GND et
CTRL. Pour les commander, il suffit d'utiliser, via l'arduino, la libraire stan-
dard arduino servo.h, d'attacher un servo à une pinne via myservo.attach(pinne)
et de lui donner une commande d'angle via servo.write(angle).

## Dynamixel AX12

Les Dynamixel eux sont plus complexe. Il faut utiliser la librairie arduino
custom disponible dans le dossier [librairies](https://github.com/Ecam-Eurobot-2017/main/tree/master/code/arduino/librairies/DynamixelSerial).
Avant utilisation, il faut le brancher à son controlleur qui l'allimente en 9v5 (cfr
rapport partie hardware Riga Lorenzo) qui sera connecté à l'arduino via la ctrl
pinne et tx/rx.

### caractéristique

* Poids : 54,6g
* Dimension : 32mm * 50mm * 40mm
* Angle autorisé : 0 à 300°
* Résolution : 0.29°
* Tension alimentation : 9 ~ 12V
* Type Protocole : Half duplex Asynchronous Serial Communication (8bit,1stop,No Parity)
* ID : de 0 à 253 identifiant possible
* Lecture possible : T°, tension, position..

Ensuite, il faudra utiliser la fonction Dynamixel.begin(baude_rate, ctrl_pin)
proposé par la libraire (Dans notre cas le baude rate était de 1M). Notons que
les dynamixels peuvent être plusieurs connecté en daisy chain l'un à la suite de
l'autre, il faudra donc leur attribué chacun une adresse dans le code (adresse
fixée en hardware). Pour ensuite lui envoyé une consigne de position, il faudra
utilisr dynamixel.move(dynamixel_adress, angle) où l'angle est un chiffre en 0
et 1024.

Evidemment bien d'autre fonction sont disponible tels que :
* Mesurer la température
* Allumer/éteindre sa led
* Se deplacer en imposant un vitesse
* ...

Mais elles ne sont pas forcément utiles.  

Pour plus de détails, aller voir dans le code se trouvant dans :
[kinematics.ino](https://github.com/Ecam-Eurobot-2017/main/blob/master/code/arduino/kinematics/kinematics.ino)

Vous pouvouez toujours allez voir [ici](http://www.pishrobot.com/files/products/datasheets/dynamixel_ax-12a.pdf) pour toute informations complémentaires  
