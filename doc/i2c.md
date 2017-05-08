# I2C

Pour les communction entre les différentes cartes du robot, nous avons choisi
d'utiliser de l'I2C, car c'est un protocole commun, efficace, nécéssitant un
minimum de connectiions et utilisable entre arduino et raspberry pi.

## Coté raspberry pi

A haut niveau, nous avons essayé de générer une couche d'abstraction I2C afin
de simplifier l'utilisation de celui-ci. Pour cela nous avons créé [i2c.py](https://github.com/Ecam-Eurobot-2017/main/blob/master/code/raspberrypi/i2c.py) qui s'occupe de rejoindre le bus, envoyé/recevoir des données à un certain
salve et compacter des données sous la forme de 8 ou 16 bits consécutif.
En important cette classe dansles autres codes, nous pouvons alors bénéficier
d'une simplification de toute la gestion de l'I2C.

Par exemple, dans le fichier [kinematics.py](https://github.com/Ecam-Eurobot-2017/main/blob/master/code/raspberrypi/kinematics.py), toutes les fonction de la ligne 32 à 54 utilise I2C.pack8 pour concatener deux
fois 4 bits et former un octet qui sera ensuite envoyé via la méthode send sur
le bus.  

Dans notre cas, nous avons utiliser se protocole pour communiquer avec trois
arduino uno : une pour les mouvements cinématiques, une pour les capteurs US et
une pour la commande des moteurs.

## Coté arduino

Pour la gestion de l'I2C du coté de l'arduino, nous avons utilisé la librairie
standard arduino Wire.h qui propose principalement : rejoindre un bus, envoyer
des données et lire des données qui nous sont adressées.

Premièrement rejoindre le bus via Wire.begin(slave_adress) en plus précisant son
adresse d'esclave, ensuite il faut definir la fonction qui se lancera lorque l'
on essaye de rentrer en contact avec elle via Wire.onReceive(function_name).

Puis nous pouvons lire des données en utilisant Wire.read() et les placer dans
une variable par exemple.

Pour plus d'informations, cfr [wire.h](https://www.arduino.cc/en/reference/wire) ou encore le code   [kinematics.ino](https://github.com/Ecam-Eurobot-2017/main/blob/master/code/arduino/kinematics/kinematics.ino) utilisant cette libraire en guise d'exemple.
