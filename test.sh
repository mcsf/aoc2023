#!/bin/sh

test_day() {
	day=$1
	cd "$day" || exit 2

	# Capture output to flush all at once, since tests are run in parallel
	out=$(mktemp)
	echo "$day" > "$out"

	for runner in run.*; do
		if [ -x "$runner" ]; then
			printf "  %s\t%s\n" "$runner" "$(pass_or_fail "$runner")" >> "$out"
		else
			printf "  %s\tnot executable\n" "$runner" >> "$out"
		fi
	done
	cat "$out"
	rm "$out"
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
			test_day "$day" &
		else
			printf "%s\n  (skipped)\n" "$day"
		fi
	done
	wait
fi
