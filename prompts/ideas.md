Tasks:
* Generate {num} original, captivating, and age-appropriate story idea{plural} (7-12 words) for {age} year-olds.
* Generate 5 related emoji shortcodes that convey each idea.

Requirements:
* Output must be JSON text with no whitespace on a single line.
* Output must be a JSON array of idea objects.
* Each idea object must be structured like: `{{"idea":"...","emoji":":keycap_1::keycap_2::keycap_3::keycap_4::keycap_5:"}}`
* `idea` must contain only the idea, with no emoji.
* `emoji` must only contain emoji.
* **Do not** give any explanation.
* **Do not** use a code block.

Output: