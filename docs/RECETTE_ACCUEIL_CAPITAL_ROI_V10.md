# Recette — Accueil capital existant et ROI — V10

Date : 30 octobre 2026. Statut : livré, déployé et vérifié en ligne.

## Livré dans le code
Accueil réécrit selon les cinq blocs validés : petite structure et flèche ; capital existant ; productivité par automatisation ; investissement et comparatif ; Ciblé/Libéré/Normé et parcours de suite. Métadonnées et totalité des textes/commandes disponibles en FR/EN/PT-BR/ES. Pas de modification du contact ni de son backend. La flèche existante est conservée. Le comparatif approuvé de 36 secondes est utilisé en vidéo optimisée, avec synthèse statique agrandissable et transcription.

## Contrôles automatisés exécutés
- node --check site.js et pipeline-animation.js : succès.
- python -m py_compile sur les trois nouveaux modules : succès.
- node tests/i18n.mjs : succès, 595 entrées statiques et 142 messages dynamiques, quatre langues et paramètres complets.
- python tests/pedagogy_static.py : succès, dix pages et 203 références/ancres locales, métadonnées, H1, traductions, navigation à sept liens et préservation des invariants métier V5/V6.
- python tests/home_roi_static.py : succès, ordre et contenu de l'accueil, flèche préservée, chargement différé, 3/9 étapes, 9/36 mois, capital initial limité, accumulation des gains et échelles identiques. Contrôle des douze médias, codecs/dimensions/durée/poids. Régénération HTML/catalogues idempotente.
- node tests/pipeline-animation.mjs : succès, langue, position et pause utilisateur conservées, lazy loading, focus/zoom, visibilité, mouvement réduit ; préfixes média V8/V9/V10 vérifiés.
- node tests/brand-motion.mjs : succès, contrôle flèche, réduction du mouvement sans téléchargement, refus autoplay et image de repli.
- python tests/pipeline_static.py : succès V8, douze médias et 37 libellés.
- python tests/protys_static.py : succès V9, placement et préservation, douze médias et 57 libellés ; GIFs contrôlés quand le dossier optionnel est disponible.
- git diff --check : succès.

Les assertions historiques interdisant « chirurgicale » à l'accueil et imposant l'ancien premier écran ont été remplacées par les exigences approuvées V10 ; leurs autres contrôles restent actifs. Le scénario navigateur historique pipelines.mjs est adapté au nouveau parcours, sans déclarer son exécution multi-moteurs.

## Recette Chrome effectuée sur l'aperçu
- Quatre langues : titre, texte et légende traduits ; source WebM et poster corrects, lecture effective.
- Premier écran : flèche en lecture, comparatif sans source vidéo tant qu'il est hors écran.
- Arrivée au comparatif : flèche en pause et comparatif en lecture.
- Pause utilisateur, ouverture de la synthèse 1200 px, pause pendant le dialog, Échap, fermeture, retour de focus et pause préservée : succès.
- Seize fenêtres intégrées, largeurs externes 320/390/768/1280 px × quatre langues : aucune extension horizontale de page ; langues chargées. Largeurs utiles 305/375/753/1265 px avec les barres de défilement de Chrome.
- Fenêtre 390 px avec JavaScript bloqué : contenu français et structure présents, aucun débordement ; contrôles vidéo masqués.
- Liens « Identifier vos premiers gains » vers diagnostic.html et « Parlons de votre écosystème » vers contact.html : navigation et formulaire visibles, langue conservée, sans soumission.
- Captures de travail contrôlées visuellement : hiérarchie du premier écran, flèche à côté, comparatif traduit, étapes et courbes.

## Médias
1200 × 1100, 36 secondes, 6 images/seconde, sans son. H.264/MP4 et VP9/WebM, quatre langues. Par fichier : vidéo environ 244 à 283 Kio ; poster environ 99 à 103 Kio. Les GIFs lourds ne sont pas chargés par le site. La vue agrandie est la synthèse statique du mois 36, explicitement annoncée.

## Limites de vérification
Pas de test sur téléphone physique, ni Safari/WebKit dans cette recette. Les fenêtres intégrées vérifient les mises en page CSS, sans prétendre remplacer un test sur appareil réel. Le mouvement réduit est vérifié par les tests unitaires et les règles CSS, sans session navigateur dédiée à cette préférence. Aucun envoi réel du formulaire. Les calendriers et courbes restent des illustrations et non des engagements contractuels.

## Anomalie détectée et corrigée
Le contrôle public a révélé une course entre l’autoplay de la flèche et sa sortie de l’écran, notamment lors des accès directs au comparatif. Le contrôleur diffère désormais le chargement tant que la visibilité n’est pas établie, et revérifie les conditions lors de la résolution de play() et des événements playing tardifs. Test unitaire ajouté et navigation directe vérifiée dans les quatre langues sur l’aperçu : flèche arrêtée, comparatif en lecture. Référence de cache du script de l’accueil renouvelée.

## Publication
Première publication applicative `c6445f1b97eb152c4c0013920ff164162dcb7239` réussie (GitHub Pages, exécution 41067622889). Seize fichiers publics contrôlés HTTP 200 et SHA-256 identiques au code livré. Quatre langues, lecture et contrôles de la synthèse vérifiés sur le domaine. Correction finale `26e939b35f4276d98e38d1add82b03e5cf29cd5c` publiée avec succès, exécution [41068286785](https://github.com/timetogrowup/PROJET_CLN/actions/runs/41068286785), tentative 2. La première tentative de cette correction a rencontré une erreur temporaire de GitHub Pages après compilation réussie ; seule l’étape de déploiement en échec a été relancée.

Contrôle final : **17 fichiers HTTP 200, toutes les empreintes SHA-256 identiques** : accueil, site.js, styles.css, deux catalogues et douze médias ROI. Dans Chrome, après revalidation du cache, script `site.js?v=20261030-v10r1`, quatre langues en lecture sur la source WebM correcte, flèche hors écran arrêtée, aucun débordement. Pause, dialog, Échap, retour de focus et pause conservée revérifiés sur la version corrigée. Premier écran public en français : flèche en lecture, comparatif sans chargement tant qu’il est hors écran.

Version publique : https://cln-performance.com/ .
