#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Génère les pages guides du site (docs/guides et docs/en/guides) et le sitemap.

Chaque guide existe en français et en anglais ; le contenu est dans GUIDES.
Relancer après modification :  python3 tools/site_guides.py
"""
import html
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs")
BASE = "https://2deathadder.github.io/linwin/"
DATE = "2026-10-06"
REPO = "https://github.com/2Deathadder/linwin"
RELEASE = REPO + "/releases/tag/v1"
VERIF = '<meta name="google-site-verification" content="6x_nVg5ShqfbiN6l9bb-sRWy_I1lIZ5-ergKv65XdYc" />'

INSTALL = """<pre><code>git clone https://github.com/2Deathadder/linwin.git
cd linwin
sudo ./linwin install
linwin check</code></pre>"""

GUIDES = [
    {
        "slug": "dual-boot-sans-cle-usb",
        "fr": {
            "title": "Dual-boot Windows 10 et Linux sans clé USB : le guide complet",
            "h1": "Installer Windows 10 à côté de Linux sans clé USB",
            "desc": "Comment installer Windows 10 en dual-boot depuis un Linux déjà installé, sans clé USB ni DVD : principe, prérequis, étapes et retour arrière avec linwin.",
            "body": """
<p>La méthode classique pour ajouter Windows à côté de Linux demande une clé USB d'au moins 8 Go, un outil pour la
préparer (Rufus, Ventoy, WoeUSB…), un passage dans le BIOS et un partitionnement à la main. <strong>linwin</strong>
fait tout cela depuis Linux, sans clé USB.</p>

<h2>Le principe : une partition remplace la clé USB</h2>
<ol>
<li><strong>Faire de la place</strong> : linwin crée trois partitions dans l'espace non alloué du disque (ou en
réduisant à chaud une racine Btrfs) : MSR, Windows et une partition FAT32 de 8 Go nommée <code>WINSETUP</code>.</li>
<li><strong>Copier l'installeur</strong> : l'ISO de Windows 10 est copiée sur <code>WINSETUP</code>, qui joue le rôle de
la clé USB. Les pilotes nécessaires (Intel RST/VMD, Wi-Fi, Ethernet) et les réponses automatiques y sont ajoutés.</li>
<li><strong>Démarrer une seule fois dessus</strong> : une entrée UEFI à usage unique (<code>BootNext</code>) lance
l'installeur au prochain redémarrage ; ensuite, le PC reprend son ordre normal.</li>
<li><strong>Installer sans intervention</strong> : l'installeur repère la partition Windows à l'octet près et
n'écrit que là, crée ton compte, puis redémarre sous Linux.</li>
<li><strong>Finaliser</strong> : Linux redevient le choix par défaut, <code>WINSETUP</code> est supprimée et Windows
est ajouté au menu de GRUB, systemd-boot, Limine ou rEFInd.</li>
</ol>

<h2>Prérequis</h2>
<ul>
<li>PC x86-64 démarré en <strong>UEFI</strong> (pas en mode Legacy/CSM), disque en <strong>GPT</strong> ;</li>
<li>l'ISO de Windows 10 (64 bits), téléchargeable chez Microsoft depuis Linux ;</li>
<li>de la place : taille de Windows (32 Go minimum, 64 Go conseillés) + 8 Go pour l'installeur ;</li>
<li>une sauvegarde de tes données, et le chargeur branché.</li>
</ul>

<h2>Les étapes</h2>
""" + INSTALL + """
<p>Puis, dans l'application <strong>linwin</strong> ou en ligne de commande :</p>
<pre><code>linwin plan --size 100G
sudo linwin prepare --size 100G
sudo linwin stage --iso ~/Downloads/Win10_22H2_French_x64v1.iso --edition Home --user moi
sudo linwin boot
sudo reboot</code></pre>
<p>Windows s'installe seul (20 à 40 minutes), puis le PC revient sous Linux qui termine la configuration.</p>

<h2>Et si je change d'avis ?</h2>
<p><code>sudo linwin cancel</code> retire Windows à n'importe quelle étape, même une fois installé : entrées de
démarrage, partitions, puis l'espace est rendu (à Linux en cas de réduction, en espace libre sinon).</p>

