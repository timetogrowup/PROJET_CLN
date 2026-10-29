# Spécifications techniques V6 — Écosystème et pipelines

Date : 29 octobre 2026. Architecture conservée : HTML/CSS/JavaScript statiques sur GitHub Pages, domaine cln-performance.com ; formulaire vers API PHP OVHcloud existante.

## Composants et données
Les sources éditoriales sont scripts/build_pedagogy.py et scripts/pipeline_content.py. Elles génèrent les pages HTML et les catalogues i18n/static.json et i18n/messages.json. Modifier les sources avant génération ; conserver le template contact V3, les identifiants DOM, ancres et paramètres d’URL.
Les messages dynamiques de synthèse v4.rec.* et les libellés des réponses évoluent ensemble. Les identifiants internes et le format structuré restent conservés ; la version de synthèse passe à 6 pour empêcher de réinterpréter les réponses V4 avec les nouveaux libellés ; les codes historiques ne servent pas de texte commercial. Une ancienne synthèse reste effaçable et un lien propose de la refaire ; aucun ajout automatique au message. Aucun nouveau champ personnel ni interface réseau.

## Interfaces et contraintes
Conserver site.js, diagnostic.js, contact.js et le contrat de l’API ; les accès et protections OVH ne sont pas modifiés. Actualiser la version de cache des ressources et des catalogues. Une seule traduction pour chaque texte visible dans chacune des trois langues supplémentaires. Les mentions et la politique de confidentialité gardent leurs obligations ; seul le pied de page commun change.
Le schéma des cinq étapes reste une liste HTML accessible sans animation, utilisable sur mobile ; l’enrichissement et les destinataires sont explicités dans les textes. Un outil indisponible ou une donnée manquante reste signalé ; pas de promesse de reprise universelle.

## Tests et livraison
1. Syntaxe Python/JS/PHP et catalogues complets ; liens et ancres des dix pages.
2. Contrôles ciblés de la promesse V6 et des recommandations ; double génération identique.
3. Régressions existantes : sécurité PHP/HTTP, dialogue humain, synthèse et transfert, parcours pipeline et matrice responsive quatre langues/deux moteurs.
4. CI sur branche feature/cln-v6-ecosysteme avant promotion main avec contrôle du SHA attendu.
5. Vérifier le workflow Pages et les ressources effectivement servies ; contrôler au minimum accueil, pipelines, contact et catalogues. Ne pas soumettre le formulaire réel.

Retour arrière : rétablir par un nouveau commit les sources éditoriales et fichiers générés de la version précédente ; aucun changement de schéma ni migration de données. Journaliser résultats réellement obtenus et limites dans RECETTE_ECOSYSTEME_PIPELINES_V6.md et MINUTE.md.

## État livré
Implémentation et vérifications conformes au présent périmètre ; SHA ed622eede0de77be0b59a918912c924f546f3dfe, CI 40873607848 et Pages 40874180979 réussies. La recette détaille les 17 ressources conformes et les limites. Pas de modification de l’API ni des données personnelles collectées.
