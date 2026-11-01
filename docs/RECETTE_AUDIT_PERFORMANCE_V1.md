# Recette — Audit de performance V1
1 novembre 2026 — livré, testé et vérifié en production. Les entrées intermédiaires ci-dessous conservent leur contexte chronologique.

## Avant modification
main 1e0a69db5dd4ac34dd5875955c1ed15fdc73814b. index.html, approche.html, pipelines.html, diagnostic.html et i18n/static.json publics : HTTP 200 et SHA-256 identiques au dépôt. Cadrage local commité avant développement : 5b5aa08.

## Réalisé
Accueil : audit autonome immédiatement après le bloc initial conservé. Méthode : deux phases, rapport, notation 0–100 conditionnée, mesures/estimations/hypothèses, trois conclusions équivalentes et choix du prestataire. Pipelines : lien moyens techniques/performance avant-après. Questionnaire : option audit dans approach et synthèse existante. Contact : seule URL de cache case-data.js modifiée. Aucun style, média, API ni secret modifié.
Sources modifiées : scripts/audit_performance.py, scripts/build_pedagogy.py, scripts/case_journey.py, case-data.js. Pages : index/approche/pipelines/diagnostic ; contact uniquement cache du schéma. Catalogues static/messages, tests/approach_static.py adapté, tests/audit-performance.mjs et workflow verify-audit ajoutés. README et journal actualisés.

## Tests locaux réussis
Catalogues : 745 entrées statiques, 201 dynamiques ; couverture complète des textes visibles. Dix pages et 187 références/ancres. Tests approach_static, home_roi_static, case_static, pipeline_static, protys_static ; génération idempotente. Syntaxe JS du schéma, questionnaire et contact. Tests case-journey (brouillon, édition, langues, expiration, stockage indisponible, validation, soumission native simulée), brand-motion et pipeline-animation, audit-performance (choix audit, quatre langues, compatibilité V11, texte libre).

## Navigateur aperçu
Chrome, largeur 1363 px : méthode FR/EN/PT-BR/ES, phases et trois conclusions effectivement traduites, aucun débordement. Capture visuelle de la méthode vérifiée. Quatre parcours audit → contact exécutés : option audit dans message traduit, texte libre inchangé ; aucun email envoyé. Les erreurs console observées concernaient l’extension Chrome de l’environnement, pas les scripts du site.

## Limites et contrôles complémentaires
PHP absent localement : tentatives php -l, sécurité, API et corps email non exécutées avec succès ici. Contrôles déportés au workflow GitHub, à consigner après résultat. Matrice responsive Chromium/WebKit également prévue dans ce workflow. Appareils physiques et réception SMTP réelle hors recette ; API inchangée. Ne pas confondre tests simulés et envoi réel.

## Publication et production
Déploiement applicatif Pages 41311994659 réussi sur main b8641eeb399fc188cb8913f4d27f7ce680db5d02. Contrôles publics détaillés dans la clôture ci-dessous.

## Compléments de recette
- Accueil et pipelines contrôlés dans Chrome dans les quatre langues : aucun débordement à 1363 px, posters localisés et aucun défaut média constaté. Animation PROTYS : pause et reprise effectives. Détails techniques de méthode : ouverture par Entrée réussie.
- Git direct sans authentification d’écriture : publication du code via connecteur GitHub, sans secret local. PR : https://github.com/timetogrowup/PROJET_CLN/pull/1 ; commit applicatif 4350db82ccad3e9dfc48ef03f06288eb471ea081.
- Deux premiers contrôles CI interrompus par dépendances du runner absentes (Pillow, puis ffprobe), corrigées dans le workflow ; aucune modification du site pour ces corrections. Révisions CI 179bf8b0f27b520a16fd8b4e3f13662425a5ed08 puis e94cc7466e70af2d6a2bf850cbff05bfaef848f7.
- Exécution finale : https://github.com/timetogrowup/PROJET_CLN/actions/runs/41311689535 . Contrôles statiques et PHP/sécurité/API/corps d’emails simulés réussis ; matrice navigateur réussie : 400 dispositions (10 pages × 4 langues × 5 largeurs × Chromium/WebKit), changements de langue, questionnaire, texte libre et rendu sûr.