<h2>Comparaison avec les méthodes classiques</h2>
<div class="table-scroll"><table>
<tr><th></th><th>Clé USB (Rufus, Ventoy…)</th><th>linwin</th></tr>
<tr><th>Clé USB</th><td>obligatoire</td><td>aucune</td></tr>
<tr><th>Partitionnement</th><td>à la main</td><td>automatique et vérifié</td></tr>
<tr><th>Pilotes SSD (VMD) et Wi-Fi</th><td>à trouver soi-même</td><td>ajoutés automatiquement</td></tr>
<tr><th>Menu de démarrage Linux</th><td>souvent à réparer</td><td>Linux reste par défaut, Windows ajouté</td></tr>
<tr><th>Retour arrière</th><td>manuel</td><td><code>linwin cancel</code></td></tr>
</table></div>
""",
        },
        "en": {
            "title": "Dual-boot Windows 10 and Linux without a USB drive: complete guide",
            "h1": "Install Windows 10 alongside Linux without a USB drive",
            "desc": "How to install Windows 10 as a dual-boot from an existing Linux system without a USB stick or DVD: how it works, requirements, steps and how to undo it, with linwin.",
            "body": """
<p>The usual way to add Windows next to Linux needs a USB stick of at least 8 GB, a tool to write it (Rufus, Ventoy,
WoeUSB…), a trip to the BIOS and manual partitioning. <strong>linwin</strong> does all of it from Linux, with no USB
drive.</p>

<h2>How it works: a partition replaces the USB stick</h2>
<ol>
<li><strong>Make room</strong>: linwin creates three partitions in unallocated disk space (or by shrinking a Btrfs
root online): MSR, Windows and an 8 GB FAT32 partition called <code>WINSETUP</code>.</li>
<li><strong>Copy the installer</strong>: the Windows 10 ISO is copied to <code>WINSETUP</code>, which acts as the USB
stick. Required drivers (Intel RST/VMD, Wi-Fi, Ethernet) and the unattended answers are added.</li>
<li><strong>Boot it once</strong>: a one-time UEFI entry (<code>BootNext</code>) starts the installer on the next
reboot; afterwards the PC goes back to its normal boot order.</li>
<li><strong>Unattended install</strong>: the installer finds the Windows partition by its exact byte offset, writes
only there, creates your account, then reboots into Linux.</li>
<li><strong>Finish</strong>: Linux becomes the default again, <code>WINSETUP</code> is removed and Windows is added
to the GRUB, systemd-boot, Limine or rEFInd menu.</li>
</ol>

<h2>Requirements</h2>
<ul>
<li>x86-64 PC booted in <strong>UEFI</strong> mode (not Legacy/CSM), <strong>GPT</strong> disk;</li>
<li>the Windows 10 ISO (64-bit), downloadable from Microsoft on Linux;</li>
<li>space: Windows size (32 GB minimum, 64 GB recommended) + 8 GB for the installer;</li>
<li>a backup of your data, and the charger plugged in.</li>
</ul>

<h2>Steps</h2>
""" + INSTALL + """
<p>Then, in the <strong>linwin</strong> app or on the command line:</p>
<pre><code>linwin plan --size 100G
sudo linwin prepare --size 100G
sudo linwin stage --iso ~/Downloads/Win10_22H2_English_x64v1.iso --edition Home --user me
sudo linwin boot
sudo reboot</code></pre>
<p>Windows installs itself (20 to 40 minutes), then the PC returns to Linux, which completes the setup.</p>

<h2>Changed your mind?</h2>
<p><code>sudo linwin cancel</code> removes Windows at any step, even after installation: boot entries, partitions,
then the space is given back (to Linux after a shrink, as free space otherwise).</p>

