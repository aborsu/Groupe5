Groupe5
=======

Travail d'analyse syntaxique. Groupe 5

REJETE
  - Virer les règles de proba trop petites ( ça sert à rien et ça encombre).
        Pour chaque LH :
            calculer m = max( P(RH) )
            virer toutes les règles qui réécrivent LH avec une proba < m * un petit nombre.

DONE
  X Finir la binarisation
  X Débinariser
  X Mail aux groupes
  X Installer parseur
  X Train/test
      0 train.txt (découpage arboré)
      - test.txt (découpage arboré)
      - test_input.txt (découpage non arboré)
  X Lexiques externes
  X Donner liste composés au groupe 3
    cat ftb6_2.mrg |grep -o -P "[^(^)]+ [^)^(]+"|grep -P "_"|tr " " "\t"|awk '{print $2 "\t" $1}' > composes.txt
  X Demander au groupe 1 des précisions
  X Division en fichiers
  X Optimisation/relecture code
  X Modifs sur le lexique: Sarah Done
  X Brancher avec parseur:
    X Réparer l'export
    X Mail Sagot
    X Commandes:
      -m nf
      -n 1 -pnt -string

  TODO :
  - Insérer la commande dans le main de extraction.
  - Tester avec les autres.

INFOS GROUPES
  GROUPE 1
    - _NUM
    - _DATE
    - _URL
  GROUPE 2
    - liste de catégories :
       ADJ
       ADV
       NC
       V
       VINF
       VPP

    - output : {truc}__cat/score
       avec : cat = catégorie prédite, score = score de confiance (surtout utile pour le groupe 3)
       exemple : {publicité}publicité__NC/70

    - infos morphologiques associées : aucune :-)

  GROUPE 3
      1. pour l'output : les accolades sont utilisées quand quelque chose a été modifié, pour nous ça peut être :
      - {au bout de}au_bout_de      (pas d'espace entre } et le mot)
      - {au}à {}le 
      - {au bord du}au_bord_de {}le      (les accolades vides {} réfèrent au dernier token)
      - {quatre-vingt dix}_NUM      (un seul underscore)      /!\ ça on doit se confirmer avec Slimane, voir ce qu'il fait avec les vrais chiffres genre 878.

      2. la ponctuation pour nous c'est un mot du lexique comme un autre, c'est pas inconnu donc on laisse passer tel quel.
      3. Etiquettent _NUM également les nombres simples en toute lettre: "deux", mais pas "un"

  GROUPE 4
    - si mot inconnu : {}forme__CAT ils auront viré un /score
    - {token_original}_TYPE, avec types in [ORG,PERS,GEO]
    - Ils nous fournissent leur lexique d'entités nommées pour modifier le ftb
