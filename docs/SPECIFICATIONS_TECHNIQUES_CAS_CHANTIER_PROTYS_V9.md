# Spécifications techniques — cas chantier PROTYS V9
29 octobre 2026.

## Architecture
Site statique GitHub Pages existant, domaine cln-performance.com. Aucun nouveau service. Générateur éditorial enrichi par `scripts/protys_case.py`, après les transformations V7/V8. Catalogues UI existants pour les quatre langues. Illustration déterministe : `scripts/render_protys_media.py`, copie dans `scripts/protys_translations.json`, dépendances Pillow/NumPy/ffmpeg/DejaVu Sans. Générer 224 images à 8 images/s, 1320 × 800, boucle de 28 s avec les phases de 4 s. GIF de présentation, WebM VP9, MP4 H.264/yuv420p faststart, poster WebP de synthèse par langue.

## Composants et interfaces
Médias web sous assets/protys/protys-{fr,en,pt-BR,es}.{webm,mp4,webp}. GIF remis séparément, non téléchargés par la page. Adapter le lecteur partagé `pipeline-animation.js` avec un préfixe paramétrable data-media-base ; conserver son comportement sur Vos besoins. Un lecteur par page. Réutiliser poster permanent, chargement différé, pause/reprise, réduction du mouvement, visibilité et dialogue d'agrandissement. Diagramme décoratif accompagné d'une transcription HTML des six étapes. Vue agrandie : poster traduit à largeur 1320 px, défilement interne, titre et bouton Fermer accessibles ; focus rendu au lien.

## Contenus et données
Données fictives uniquement, sans appel à PROTYS. Texte de contexte court fondé sur le besoin fourni ; pas d'explication juridique détaillée. Explication sous l'animation : enrichissement successif, préparation des tâches et retour des résultats. Transition vers les autres processus. Ancre #chantier-protys pour le nouveau cas ; #exemple reste attachée à l'ancien scénario conservé dans details/summary. À l'arrivée sur #exemple, ouvrir l'accordéon afin que les liens V8 gardent leur sens.

## Contraintes
Textes intégrés aux médias traduits à la génération, jamais superposés en français à l'exécution. Adapter les polices aux cadres. Sources/pistes muettes ; pas de chargement vidéo si réduction du mouvement active. Vidéos ciblées sous 2,5 Mo chacune, GIF sous 25 Mo. Le cache des pages de cette livraison porte V9. Aucun remplacement du logo ou de l'animation V8.

## Tests et publication
Syntaxe JS, catalogues, références/ancres, structure, contrôles V7/V8, tests du préfixe média partagé et d'ouverture du scénario générique. Tester les codecs, dimensions, durées, tailles et couverture des chaînes ; examiner les quatre posters et les phases. Vérifier idempotence des pages. Recette Chrome avec quatre langues, pause et dialogue en aperçu puis sur site public ; consigner les limites concernant Safari et les appareils physiques. Déploiement Pages lié au commit, puis HTTP 200 et empreintes des médias. Journal et recette mis à jour après livraison.

## État livré
Réalisé dans le commit 383adf95e6e96b8dd2526e789e1d793d6422944b ; déploiement Pages 40925612190 réussi. Douze médias web et quatre GIF contrôlés. Recette publique et limites : RECETTE_CAS_CHANTIER_PROTYS_V9.md.
