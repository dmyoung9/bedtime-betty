Generate {num} original, unique, and interesting idea{plural} for bedtime {obj_plural} for {age} year-olds that could be written and illustrated by a unique, interesting, or unlikely pairing of an author and illustrator from those you've mentioned. Each {obj_key} should subtly teach an age-appropriate "moral of the story"-type lesson. Also generate a short string of 3-5 emoji that conveys the plot of each {obj_key}.

Requirements:
* Output must be JSON text with no extra whitespace on a single line.
* Output must be of the following format: `{{"data": [{{"author":"...","illustrator":"...","title":"...","outline":"...","emoji":"...","lesson":"..."}},...]}}`
* `data` must be a JSON array of {num} {obj_key} object{plural}.
* `outline` **must not** contain emoji characters.
* `emoji` **must only** contain emoji characters.
* **Do not** give any explanation.
* **Do not** use a code block.