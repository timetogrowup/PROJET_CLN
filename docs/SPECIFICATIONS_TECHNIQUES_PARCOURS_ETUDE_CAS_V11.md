# Spécifications techniques — Étude de cas — V11

Date : 30 octobre 2026. Statut : avant développement.

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
