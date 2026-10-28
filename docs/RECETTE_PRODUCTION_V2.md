# Livraison V2 — 28 octobre 2026

## Périmètre livré
Sélecteur commun Français (défaut), English, Português (Brasil), Español. Traductions des neuf pages, navigation, textes accessibles, formulaire, messages et synthèses du diagnostic. Préférence conservée 365 jours, priorité au paramètre lang explicite. Les contenus libres saisis par les visiteurs restent inchangés. Les traductions nécessitent JavaScript ; aucune promesse de référencement multilingue côté serveur.

Captcha addition signé valable dix minutes, utilisable une seule fois. Vérification serveur avant SMTP. Une même adresse normalisée ne peut envoyer qu'une demande toutes les dix minutes et trois par heure. Limite IP complémentaire : une par minute et cinq par heure. Trente tentatives par IP et par heure. Compteurs privés sous verrou, empreintes HMAC sans adresse email/IP en clair ; purge des entrées expirées. Un échec SMTP ne consomme pas le quota des envois acceptés.

## Références
- [Besoins détaillés](EXPRESSION_BESOIN_DETAILLEE_V2.md)
- [Spécification technique](SPECIFICATION_TECHNIQUE_V2.md)
- [Stratégie appliquée](STRATEGIE_DEVELOPPEMENT_V2.md)
- Backend main : ffb6fd2f6dc69a5f8dc8b19e703e90ece2593138.
- Frontend main : 416d9f4ea263a23cb2d889745c4e23873d90e448.
- [CI de validation](https://github.com/timetogrowup/PROJET_CLN/actions/runs/40765530687) : succès.
- [Déploiement API](https://github.com/timetogrowup/PROJET_CLN/actions/runs/40765775847) : succès.
- [Publication Pages](https://github.com/timetogrowup/PROJET_CLN/actions/runs/40766546473) : succès.
- Contrôle public du formulaire dans les quatre langues : titres, liens, libellés et captcha traduits, sélecteur fonctionnel.

## Vérifications
- 23 contrôles PHP : intégrité/expiration/rejeu captcha, limites, échecs SMTP et concurrence.
- HTTP en environnement isolé : CORS, challenge, types/champs, taille, redirections et refus captcha.
- Catalogues : 236 textes statiques et 70 messages dynamiques, complétude et paramètres vérifiés.
- Navigateur CI : 360 combinaisons de pages/langues/formats/moteurs et parcours diagnostic, changement de langue, conservation des saisies et rendu sûr.
- Production : challenge HTTPS 200 avec CORS pour le site autorisé.
- Envoi autorisé à contact@cln-performance.com avec Reply-To identique : redirection 303 merci.html?status=success&lang=en. Acceptation SMTP confirmée ; réception humaine de ce nouveau test à confirmer.
- Réutilisation du captcha : 303 status=captcha_used.
- Nouveau captcha et même email immédiatement : 303 status=rate&lang=en&wait=589. Aucun second envoi accepté.

## Retour arrière
Revenir aux fichiers frontend du commit c3a840303084f8ce70b2667a88d9d83adc5496f5 ET restaurer le backend précédent par le workflow SFTP (ou la sauvegarde privée produite par le déploiement). Ne pas laisser le frontend ancien sans captcha associé au backend V2 qui l'exige. Conserver les secrets et dépendances privés hors de www. Vérifier GET 405/Allow POST, puis un parcours autorisé après restauration. Ne pas désactiver la vérification de la clé SFTP.

## Limites et suivi
Une addition simple limite les soumissions opportunistes ; elle n'arrête pas un robot sophistiqué. Une acceptation SMTP ne prouve pas la réception en boîte. Une relecture par des locuteurs natifs et un contrôle sur téléphone physique restent souhaitables. Les informations légales expressément exclues par le propriétaire ne sont pas ajoutées. Les points antérieurs de MINUTE (dont validation de l'adresse du titulaire OVH) restent suivis.
