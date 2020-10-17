stress_names = [
    'grave', # `
    'acute', # ^
    'tilde'  # ~
]

utf8_stress_map = {
    0: u'\u0300', # grave
    1: u'\u0301', # acute
    2: u'\u0303'  # tilde
}

ascii_stress_map = {
    0: "`", # grave
    1: "^", # acute - no printable acute accent in ascii table only in extended ASCII:239
    2: "~"  # tilde
}