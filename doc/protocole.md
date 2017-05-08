# Protocoles utilisé pour la communction

Pour communiquer en i2c entre nos différents carte, il faut que la raspberry pi
sache quoi envoyer (et à qui) pour effectuer une certain action, ou dans l'autre
sens, lorqu'une arduino recoit de l'information via le bus, que doit-elle en faire ?

Nous avons alors du définir un protocole (API) pour définir un sens à l'information
pour chaqu'une de nos cartes arduinoo à savoir, celle qui s'occupe :

* de la cinémtique via les servos moteurs
* des capteurs ultrasons
* de l'avance du robot via les moteurs

Et vous trouverez le détail de chacun de ceux-ci dans la suite de ce document.

## Cinématique et commande des servos moteurs

### Cahier de charge

* Envoyer à quel servo veut-on parler
* Envoyer une action pour ce servo (open/close - up/down)

Nous avons alors besoin de 2 bits pour définir à qui l'on parle (car 4 servo au
total). Prenons 4 bits pour être sûre.
Nous avons également besoin d'1 bit pour envoyer l'action shouaitée (position
initial/repos => 0 ou action => 1). Prenons 4 bits pour faire un total de 8.

Donc AAAA XXXX, où A définit le servo auquel on parle, et X l'action à réaliser.

### Utilistaion pour chaque servo

#### Pince
Servo se trouvant sur la pince, destiné à l'ouvrir et la fermer.

* A : 0
* X : 0 pour ouvert, 1 pour fermé

#### Dynamixel
Servo destiné à monter et redescendre la pince.

* A : 1
* X : 0 pour horizontal, 1 pour vertial

#### Belier
Servo destiné à pousser les module hors du chargeur.

* A : 2
* X : 0 pour la position arrière, 1 pour sortir le bélier

#### Funny action
Servo destiné à tirer un ficelle relachant la funny action bloquée par un ressort.

* A : 3
* X : 0 pour relacher la ficelle, 1 pour la tirer

Chacune de ses commande sera donc envoyée en I2C par la raspberry pi vers l'
arduino servo, afin d'effectuer l'action voulue sur le servo adéquat.

L'octet recu sera stocké dans deux variables via la lecture I2C de la part de l'
arduino, ensuite un swtich case effectura le choix du servo et de l'action via
un if else.

Il pourrait être interresant d'ajouter dans le swtich case un "default" qui s'
occuperait de renvoyer, en I2C, à la raspberry pi, un message particulier qui
aurrait pour objetif de lui préciser qu'elle ne comprend pas ce qu'elle a recu.
(En cas d'interférence I2C par exemple, mais nous n'en avons pas eu besoin)

Pour plus d'info sur l'utilisation en elle même, voir [kinematics.ino](https://github.com/Ecam-Eurobot-2017/main/tree/master/code/arduino/kinematics).

## Capteurs ultrasons

### Cahier de charge

* Demander la mesure de tout les capteurs en une fois
* Demander la mesure d'un capteur spécifique
* Si le capteur demandé n'existe pas, renvoyer une séquence d'erreur que la Raspberry peut comprendre
* Demander d'énumérer les capteurs qui existent

La raspberry pi enverra alors un byte de deux parties codées sur 4 bits :
* La commande
* L'index du capteur (si applicable)

### Commande utilisées

#### Commande de la raspberry pi

* 0001 xxxx        demander la mesure du capteur `xxxx`
* 0010 0000        demander la mesure de tous les capteurs
* 0011 0000        demander d'énumérer tous les capteurs
* 0100 0000        demander le nombre de capteurs présents

#### Réponse de l'Arduino

* Une distance en cm (int 16 bits). On sépare le int en 2 bytes pour l'envoyer par I2C et puis on le reassemble sur la Pi. Si une erreur survient (e.g. le capteur n’existe pas) on renvoie 0.
* n-fois 2 bytes (une fois par capteur)
* n-fois 1 byte avec l'indice du capteur. On pourrait coder 2 capteurs par byte, mais alors il faut gérer le cas d'un nombre impaire de capteurs.
* un byte contenant le nombre n de capteurs présent sur l'Arduino, ceci permet de savoir combien de bytes seront envoyés quand on demande les mesures de tous les capteurs

Pour plus d'info sur l'utilisation en elle même, voir [us_sensor.ino](https://github.com/Ecam-Eurobot-2017/main/tree/master/code/arduino/us_sensors)

## Moteurs

### Cahier de charge

* Tourner à gauche de X degrés
* Tourner à droite de X degrés
* Avancer de X cm
* Reculer de X cm
* Arreter les moteurs
* Contrôle vitesse
* Demander le déplacement déjà effectuer
* Demander si action finie ou pas
* Demander si l'action est stoppée
* Redémarrer l'action stoppée

Dans cette parite, nous avons utilisé un "enum" qui est constitué de chaqu'une
des actions possible. Chaque valeur I2C reçu sera remplacer par sa position dans
l'enum.
Ensuite nous recevons la "data" qui elle sera directement la valeur chiffrée
shouhaitée (par exemple x centimètre pour l'avance ou encore degrès pour la
rotation).

Pour plus d'info sur l'utilisation en elle même, voir [motors.ino](https://github.com/Ecam-Eurobot-2017/main/blob/master/code/arduino/motors/motors.ino)
