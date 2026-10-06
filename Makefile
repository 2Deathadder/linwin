# SPDX-License-Identifier: GPL-3.0-or-later
# Installation de linwin :  sudo make install            (dans /usr/local)
#                           make install PREFIX=/usr DESTDIR=…   (paquets)
# Avec PREFIX=/usr, linwin reconnaît la copie de /usr/lib/linwin comme celle du paquet.

PREFIX ?= /usr/local
DESTDIR ?=
APPID = io.github._2Deathadder.linwin
LIBDIR = $(PREFIX)/lib/linwin
DATADIR = $(PREFIX)/share
MANDIR = $(DATADIR)/man

all:
	@:

check:
	bash -n linwin
	python3 -m py_compile linwin-gui
	rm -rf __pycache__

install:
	install -Dm755 linwin $(DESTDIR)$(LIBDIR)/linwin
	install -Dm755 linwin-gui $(DESTDIR)$(LIBDIR)/linwin-gui
	install -d $(DESTDIR)$(PREFIX)/bin
	ln -sfn ../lib/linwin/linwin $(DESTDIR)$(PREFIX)/bin/linwin
	ln -sfn ../lib/linwin/linwin-gui $(DESTDIR)$(PREFIX)/bin/linwin-gui
	install -Dm644 data/$(APPID).desktop $(DESTDIR)$(DATADIR)/applications/$(APPID).desktop
	install -Dm644 data/$(APPID).metainfo.xml $(DESTDIR)$(DATADIR)/metainfo/$(APPID).metainfo.xml
	install -Dm644 data/$(APPID).svg $(DESTDIR)$(DATADIR)/icons/hicolor/scalable/apps/$(APPID).svg
	install -Dm644 data/linwin.1 $(DESTDIR)$(MANDIR)/man1/linwin.1
	install -Dm644 data/linwin.fr.1 $(DESTDIR)$(MANDIR)/fr/man1/linwin.1
	ln -sfn linwin.1 $(DESTDIR)$(MANDIR)/man1/linwin-gui.1
	ln -sfn linwin.1 $(DESTDIR)$(MANDIR)/fr/man1/linwin-gui.1

uninstall:
	rm -f $(DESTDIR)$(PREFIX)/bin/linwin $(DESTDIR)$(PREFIX)/bin/linwin-gui
	rm -rf $(DESTDIR)$(LIBDIR)
	rm -f $(DESTDIR)$(DATADIR)/applications/$(APPID).desktop
	rm -f $(DESTDIR)$(DATADIR)/metainfo/$(APPID).metainfo.xml
	rm -f $(DESTDIR)$(DATADIR)/icons/hicolor/scalable/apps/$(APPID).svg
	rm -f $(DESTDIR)$(MANDIR)/man1/linwin.1 $(DESTDIR)$(MANDIR)/man1/linwin-gui.1
	rm -f $(DESTDIR)$(MANDIR)/fr/man1/linwin.1 $(DESTDIR)$(MANDIR)/fr/man1/linwin-gui.1

.PHONY: all check install uninstall
