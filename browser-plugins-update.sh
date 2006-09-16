#!/bin/sh
# Author: Elan Ruusamäe <glen@pld-linux.org>
# Date: 2006-09-13
# See more browser-plugins.README

# TODO
# - implement blacklist.d/anyfile-browser.arch.blacklist support
# - check not to link amd64 plugins to opera.i386 dir

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

# bool blacklisted(char *browser, char *pluginfile)
# returns true if pluginfile is blacklisted for browser
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
		echo >&2 "$0: browser plugin dir empty for $browser; exiting!"
		exit 1
	fi
	echo "$dir"
}

remove_plugins() {
	# kill dead links
	for browser in $browsers; do
		find $(browserplugindir "$browser") -type l | while read link; do
			[ -f "$link" ] || rm -f "$link"
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
				if blacklisted "$browser" "$pluginfile"; then
					# just in case unlink it
					if [ -f "$link" ]; then
						echo "Removing $pluginfile from $browserplugindir"
						rm -f "$link"
					fi
				else
					# skip existing links
					[ ! -L $link ] || continue
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
