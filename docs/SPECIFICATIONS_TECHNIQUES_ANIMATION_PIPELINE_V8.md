# Spécifications techniques — animation pipeline V8
29 octobre 2026.

## Architecture et composants
Site statique existant sur GitHub Pages, domaine cln-performance.com. Aucun backend ou service supplémentaire. `scripts/render_pipeline_video.py` et `scripts/pipeline_video_translations.json` génèrent les médias à partir du dessin procédural approuvé : 1100 × 680, 180 images à 12 images/s. Dépendances de génération : Pillow, NumPy, ffmpeg et polices DejaVu Sans. Sorties dans `assets/pipeline/` : WebM VP9, MP4 H.264/yuv420p faststart, poster WebP par langue. Conserver le script et ses traductions pour toute reproduction.

`scripts/pipeline_animation.py` est appelé après l'identité V7 dans le générateur de pages ; déplacement idempotent de #bout-en-bout, nouvelle figure, commandes et transcription textuelle des cinq phases. Catalogues UI via le mécanisme CLN existant. `pipeline-animation.js` gère les médias et le dialogue ; `styles.css` les proportions et le dialogue responsive. Ressources statiques versionnées V8.

## Données et interfaces
Aucune donnée utilisateur. Exemple synthétique demande #1042, contexte client, priorité HAUTE et délai de 24 h explicitement illustratifs. Les quatre variantes sont traduites dans le fichier JSON, pas par traduction automatique à l'exécution.

Vidéo sans autoplay déclaratif et sans source initiale : chargement via JS uniquement si mouvement permis et figure visible. Définir `muted`, `loop`, `playsinline`, `preload=none`, poster et dimensions. Associer le lecteur décoratif à une explication HTML accessible ; les étapes sont disponibles dans une transcription native details/summary. Commandes explicites pause/reprise et agrandissement ; aucun contrôle ne dépend d'une icône seule.

Le changement de langue conserve le temps courant et la pause volontaire ; remplacer source et poster, attendre les métadonnées avant restauration du temps. Ignorer les promesses devenues obsolètes lors de changements rapides. Suspendre hors vue, onglet caché et pendant le dialogue. Respecter le changement de prefers-reduced-motion à chaud. Une erreur de lecture conserve le poster et le contenu textuel.

Le dialogue natif possède titre traduit et bouton Fermer. Une image fixe dans la langue courante, à largeur minimale 1000 px, conserve la lisibilité sur mobile, avec défilement interne. showModal assure confinement du focus ; Escape ferme ; remettre le focus sur Agrandir après fermeture. Le poster de synthèse présente tous les résultats sans nécessiter d'animation. Pas de deuxième vidéo en lecture.

## Tests
Syntaxe JS, catalogues, références locales, structure et conservation V6/V7, idempotence. ffprobe : codecs, dimensions et 15 secondes dans huit vidéos ; contrôler visuellement les quatre posters et un instant de chaque phase. Tests unitaires du cycle de vie avec événements de langue et refus de lecture. Navigateur réel en aperçu et production : lecture, pause, langues, agrandissement et fermeture. Contrôler les ressources publiques par statut et empreinte. Préciser les limites d'appareils/moteurs dans la recette.

## État livré
Implémentation et douze médias livrés dans le commit 66be840326187a7422851aeda1c50bb90ba03c7a. Générateur, tests et script de rendu versionnés. Recette publique et limites documentées dans RECETTE_ANIMATION_PIPELINE_V8.md.