<h2>Compared with the usual methods</h2>
<div class="table-scroll"><table>
<tr><th></th><th>USB stick (Rufus, Ventoy…)</th><th>linwin</th></tr>
<tr><th>USB drive</th><td>required</td><td>none</td></tr>
<tr><th>Partitioning</th><td>manual</td><td>automatic and verified</td></tr>
<tr><th>SSD (VMD) and Wi-Fi drivers</th><td>find them yourself</td><td>added automatically</td></tr>
<tr><th>Linux boot menu</th><td>often needs repair</td><td>Linux stays default, Windows added</td></tr>
<tr><th>Undo</th><td>manual</td><td><code>linwin cancel</code></td></tr>
</table></div>
""",
        },
    },
    {
        "slug": "ubuntu-mint-debian",
        "fr": {
            "title": "Installer Windows 10 à côté d'Ubuntu, Linux Mint ou Debian sans clé USB",
            "h1": "Windows 10 à côté d'Ubuntu, Linux Mint ou Debian, sans clé USB",
            "desc": "Ajouter Windows 10 en dual-boot à un Ubuntu, Linux Mint ou Debian existant, sans clé USB : place disponible (ext4), GRUB, pilotes, étapes avec linwin.",
            "body": """
<p>Ubuntu, Linux Mint et Debian s'installent par défaut avec une racine <strong>ext4</strong> et le chargeur
<strong>GRUB</strong>. linwin gère cette configuration ; le seul point d'attention est la place disponible.</p>

<h2>1. Vérifier la place</h2>
<p>ext4 ne peut pas être réduit pendant que Linux tourne. linwin utilise donc <strong>l'espace non alloué</strong>
du disque. Vérifie ce qui est disponible :</p>
<pre><code>linwin check</code></pre>
<p>La ligne « Espace non alloué » indique la taille maximale possible pour Windows. Si elle est insuffisante,
démarre une fois sur un système live (par exemple la clé d'installation d'Ubuntu, avec GParted) pour réduire la
partition Linux, puis relance linwin : il utilisera l'espace libéré. Aucune partition existante n'est modifiée par
linwin dans ce mode.</p>

<h2>2. Installer linwin</h2>
<pre><code>sudo apt install git
git clone https://github.com/2Deathadder/linwin.git
cd linwin
sudo ./linwin install</code></pre>
<p>Les outils manquants (<code>wimtools</code>, <code>cabextract</code>, <code>dosfstools</code>,
<code>efibootmgr</code>) s'installent automatiquement avec apt. L'interface graphique fonctionne à partir d'Ubuntu
24.04 et Debian 13 (paquets <code>python3-gi gir1.2-gtk-4.0 gir1.2-adw-1</code>) ; sinon, la ligne de commande fait
exactement la même chose.</p>

<h2>3. Installer Windows</h2>
<pre><code>sudo linwin prepare --size 100G
sudo linwin stage --iso ~/Téléchargements/Win10_22H2_French_x64v1.iso --edition Home --user moi
sudo linwin boot
sudo reboot</code></pre>

<h2>4. Le menu GRUB</h2>
<p>Ubuntu masque le menu GRUB quand il ne connaît qu'un système. Après l'installation, linwin ajoute une entrée
<strong>Windows</strong> à GRUB (<code>/etc/grub.d/35_linwin_windows</code>), réactive l'affichage du menu
(5 secondes) et régénère la configuration avec <code>update-grub</code>. Ubuntu reste le choix par défaut.</p>

<h2>Wi-Fi sous Windows</h2>
<p>Les portables récents ont souvent une carte Wi-Fi Intel AX2xx, MediaTek MT79xx ou Realtek RTL8852 que Windows 10
ne connaît pas. linwin ajoute le pilote du catalogue Microsoft Update pour chaque carte réseau : Windows a Internet
dès le premier démarrage.</p>
""",
        },
        "en": {
            "title": "Install Windows 10 alongside Ubuntu, Linux Mint or Debian without a USB drive",
            "h1": "Windows 10 alongside Ubuntu, Linux Mint or Debian, without a USB drive",
            "desc": "Add Windows 10 as a dual-boot to an existing Ubuntu, Linux Mint or Debian without a USB stick: free space (ext4), GRUB, drivers and steps with linwin.",
            "body": """
<p>Ubuntu, Linux Mint and Debian install by default with an <strong>ext4</strong> root and the <strong>GRUB</strong>
boot loader. linwin supports this setup; the only thing to check is the available space.</p>

