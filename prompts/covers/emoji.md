Generate a short string of 3-5 emoji that conveys the plot of each story.

Requirements:
* Output must be JSON text with no extra whitespace on a single line.
* Output must be of the following format: `{{"stories": [{{"author":"...","illustrator":"...","title":"...","lesson":"...","outline":"...","emoji":"..."}},...]}}`
* `stories` must be a JSON array of {num} story object{plural}.
* `outline` must not contain any emoji characters.
* `emoji` must only contain emoji characters.
* **Do not** give any explanation.
* **Do not** use a code block.