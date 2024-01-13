BEGIN {
	FS = "[{}:,]+"
}

/^$/ {
	exit
}

{
	nrules[$1] = (NF - 3) / 2
	for (rule = 1; rule <= nrules[$1]; rule++) {
		split($(rule * 2), parts, "[<>]")
		rules[$1, rule, "var"] = parts[1]
		rules[$1, rule, "gt"]  = match($(rule * 2), ">")
		rules[$1, rule, "val"] = parts[2]
		rules[$1, rule, "dst"] = $(rule * 2 + 1)
	}
	fallbacks[$1] = $(NF - 1)
}

END {
	init[1] = init[3] = init[5] = init[7] = 1
	init[2] = init[4] = init[6] = init[8] = 4001
	print count_range(init, "in")
}

function count_range(range, flow,
					 i, total, recur_range) {
	if (flow == "R") return 0 
	if (flow == "A") return length_product(range) 

	for (i = 1; i <= nrules[flow]; i++) {
		rg_partition(flow, i, range, recur_range)
		total += count_range(recur_range, rules[flow, i, "dst"])
	}

	return total + count_range(range, fallbacks[flow])
}

function length_product(range) {
	return (range[2] - range[1]) * (range[4] - range[3]) \
			* (range[6] - range[5]) * (range[8] - range[7])
}

function rg_partition(flow, rule_id, range, recur_range,
					  i, var, gt, val, var_idx) {
	var = rules[flow, rule_id, "var"]
	gt  = rules[flow, rule_id, "gt"]
	val = rules[flow, rule_id, "val"]
	var_idx = index("xmas", var) * 2 - 1

	for (i = 1; i <= 8; i++) recur_range[i] = range[i]

	if (!gt) {
		recur_range[var_idx + 1] = val
		range[var_idx] = val
	} else {
		recur_range[var_idx] = val + 1
		range[var_idx + 1] = val + 1
	}
}
