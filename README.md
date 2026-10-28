# CLN Performance

Site vitrine CLN — Ciblé, Libéré, Normé.

## Architecture actuelle

- Référentiel : `timetogrowup/PROJET_CLN`, branche `main`.
- Site public : https://cln-performance.com, hébergé sur GitHub Pages.
- Traitement du formulaire : `https://api.cln-performance.com/contact.php`, sur OVHcloud Starter, PHP 8.4, racine `www`.
- Boîte officielle : `contact@cln-performance.com`.
- État détaillé et résultats datés : [MINUTE.md](MINUTE.md).

Le formulaire public est actif depuis le 28 octobre 2026. Le transport SMTP, la réception d'un test et le parcours de soumission public ont été vérifiés. Le contact direct par email reste disponible. Voir MINUTE.md pour les limites de recette et les points ouverts.

## Publication

Les changements de `main` sont publiés par GitHub Pages. GitHub Pages ne peut pas exécuter `contact.php`.

Le workflow manuel **Deploy OVH contact API** (`.github/workflows/deploy-ovh-api.yml`) s'exécute sur `main` :

1. Vérification de syntaxe PHP.
2. Transfert de `contact.php` et des dépendances/configurations SMTP privées par SFTP, avec clé serveur épinglée dans `deploy/ovh_known_hosts`.
3. Sauvegarde d'un éventuel fichier précédent hors de `www`, vérification du transfert et retour arrière si le contrôle HTTP échoue.

Sans clé serveur vérifiée, le workflow effectue uniquement une découverte des clés publiques et s'arrête avant toute authentification. Les clés découvertes doivent être comparées à une source OVHcloud de confiance avant leur ajout à `deploy/ovh_known_hosts`. Ne pas accepter automatiquement une nouvelle clé ou désactiver sa vérification.

Il nécessite le secret Actions `OVH_FTP_PASSWORD`, saisi directement dans GitHub par le titulaire de l'accès. Ne jamais publier un mot de passe dans le dépôt ou dans une conversation. Le mot de passe FTP est distinct de celui du Manager OVHcloud.

Le contrôle de déploiement attend **405 et Allow: POST** pour une requête GET : c'est le rejet normal d'une méthode non autorisée, et non une preuve d'envoi de mail.

## Validation avant activation du formulaire

- Vérifier HTTPS et l'exécution du PHP sur OVHcloud.
- Tester les données invalides, consentement, origine, champ piège et limitation du débit.
- Tester un envoi contrôlé et constater sa réception dans la boîte officielle, puis vérifier Reply-To.
- Compléter les mentions légales et l'information de confidentialité avec les données validées de l'éditeur.
- Afficher le formulaire seulement après validation du backend, puis tester le parcours public complet, mobile compris.

Le script déployé utilise PHPMailer 7.1.1 et le SMTP authentifié OVHcloud (`ssl0.ovh.net`, port 465, TLS). Expéditeur, enveloppe et compte SMTP : `contact@cln-performance.com`. Le prospect reste en Reply-To. Aucun repli vers `mail()`.

Le secret Actions `CLN_SMTP_PASSWORD` contient le mot de passe de la boîte officielle. Le workflow le provisionne dans `~/.cln-secrets/mail.json`, hors de `www`, dossier 0700 et fichier 0600. Les dépendances sont installées dans `~/.cln-mailer/7.1.1`. Aucun secret n'est commité ni affiché. Le workflow a ainsi accès à l'envoi via cette boîte : protéger les droits d'écriture et d'exécution du dépôt.

La réception réelle reste un critère distinct de l'acceptation SMTP. Le formulaire contient l'information de confidentialité, des liens vers les deux pages dédiées et une synthèse de diagnostic à expiration de 30 jours. Le 28 octobre 2026, le déploiement SMTP a réussi et Patrick a confirmé la réception du message de recette. Les pages légales et de confidentialité sont publiées selon les informations retenues par Patrick ; le formulaire a ensuite été activé et testé depuis son interface publique. Les contrôles complémentaires sont suivis dans MINUTE.md.

## Prévisualisation locale

```sh
python -m http.server 8000
```

Pour valider la syntaxe du backend dans un environnement équipé de PHP :

```sh
php -l contact.php
```

Une simple prévisualisation locale ne reproduit pas l'origine autorisée et le transport mail de production.

## Éléments historiques

`deploy-hostinger.yml` est limité à un lancement manuel ; il ne constitue plus la procédure de publication actuelle. `publish.ps1`, `test_mailbox.py` et les anciens exemples SMTP doivent être considérés comme historiques et vérifiés avant toute réutilisation. Ne pas lancer l'ancien déploiement Hostinger pour publier sur l'architecture actuelle.
