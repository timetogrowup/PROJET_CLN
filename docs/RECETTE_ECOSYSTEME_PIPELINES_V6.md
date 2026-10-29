# Recette V6 — Écosystème et pipelines

Date : 29 octobre 2026. Statut : livré et vérifié en production.

## Réalisation
Les six pages commerciales, la confirmation et le message commun des dix pages ont été revus en quatre langues. L’accueil présente dès son introduction les pipelines, l’existant, l’enrichissement progressif et la valeur dans les applications destinataires. Les trois exemples précisent les sources, les enrichissements et les destinations. Méthode et FAQ privilégient les interfaces existantes et une réalisation sans modification des outils lorsque possible ; une évolution indispensable doit être limitée et justifiée.

Les questionnaires, recommandations, titres et descriptions suivent ce positionnement. Les anciennes ancres restent accessibles. Les pages légales conservent leur contenu réglementaire et de confidentialité ; leur pied de page commun est actualisé.

## Prévention d’une régression
Les nouveaux libellés changent la signification des choix de questionnaire. La version de synthèse passe donc de 4 à 6 : les anciennes réponses ne sont pas réinterprétées avec les nouveaux libellés. Une ancienne synthèse peut être effacée et propose de refaire le point. Le transfert et l’ajout au message restent volontaires ; aucune saisie visiteur n’est traduite.

## Sources et preuves
- Documents initiaux : 978648be88378a70e4825122ae20979ee8707ef7.
- Candidat : ed622eede0de77be0b59a918912c924f546f3dfe.
- CI : https://github.com/timetogrowup/PROJET_CLN/actions/runs/40873607848.
- Architecture : GitHub Pages et API PHP OVH conservées ; aucune nouvelle dépendance de production ni nouvelle collecte.

## Contrôles locaux réalisés
Dix pages et 195 références locales/ancres valides ; métadonnées, navigation, cibles d’évitement et traductions visibles complètes. Catalogues : 522 entrées statiques et 133 messages dynamiques, quatre langues et paramètres complets. Contrôles ciblés V6 : promesse au premier écran, enrichissement, destinations et isolation des synthèses anciennes. Génération répétée identique ; syntaxe JavaScript et absence d’erreurs d’espacement vérifiées.

PHP est absent de l’environnement local : les contrôles PHP et HTTP sont exécutés dans GitHub Actions, avec les tests navigateur Chromium/WebKit.

## Limites
Aucun email réel envoyé. Les scénarios sont illustratifs, aucun système client n’est connecté. Pas d’essai sur téléphone physique ni de validation par lecteur d’écran ou prospects. La qualité rédactionnelle des traductions pourra être affinée par des locuteurs natifs. La faisabilité d’une connexion et la valeur produite restent à qualifier par mission.

## CI complète réussie
Exécution 40873607848 sur le commit ed622eede0de77be0b59a918912c924f546f3dfe : toutes les étapes sont réussies.

| Contrôle | Résultat |
|---|---|
| PHP et sécurité | Syntaxe, 26 contrôles dont concurrence, tests HTTP/CORS/redirections et jeton humain |
| Catalogues et structure | 522 textes statiques, 133 messages dynamiques, dix pages, 195 références et critères V6 |
| Fenêtre humaine | Chromium et WebKit : affichage différé, annulation, clavier, erreur réseau, expiration et soumission simulée |
| Responsive | 400 affichages : dix pages × quatre langues × cinq largeurs × deux moteurs |
| Questionnaire et transfert | 42 assertions : choix, synthèse, consentement, anciennes versions, expiration, texte visiteur, erreur de stockage |
| Parcours pipelines | 84 assertions : étapes, langues, clavier, navigation, méthode et contact ; aucune requête tierce |

Publication lancée par promotion de main au SHA attendu ; aucun historique réécrit. Workflow Pages : https://github.com/timetogrowup/PROJET_CLN/actions/runs/40874180979.

## Publication et vérification publique
[Publication Pages 40874180979](https://github.com/timetogrowup/PROJET_CLN/actions/runs/40874180979) terminée avec succès. Le code livré est ed622eede0de77be0b59a918912c924f546f3dfe.

Dix pages, trois scripts, la feuille de style, les deux catalogues et le sitemap : dix-sept ressources publiques répondent HTTP 200 en HTTPS normal et correspondent octet par octet aux fichiers V6 testés, avec paramètre de version et demande sans cache.

Le navigateur public a confirmé le nouvel accueil et sa présentation visuelle, puis le lien vers l’exemple, ses cinq étapes, les enrichissements successifs et les applications destinataires. Aucun formulaire de production soumis.

A01 à A08 : critères techniques et éditoriaux réalisés et contrôlés. La compréhension par de nouveaux lecteurs reste à évaluer séparément. La clôture documentaire ne modifie aucun fichier exécutable.
