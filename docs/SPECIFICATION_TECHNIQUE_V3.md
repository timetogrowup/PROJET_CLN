# Spécification technique détaillée V3
Date : 28 octobre 2026. Références : besoin et expression détaillée V3.

## Frontend
Remplacer fieldset de calcul par champs cachés human_token, human_confirmed et lang dans le formulaire. Ajouter hors du formulaire un élément HTML dialog avec aria-labelledby/aria-describedby, texte, checkbox sans état mémorisé, statut aria-live, annuler, réessayer et confirmer. Événement submit : preventDefault, validation native reportValidity puis showModal. Aucun appel de vérification au chargement de la page. Un deuxième événement submit n'ouvre pas plusieurs fenêtres.

Machine d'états : fermé → préparation → prêt → envoi ; erreur → nouvelle préparation ; annulation → fermé. Utiliser AbortController et numéro de génération pour ignorer une réponse réseau d'une fenêtre fermée. Délai réseau vingt secondes ; bouton réessayer après échec. À chaque ouverture/renouvellement, décocher et effacer le jeton. Confirmer exige case cochée, jeton présent, non expiré et état prêt. Sauvegarder le brouillon puis effectuer le POST natif unique avec HTMLFormElement.prototype.submit. Aucune saisie n'est transmise lors de l'ouverture, seul le jeton est demandé.

Position : dialog fixed, marges nulles ; petite largeur ou hauteur : centré ; sinon tirer x/y dans les bornes du viewport en déduisant dimensions et marges. Plafonner largeur et hauteur avec défilement intérieur. Resize repositionne uniquement si nécessaire pour rester dans les bornes. Native dialog gère inertie de l'arrière-plan, focus et Échap. Fermer efface checkbox/jeton, annule fetch et rend le focus. Commandes identifiées par IDs stables, textes data-msg gérés par site.js.

## Backend et protocole
GET contact.php?op=human : JSON {token, expires}, cache no-store, CORS exact aux deux origines autorisées. Jeton base64url JSON avec identifiant aléatoire 128 bits, version/purpose human-v3, expiration 600 secondes, signature HMAC-SHA256 de purpose|id|expires. Aucun opérande ni réponse de calcul. POST human_confirmed=1 et human_token exigés. Vérifier type, format, purpose, signature constante et expiration. Consommer sous verrou avant SMTP pour refuser le rejeu. Refuser explicitement les anciens champs/captchas sans nouvelle autorisation.

Réutiliser stockage privé et clé persistante existants, empreintes HMAC, purge et verrou de concurrence. Conserver quotas email 600 s / 3 par heure, IP 60 s / 5 par heure et 30 tentatives par heure. Échec SMTP ne consomme pas le quota accepté. Limites de taille, validation, honeypot, consentement, destinataire et TLS inchangés. Statuts human_required, human_invalid, human_used traduits et redirections 303 avec lang. GET générique reste 405 Allow POST pour le déploiement.

## Migration et publication
Backend et frontend sont versionnés ensemble mais hébergés séparément. Tester l'ensemble sur branche de recette avant main. Déployer API et publier frontend dans la même séquence ; pendant la courte propagation, un ancien formulaire peut être refusé sans envoi et doit être rechargé. Aucune compatibilité permanente avec le calcul ; pas de baisse des quotas. Invalider caches d'assets via version V3 et conserver fetch catalogues no-cache.

## Vérification et retour arrière
Tests unitaires jeton, confirmation, purpose/expiration/rejeu, quotas et concurrence ; HTTP origine/champs/refus ; navigateur deux moteurs, quatre langues, cinq largeurs, validations, fermeture/focus, position, indisponibilité, expiration et un seul POST simulé. Aucune soumission réelle nécessaire pour cette évolution. En production, vérifier ressources, fenêtre et refus serveur sans cocher via automatisation UI. Retour arrière coordonné fichiers frontend et API du commit ed6fb95c753a9ab0b0492b1e087ed477128d7327, en conservant secrets et état privé. Ne jamais rétablir un frontend incompatible avec son API.
