# Recette — cas chantier PROTYS V9
29 octobre 2026. Statut : livré et vérifié en production.

## Livré
Cas fictif Chantier A après l'introduction de Nos pipelines en action. Six étapes et synthèse, boucle de 28 secondes, vague bleu-gris, cadre/titre scintillants et contours renforcés. Quatre langues : français, anglais, portugais du Brésil, espagnol. Chaque illustration contient ses propres textes traduits ; aucune langue ne masque le bloc. Ancien exemple de planification conservé dans un accordéon ; l'ancre #exemple l'ouvre automatiquement.

Quatre GIF de présentation remis séparément ; douze médias web versionnés (WebM/MP4/posters). Lecteur partagé paramétré par préfixe, pause/reprise, agrandissement fixe de 1320 px, transcription et accompagnement traduits. Les données restent fictives ; pas d'appel PROTYS, de délai légal ni d'autorisation de travaux. Bilan final : une réponse attendue et un dépôt à reprendre.

## Contrôles locaux réalisés
- Syntaxe pipeline-animation.js ; catalogues : 545 entrées statiques, 140 dynamiques, quatre langues et variables complètes.
- Contrôles pédagogiques : dix pages, 204 références et ancres, métadonnées et traductions ; invariants V5/V6 conservés.
- Tests V8 du lecteur et des médias : réussis. Test additionnel du préfixe PROTYS : bons médias FR/ES sans changement du préfixe V8 par défaut.
- Tests V7 de lecture/pause et réduction du mouvement : réussis.
- V9 : bloc unique et ordre, conservation de l'ancien exemple et du cas V8, 57 chaînes de l'illustration traduites, douze médias web vérifiés (codecs VP9/H.264, 1320 × 800, 28 s, moins de 2,5 Mo par vidéo). Quatre GIF de 28 000 ms, boucle infinie et moins de 25 Mo.
- Vidéos WebM environ 540–563 Ko ; MP4 environ 1,3–1,4 Mo ; posters environ 86–94 Ko. GIF environ 15–16 Mo ; les GIF ne sont pas chargés par le site.
- Posters des quatre langues inspectés visuellement : textes dans les cadres ; le vocabulaire français n'est conservé que dans les noms propres. La version internationale situe le contexte réglementaire en France.
- Génération répétée : HTML et catalogues identiques, sans accumulation de blocs ni scripts.

## Aperçu Chrome
Lecture WebM effective dans les quatre langues, sources correspondantes ; aucun débordement horizontal à la largeur contrôlée. Pause, dialogue ouvert à 1320 px, Échap et retour du focus vérifiés ; pause volontaire conservée. Accès direct à #exemple : accordéon ouvert et cinq étapes conservées. Vos besoins : animation V8 toujours en lecture avec son média propre.

## Limites
Téléphones physiques et Safari non testés. La matrice multi-largeurs et multi-moteurs historique n'est pas relancée dans cette session. Préférence système de réduction du mouvement et absence de JavaScript : structure et tests unitaires, sans session navigateur dédiée. La vue agrandie est une synthèse fixe, pas une deuxième animation. Aucun envoi de formulaire ni modification de l'API. Les polices du GIF sont à lire en vue agrandie sur un petit écran.

## Publication
- Commit applicatif : `383adf95e6e96b8dd2526e789e1d793d6422944b`.
- Déploiement [GitHub Pages 40925612190](https://github.com/timetogrowup/PROJET_CLN/actions/runs/40925612190) : succès, SHA identique au commit applicatif.
- Page : https://cln-performance.com/pipelines.html#chantier-protys. Ordre public vérifié : introduction, nouveau cas chantier, ancien exemple replié, capacités.
- 17 fichiers publics contrôlés : pipelines.html, solutions.html, lecteur JS partagé, CSS, catalogue statique et douze médias ; tous HTTP 200 et SHA-256 identiques à la livraison.
- Chrome public : lecture effective de la bonne vidéo WebM en FR/EN/PT-BR/ES ; pas de débordement à la largeur contrôlée. Pause effective, dialogue ouvert avec image de 1320 px ; Échap ferme, rend le focus au lien et conserve la pause volontaire.
- Lien public #exemple : accordéon ouvert, cinq étapes conservées. Les GIF de présentation dans les quatre langues sont remis séparément ; aucune vidéo française imposée sur les pages traduites.
- Les limites d'appareils et de réglages système ci-dessus restent explicites.