<h2>1. Check the space</h2>
<p>ext4 cannot be shrunk while Linux is running, so linwin uses the disk's <strong>unallocated space</strong>.
Check what is available:</p>
<pre><code>linwin check</code></pre>
<p>The “unallocated space” line shows the maximum possible Windows size. If it is too small, boot once into a live
system (for example the Ubuntu install stick, with GParted) to shrink the Linux partition, then run linwin again: it
will use the freed space. In this mode linwin does not modify any existing partition.</p>

<h2>2. Install linwin</h2>
<pre><code>sudo apt install git
git clone https://github.com/2Deathadder/linwin.git
cd linwin
sudo ./linwin install</code></pre>
<p>Missing tools (<code>wimtools</code>, <code>cabextract</code>, <code>dosfstools</code>, <code>efibootmgr</code>)
are installed automatically with apt. The graphical interface works on Ubuntu 24.04+ and Debian 13+ (packages
<code>python3-gi gir1.2-gtk-4.0 gir1.2-adw-1</code>); otherwise the command line does exactly the same.</p>

<h2>3. Install Windows</h2>
<pre><code>sudo linwin prepare --size 100G
sudo linwin stage --iso ~/Downloads/Win10_22H2_English_x64v1.iso --edition Home --user me
sudo linwin boot
sudo reboot</code></pre>

<h2>4. The GRUB menu</h2>
<p>Ubuntu hides the GRUB menu when it only knows one system. After installation, linwin adds a
<strong>Windows</strong> entry to GRUB (<code>/etc/grub.d/35_linwin_windows</code>), shows the menu again
(5 seconds) and regenerates the configuration with <code>update-grub</code>. Ubuntu stays the default.</p>

<h2>Wi-Fi in Windows</h2>
<p>Recent laptops often have an Intel AX2xx, MediaTek MT79xx or Realtek RTL8852 Wi-Fi card that Windows 10 does not
know. linwin adds the Microsoft Update Catalog driver for every network card, so Windows is online on first boot.</p>
""",
        },
    },
    {
        "slug": "intel-vmd-rst-ssd-invisible",
        "fr": {
            "title": "L'installeur Windows 10 ne voit pas le SSD (Intel VMD / RST) : solution sans BIOS",
            "h1": "L'installeur Windows 10 ne voit pas le SSD : Intel VMD et pilote RST",
            "desc": "« Aucun lecteur n'a été trouvé » à l'installation de Windows 10 : le SSD est derrière Intel VMD/RST. Comment ajouter le pilote iaStorVD sans toucher au BIOS, automatiquement avec linwin.",
            "body": """
<h2>Le symptôme</h2>
<p>Pendant l'installation de Windows 10, l'écran « Où souhaitez-vous installer Windows ? » est vide, avec le message
<em>« Aucun lecteur n'a été trouvé. Cliquez sur Charger un pilote… »</em>. Le SSD fonctionne pourtant sous Linux.</p>

<h2>La cause : Intel VMD</h2>
<p>Sur la plupart des PC Intel de 11e génération et plus récents (Alder Lake, Raptor Lake, Meteor Lake…), le SSD
NVMe est placé derrière le contrôleur <strong>Intel VMD</strong> (Volume Management Device), géré par le pilote
<strong>Intel RST</strong> (<code>iaStorVD</code>). Linux a ce pilote ; l'installeur de Windows 10, non. Beaucoup de
BIOS ne permettent pas de désactiver VMD, ou cela casse le démarrage d'un Windows existant.</p>
<p>Pour savoir si ton PC est concerné, sous Linux :</p>
<pre><code>ls /sys/bus/pci/drivers/vmd/</code></pre>
<p>Si un identifiant de périphérique s'affiche (par exemple <code>10000:e0:06.0</code>), VMD est actif.</p>

