# Spécifications techniques — Étude de cas — V11

Date : 30 octobre 2026. Statut : réalisé, publié et vérifié.

## Architecture
HTML/CSS/JS statiques et API PHP/SMTP OVH existants conservés. contact.php incorpore déjà le champ POST message dans le corps texte du mail : réutiliser ce contrat, sans changer l'API ni les secrets. Déploiement frontend GitHub Pages. Aucun nouveau service.

## Génération
Ajouter scripts/case_journey.py en dernière transformation de build_pedagogy.py (après V10 et après la mise à jour de confidentialité historique). Cette transformation reconstruit diagnostic.html, adapte le main du contact et les dix menus, traduit tous les textes et synchronise les liens de questionnaire. Préserver solutions.html/realisations.html et leurs ancres. Génération idempotente, versions de cache V11.

## Composants
- case-data.js : schéma version 11, listes de codes autorisés, normalisation et construction de synthèse factuelle localisée via i18n/messages.json.
- diagnostic.js : validations requises, inconnus exclusifs, maximum deux objectifs ; transfert sessionStorage puis navigation. En cas d'erreur stockage, afficher une synthèse copiable sur place.
- contact.js : conserver la machine de vérification humaine, ajouter lecture du transfert et gestion du brouillon ; supprimer l'ancien mécanisme de recommandation à ajouter manuellement.
- textarea#message[name=message] : unique pavé « Votre situation », obligatoire, 10 000 caractères maximum, effectivement soumis. Retirer l'ancien aperçu et les boutons d'ajout de synthèse.
- site.js : sélection de langue conservée. Le nouveau transfert n'utilise pas l'ancien localStorage clnRecommendation.
- confidentialité : décrire transfert/brouillon d'onglet à trente minutes et envoi automatique de la situation lors du formulaire.

## Données
Transfert clnCaseTransfer : {version:11,id,generatedAt,answers}. Codes : applications, people, connections, difficulties[], goals[], approach, horizon, situation. Texte libre 2 000 caractères, rendu par value/textContent. Vérifier version, identifiant, horodatage (non futur, maximum trente minutes), types et codes. Pas de HTML injecté ni de données dans les URL ; seul summary=1 signale un transfert.
Brouillon clnContactDraft dans sessionStorage : {fields:{name,_replyto,company,message},summaryId,caseAnswers,generatedText,expires}. Trente minutes depuis la dernière modification ; pas de mot de passe ni de jeton humain persisté. Une validation portant un nouvel identifiant remplace message ; à transfert identique ou consommé, conserver le brouillon. Nettoyer le transfert après application réussie. Restaurer sur erreur d'envoi ; effacer après succès.

## Interfaces et compatibilité
Le questionnaire ne fait aucune requête de soumission. Contact remplit message avant activation du bouton d'envoi. La langue des libellés et de la synthèse initiale suit CLN.lang. Après édition, ne pas traduire le texte du visiteur. Détecter les anciennes synthèses sans les réinterpréter ; conserver le contact utilisable. L'accès direct ?need=... peut être conservé comme contexte facultatif sûr sans nécessiter un bouton d'ajout ; aucune reprise arbitraire d'un ancien questionnaire.

## Tests
- Statique : dix menus à cinq liens, pages et liens préservés, catalogue complet, structure, pas de champs message désactivés ou sans name.
- JS : schéma/codes, inconnus/max deux, texte libre, langues, expiration/ancienne version, stockage bloqué ; transfert, nouvelle validation, restauration, protection des éditions et changement de langue.
- PHP : tests de sécurité existants et capture SMTP locale simulée du corps produit par le véritable contact.php, quatre langues, modifications et caractères spéciaux. Aucun email réel ni vérification humaine publique nécessaire.
- Chrome : parcours complet questionnaire-contact, modification et reload, accès direct, navigation et tailles disponibles ; ne pas soumettre le formulaire public.
- Idempotence générateur, non-régression accueil/médias/mouvement ; HTTP et SHA-256 publics après publication. Documenter les limites moteurs/appareils et l'absence d'envoi SMTP réel.

## Livraison effective — 30 octobre 2026
Version `24279fb679521ad72f193608e5245b4aa5a17cb5`, déployée avec succès sur GitHub Pages ([exécution 41083532813](https://github.com/timetogrowup/PROJET_CLN/actions/runs/41083532813), première tentative). Nouveau parcours : https://cln-performance.com/diagnostic.html?lang=fr .

Dix menus à cinq liens, pages retirées du menu conservées avec les liens hors menu. Sept questions fermées et une situation facultative, quatre langues. Contact automatiquement prérempli dans le champ message, texte éditable conservé sur reload/erreur. Validation finale du contact seule responsable de l'envoi ; traitement PHP/SMTP conservé. Transfert et brouillon de session d'onglet à trente minutes, sans réponses dans l'URL.

Tests JS, structure/catalogues (665/200), dix pages/185 références, régressions V7 à V10 et PHP réussis. Les quatre corps d'emails ont été contrôlés avec le véritable contact.php et un mailer simulé, sans SMTP réel. Recette Chrome : quatre parcours complets, 32 dispositions, limite des objectifs et inconnus exclusifs. Dix-sept fichiers publics HTTP 200 et SHA-256 identiques ; transfert et conservation des modifications revérifiés en ligne dans les quatre langues.

Détails et limites : [rapport de recette](RECETTE_PARCOURS_ETUDE_CAS_V11.md). Pas de test Safari/WebKit, d'appareil physique ni de réception SMTP réelle. Un stockage bloqué donne une synthèse copiable au lieu d'un transfert automatique.

Un identifiant de repli est utilisé lorsque crypto.randomUUID() est indisponible, notamment sur l’aperçu HTTP ; cet identifiant n’a aucun rôle de sécurité. Le gestionnaire partagé conserve les messages de validation spécifiques des groupes. Les tests PHP nécessitent PHP CLI et mbstring.
