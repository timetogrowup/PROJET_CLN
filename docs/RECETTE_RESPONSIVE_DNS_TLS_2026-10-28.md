# Contrôles complémentaires CLN Performance — 28 octobre 2026

## Résultat

Le site et le formulaire restent fonctionnels. La recette responsive a détecté puis permis de corriger un débordement de navigation sur tablette. DKIM est actif et DMARC a été ajouté en observation. Les certificats HTTPS sont valides.

## Affichage mobile et tablette

- Première exécution : https://github.com/timetogrowup/PROJET_CLN/actions/runs/40757946230
- Résultat initial : 54 cas sans débordement ; 18 débordements à 768 px (menu/CTA d'en-tête) sur neuf pages, dans Chromium et WebKit.
- Correction : navigation réorganisée jusqu'à 1024 px, version de styles 20261028-3 ; commit 429b0026d6e38c8b4d85c583987ac0ece84cbbb7.
- Nouvelle exécution : https://github.com/timetogrowup/PROJET_CLN/actions/runs/40758870893
- Résultat : **144/144 cas réussis**, neuf pages × huit largeurs (320, 375, 390, 768, 820, 1024, 1100, 1280) × deux moteurs (Chromium et WebKit).
- Contrôles : pas de débordement horizontal, navigation visible, formulaire actif, synthèse vide et piège antispam masqués ; validation native des champs requis empêchant l'envoi vide.
- Simulation sur une copie locale des sources du commit ; aucune utilisation de session utilisateur ni envoi de mail.
- Limites : ces tests de géométrie et visibilité ne remplacent pas la revue visuelle sur appareils physiques, l'audit complet d'accessibilité ou la comparaison pixel par pixel.

## Messagerie

- MX publics : 1 mx1.mail.ovh.net, 5 mx2.mail.ovh.net, 100 mx3.mail.ovh.net.
- SPF : v=spf1 include:mx.ovh.com -all.
- DKIM : activation confirmée par le Manager OVHcloud ; deux CNAME présents et clés publiques résolues. Pas de désactivation effectuée.
- ovhmo-selector-1._domainkey vers ovhmo-selector-1._domainkey.5052001.av.dkim.mail.ovh.net.
- ovhmo-selector-2._domainkey vers ovhmo-selector-2._domainkey.5052002.av.dkim.mail.ovh.net.
- La présence des clés et l'état Manager ne constituent pas une vérification cryptographique de tous les messages reçus. Lecture des en-têtes d'un message conservée comme contrôle supplémentaire.
- DMARC absent initialement ; ajout confirmé dans le Manager (zone de 26 à 27 entrées) et par résolution DNS publique :
  - Nom : _dmarc.cln-performance.com
  - Type : TXT
  - Valeur : v=DMARC1; p=none; rua=mailto:contact@cln-performance.com
- Politique d'observation, sans demande de rejet DMARC ; rapports agrégés destinés à la boîte officielle, sans rapports forensiques.
- Aucun changement des A/AAAA, MX, SPF, DKIM ni des paramètres de confidentialité du domaine.
- L'analyse de rapports précède une éventuelle politique quarantine/reject ; aucune de ces politiques strictes n'est activée dans cette intervention.

## HTTPS

Validation réelle du certificat, du nom d'hôte et de la chaîne de confiance par le runtime GitHub Actions :
- cln-performance.com : Let's Encrypt YR1, expiration le 24 janvier 2027 à 17:30:31 UTC.
- api.cln-performance.com : Let's Encrypt YE2, expiration le 24 janvier 2027 à 19:11:59 UTC.
- Environ 88 jours restants au contrôle. Certificat de l'API également montré Active dans le Manager.
- Aucun certificat renouvelé manuellement ou commandé. Le contrôle manuel scripts/check_tls.py échoue si l'échéance est à 14 jours ou moins ; aucun contrôle récurrent n'a été programmé.
- Hébergement Starter actif et renouvellement automatique de l'abonnement indiqué au 25 octobre 2027 ; cela ne doit pas être confondu avec la date du certificat.

## Domaine et formalité de validation

- Domaine : Registered et Active dans le Manager.
- Renouvellement automatique du domaine confirmé pour le 26 octobre 2027.
- DNSSEC et protection contre le transfert indiqués activés, sans modification.
- Aucune opération de domaine en cours affichée.
- Message OVHcloud du 26 octobre demandant la validation de l'adresse du titulaire avant le 10 décembre 2026 retrouvé. Aucun code ou lien de validation n'est copié ici.
- Aucune preuve explicite de validation de cette adresse n'a été trouvée : le statut actif du domaine et l'absence d'opération en cours ne suffisent pas à conclure.
- Action restant au titulaire : vérifier le message OVHcloud et accomplir la confirmation si elle n'a pas déjà été réalisée.

## Références de méthode

- https://docs.ovhcloud.com/fr/guides/web-cloud/domains/dns-zone-dkim
- https://docs.ovhcloud.com/fr/guides/web-cloud/domains/dns-zone-dmarc
- https://docs.ovhcloud.com/fr/guides/web-cloud/web-hosting/ssl-letsencrypt
- https://playwright.dev/docs/emulation
