%if 0%{?qubes_builder}
%define _sourcedir %(pwd)/xfce4-settings-qubes
%endif

Name:		xfce4-settings-qubes
Version:	4.0.1
Release:	1%{?dist}
Summary:	Default Xfce4 panel settings for Qubes

Group:		User Interface/Desktops
License:	GPLv2+
URL:		http://www.qubes-os.org/
Source0:	xfce4-panel-qubes-default.xml
Source2:	xsettings.xml
Source3:	xfwm4.xml
Source4:	xfce4-desktop.xml
Source5:	xfce4-session.xml
Source6:	xfce4-power-manager.xml
Source7:	xfce4-keyboard-shortcuts.xml
Source8:	xfce4-xss-lock.desktop

Requires:	qubes-artwork
Requires:	xfce4-panel
Requires:	xss-lock
Requires(post):	xfce4-panel

%description
%{summary}

%prep

%build


%install
install -m 644 -D %{SOURCE0} %{buildroot}%{_sysconfdir}/xdg/xfce4/panel/default.xml.qubes
install -m 644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xsettings.xml.qubes
install -m 644 -D %{SOURCE3} %{buildroot}%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfwm4.xml
install -m 644 -D %{SOURCE4} %{buildroot}%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml
install -m 644 -D %{SOURCE5} %{buildroot}%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-session.xml.qubes
install -m 644 -D %{SOURCE6} %{buildroot}%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-power-manager.xml.qubes
install -m 644 -D %{SOURCE7} %{buildroot}%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml.qubes
install -m 644 -D %{SOURCE8} %{buildroot}%{_sysconfdir}/xdg/autostart/xfce4-xss-lock.desktop
ln -s ../../panel/default.xml %{buildroot}%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml

%define settings_replace() \
qubesfile="%{1}" \
origfile=${qubesfile%.qubes} \
backupfile=${origfile}.xfce4 \
if [ -r "$origfile" -a ! -r "$backupfile" ]; then \
	mv -f "$origfile" "$backupfile" \
fi \
cp -f "$qubesfile" "$origfile" \
%{nil}

%triggerin -- xfce4-panel
%settings_replace %{_sysconfdir}/xdg/xfce4/panel/default.xml.qubes

%triggerin -- xfce4-settings
%settings_replace %{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xsettings.xml.qubes

%triggerin -- xfce4-session
%settings_replace %{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-session.xml.qubes

%triggerin -- xfce4-power-manager
%settings_replace %{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-power-manager.xml.qubes

%triggerin -- libxfce4ui
%settings_replace %{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml.qubes

%triggerin -- xscreensaver-base

conffile=/etc/xscreensaver/XScreenSaver.ad.tail

if ! grep -q "! Qubes options begin" $conffile; then
    ( echo -e "! Qubes options begin - do not edit\n! Qubes options end"; cat $conffile) > $conffile.tmp
    mv $conffile.tmp $conffile
fi

sed -e '/! Qubes options begin/,/! Qubes options end/c \
! Qubes options begin - do not edit\
*newLoginCommand:\
*fade: False\
! Qubes options end' -i $conffile

update-xscreensaver-hacks

%postun
REPLACEFILE="${REPLACEFILE} %{_sysconfdir}/xdg/xfce4/panel/default.xml.qubes"
REPLACEFILE="${REPLACEFILE} %{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xsettings.xml.qubes"
REPLACEFILE="${REPLACEFILE} %{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-session.xml.qubes"
REPLACEFILE="${REPLACEFILE} %{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-power-manager.xml.qubes"
REPLACEFILE="${REPLACEFILE} %{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml.qubes"
if [ $1 -lt 1 ]; then
	for file in ${REPLACEFILE}; do
		origfile=${file%.qubes}
		backupfile=${origfile}.xfce4
		mv -f "$backupfile" "$origfile"
	done
fi

%files
%{_sysconfdir}/xdg/xfce4/panel/default.xml.qubes
%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xsettings.xml.qubes
%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfwm4.xml
%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml
%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml
%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-session.xml.qubes
%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-power-manager.xml.qubes
%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml.qubes
%{_sysconfdir}/xdg/autostart/xfce4-xss-lock.desktop

%changelog

