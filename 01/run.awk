#!/usr/bin/env awk -f

BEGIN {
	PATTERN = "one|two|three|four|five|six|seven|eight|nine"
	NRETTAP = reverse(PATTERN)

	split(PATTERN, DIGITS, "|")
	for (n in DIGITS) VALUES[DIGITS[n]] = n
}

{
	sum1 += get_digit($0) get_digit(reverse($0))
	sum2 += get_digit_or_word($0, 0) get_digit_or_word($0, 1)
}

function get_digit(s) {
	match(s, "[[:digit:]]")
	return substr(s, RSTART, 1)
}

function get_digit_or_word(s, is_reverse,   idx_int, idx_word, len_word, r) {
	if (is_reverse) s = reverse(s)

	match(s, "[[:digit:]]")
	idx_int = RSTART

	match(s, is_reverse ? NRETTAP : PATTERN)
	idx_word = RSTART
	len_word = RLENGTH

	if (idx_int && (idx_int < idx_word || ! idx_word)) {
		return substr(s, idx_int, 1)
	}

	r = substr(s, idx_word, len_word)
	if (is_reverse) r = reverse(r)
	return VALUES[r]
}

function reverse(s,   i, r) {
	for (i=length(s); i>=1; i--) r = r substr(s, i, 1)
	return r
}

END {
	print sum1
	print sum2
}
