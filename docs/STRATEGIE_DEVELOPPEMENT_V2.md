# Stratégie de développement V2
Date : 28 octobre 2026. Périmètre : captcha, fréquence par email et quatre langues.

## Séquence
1. Lire l'état de production et sauvegarder les sources ; conserver les deux besoins initiaux dans docs.
2. Versionner l'expression détaillée et la spécification technique avant développement.
3. Construire le catalogue exhaustif FR/EN/pt-BR/ES ; préserver les informations factuelles et les exclusions légales.
4. Implémenter la sélection de langue commune et les traductions statiques ; isoler les scripts diagnostic/contact ; remplacer les synthèses HTML par des données structurées.
5. Implémenter le coeur de sécurité PHP testable : captcha authentifié/expirant, consommation unique, limites email et IP, verrou et purge.
6. Intégrer le SMTP existant et la langue dans le mail ; configurer la clé privée persistante via le SFTP existant.
7. Vérifier localement syntaxe JS et catalogues ; exécuter en CI les tests PHP, HTTP, concurrence et responsive multilingue.
8. Corriger toutes les régressions détectées avant publication. Les tests sont sur une copie isolée et ne réinitialisent jamais les quotas de production.
9. Déployer le backend réversible, vérifier challenge HTTPS et refus d'un POST sans contrôle. Publier ensuite pages, traductions, scripts et confidentialité sur main en un seul ensemble cohérent.
10. Vérifier le site public dans les quatre langues et un envoi autorisé vers contact@cln-performance.com ; vérifier sans prétendre que l'acceptation SMTP garantit la réception.
11. Mettre à jour README et MINUTE : commits, essais, preuves, limites restantes et procédure de retour arrière.

## Garde-fous
Ne pas modifier DNS, hébergement, secrets SMTP/FTP existants ou destinataire pendant ce chantier. Ne pas désactiver TLS, DKIM ou DMARC. Aucune donnée libre traduite automatiquement ; aucune identité légale inventée. La correction des quotas ne doit pas créer de journal d'adresses en clair. Les changements sensibles sont serveur, pas seulement navigateur.

## Critères de sortie
Catalogues complets et accessibles ; règles du diagnostic inchangées ; absence de perte de saisies lors du changement de langue ; refus serveur des captchas et quotas contournés ; contrôles concurrents réussis ; tests CI verts ; frontend et backend effectivement déployés ; retour arrière disponible et suivi à jour.

## Gestion des limites
Signaler explicitement les vérifications qui ne peuvent pas être conclues (réception humaine, qualité linguistique par un locuteur natif, téléphone physique). Ne pas confondre tests simulés et attestation de conformité ou protection absolue contre les robots.
