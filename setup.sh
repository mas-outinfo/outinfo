#!/bin/bash
# ------------------------------------------------------------------------------
# SCRIPT DE CONFIGURATION POUR L'ENVIRONNEMENT WWW DES ETUDIANTS AU CREMI
# ------------------------------------------------------------------------------

# Les 5 variables suivantes sont à modifier selon les UE
UE="outinfo" # nom de l'UE (= nom du dossier créé à la racine du compte)
CODE="OI" # code de l'UE = préfixe utilisé pour le token (= dossier secret)
DIRS="BONUS PROJET TP1 TP2" # noms des sous-dossiers à créer
MAIL="mas.outinfo@gmail.com" # adresse pour l'envoi du mail
BASE="https://www.labri.fr/perso/schlick/$UE" # URL de l'archive à récupérer

TOKEN="$CODE-$(cat /dev/urandom | tr -dc 'A-Z' | head -c 5)" # token secret
WWW="/net/www/$USER" # chemin d'accès à l'espace www de l'étudiant
OLD="$(find $WWW -name $CODE-*)" # recherche d'un ancien dossier éventuel
NEW="$WWW/$TOKEN" # nom du nouveau dossier secret

echo "Installation des fichiers"
wget -q $BASE/$UE.zip -O $UE.zip # récupération de l'archive
unzip -oq $UE.zip -d $HOME/$UE # décompression de l'archive
rm $UE.zip # suppression de l'archive
chmod 755 $HOME/$UE/*.desktop # modification des raccourcis
mv $HOME/$UE/*.desktop $HOME/Bureau # déplacement des raccourcis

echo "Création des dossiers de l'espace www"
if [ -n "$OLD" ]; then
  mv $OLD $NEW # nouveau nom pour l'ancien dossier
else
  mkdir $NEW # création du nouveau dossier
fi
touch $WWW/index.html # création d'un fichier de masquage du dossier secret
for DIR in $DIRS; do
  mkdir -p $WWW/$TOKEN/$DIR # création des sous-dossiers
done

echo "Envoi du mail contenant l'URL"
NOM="$(getent passwd $USER | cut -d: -f5 | tr '[:upper:]' '[:lower:]' | tr ' ' '-')"
URL="https://$NOM.emi.u-bordeaux.fr/$TOKEN" # création de l'URL de l'étudiant
echo $URL | mail -s $URL $MAIL # envoi du mail contenant l'URL de l'étudiant

rm $0 # auto-destruction du script
echo "Configuration terminée"
