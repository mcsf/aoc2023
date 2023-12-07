#!/bin/sh

test_day() {
	day=$1
	cd "$day" || exit 2
	echo "$day"
	for runner in run.*; do
		if [ -x "$runner" ]; then
			printf "  %s\t%s\n" "$runner" "$(pass_or_fail "$runner")"
		else
			printf "  %s\tnot executable\n" "$runner"
		fi
	done
}

pass_or_fail() {
	tmp=$(mktemp)
	runner="$1"
	if command time -ho "$tmp" "./$runner" < input | diff - expected; then
		printf "PASS (%s)\n" "$(awk '{print $1}' "$tmp")"
	else
		echo FAIL
	fi
	rm "$tmp"
}

cd "$(dirname "$0")" || exit 2

if [ -n "$1" ]; then
	if [ -f "$1"/expected ]; then
		test_day "$1"
	fi
else
	for day in */; do
		if [ -f "$day"/expected ]; then
			test_day "$day"
		else
			printf "%s\n  (skipped)\n" "$day"
		fi
	done
fi