## CI validée et intégration
Exécution 41311689535 : succès complet. 26 contrôles de sécurité, tests HTTP et quatre corps d’emails capturés avec double de mailer (aucun SMTP). 400 dispositions réussies de 320 à 1280 px sur Chromium et WebKit ; aucune régression bloquante constatée. PR #1 fusionnée sur main : b8641eeb399fc188cb8913f4d27f7ce680db5d02.

## Clôture — production vérifiée le 1 novembre 2026
- Déploiement : https://github.com/timetogrowup/PROJET_CLN/actions/runs/41311994659 — succès. Site : https://cln-performance.com/ .
- Seize fichiers publics HTTP 200, empreintes SHA-256 identiques au code livré : cinq pages HTML concernées, schéma et deux catalogues ; styles, scripts conservés et échantillon de trois médias également identiques.
- Chrome public : accueil, méthode, pipelines et questionnaire dans les quatre langues ; phases et trois conclusions traduites, aucun débordement à 1363 px, aucun défaut média constaté. Quatre parcours audit → contact effectivement exécutés et vérifiés : intérêt audit localisé dans message, texte libre conservé, aucun envoi. Une exécution navigateur groupée a dépassé son délai ; contrôles repris en lots plus courts et tous confirmés.
- Aucune anomalie résiduelle bloquante constatée. Appareils physiques et réception SMTP réelle non testés ; accessibilité vérifiée structurellement et au clavier sur les nouveaux contenus, sans certification exhaustive. Les tests PHP ont bien été exécutés en CI malgré l’absence de PHP local.
- Prévu / Réalisé : périmètre ciblé livré. Testé : contrôles locaux et CI réussis. Publié : main via Pages. Vérifié en production : empreintes, quatre langues et quatre transferts audit sans email.

## Dernier ajustement livré — Multisélection, 1 novembre 2026
La question « Où en êtes-vous dans votre réflexion sur les applications ? » utilise des cases à cocher et accepte plusieurs réponses sans plafond. « Nous ne savons pas encore » reste exclusif. Toutes les réponses sélectionnées sont reprises dans le message de contact ; les anciens transferts V11 à choix unique restent compatibles. Les quatre langues sont conservées.

Références : commit multisélection a7721f0ee690d1c905cb945f078b3fff4b8ec553 ; correctif de cache du parcours 79a69f0f99b6066551b402ac2ac3aef7fb7f2e74 ; déploiement GitHub Pages [41312957038](https://github.com/timetogrowup/PROJET_CLN/actions/runs/41312957038) terminé avec succès. Contrôle public effectué après ce déploiement : audit + amélioration de l’existant + comparaison sélectionnés simultanément puis repris ensemble dans le message contact ; choix inconnu exclusif. Aucun email réel envoyé.

Tests ciblés exécutés avec succès : audit-performance.mjs (listes, dédoublonnage, inconnu, compatibilité, synthèse quatre langues), case-journey.mjs, case_static.py (génération idempotente), pedagogy_static.py (dix pages et liens), catalogues et syntaxe JavaScript. La matrice complète de 400 dispositions concerne la livraison de l’offre d’audit précédente ; elle n’a pas été relancée pour cette correction. Le contrôle navigateur public de la multisélection et de son transfert a été exécuté en français ; les autres langues sont couvertes par les tests de synthèse locaux.

Anomalie rencontrée et corrigée : une page Contact ancienne en cache produisait un message vide pour une liste de choix. Après renouvellement des références et de l’URL de transfert, les trois réponses sont effectivement présentes. Aucun défaut bloquant résiduel constaté sur ce parcours vérifié.