<h2>La solution manuelle</h2>
<ol>
<li>Télécharger l'installeur Intel RST correspondant au contrôleur et en extraire le pilote « F6 »
(<code>iaStorVD.inf</code>, <code>.sys</code>, <code>.cat</code> et les fichiers que l'INF copie) ;</li>
<li>les copier sur la clé d'installation ;</li>
<li>dans l'installeur : <em>Charger un pilote</em> → <em>Parcourir</em> → dossier du pilote.</li>
</ol>
<p>Piège fréquent : si un seul fichier exigé par l'INF manque, Windows répond que le pilote « n'est pas compatible ».</p>

<h2>La solution automatique avec linwin</h2>
<p>linwin détecte VMD, télécharge le pilote Intel RST 20.2.6.1025 chez Intel (empreintes SHA-256 vérifiées) pour les
contrôleurs 467F, A77F, 7D0B et AD0B (12e à 14e génération, Core Ultra), ou le pilote du catalogue Microsoft Update
pour les autres (par exemple 9A0B en 11e génération). Il l'ajoute :</p>
<ul>
<li>à l'environnement de l'installeur, qui le charge avant de chercher le disque ;</li>
<li>au Windows installé, pour qu'il démarre ensuite sur ce SSD.</li>
</ul>
<p>Rien à changer dans le BIOS, et pas de clé USB : voir le <a href="../dual-boot-sans-cle-usb/">guide complet</a>.</p>
""",
        },
        "en": {
            "title": "Windows 10 installer doesn't see the SSD (Intel VMD / RST): fix without BIOS changes",
            "h1": "Windows 10 setup can't find the SSD: Intel VMD and the RST driver",
            "desc": "“We couldn't find any drives” when installing Windows 10: the SSD sits behind Intel VMD/RST. How to add the iaStorVD driver without touching the BIOS, automatically with linwin.",
            "body": """
<h2>The symptom</h2>
<p>During Windows 10 setup, the “Where do you want to install Windows?” screen is empty and says <em>“We couldn't
find any drives. To get a storage driver, click Load driver.”</em> Yet the SSD works fine in Linux.</p>

<h2>The cause: Intel VMD</h2>
<p>On most Intel PCs from 11th gen onwards (Alder Lake, Raptor Lake, Meteor Lake…), the NVMe SSD sits behind the
<strong>Intel VMD</strong> (Volume Management Device) controller, handled by the <strong>Intel RST</strong> driver
(<code>iaStorVD</code>). Linux has this driver; the Windows 10 installer does not. Many BIOSes cannot disable VMD,
and doing so can break an existing Windows install.</p>
<p>To check whether your PC is affected, on Linux:</p>
<pre><code>ls /sys/bus/pci/drivers/vmd/</code></pre>
<p>If a device address shows up (for example <code>10000:e0:06.0</code>), VMD is active.</p>

<h2>The manual fix</h2>
<ol>
<li>Download the Intel RST installer for your controller and extract the “F6” driver (<code>iaStorVD.inf</code>,
<code>.sys</code>, <code>.cat</code> and every file the INF copies);</li>
<li>copy them to the install stick;</li>
<li>in setup: <em>Load driver</em> → <em>Browse</em> → driver folder.</li>
</ol>
<p>Common pitfall: if a single file required by the INF is missing, Windows says the driver is “not compatible”.</p>

<h2>The automatic fix with linwin</h2>
<p>linwin detects VMD and downloads Intel RST 20.2.6.1025 from Intel (pinned SHA-256 checksums) for controllers
467F, A77F, 7D0B and AD0B (12th–14th gen, Core Ultra), or the Microsoft Update Catalog driver for others (for example
9A0B on 11th gen). It adds it:</p>
<ul>
<li>to the installer environment, which loads it before looking for disks;</li>
<li>to the installed Windows, so it can then boot from that SSD.</li>
</ul>
<p>No BIOS change and no USB stick: see the <a href="../dual-boot-sans-cle-usb/">complete guide</a>.</p>
""",
        },
    },
    {
        "slug": "ajouter-windows-grub-systemd-boot-limine",
        "fr": {
            "title": "Ajouter Windows au menu GRUB, systemd-boot, Limine ou rEFInd",
            "h1": "Ajouter Windows au menu de démarrage : GRUB, systemd-boot, Limine, rEFInd",
            "desc": "Faire apparaître Windows dans le menu de démarrage de Linux : entrée GRUB (chainloader), systemd-boot, Limine et rEFInd, menu caché, ordre UEFI. Automatique avec linwin.",
            "body": """
<p>Après l'installation de Windows, deux problèmes reviennent souvent : Windows prend la première place au démarrage,
et il n'apparaît pas dans le menu du chargeur de Linux. Voici comment chaque chargeur le gère, et ce que linwin fait
automatiquement.</p>

<h2>Remettre Linux en premier</h2>
<p>Windows se place en tête de l'ordre UEFI. Pour remettre le chargeur de Linux en premier :</p>
<pre><code>efibootmgr                         # repère le numéro de l'entrée Linux (ex. 0003)
sudo efibootmgr --bootorder 0003,0001</code></pre>
<p>linwin le fait des deux côtés : Windows s'enlève lui-même de la tête de liste à sa première session
(<code>bcdedit</code>), et linwin remet l'entrée qui a démarré Linux en premier.</p>

<h2>GRUB (Ubuntu, Debian, Mint, Fedora, openSUSE…)</h2>
<p>Sans <code>os-prober</code> activé, GRUB ne détecte pas Windows. Entrée explicite, indépendante d'os-prober :</p>
<pre><code>menuentry 'Windows' --class windows {
	insmod part_gpt
	insmod fat
	insmod chain
	search --no-floppy --fs-uuid --set=root UUID-DE-LA-PARTITION-EFI
	chainloader /EFI/Microsoft/Boot/bootmgfw.efi
}</code></pre>
<p>linwin l'écrit dans <code>/etc/grub.d/35_linwin_windows</code>, réactive le menu s'il est caché
(<code>GRUB_TIMEOUT_STYLE=hidden</code> sur Ubuntu, <code>menu_auto_hide</code> sur Fedora) et régénère la
configuration (<code>update-grub</code> ou <code>grub-mkconfig</code>/<code>grub2-mkconfig</code>).</p>

<h2>systemd-boot</h2>
<p>systemd-boot affiche tout seul Windows s'il est sur la même partition EFI. Le menu reste caché si
<code>timeout</code> vaut 0 : linwin règle <code>timeout 5</code> dans <code>loader/loader.conf</code>.</p>

<h2>Limine</h2>
<p>Limine n'ajoute pas Windows automatiquement. Avec <code>limine-entry-tool</code> (Arch, CachyOS, Omarchy) :</p>
<pre><code>sudo limine-entry-tool --add-efi "Windows" /boot/EFI/Microsoft/Boot/bootmgfw.efi</code></pre>
<p>Sinon, une entrée dans <code>limine.conf</code> avec <code>protocol: efi</code> et
<code>path: boot():/EFI/Microsoft/Boot/bootmgfw.efi</code>. linwin utilise l'outil s'il est présent, sinon écrit
l'entrée.</p>

<h2>rEFInd</h2>
<p>rEFInd détecte Windows tout seul : rien à faire.</p>

<p>Pour tout faire automatiquement, installation de Windows comprise : voir le
<a href="../dual-boot-sans-cle-usb/">guide du dual-boot sans clé USB</a>.</p>
""",
        },
        "en": {
            "title": "Add Windows to the GRUB, systemd-boot, Limine or rEFInd boot menu",
            "h1": "Add Windows to the boot menu: GRUB, systemd-boot, Limine, rEFInd",
            "desc": "Make Windows appear in the Linux boot menu: GRUB chainloader entry, systemd-boot, Limine and rEFInd, hidden menus and UEFI boot order. Automatic with linwin.",
            "body": """
<p>After installing Windows, two problems are common: Windows takes first place in the boot order, and it does not
show up in the Linux boot loader menu. Here is how each boot loader handles it, and what linwin does
automatically.</p>

<h2>Put Linux first again</h2>
<p>Windows puts itself first in the UEFI boot order. To put the Linux boot loader back first:</p>
<pre><code>efibootmgr                         # find the Linux entry number (e.g. 0003)
sudo efibootmgr --bootorder 0003,0001</code></pre>
<p>linwin does it on both sides: Windows removes itself from the top at its first logon (<code>bcdedit</code>),
and linwin puts the entry that booted Linux first.</p>

<h2>GRUB (Ubuntu, Debian, Mint, Fedora, openSUSE…)</h2>
<p>Without <code>os-prober</code> enabled, GRUB does not detect Windows. An explicit entry, independent of
os-prober:</p>
<pre><code>menuentry 'Windows' --class windows {
	insmod part_gpt
	insmod fat
	insmod chain
	search --no-floppy --fs-uuid --set=root EFI-PARTITION-UUID
	chainloader /EFI/Microsoft/Boot/bootmgfw.efi
}</code></pre>
<p>linwin writes it to <code>/etc/grub.d/35_linwin_windows</code>, shows the menu again if it is hidden
(<code>GRUB_TIMEOUT_STYLE=hidden</code> on Ubuntu, <code>menu_auto_hide</code> on Fedora) and regenerates the
configuration (<code>update-grub</code> or <code>grub-mkconfig</code>/<code>grub2-mkconfig</code>).</p>

<h2>systemd-boot</h2>
<p>systemd-boot shows Windows automatically when it is on the same EFI partition. The menu stays hidden if
<code>timeout</code> is 0: linwin sets <code>timeout 5</code> in <code>loader/loader.conf</code>.</p>

<h2>Limine</h2>
<p>Limine does not add Windows automatically. With <code>limine-entry-tool</code> (Arch, CachyOS, Omarchy):</p>
<pre><code>sudo limine-entry-tool --add-efi "Windows" /boot/EFI/Microsoft/Boot/bootmgfw.efi</code></pre>
<p>Otherwise, an entry in <code>limine.conf</code> with <code>protocol: efi</code> and
<code>path: boot():/EFI/Microsoft/Boot/bootmgfw.efi</code>. linwin uses the tool when present, or writes the
entry.</p>

<h2>rEFInd</h2>
<p>rEFInd finds Windows on its own: nothing to do.</p>

<p>To do everything automatically, Windows installation included, see the
<a href="../dual-boot-sans-cle-usb/">dual-boot without USB guide</a>.</p>
""",
        },
    },
]

UI = {
    "fr": {"home": "Accueil", "guides": "Guides", "manual": "Manuel", "other": "English", "dl": "Télécharger linwin v1",
           "cta": "linwin est libre (GPL-3.0) et fonctionne sur toutes les distributions courantes.",
           "list_title": "Guides : dual-boot Windows et Linux sans clé USB",
           "list_desc": "Guides pratiques pour installer Windows 10 à côté de Linux sans clé USB : Ubuntu, GRUB, systemd-boot, Intel VMD/RST.",
           "footer": "linwin v1 — logiciel libre sous licence GPL-3.0, par 2Deathadder. linwin n'est affilié ni à Microsoft ni à Intel."},
    "en": {"home": "Home", "guides": "Guides", "manual": "Manual (French)", "other": "Français", "dl": "Download linwin v1",
           "cta": "linwin is free software (GPL-3.0) and works on all common distributions.",
           "list_title": "Guides: Windows and Linux dual-boot without a USB drive",
           "list_desc": "Practical guides to install Windows 10 alongside Linux without a USB drive: Ubuntu, GRUB, systemd-boot, Intel VMD/RST.",
           "footer": "linwin v1 — free software under the GPL-3.0 license, by 2Deathadder. linwin is not affiliated with Microsoft or Intel."},
}


def url(lang, path=""):
    return BASE + ("en/" if lang == "en" else "") + path


def page(lang, path, depth, title, desc, h1, body, crumbs, article=True):
    """depth : nombre de niveaux sous la racine de la langue (pour les liens relatifs)."""
    other = "en" if lang == "fr" else "fr"
    root = "../" * depth                     # racine de la langue
    css = "../" * (depth + (1 if lang == "en" else 0)) + "style.css"
    ui = UI[lang]
    graph = [{
        "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u}
                            for i, (n, u) in enumerate(crumbs)],
    }]
    if article:
        graph.append({
            "@type": "TechArticle",
            "headline": h1,
            "description": desc,
            "inLanguage": lang,
            "datePublished": DATE,
            "dateModified": DATE,
            "author": {"@type": "Person", "name": "2Deathadder", "url": "https://github.com/2Deathadder"},
            "image": BASE + "og.png",
            "mainEntityOfPage": url(lang, path),
            "about": {"@id": BASE + "#app"},
        })
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    e = html.escape
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url(lang, path)}">
<link rel="alternate" hreflang="fr" href="{url('fr', path)}">
<link rel="alternate" hreflang="en" href="{url('en', path)}">
<link rel="alternate" hreflang="x-default" href="{url('en', path)}">
<meta name="robots" content="index, follow">
{VERIF}
<meta property="og:type" content="{'article' if article else 'website'}">
<meta property="og:site_name" content="linwin">
<meta property="og:locale" content="{'fr_FR' if lang == 'fr' else 'en_US'}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url(lang, path)}">
<meta property="og:image" content="{BASE}og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0f1724">
<link rel="stylesheet" href="{css}">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<div class="wrap">
  <header class="top">
    <a class="brand" href="{root or './'}">linwin</a>
    <nav>
      <a href="{root or './'}">{ui['home']}</a>
      <a href="{root}guides/">{ui['guides']}</a>
      <a href="{REPO}#readme">{ui['manual']}</a>
      <a href="{url(other, path)}" hreflang="{other}" lang="{other}">{ui['other']}</a>
    </nav>
  </header>
  <main class="article">
    <h1>{e(h1)}</h1>
{body}
    <section>
      <p>{ui['cta']}</p>
      <div class="cta">
        <a class="btn primary" href="{RELEASE}">{ui['dl']}</a>
        <a class="btn ghost" href="{REPO}#readme">{ui['manual']}</a>
      </div>
    </section>
  </main>
  <footer>{ui['footer']} <a href="{REPO}">github.com/2Deathadder/linwin</a></footer>
</div>
</body>
</html>
"""


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)


