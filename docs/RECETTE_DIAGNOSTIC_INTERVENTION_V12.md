# Recette — Page Comment nous travaillons — V12
Date : 30 octobre 2026. Statut : recette locale réussie, publication en préparation.

## Réalisation
Page reconstruite autour d'un diagnostic initial en quelques jours et de conditions visibles : périmètre défini, interlocuteurs/informations disponibles, calendrier de réalisation convenu ensuite. Livrables affichés au premier niveau. Intervention chirurgicale peu invasive, trois engagements, quatre étapes statiques, deux usages de l'IA, investissement et rémunération avec détails dépliables, FAQ et deux CTA vers le questionnaire. Ancres #pipeline et #remuneration préservées. Quatre langues, aucun média ou JavaScript ajouté. Les autres pages et les services de contact sont inchangés.

## Contrôles exécutés
- python tests/approach_static.py : succès, diagnostic/conditions/livrables, ordre des sections, quatre étapes, deux CTA, quatre détails natifs, IA et garde-fous, ancres/menu, génération idempotente.
- node tests/i18n.mjs : succès, 714 entrées statiques et 200 messages dynamiques, langues et paramètres complets.
- python tests/pedagogy_static.py : succès, dix pages et 186 références/ancres locales, métadonnées, H1, traductions et cinq liens de navigation. L'interdiction historique de « chirurgicale » est adaptée à la décision approuvée sur l'accueil et la méthode ; les autres invariants restent actifs.
- python tests/case_static.py et node tests/case-journey.mjs : succès, parcours V11, conservation/édition des réponses et gestion des erreurs/versions, sans réseau ni email.
- python tests/home_roi_static.py ; node tests/brand-motion.mjs ; node tests/pipeline-animation.mjs : succès, accueil V10, médias/échelles/génération et lecteurs V7–V10 préservés.
- Compilation Python du module et git diff --check : succès.

## Recette Chrome de l'aperçu
- FR/EN/PT-BR/ES : titres traduits, quatre étapes, lien final vers le questionnaire avec langue conservée, aucune extension horizontale.
- Ouverture de détails techniques par Entrée dans les quatre langues : succès.
- Premier écran et schéma de méthode inspectés visuellement : hiérarchie claire, livrables en encadré, étapes numérotées statiques.
- Seize fenêtres intégrées : quatre langues × 320/390/768/1280 px (largeurs utiles 305/375/753/1265 px). Aucun débordement.
- Sans JavaScript : fenêtre de 390 px, contenu français présent et détails natifs ouverts au clavier ; aucun débordement.

## Limites
Chrome disponible ; Safari/WebKit et appareils physiques non testés dans cette recette. Les fenêtres intégrées contrôlent les mises en page CSS sans simuler un appareil réel. Aucun test d'email réel, les traitements du questionnaire/contact et PHP n'étant pas modifiés. Les délais, coûts et gains restent cadrés par projet ; aucun chiffre financier ajouté.

## Publication
En préparation ; références et vérifications publiques à compléter après déploiement.
