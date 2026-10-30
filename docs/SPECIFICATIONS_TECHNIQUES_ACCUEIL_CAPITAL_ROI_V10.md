# Spécifications techniques — Accueil capital et ROI — V10

Date : 30 octobre 2026. Statut : réalisé, publié et vérifié.

## Architecture
Site statique HTML/CSS/JavaScript conservé, hébergement et domaine existants (GitHub Pages / cln-performance.com). Aucun service, API métier, compte utilisateur ou dépendance frontend supplémentaire. site.js assure les langues et la flèche ; pipeline-animation.js pilote le comparatif comme les lecteurs V8/V9.

## Génération et composants
- scripts/home_capital_roi.py : transformation finale du générateur scripts/build_pedagogy.py, après l'identité V7 et les cas V8/V9. Reconstruire uniquement le main de index.html à partir de textes traduits ; conserver la figure de la flèche existante. Transformation idempotente, ancres stables dont #pipelines.
- scripts/roi_animation.py : source procédurale exacte du scénario approuvé, textes embarqués FR/EN/PT-BR/ES, trois et neuf étapes, calendrier 0–36 mois, deux échelles identiques.
- scripts/render_roi_media.py : génération reproductible des WebM VP9, MP4 H.264 et posters WebP, via Pillow, DejaVu Sans et ffmpeg. GIFs conservés comme livrables séparés ; le site utilise les vidéos optimisées.
- index.html : introduction et flèche ; capital ; productivité ; #investissement avec figure, légende, pause, agrandissement et transcription ; engagements #pipelines et CTA.
- assets/roi/roi-{fr,en,pt-BR,es}.{webm,mp4,webp} : 12 médias. Vidéos muettes, 1200 × 1100, 36 secondes ; image de synthèse au mois 36.
- styles.css : styles limités à l'accueil et au lecteur ROI, reprise de la palette du site et des teintes bleu gris du média. Deux colonnes de lecture éditoriale sur grand écran, une sur téléphone.

## Données et interfaces
Aucune collecte ni nouvelle persistance. Catalogue i18n/static.json pour l'éditorial, i18n/messages.json pour les commandes. Le choix de langue existant synchronise le poster, les deux sources vidéo et la vue agrandie ; conserver pause et position lors d'un changement de langue. Chaque lien interne conserve la langue via site.js. Un seul lecteur pipeline par page, en plus de la flèche indépendante. Contrat data-media-base="assets/roi/roi". Dialog natif, image finale 1200 px avec défilement interne.

## Accessibilité et mouvement
Vidéo décorative aria-hidden, texte explicatif et transcription structurée. Poster présent dans le HTML ; preload=none et aucune source vidéo active avant visibilité. prefers-reduced-motion donne une image statique sans télécharger le comparatif. Pause hors écran, onglet masqué et dialog ouvert ; Échap natif et focus restitué au lien. Flèche préexistante conservée avec son contrôleur, pause utilisateur et fallback. Contrôles traduits. Vue agrandie explicitement nommée « synthèse » puisqu'elle est statique.

## Contraintes
Une H1, titres hiérarchiques, navigation à sept liens, formulaire inchangé. Pas de lecture de GIF lourd dans la page, de piste sonore ni de requête tiers nouvelle. Objectif ≤ 2,5 Mo par vidéo, ≤ 200 Ko par poster ; ajuster la compression en fonction du rendu. Échelles financières sans montants, courbes de solde cumulé, durées illustratives. Mise à jour du cache de l'accueil sans altérer les références des pages non concernées.

## Tests et recette
1. Syntaxe JS/Python, contrôles i18n et structure/liens des dix pages.
2. Adapter uniquement les assertions V6 incompatibles avec la décision V10 (ancienne promesse H1 et interdiction du mot chirurgicale à l'accueil). Préserver les autres invariants.
3. Tests ROI : ordre des sections, flèche conservée, quatre langues complètes, 3/9 étapes, mois 9/36, gains continus, courbes aux mêmes dimensions, codecs/durée/dimensions/poids des 12 médias.
4. Lecteur partagé : langue, pause/position, lazy loading, réduction du mouvement, focus du dialog, régressions V8/V9.
5. Chrome : accueil quatre langues ; grand et petit écran si capacité disponible ; pause, zoom, Échap, liens ; absence de débordement. Sans JS/réduction : tests statiques/unitaires, compléter par navigateur si disponible.
6. Régénération idempotente puis diff sans erreurs ; publication GitHub Pages ; contrôle HTTP et empreintes des fichiers publics et visite de l'accueil.
7. Documenter explicitement toute matrice mobile/moteurs non exécutée ; ne pas déclarer de tests Safari ou téléphone réel sans les avoir réalisés.

## Livraison effective — 30 octobre 2026
Accueil livré en quatre langues, flèche conservée, cinq blocs éditoriaux, comparatif 36 secondes avec 3/9 étapes et deux graphiques indépendants. Médias optimisés (huit vidéos et quatre posters), transcription, pause/reprise et synthèse statique agrandissable. Aucun changement du traitement du contact.

Version applicative initiale : `c6445f1b97eb152c4c0013920ff164162dcb7239`. Correction du mouvement de la flèche : `26e939b35f4276d98e38d1add82b03e5cf29cd5c`. Cette correction empêche un événement de lecture tardif de relancer la flèche hors écran ; elle est couverte par un test supplémentaire.

GitHub Pages : publication de la correction réussie, exécution [41068286785](https://github.com/timetogrowup/PROJET_CLN/actions/runs/41068286785), tentative 2 après un échec temporaire du service de déploiement. Accueil : https://cln-performance.com/ . Dix-sept fichiers publics HTTP 200 et SHA-256 identiques ; quatre langues et contrôles validés sur le domaine. Tests détaillés et limites dans [le rapport de recette](RECETTE_ACCUEIL_CAPITAL_ROI_V10.md). Safari et appareils physiques non testés ; les seize fenêtres de recette sont des vérifications CSS dans Chrome.

Le contrôleur partagé site.js a été corrigé pour différer la lecture initiale de la flèche hors écran et revérifier son autorisation après play() et lors des événements playing. Le cache du script de l’accueil porte 20261030-v10r1.
