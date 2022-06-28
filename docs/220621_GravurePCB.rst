Fabrication d’un PCB
====================

1/ Matériel et outils nécessaires
---------------------------------

1.1. Matériel
~~~~~~~~~~~~~

-  Une plaque cuivré mono-couche de 80mm*95mm.
-  Acide chlorydrique 23% (Magasin de bricolage)
-  Eau oxygénée (10 ou 30 volumes)
-  Papier de publicité (glacé)
-  Alcool à 90°
-  Dissolvant de maquillage
-  Acétone

1.2. Outils
~~~~~~~~~~~

-  Imprimante papier laser
-  Bac en plastique de récupération (ex : boite de glace)
-  Gants jetables
-  Scie à métaux ou dremel
-  Paire de ciseaux

2/ Gravure
----------

2.1. Impression
~~~~~~~~~~~~~~~

-  Imprimer le PCB sur du papier glacé de type publicité avec
   l’imprimante laser.
-  Découper les contours de l’empreinte.

2.2. Transfert des pistes sur la plaque de cuivre
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Poncer la plaque cuivré à l’aide d’un papier de verre très fin
   (1000).
-  Nettoyer la surface cuivré à l’aide d’alcool. Nettoyer jusqu’à ce
   qu’il n’y ai plus de traces sur l’essuie tout.
-  Découper l’empreinte du PCB au ciseaux
-  Dans le bac, verser du dissolvant à la surface de la plaque cuivré.
   Bien répartir ce dernier afin qu’il prenne tout l’espace de la
   plaque.
-  Sans attendre, déposer le papier glacé avec l’ancre imprimé face au
   cuivre.
-  Tamponner à l’aide d’un papier essuie tout.
-  Laisser sécher la plaque une quinzaine d eminutes de manière à ce que
   le papier ne soit plus du tout humide
-  Une fois le papier totalement sec, très délicatement passer la plaque
   sous le robinet d’eau froide. Avec les doigts frotter de manière à
   dissoudre le papier. Seule les pistes doivent rester sur la plaque de
   cuivre.

.. _gravure-1:

2.3. Gravure
~~~~~~~~~~~~

-  Préparer une solution dont le volume permettra de recouvrir la
   plaque. Les concentrations sont 66% d’eau, 3,3% d’eau oxygénée et 30%
   d’acide chlorhydrique.
-  Plonger la plaque dans la solution.
-  Laisser agir au moins une heure. Le cuivre apparent doit laisser
   place au support de couleur souvent jaune ou verte. Attention à ne
   pas laisser trop longtemps au risque que l’acide attaque les pistes).
-  Après gravure, rincer le circuit à l’eau.
-  Enfin effacer l’encre à l’aide d’un papier essuie tout imbibé
   d’acétone.

3/ Perçage du PCB et soudure
----------------------------

-  A l’aide d’une dremel sur colonne ou d’une dremel à la main percer
   les trous du circuit imprimé avec un foret de 0,8mm.
-  Élargir les trous dans lesquelles on soudera des pins duponts males
   (Encadrés en vert cf. visuels ci dessous) à l’aide d’un foret de
   0,9mm ou 1mm.
-  A ces mêmes emplacements, souder des broches duponts mâles.
   /! Attention on soude les composants de manière a ce qu’il soit sur
   la face opposé au circuit. Seule les pattes traverssent et sont
   soudés du coté du circuit. (PCB_step3-1.png)
-  Souder 2 résistances de 220ohm et 6 résistances de 1Kohm (cf. photo
   ci dessous, 220ohm en bleu et 1kohm en orange). (PCB_step3-2.png)
-  Souder les deux diodes en veillant à respecter la polarité. Sur une
   diode le plus est matérialisé par la patte la plus longue. (Une LED
   rouge et une LED verte cf.photo ci dessous) (PCB_step3-3.png).
-  Souder 4 fils qui servirons de pont (en vert cf. dessin ci dessous).
   (PCB_step3-4.png)
-  Souder sur les broches duponts, dans le sens indiqué les 3 modules
   RTC (Horloge), l’indicateur de niveau de batterie et le relai.
   (PCB_step3-5.png)
-  Souder 3 ILS sur les emplacements indiqués (en orange cf. dessin ci
   dessous). (PCB_step3-6.png)

Liens connexes
--------------

-  Préparation de la solution de gravure :
   https://arlontronique.wordpress.com/menu/graver-ses-propres-circuits-imprimes/
-  Transfert des pistes sur le cuivre : https://youtu.be/8joLK039fjk
