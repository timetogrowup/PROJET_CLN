# Spécifications techniques — identité CLN — V7
Date : 29 octobre 2026.

## Architecture et composants
Le site reste statique HTML/CSS/JS, versionné dans PROJET_CLN et publié par GitHub Pages sur https://cln-performance.com/. Aucun nouveau service, compte, stockage visiteur ou appel tiers.
- `assets/brand/cln-signature.webm` : VP9, format préféré.
- `assets/brand/cln-signature.mp4` : H.264/yuv420p, repli compatible, faststart.
- `assets/brand/cln-signature-poster.webp` : affiche fixe et symbole des en-têtes.
- `scripts/brand_identity.py` : transformation commune appelée par `build_pedagogy.py` avant écriture des catalogues.
- `styles.css` : dimensions, recadrage, présentation responsive et préférence sans animation.
- `site.js` : lecture progressive, pause/reprise, visibilité, préférence de mouvement.
- `i18n/messages.json` : deux clés `brand.play` / `brand.pause`, quatre traductions chacune.

## Données et interfaces
Source : GIF approuvé LOGO_CLN_scintillements_x20.gif (640 × 640, 120 événements). Extraction d'une fenêtre x=80, y=205, largeur=520, hauteur=220. Le nom de marque est du texte HTML, pas du texte rasterisé. Les en-têtes emploient une image décorative à alt vide car le nom adjacent donne déjà le nom du lien.

La figure `.brand-signature` contient le poster permanent, la vidéo décorative `#brand-animation` (aria-hidden, hors tabulation), un figcaption et un vrai bouton `aria-controls`. Aucun attribut autoplay : le JS ajoute les URL `data-src` seulement lorsque la lecture est permise. Sources WebM puis MP4 ; poster visible tant que la lecture n'a pas réussi. `muted`, `loop`, `playsinline`, `preload=none`. Pas de son.

`prefers-reduced-motion` est surveillé au chargement et pendant la visite. `IntersectionObserver` suspend la vidéo hors vue ; sans cette API, la lecture reste gérée par visibilité d'onglet et préférence. Les refus de play() n'interrompent pas le site. La pause manuelle est conservée en mémoire pour la visite, sans cookie ni stockage persistant. Le bouton utilise le mécanisme de traduction CLN existant. Les pages référencent CSS/JS avec le cache-buster V7.

## Contraintes et tests
Vérifier syntaxe JS, catalogues, références locales, structure et contenus V6, intégration dans les dix pages, taille/codecs des médias et régénération reproductible. Tests unitaires de cycle de vie dans `tests/brand-motion.mjs`. Contrôle navigateur réel en aperçu puis en production : lecture, pause/reprise, langues, menu et débordement. La couverture des appareils et moteurs réellement utilisés est précisée dans le rapport de recette. La conversion vidéo peut légèrement modifier les dégradés par compression ; ce n'est pas une nouvelle génération du logo.
