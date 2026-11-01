# Recette — Audit de performance V1
1 novembre 2026 — publication en attente.

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
À compléter après résultats CI, commit et déploiement Pages. Aucun succès de publication déclaré à ce stade.
