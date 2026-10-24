# Migration CLN vers GitHub Pages (préparation)

Ce dossier prépare la migration du site vers GitHub Pages avec le futur domaine `cln-performance.fr`.

## Avant publication
1. Acheter et activer `cln-performance.fr` chez OVHcloud.
2. Activer et tester la messagerie `patrick.lyonnet@cln-performance.fr` chez OVHcloud. **Ne pas considérer cette adresse comme opérationnelle avant les tests d'envoi et réception.**
3. Choisir un service de traitement des formulaires compatible avec un site statique et configurer la destination des demandes, la validation et la protection anti-spam.
4. Adapter `contact.html` pour supprimer la dépendance à `contact.php`, et tester le parcours diagnostic → contact.
5. Dans GitHub > Settings > Pages, configurer la publication de `main` (racine), après validation de la branche de migration.
6. Configurer le domaine personnalisé dans GitHub Pages, puis les DNS web chez OVHcloud selon les valeurs officielles indiquées par GitHub. Conserver les MX, SPF, DKIM, DMARC et autres enregistrements liés au courrier.
7. Attendre l'activation HTTPS et tester le site sur mobile et ordinateur.

## Points de vigilance
- GitHub Pages n'exécute pas PHP : `contact.php` ne fonctionnera pas en production.
- Ne pas basculer le formulaire vers une boîte qui n'existe pas encore.
- Ne pas créer un fichier `CNAME` ni basculer les DNS tant que le domaine n'est pas acquis.
- Le workflow `deploy-hostinger.yml` est historique et doit être désactivé/supprimé lors de la mise en production GitHub Pages.
- Le domaine historique `cln-solutions.fr` et son adresse e-mail ne sont pas transférés automatiquement vers `cln-performance.fr`.
- Éviter d'afficher un numéro de téléphone ou un lien LinkedIn fictif sur le site public.
