%define modname email_admin

Summary: Issabel Email Module
Name: issabel-email_admin
Version: 6.0.0
Release: 8
License: GPL
Group:   Applications/System
Source0: issabel-%{modname}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch
Requires(pre): issabel-framework >= 5.0.0-1
Requires(pre): postfix
Requires: issabel-php-phpmailer

# SMTP AUTH PLAIN mechanism used when authenticating against the relay
Requires: cyrus-sasl-plain

Obsoletes: elastix-email_admin

%description
Issabel Email Module

Issabel 6 does not ship a mail server. This module only configures the
outbound SMTP relay: a send-only Postfix (satellite) that forwards all
locally generated mail (Asterisk voicemail, mail(), PHPMailer, CI_Email,
cron, fail2ban) to an external smarthost with SASL/TLS.

%prep
%setup -n %{name}-%{version}

%install
rm -rf $RPM_BUILD_ROOT

# ** /etc path ** #
mkdir -p    $RPM_BUILD_ROOT/etc/postfix
mkdir -p    $RPM_BUILD_ROOT/usr/share/issabel/privileged
mkdir -p    $RPM_BUILD_ROOT/usr/share/issabel/module_installer/%{name}-%{version}-%{release}/

# ** postfix config (send-only satellite) ** #
mv setup/etc/postfix/main.cf.issabel          $RPM_BUILD_ROOT/etc/postfix/

# ** privileged helper ** #
mv setup/usr/share/issabel/privileged/*       $RPM_BUILD_ROOT/usr/share/issabel/privileged
chmod +x $RPM_BUILD_ROOT/usr/share/issabel/privileged/*

# Files provided by all Issabel modules
mkdir -p    $RPM_BUILD_ROOT/var/www/html/
mv modules/ $RPM_BUILD_ROOT/var/www/html/

rmdir setup/etc/postfix setup/etc
rmdir setup/usr/share/issabel/privileged setup/usr/share/issabel setup/usr/share setup/usr

mv setup/   $RPM_BUILD_ROOT/usr/share/issabel/module_installer/%{name}-%{version}-%{release}/
mv menu.xml $RPM_BUILD_ROOT/usr/share/issabel/module_installer/%{name}-%{version}-%{release}/

%pre
mkdir -p /usr/share/issabel/module_installer/%{name}-%{version}-%{release}/
touch /usr/share/issabel/module_installer/%{name}-%{version}-%{release}/preversion_%{modname}.info
if [ $1 -eq 2 ]; then
    rpm -q --queryformat='%{VERSION}-%{RELEASE}' %{name} > /usr/share/issabel/module_installer/%{name}-%{version}-%{release}/preversion_%{modname}.info
fi

%post
# Habilito inicio automático del MTA de sólo salida
systemctl enable postfix || :

# Reemplazo la configuración de Postfix solo en instalación limpia
if [ $1 -eq 1 ]; then
    [ -f /etc/postfix/main.cf ] && mv /etc/postfix/main.cf /etc/postfix/main.cf.orig
    cp /etc/postfix/main.cf.issabel /etc/postfix/main.cf
fi

pathModule="/usr/share/issabel/module_installer/%{name}-%{version}-%{release}"

# En upgrade, elimino del menú las páginas que ya no existen en Issabel 6
if [ $1 -eq 2 ]; then
    for m in email_domains email_accounts email_relay antispam email_list email_stats vacations; do
        issabel-menuremove "$m" || :
    done
fi

# Run installer script to fix up ACLs and add module to Issabel menus.
issabel-menumerge /usr/share/issabel/module_installer/%{name}-%{version}-%{release}/menu.xml

pathSQLiteDB="/var/www/db"
mkdir -p $pathSQLiteDB
preversion=`cat $pathModule/preversion_%{modname}.info`
rm -f $pathModule/preversion_%{modname}.info

if [ $1 -eq 1 ]; then #install
  # The installer database
    issabel-dbprocess "install" "$pathModule/setup/db"
elif [ $1 -eq 2 ]; then #update
    issabel-dbprocess "update"  "$pathModule/setup/db" "$preversion"
fi

# add string localhost first in /etc/hosts
if [ -f /etc/hosts  ] ; then
   sed -ie '/127.0.0.1/s/[\t| ]localhost[^\.]/ /g'  /etc/hosts  # busca el patron 127.0.0.1 y reemplaza [\t| ]localhost[^\.] por " "
   sed -ie 's/127.0.0.1/127.0.0.1\tlocalhost/'  /etc/hosts      # reemplaza 127.0.0.1 por 127.0.0.1\tlocalhost
fi

%clean
rm -rf $RPM_BUILD_ROOT

%preun
pathModule="/usr/share/issabel/module_installer/%{name}-%{version}-%{release}"
if [ $1 -eq 0 ] ; then # Validation for desinstall this rpm
  echo "Delete Email menus"
  issabel-menuremove "%{modname}"

  echo "Dump and delete %{name} databases"
  issabel-dbprocess "delete" "$pathModule/setup/db"
fi

%files
%defattr(-, root, root)
%{_localstatedir}/www/html/*
/usr/share/issabel/module_installer/*
/etc/postfix/main.cf.issabel
%defattr(755, root, root)
/usr/share/issabel/privileged/*

%changelog
* Tue Oct 13 2026 Issabel Foundation <info@issabel.org> - 6.0.0-8
- remote_smtp: fix checkSMTP() reading a non-existent PHPMailer 6 error key
  ($error['smtp_msg']); use $error['detail'] to detect a missing STARTTLS.

* Mon Oct 12 2026 Issabel Foundation <info@issabel.org> - 6.0.0-6
- remote_smtp: drop the jQuery iButton plugin (and its assets); the status
  toggle now uses the theme's Bootstrap 5 switch.

* Fri Oct 09 2026 Issabel Foundation <info@issabel.org> - 6.0.0-5
- Drop the local mail server: no more postfix local delivery, cyrus-imapd,
  spamassassin or mailman. Keep only the outbound SMTP relay (remote_smtp)
  backed by a send-only Postfix satellite.
* Fri Oct 09 2026 Issabel Foundation <info@issabel.org> - 6.0.0-4
- Drop the Mailman dependency: mailman3-enhanced installs an httpd config that
  proxies /admin to its web UI, hijacking Issabel's /admin GUI. See TODO.md.
* Fri Oct 09 2026 Issabel Foundation <info@issabel.org> - 6.0.0-3
- Require mailman3-enhanced instead of mailman, which does not exist in EL10.
