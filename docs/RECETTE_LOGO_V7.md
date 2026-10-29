# Recette — logo CLN V7
29 octobre 2026. Statut : livré et vérifié en production.

## Livré dans le code
Logo d'en-tête recadré : 112 × 48 px, et 100 × 44 px à 600 px et moins ; nom adjacent conservé. Animation sur l'accueil : largeur maximale 440 px (300 px sur mobile), nom de marque, pause/reprise traduite. Exemple déplacé sous l'introduction, jamais supprimé. Vidéos muettes de 520 × 220, WebM 48 Ko environ, MP4 85 Ko environ, poster 2,7 Ko environ. Source approuvée : GIF x20, 120 scintillements, vague large et fond bleu intense. La compression et le recadrage conservent le mouvement du GIF.

## Contrôles exécutés
- `node --check site.js` : réussi.
- `node tests/brand-motion.mjs` : lecture, pause/reprise, pause volontaire conservée, changement de préférence, réduction de mouvement sans chargement vidéo et refus autoplay avec poster : réussis (simulation unitaire, pas émulation de navigateur).
- `python tests/pedagogy_static.py` : dix pages, 196 références/ancres locales, métadonnées, liens d'évitement, couverture des traductions et règles V5/V6 réussis.
- `node tests/i18n.mjs` : 522 entrées statiques, 135 dynamiques ; langues et variables complets.
- Deux générations consécutives : empreintes identiques des HTML et catalogues. La présentation V7 survit à la génération V6.
- Navigateur Chrome de l'aperçu : vidéo WebM réellement sélectionnée et en lecture ; bouton pause puis reprise vérifiés ; figure 440 px, en-tête 112 × 48 px, aucun débordement horizontal au viewport de l'aperçu.
- Changement réel entre français, anglais, portugais brésilien et espagnol : libellés du bouton traduits, sept liens de menu, absence de débordement sur l'accueil à la largeur de l'aperçu.

## Limites
Les scénarios sans JavaScript / réduction des animations sont couverts par structure et tests unitaires, pas par une session navigateur configurée pour chacun. La matrice multi-largeurs Chromium/WebKit historique n'est pas relancée dans cette session ; validation des téléphones physiques et de Safari reste à faire. Aucun mail de test n'est envoyé pour ce changement visuel ; API et scripts du formulaire inchangés.

## Publication
- Commit applicatif : `1731d07b8ed0330e2edf8b8dc20a5b550b4020ec`.
- Déploiement GitHub Pages [40882512018](https://github.com/timetogrowup/PROJET_CLN/actions/runs/40882512018) : terminé avec succès, SHA identique au commit applicatif.
- Site public : https://cln-performance.com/ ; hébergement conservé, aucun changement Hostinger ni API.
- Dix pages publiques + styles.css + site.js + i18n/messages.json + trois médias : 16 réponses HTTP 200, empreintes SHA-256 identiques aux fichiers livrés.
- Chrome en production : vidéo WebM réellement en lecture, pause puis reprise fonctionnelles, bouton traduit lors du passage en anglais ; symbole d'en-tête mesuré à 112 px, sans débordement à la largeur contrôlée.
- Navigation vers Contact en production : formulaire présent, logo agrandi, aucune vidéo chargée sur cette page, aucun débordement à la largeur contrôlée. Aucun envoi effectué.
- Les vérifications publiques confirment la livraison V7 ; elles ne constituent pas une nouvelle recette complète de l'API ou une certification d'accessibilité.
