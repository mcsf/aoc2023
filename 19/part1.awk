BEGIN {
	mode = 1
	FS = "[{},]"

	print "def validate(part, rule):"
	print "  if rule.isupper():"
	print "    return rule"
	print ""
	print "  x, m, a, s = part"
	print ""
}

!length($0) {
	mode = 2
	FS = "[{},=xmas]+"

	print ""
	print "parts = ["
	next
}

mode == 1 {
	printf "  if rule == '%s':\n", $1
	for (i = 2; i <= NF; i++) {
		n = split($i, parts, ":")
		if (n == 2) {
			printf "    if %s:\n      return validate(part, '%s')\n",
				   parts[1], parts[2]
		} else if (n == 1) {
			printf "    return validate(part, '%s')\n", parts[1]
		}
	}
	print ""
}

mode == 2 {
	printf "  ("
	for (i = 2; i <= NF - 1; i++) {
		term = i < NF - 1 ? ", " : ""
		printf "%s%s", $i, term
	}
	print "),"
}

END {
	print "]"
	print ""
	print "s = 0"
	print "for p in parts:"
	print "  result = validate(p, 'in')"
	print "  if result == 'A':"
	print "    s += sum(p)"
	print ""
	print "print(s)"
}
