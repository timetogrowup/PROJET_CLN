# Spécifications techniques — Démarche CLN — V12
Date : 30 octobre 2026. Statut : réalisé et vérifié.

## Architecture et composants
Site statique conservé, aucun nouvel appel réseau métier ni bibliothèque. Nouveau module scripts/approach_diagnostic.py appelé à la fin de build_pedagogy.py, après V11 et avant écriture finale des catalogues. Il remplace uniquement main, titre et description de approche.html et lui ajoute une classe de page dédiée. Conserver header/footer V11 et les cinq entrées. CSS dédié dans styles.css, cache V12 sur cette page uniquement. Aucun JavaScript nouveau et aucun média lourd.

## Structure
Section d'introduction à deux colonnes : promesse, conditions/CTA et encadré livrables. Section d'engagements ; section #pipeline avec liste ordonnée à quatre étapes et détails techniques natifs ; section IA à deux colonnes ; section #remuneration avec premier niveau court et détails ; FAQ et CTA final. Conserver les ancres entrantes #pipeline et #remuneration. Un H1, H2 de sections et H3 des étapes/blocs. Les détails reposent sur details/summary sans script, focus visible et commandes natives.

## Données et interfaces
Éditorial FR dans le HTML, trois traductions dans i18n/static.json via helper du module. site.js existant pour choix de langue, propagation aux liens et métadonnées. Pas de saisie ni persistance nouvelle. CTA diagnostic.html conservant la langue via le mécanisme V11. Contact/PHP/SMTP et scripts de questionnaire inchangés.

## Contraintes
Conserver l'identité et les couleurs du site. Colonnes et grille de quatre étapes avec repli en une colonne sur téléphone ; aucune ligne de schéma imposant un défilement horizontal. Sans animations nouvelles, GIF ROI laissé sur l'accueil. Ne pas masquer les conditions du diagnostic ni les limites de la proposition derrière les détails. Confidentialité des usages IA évoquée sans inventer de fournisseur ou de certification.

## Vérifications
- Génération idempotente des dix pages et des deux catalogues ; nouvelle page seule modifiée hors styles/catalogue.
- Syntaxe Python ; catalogue et liens/métadonnées des dix pages ; ancres, deux CTA principaux, quatre étapes, deux usages IA et détails.
- Adapter l'ancienne assertion interdisant « chirurgicale » sur approche.html à la nouvelle décision métier ; conserver ses autres contrôles.
- Non-régression du questionnaire/contact V11 et accueil V10 par tests existants appropriés, sans email réel.
- Chrome : quatre langues, présentation, ouverture au clavier des détails, CTA vers questionnaire, retour, ancres, tailles disponibles et absence de débordement.
- Publication GitHub Pages, statut et empreintes des fichiers publics, lecture des quatre langues sur domaine. Documenter toute limite Safari/appareils physiques.

## Livraison effective — 30 octobre 2026
Version applicative `163b615b517eb41d4ef5a1c029094ebf97497f36` publiée avec succès sur GitHub Pages, [exécution 41087397831](https://github.com/timetogrowup/PROJET_CLN/actions/runs/41087397831), première tentative. Page : https://cln-performance.com/approche.html?lang=fr .

Livré : diagnostic/conditions/livrables visibles, trois engagements, quatre étapes statiques, deux usages de l'IA, investissement/rémunération en lecture progressive, FAQ et deux CTA. Quatre langues, détails natifs au clavier, ancres #pipeline et #remuneration conservées. Aucun nouveau JavaScript, média ou traitement serveur ; autres pages conservées.

Contrôles : catalogues 714/200, dix pages et 186 références, génération idempotente et régressions pertinentes V7–V11. Chrome : quatre langues, détails au clavier, CTA avec langue, seize dispositions sans débordement et lecture sans JavaScript. Six fichiers publics HTTP 200 et SHA-256 identiques ; contenu, liens et ancres vérifiés sur le domaine. Safari/WebKit et téléphones physiques non testés. Détails : [rapport de recette](RECETTE_DIAGNOSTIC_INTERVENTION_V12.md).