def main():
    urls = [("", 0.9), ("en/", 0.9)]
    for lang in ("fr", "en"):
        prefix = "en/" if lang == "en" else ""
        home = url(lang)
        # une page par guide
        for g in GUIDES:
            c = g[lang]
            path = f"guides/{g['slug']}/"
            crumbs = [(UI[lang]["home"], home), (UI[lang]["guides"], url(lang, "guides/")), (c["h1"], url(lang, path))]
            write(prefix + path + "index.html", page(lang, path, 2, c["title"] + " | linwin", c["desc"], c["h1"], c["body"], crumbs))
        # liste des guides
        items = "\n".join(
            f'      <div class="card"><h3><a href="{g["slug"]}/">{html.escape(g[lang]["h1"])}</a></h3>'
            f'<p>{html.escape(g[lang]["desc"])}</p></div>' for g in GUIDES)
        body = f'    <div class="grid">\n{items}\n    </div>'
        crumbs = [(UI[lang]["home"], home), (UI[lang]["guides"], url(lang, "guides/"))]
        write(prefix + "guides/index.html", page(lang, "guides/", 1, UI[lang]["list_title"] + " | linwin",
                                                  UI[lang]["list_desc"], UI[lang]["list_title"], body, crumbs, article=False))
    urls += [("guides/", 0.7), ("en/guides/", 0.7)]
    for g in GUIDES:
        urls += [(f"guides/{g['slug']}/", 0.8), (f"en/guides/{g['slug']}/", 0.8)]
    # sitemap : chaque page avec son équivalent dans l'autre langue
    entries = []
    for path, prio in urls:
        bare = path[3:] if path.startswith("en/") else path
        entries.append(f"""  <url>
    <loc>{BASE}{path}</loc>
    <lastmod>{DATE}</lastmod>
    <priority>{prio}</priority>
    <xhtml:link rel="alternate" hreflang="fr" href="{BASE}{bare}"/>
    <xhtml:link rel="alternate" hreflang="en" href="{BASE}en/{bare}"/>
  </url>""")
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
          + "\n".join(entries) + "\n</urlset>\n")
    print("\n".join(BASE + p for p, _ in urls))


if __name__ == "__main__":
    main()
