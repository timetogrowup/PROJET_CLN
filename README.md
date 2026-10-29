> Actualisation V6 — 29 octobre 2026 : le positionnement commercial courant valorise le SI existant par les pipelines et l’enrichissement des données dans les applications destinataires. Voir [MINUTE](MINUTE.md) et la [recette V6](docs/RECETTE_ECOSYSTEME_PIPELINES_V6.md). Les descriptions antérieures ci-dessous restent historiques lorsqu’elles divergent.

# Mise à jour V5 du 29 octobre 2026

Les pipelines deviennent un savoir-faire visible de CLN Performance : bloc sur l’accueil, page [Nos pipelines en action](https://cln-performance.com/pipelines.html), cinq étapes, gestion des exceptions, rôle humain et lien avec les bénéfices constatés. Menu de sept liens et quatre langues. Les éléments V4 restent applicables.

Documents : [besoin métier V5](docs/BESOIN_METIER_PIPELINES_V5.md), [spécifications V5](docs/SPECIFICATIONS_TECHNIQUES_PIPELINES_V5.md), [stratégie V5](docs/STRATEGIE_DEVELOPPEMENT_PIPELINES_V5.md), [recette V5](docs/RECETTE_PIPELINES_V5.md).

Le générateur `python3 scripts/build_pedagogy.py` utilise désormais `scripts/pipeline_content.py`. La matrice navigateur couvre dix pages ; `tests/pipelines.mjs` vérifie le nouveau parcours. Les sections V4 et antérieures ci-dessous sont conservées comme historique.

---

# CLN Performance

## Version pédagogique V4 du 29 octobre 2026

Site statique publié sur GitHub Pages : https://cln-performance.com. API de contact OVHcloud conservée. Navigation orientée besoins, exemples illustratifs, questionnaire quotidien et transfert volontaire de synthèse. CLN privilégie une amélioration durable et l’autonomie du client ; une rémunération liée aux bénéfices effectivement constatés peut être convenue, sans revenu récurrent recherché.

Documents : [besoin métier](docs/BESOIN_METIER_PEDAGOGIE_BENEFICES_V4.md), [spécifications techniques](docs/SPECIFICATIONS_TECHNIQUES_PEDAGOGIE_V4.md), [stratégie](docs/STRATEGIE_DEVELOPPEMENT_PEDAGOGIE_V4.md), [référence des pages V2](docs/REFERENCE_DESCRIPTION_PAGES_V2.md), [recette V4](docs/RECETTE_PEDAGOGIE_V4.md).

Maintenance : `python3 scripts/build_pedagogy.py` régénère les contenus éditoriaux et leurs traductions. Contrôles : `node tests/i18n.mjs`, `python3 tests/pedagogy_static.py`, tests PHP et navigateur dans le workflow de vérification. Les tests navigateur utilisent une API simulée et ne doivent jamais envoyer de mail réel.

Les sections antérieures ci-dessous sont historiques, notamment les références à Hostinger et à cln-solutions.fr.

---

# CLN Performance

Site vitrine CLN — Ciblé, Libéré, Normé.

## Version V3 — 28 octobre 2026

Le calcul a été supprimé. Après validation des champs, « Envoyer la demande » ouvre une fenêtre « Vérification humaine » avec case « Je suis un humain », confirmation et annulation. Position variable bornée sur ordinateur, centrage sur petit écran, clavier et quatre langues. Autorisation signée à usage unique demandée uniquement à l’ouverture ; les limites email/IP restent appliquées. Il s’agit d’une déclaration, pas d’une preuve d’humanité.

[Besoin V3](docs/BESOIN_CONFIRMATION_HUMAINE_V3.md) · [Expression détaillée](docs/EXPRESSION_BESOIN_DETAILLEE_V3.md) · [Spécification](docs/SPECIFICATION_TECHNIQUE_V3.md) · [Stratégie](docs/STRATEGIE_DEVELOPPEMENT_V3.md) · [Recette et publication](docs/RECETTE_PRODUCTION_V3.md).

## Historique V2 — 28 octobre 2026

Sélecteur FR (défaut), EN, pt-BR et ES sur les neuf pages, diagnostic et messages du formulaire compris. La langue suit les liens et reste mémorisée ; les saisies libres restent inchangées. Traductions côté navigateur avec JavaScript.

Captcha signé, valable dix minutes et utilisable une seule fois. Vérification PHP : dix minutes entre deux demandes par email, trois par heure ; contrôle IP complémentaire (une par minute, cinq par heure, trente tentatives par heure). Compteurs privés sous verrou avec empreintes HMAC.

[Besoins détaillés](docs/EXPRESSION_BESOIN_DETAILLEE_V2.md) · [Spécification](docs/SPECIFICATION_TECHNIQUE_V2.md) · [Stratégie](docs/STRATEGIE_DEVELOPPEMENT_V2.md) · [Recette et retour arrière](docs/RECETTE_PRODUCTION_V2.md).

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

