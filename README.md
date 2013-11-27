Groupe5
=======

Travail d'analyse syntaxique. Groupe 5

Contributeurs :

  Augustin
  Sarah
  Maximin


Ont cloné :
  Sarah
  Augustin

Idee:
    Virer les règles de proba trop petites ( ça sert à rien et ça encombre).
    
    Pour chaque LH :
        calculer m = max( P(RH) )
        virer toutes les règles qui réécrivent LH avec une proba < m * un petit nombre.

TODO
  - composés
    de le
  - Finir la binarisation
  - Suppression des règles inutiles
  - Faire le tour des groupes, définir le format de tout et modifier dans ftb.  
      quelles CAT ? mapping eux : ftb
      remplacement des entités nommées.
      eventuellement fournir aux autres groupes un fichier texte ftb, être capable d'en refaire un fichier arboré d'origine.
      -G1: tokenisation
      -G2: Analyse morpho des inconnus
      -G3: Identification des formes, correction ortho
      -G4: Entités nommées.
  - Brancher avec le parseur
  - Faire un lecteur de texte au format du groupe 4 qui réécrit les infos après.

   {....1}token1 {....2}token2

   parse: token1 token2

   resultat: (token1 (token2))

   remet: ({...}token ({...}token))

  - stade plus avancé :
   
   {....1}token1 {....2}token2

   parse: token1_cat token2_cat

   lexique non-ambigu:
      token1_catx : catx : proba

   resultat: (token1 (token2))

   remet: ({...}token ({...}token))
