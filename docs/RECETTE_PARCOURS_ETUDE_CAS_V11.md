# Recette — Navigation et étude de cas — V11

Date : 30 octobre 2026. Statut : livré, publié et vérifié en ligne.

## Réalisation
Dix menus ramenés à cinq liens. « Vos besoins » et « Exemples concrets » conservés comme pages avec leurs adresses/ancres ; tous les liens hors menu vers ces pages ont été comparés à la version précédente et conservés. « Et si on étudiait votre cas ? » remplace les liens de questionnaire. Sept questions fermées cohérentes et une situation libre facultative. Transfert version 11 en session d'onglet, trente minutes ; pas de réponses dans l'URL. Contact prérempli automatiquement dans le véritable champ message intitulé « Votre situation », éditable, repris dans l'email. Brouillon à chaque modification, reprise sur reload/erreur, nouvelles validations et langues traitées. Confidentialité actualisée. API PHP et SMTP de production inchangés.

## Tests automatisés exécutés
- Syntaxe : site.js, case-data.js, diagnostic.js, contact.js et scripts de test JS ; compilation Python des nouveaux scripts : succès.
- node tests/case-journey.mjs : succès. Quatre langues, transfert automatique, situation modifiable, reload, erreur, nouvelle validation, conservation des coordonnées, changement de langue sur texte automatique/édité, version ancienne, expiration, stockage bloqué, exclusivité inconnus et deux objectifs maximum ; capture du véritable champ soumis via le contrat de soumission native simulé. Aucune requête réseau réelle.
- node tests/i18n.mjs : succès, 665 entrées statiques et 200 messages dynamiques, quatre langues complètes.
- python tests/case_static.py : succès. Dix menus, pages conservées, options localisées, message effectivement soumis, génération idempotente.
- python tests/pedagogy_static.py : succès. Dix pages, 185 références/ancres, métadonnées et couverture des traductions, navigation et isolation des versions actualisées.
- python tests/home_roi_static.py ; node tests/brand-motion.mjs ; node tests/pipeline-animation.mjs ; python tests/pipeline_static.py ; python tests/protys_static.py : succès, régressions V7/V8/V9/V10 et reproductibilité préservées.
- PHP 8.3.6 CLI avec mbstring : contact.php syntaxiquement valide ; php tests/security.php : 26 contrôles réussis, concurrence incluse ; python tests/test_api.py : CORS, challenges, limites/types et redirections réussis.
- python tests/test_case_email.py : succès. Véritable contact.php exécuté sur serveur PHP local isolé, véritable contrôle de token et consentement, mailer remplacé uniquement dans le dossier temporaire du test. Les quatre situations localisées, modifiées et contenant accents/caractères spéciaux sont retrouvées intégralement dans le corps des mails capturés. Aucun SMTP ni email réel.
- git diff --check : succès. contact.php et contact_security.php inchangés.

## Recette Chrome exécutée
- Quatre parcours questionnaire → contact : synthèse traduite automatiquement, texte libre conservé, cinq liens de menu. Modification de la situation puis rechargement : contenu conservé dans les quatre langues.
- Trois objectifs sélectionnés : validation bloquée avec « Choisissez deux objectifs maximum ». Choix d'incertitude : autres objectifs désélectionnés.
- Trente-deux dispositions : questionnaire/contact × quatre langues × fenêtres intégrées 320/390/768/1280 px ; aucune extension horizontale. Largeurs utiles Chrome 305/375/753/1265 px.
- Synthèse visible dans le pavé éditable et notice d'inclusion automatique dans le mail. Aucun bouton d'ajout de recommandation.

## Anomalies corrigées avant publication
L'aperçu HTTP ne fournit pas crypto.randomUUID(). Un identifiant de transfert de repli (sans rôle de sécurité) assure désormais le parcours dans cet environnement. Les messages spécifiques des groupes de cases sont préservés par le gestionnaire de validation partagé au lieu d'être remplacés par un message générique.

## Limites
Chrome disponible ; pas de Safari/WebKit ni appareil physique exécuté dans cette recette. Les anciens tests de parcours navigateur ont été actualisés pour une exécution CI ultérieure, sans prétendre les avoir lancés ici sur deux moteurs. Les cas stockage bloqué/expiration/ancien format sont couverts par les tests JS isolés. Pas d'envoi SMTP réel ni vérification de réception en boîte : contenu du mail et protections contrôlés en simulation, API de production conservée. Si le stockage d'onglet est bloqué, une synthèse copiable et un accès au contact remplacent le transfert automatique.

## Publication et contrôle public
Version applicative `24279fb679521ad72f193608e5245b4aa5a17cb5`. GitHub Pages : succès dès la première tentative, [exécution 41083532813](https://github.com/timetogrowup/PROJET_CLN/actions/runs/41083532813).

Dix-sept fichiers HTTP 200 et SHA-256 identiques : dix pages HTML, site.js/case-data.js/diagnostic.js/contact.js, styles.css et les deux catalogues. solutions.html et realisations.html restent accessibles. L’API contact répond 405 avec Allow: POST à une lecture GET, conformément à son contrat ; aucune requête d’envoi publique effectuée.

Recette du domaine, quatre langues : questionnaire → contact, situation localisée automatiquement remplie, texte libre conservé, modification puis rechargement avec contenu préservé, cinq liens de menu et absence de débordement. Les URL de transfert contiennent uniquement summary=1 et lang, aucune réponse.

Questionnaire : https://cln-performance.com/diagnostic.html?lang=fr .
