#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
set_ppt_language_batch.py
-------------------------
Script Python "tout-en-un" SANS PARAMÈTRES CLI.
-> Modifie simplement les variables ci-dessous.

Fonctions :
- Écrit un script PowerShell localement (COM PowerPoint).
- Parcourt tous les .pptx du dossier visé (optionnellement récursif).
- Applique la langue de vérification (FR/EN) sur TOUT le contenu : zones de texte, tableaux, SmartArt, masques, notes.
- Sauvegarde une COPIE suffixée '.lang.<LANG>.pptx' OU remplace l'original (selon OVERWRITE_ORIGINAL).

PRÉ-REQUIS :
- Windows + Microsoft PowerPoint (application de bureau) installé.
- PowerShell (pwsh ou powershell) accessible.
- Python 3.8+.

⚠️ Environnement d’entreprise : si COM/Office est bloqué par la politique IT, contacte l’IT.
"""

import os
import sys
import shutil
import tempfile
import subprocess
from textwrap import dedent

# ===========================
# 🔧 VARIABLES À ADAPTER ICI
# ===========================
LANGUAGE = "fr-FR"           # "fr-FR" | "en-US" | "en-GB"
MODE = "all"                 # "all" (tout en LANGUAGE) | "bilingual" (les slides dont le Titre matche EN_PATTERN seront en en-US)
EN_PATTERN = r"(^EN\b)|(\bEN$)|(\[EN\])|(\(EN\))"  # utilisé si MODE == "bilingual"

BASE_DIR = os.getcwd()       # Dossier de départ : par défaut le dossier courant.
RECURSIVE = True             # True = traite aussi les sous-dossiers ; False = juste BASE_DIR

OVERWRITE_ORIGINAL = False   # False = crée une copie .lang.<LANG>.pptx ; True = remplace l’original
# ===========================


PS1_CONTENT = dedent(r'''
param(
    [Parameter(Mandatory=$true)]
    [string]$InputPptx,
    [string]$OutputPptx = "",
    [ValidateSet("fr-FR","en-US","en-GB")]
    [string]$Language = "fr-FR",
    [ValidateSet("all","bilingual")]
    [string]$Mode = "all",
    # Utilisé en mode "bilingual" pour détecter les slides EN (titre contient l’un de ces motifs)
    [string]$EnTitlePattern = "(^EN\b)|(\bEN$)|(\[EN\])|(\(EN\))"
)

# --- Mappage LCID (PowerPoint attend des LCID numériques)
$lcidMap = @{
    "fr-FR" = 1036  # msoLanguageIDFrench
    "en-US" = 1033  # msoLanguageIDEnglishUS
    "en-GB" = 2057  # msoLanguageIDEnglishUK
}
$lcidDefault = $lcidMap[$Language]
if (-not $lcidDefault) { throw "Langue non supportée: $Language" }

if ([string]::IsNullOrWhiteSpace($OutputPptx)) {
    $OutputPptx = [IO.Path]::ChangeExtension($InputPptx, ".lang.$($Language).pptx")
}

function Set-ShapeLanguage {
    param($shape, [int]$lcid)
    try {
        # Groupes
        if ($shape.Type -eq 6 -and $shape.GroupItems -ne $null) { # msoGroup
            foreach ($g in $shape.GroupItems) { Set-ShapeLanguage -shape $g -lcid $lcid }
        }

        # Zones de texte
        if ($shape.HasTextFrame -and $shape.TextFrame.HasText) {
            $shape.TextFrame.TextRange.LanguageID = $lcid
        }

        # Tableaux
        if ($shape.HasTable) {
            $rows = $shape.Table.Rows.Count
            $cols = $shape.Table.Columns.Count
            for ($r=1; $r -le $rows; $r++) {
                for ($c=1; $c -le $cols; $c++) {
                    $cellShape = $shape.Table.Cell($r,$c).Shape
                    if ($cellShape.TextFrame.HasText) {
                        $cellShape.TextFrame.TextRange.LanguageID = $lcid
                    }
                }
            }
        }

        # SmartArt (best effort)
        if ($shape.SmartArt -ne $null) {
            foreach ($node in $shape.SmartArt.AllNodes) {
                $tf2 = $node.TextFrame2
                if ($tf2 -and $tf2.HasText -ne $false) {
                    $tf2.TextRange.LanguageID = $lcid
                }
            }
        }
    } catch {
        # on ignore les éléments non textuels / non accessibles
    }
}

function Set-SlideLanguage {
    param($slide, [int]$lcid)
    foreach ($s in $slide.Shapes) { Set-ShapeLanguage -shape $s -lcid $lcid }
}

# --- Ouvre PowerPoint (COM)
$pp = New-Object -ComObject PowerPoint.Application
$pp.Visible = [Microsoft.Office.Core.MsoTriState]::msoTrue
$pp.DisplayAlerts = [Microsoft.Office.Core.MsoTriState]::msoFalse

$pres = $pp.Presentations.Open($InputPptx, $false, $false, $false)

# Masques (pour hériter aux nouvelles zones)
try {
    foreach ($s in $pres.SlideMaster.CustomLayouts) {
        foreach ($sh in $s.Shapes) { Set-ShapeLanguage -shape $sh -lcid $lcidDefault }
    }
    foreach ($sh in $pres.SlideMaster.Shapes) { Set-ShapeLanguage -shape $sh -lcid $lcidDefault }
} catch {}

# Slides
foreach ($slide in $pres.Slides) {
    $lcidForSlide = $lcidDefault

    if ($Mode -eq "bilingual") {
        # Si le titre de la diapo match le motif EN → anglais US
        try {
            $title = $slide.Shapes.Title.TextFrame.TextRange.Text
        } catch { $title = "" }
        if ($title -match $EnTitlePattern) { $lcidForSlide = $lcidMap["en-US"] }
    }

    Set-SlideLanguage -slide $slide -lcid $lcidForSlide
}

# Notes & Masques des pages de notes
try {
    foreach ($slide in $pres.Slides) {
        foreach ($sh in $slide.NotesPage.Shapes) { Set-ShapeLanguage -shape $sh -lcid $lcidDefault }
    }
} catch {}

# Sauvegarde
$pres.SaveCopyAs($OutputPptx)
$pres.Close()
$pp.Quit()

Write-Host "✅ Langue appliquée. Fichier : $OutputPptx"
''').strip()


def find_powershell():
    """Trouve pwsh/powershell."""
    candidates = [
        shutil.which("pwsh"),
        shutil.which("powershell"),
        r"C:\Program Files\PowerShell\7\pwsh.exe",
        r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
    ]
    for c in candidates:
        if c and os.path.exists(c):
            return c
    return None


def write_ps1(temp_dir):
    """Écrit le PS1 temporaire et retourne son chemin."""
    ps1_path = os.path.join(temp_dir, "Set-PptLanguage.ps1")
    with open(ps1_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(PS1_CONTENT)
    return ps1_path


def list_pptx_files(base_dir, recursive=True):
    """Liste les fichiers .pptx à traiter."""
    pptx_files = []
    if recursive:
        for root, _, files in os.walk(base_dir):
            for name in files:
                if name.lower().endswith(".pptx"):
                    pptx_files.append(os.path.join(root, name))
    else:
        for name in os.listdir(base_dir):
            if name.lower().endswith(".pptx"):
                pptx_files.append(os.path.join(base_dir, name))
    return sorted(pptx_files)


def run_ps_for_file(ps_exe, ps1_path, input_path, output_path, language, mode, en_pattern):
    """Exécute PowerShell pour un fichier donné."""
    cmd = [
        ps_exe,
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "-File", ps1_path,
        "-InputPptx", input_path,
        "-OutputPptx", output_path,
        "-Language", language,
        "-Mode", mode,
        "-EnTitlePattern", en_pattern
    ]
    print("   ▶", os.path.basename(input_path))
    # On capture les sorties pour afficher des erreurs propres si besoin
    completed = subprocess.run(cmd, capture_output=True, text=True)
    if completed.stdout:
        print("     ", completed.stdout.strip())
    if completed.returncode != 0:
        if completed.stderr:
            print("     ❌", completed.stderr.strip())
        return False
    return True


def main():
    print("=== Batch PowerPoint Language Setter ===")
    print(f"- Dossier     : {BASE_DIR}")
    print(f"- Récursif    : {RECURSIVE}")
    print(f"- Langue      : {LANGUAGE}")
    print(f"- Mode        : {MODE}")
    if MODE == "bilingual":
        print(f"- Motif EN    : {EN_PATTERN}")
    print(f"- Remplacement original : {OVERWRITE_ORIGINAL}")
    print("=======================================\n")

    if not os.path.isdir(BASE_DIR):
        print(f"❌ Dossier introuvable : {BASE_DIR}", file=sys.stderr)
        sys.exit(2)

    ps_exe = find_powershell()
    if not ps_exe:
        print("❌ PowerShell introuvable. Installe pwsh/powershell et réessaie.", file=sys.stderr)
        sys.exit(3)

    files = list_pptx_files(BASE_DIR, RECURSIVE)
    if not files:
        print("Aucun fichier .pptx trouvé. Rien à faire.")
        return

    with tempfile.TemporaryDirectory(prefix="ppt_lang_batch_") as tdir:
        ps1_path = write_ps1(tdir)

        ok = 0
        ko = 0
        for f in files:
            folder = os.path.dirname(f)
            name, ext = os.path.splitext(os.path.basename(f))

            if OVERWRITE_ORIGINAL:
                # On crée une sortie temporaire, puis on remplace l'original
                out_tmp = os.path.join(folder, f"{name}.tmp.lang.{LANGUAGE}{ext}")
                success = run_ps_for_file(ps_exe, ps1_path, f, out_tmp, LANGUAGE, MODE, EN_PATTERN)
                if success:
                    # Remplacement atomique
                    try:
                        backup = f + ".bak"
                        if os.path.exists(backup):
                            os.remove(backup)
                        os.replace(f, backup)      # sauvegarde
                        os.replace(out_tmp, f)      # remplace
                        os.remove(backup)           # supprime la sauvegarde si tout va bien
                        print(f"     ✅ Remplacé : {f}")
                        ok += 1
                    except Exception as e:
                        print(f"     ❌ Échec remplacement : {e}")
                        ko += 1
                else:
                    # En cas d'échec, on nettoie le tmp si présent
                    try:
                        if os.path.exists(out_tmp):
                            os.remove(out_tmp)
                    except:
                        pass
                    ko += 1
            else:
                # On génère une COPIE suffixée
                out_copy = os.path.join(folder, f"{name}.lang.{LANGUAGE}{ext}")
                success = run_ps_for_file(ps_exe, ps1_path, f, out_copy, LANGUAGE, MODE, EN_PATTERN)
                if success:
                    print(f"     ✅ Copie générée : {out_copy}")
                    ok += 1
                else:
                    ko += 1

    print("\n=== Résumé ===")
    print(f"  ✅ Réussis : {ok}")
    print(f"  ❌ Échecs : {ko}")
    if ko > 0:
        print("\nConseils si erreurs COM/Office :")
        print(" - Ferme PowerPoint avant d’exécuter le script.")
        print(" - Vérifie que PowerPoint (version desktop) est installé.")
        print(" - Si COM/Office est bloqué par la politique IT, demande une autorisation ou utilise un poste autorisé.")


if __name__ == "__main__":
    main()
