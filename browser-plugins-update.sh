#!/bin/sh
# Author: Elan Ruusamäe <glen@pld-linux.org>
# Date: 2006-09-13, Initial revision
# Date: 2006-10-31, Added arch checking
#
# For more information see browser-plugins.README
#
# TODO
# - implement uninstall

sysconfdir='/etc/browser-plugins'
browsersdir="$sysconfdir/browsers.d"
blacklistdir="$sysconfdir/blacklist.d"
plugindirs='/usr/lib/browser-plugins /usr/lib64/browser-plugins'

# bool in_blacklist(char *blacklistfile, char *pluginfile)
# returns true if pluginfile is listed in blacklistfile 
in_blacklist() {
	local blacklistfile="$1"
	local pluginfile="$2"
	while read glob; do
		if [[ "$glob" = \#* ]] || [[ "$glob" = "" ]]; then
			continue
		fi
		if [[ "$pluginfile" = $glob ]]; then
			echo >&3 "  $pluginfile blacklisted with $glob ($blacklistfile)"
			return 0
		fi
	done < $blacklistfile

	return 1
}

# bool arch_compatible(char *browser, char *plugindir)
# returns true if browser and plugindir are from same arch
arch_compatible() {
	local browser="$1"
	local plugindir="$2"

	if ([[ "$browser" = *.x86_64 ]] && [[ "$plugindir" != */lib64/* ]]) || \
		([[ "$browser" != *.x86_64 ]] && [[ "$plugindir" = */lib64/* ]]); then
		echo >&3 "  $browser not compatible with $plugindir"
		return 1
	fi
	return 0
}

# bool blacklisted(char *browser, char *pluginfile)
# returns true if pluginfile is blacklisted for browser
# returns also true if pluginfile is from incompatible arch
blacklisted() {
	local browser="$1"
	local pluginfile="$2"
	# check browser blacklist file
	if [ -f "$blacklistdir/$browser.blacklist" ]; then
		if in_blacklist "$blacklistdir/$browser.blacklist" "$pluginfile"; then
			return 0
		fi
	fi
	# retrun true for now
	return 1
}

# char **get_browsers(void)
# returns list of installed browsers
get_browsers() {
	for dir in "$browsersdir"/*.*; do
		if [ -L "$dir" ]; then
			dir="${dir#$browsersdir/}"
			browsers="$browsers $dir"
		fi
	done

	echo >&3 "browsers: $browsers"
}

# char *browserplugindir(char *)
# returns plugin directory for browser
browserplugindir() {
	local browser="$1"
	local dir
	dir=$(readlink "$browsersdir/$browser")
	if [ -z "$dir" ]; then
		echo >&2 "$0: ERROR: browser plugin dir pointing to nowhere for $browser!"
		exit 1
	fi
	echo "$dir"
}

# kill dead links to plugins from browser dirs.
# dead links appear if plugin is removed or if newer plugin version no longer
# includes previously packaged file
remove_plugins() {
	for browser in $browsers; do
		find $(browserplugindir "$browser") -type l | while read link; do
			if [ ! -f "$link" ]; then
				echo "Removing $link"
				rm -f "$link"
			fi
		done
	done
}

install_plugins() {
	# link new plugins
	for plugindir in $plugindirs; do
		# skip non-existing plugindirs
		[ -d "$plugindir" ] || continue

		cd "$plugindir"
		find -type f | while read line; do
			pluginfile="${line#./}"
			echo >&3 "pluginfile: $pluginfile"
			for browser in $browsers; do
				echo >&3 " check $pluginfile for $browser"
				browserplugindir=$(browserplugindir "$browser")
				link="$browserplugindir/$pluginfile"

				if ! arch_compatible "$browser" "$plugindir"; then
					continue
				fi

				if blacklisted "$browser" "$pluginfile"; then
					# just in case unlink it
					if [ -f "$link" ]; then
						echo "Removing $pluginfile from $browserplugindir"
						rm -f "$link"
					fi
				else
					# skip existing links
					[ ! -L $link ] || continue
					if [[ "$pluginfile" = */* ]]; then
						# FIXME: what's the proper handling for this?
						echo >&2 "$0: Warning: pluginfile $pluginfile includes subdir, file ignored"
						continue
					fi
					echo "Installing $pluginfile to $browserplugindir"
					ln -s "$plugindir/$pluginfile" "$link"
				fi
			done
		done
	done
}

if [[ "$*" = *debug* ]]; then
	exec 3>&2
else
	exec 3>/dev/null
fi

get_browsers

remove_plugins
install_plugins
