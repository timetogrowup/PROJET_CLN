# Recette — animation pédagogique pipeline V8
29 octobre 2026. Statut : livré et vérifié en production.

## Livraison
La section #bout-en-bout de Vos besoins est déplacée après l'introduction, avant les quatre besoins. Animation muette 15 s en boucle, vague bleu-gris, cadre et titre scintillants, contours des cadres renforcés ×5. Versions françaises, anglaises, portugaises brésiliennes et espagnoles : 37 chaînes de l'illustration traduites, mêmes trajectoires et durées. Huit vidéos (WebM et MP4) et quatre posters de synthèse, tous inférieurs à 1 Mo par fichier. Scripts de rendu et traductions versionnés.

Pause/reprise traduite ; changement de langue sans rechargement, conservation de la pause et du temps même sur plusieurs changements successifs ; chargement conditionné à la visibilité. Vue agrandie fixe dans la langue choisie, défilement interne, fermeture et retour du focus. Transcription textuelle traduite disponible dans un accordéon. Poster par défaut sans JS et en mode réduction des animations. Le repli sans JS est français, langue HTML initiale.

## Vérifications
- Syntaxe pipeline-animation.js et tests du lecteur : réussis.
- tests/pipeline_static.py : placement unique, chargement différé, transcription, douze médias, huit codecs/durées de 15 secondes et 37 chaînes traduites : réussis.
- Posters des quatre langues inspectés visuellement : textes dans les cadres et résultats lisibles. WebM : environ 461–478 Ko ; MP4 : 849–873 Ko ; posters : 56–61 Ko.
- Contrôles statiques V6/V7 : dix pages, 200 références/ancres, métadonnées et couverture complète des traductions réussis.
- Catalogue : 531 entrées statiques, 140 dynamiques, quatre langues et variables complètes.
- Deux générations consécutives : HTML et catalogues inchangés (idempotence).
- Tests unitaires du lecteur : sources dans la langue choisie, pause et position conservées lors de changements successifs, aucun chargement vidéo initial si réduction du mouvement, dialogue/focus et visibilité réussis. Ces tests simulent le DOM, sans prétendre émuler un navigateur.
- Aperçu Chrome : lecture française ; agrandissement, suspension pendant la vue agrandie, fermeture Échap et retour du focus réussis. Passage en anglais pendant une pause : poster anglais, lecteur toujours arrêté, puis reprise de la bonne vidéo anglaise. Aucun débordement horizontal à la largeur de l'aperçu.

- Lecture WebM FR/EN/PT-BR/ES dans Chrome : langue de la source et du poster correspondante, aucune erreur de débordement à la largeur contrôlée. Fermeture par bouton et Échap testées.

## Limites
Pas de recette sur téléphones physiques ni Safari dans cette session. Le mode sans JS et le réglage système de réduction du mouvement sont contrôlés par structure et tests unitaires, pas par une session navigateur dédiée. La vue agrandie est volontairement fixe : elle montre une synthèse lisible des résultats, pas une seconde vidéo. Aucun mail de test envoyé et aucun changement du backend de contact.

## Publication
- Commit applicatif : `66be840326187a7422851aeda1c50bb90ba03c7a`.
- Déploiement [GitHub Pages 40894964249](https://github.com/timetogrowup/PROJET_CLN/actions/runs/40894964249) : succès, même SHA applicatif.
- Page publique : https://cln-performance.com/solutions.html ; ordre vérifié : introduction, animation bout-en-bout (unique), premier besoin.
- 17 fichiers publics contrôlés après fin de déploiement : page, JS dédié, CSS, deux catalogues et douze médias ; HTTP 200 et empreintes SHA-256 identiques aux fichiers livrés. Le premier contrôle lancé pendant le déploiement avait rencontré des 404 transitoires ; contrôle relancé après succès et entièrement réussi.
- Chrome en production : lecture WebM effective dans chacune des quatre langues, bon poster associé, aucun débordement au viewport contrôlé. Pause effective ; dialogue ouvert avec image de 1100 px ; Échap ferme, le focus revient au lien Agrandir et la pause volontaire est conservée.
- Les limites mobile physique/Safari et la couverture spécifique sans JS/réduction du mouvement restent celles indiquées ci-dessus.
