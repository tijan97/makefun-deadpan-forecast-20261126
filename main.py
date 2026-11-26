"""Deadpan forecast for a city that does not exist.

Competition: "Deadpan Forecasts for Cities That Do Not Exist"
(u-coral-ibis-18-deadpan-forecasts-for-cities-that-do-151d4d8c).

The brief: one line, at most 160 characters, a weather forecast for an
invented city. It must be absurd yet land like something a real forecaster
would read off the map, with a concrete image, number or detail that makes
the invented place feel real. A judge model briefed as a dry, deadpan TV
meteorologist compares entries two at a time and weighs, in order:
1. on-subject forecast for a city that does not exist,
2. funnier joke, landing on a first read with a deadpan twist,
3. more vivid detail (concrete image, number or detail),
4. believable broadcast tone (plain, confident, straight-faced),
5. good use of the 160 characters (tight, well paced, no padding).

How the chosen line is built to hit each criterion:

* Invented city: "Gloombury" -- a name that sounds like a real damp
  English market town (cf. Glastonbury, Bloomsbury) while existing
  nowhere on any map, so criterion 1 is satisfied on the first word.
* Absurd but broadcast-plausible weather: "23 millimetres of rain
  falling sideways by noon". Rain falling sideways is physically
  absurd as a forecast quantity, yet it is exactly the kind of thing a
  forecaster says about wind-driven rain -- the absurdity hides inside
  a familiar sentence shape, which is what makes it deadpan rather
  than random. The number 23 (not a round 20 or 25) makes it feel
  measured rather than invented.
* The joke, landing on a first read: "easing to a drizzle of lost
  umbrellas after six". A drizzle is a real forecast word; "of lost
  umbrellas" swaps the expected precipitation noun for the debris of
  the storm itself. It is a single twist, not a pile of absurdity,
  and it follows naturally from the sideways rain -- the umbrellas
  were lost *because* of the weather just described.
* Broadcast tone and closing beat: "High of 9 degrees, low of mild
  regret." The high/low pair is the most recognisable forecaster
  sign-off there is. "Mild regret" is not a temperature, but it is
  delivered in exactly the slot where a temperature belongs, which
  is the deadpan move: the sentence never breaks character, never
  winks, never explains the joke.
* Length: 157 of the 160 allowed characters. Tight, no padding, and
  no wasted words -- every clause carries either a number, an image,
  or the joke.

Rejected alternatives, and why:
* "Rain falling upwards" -- a bigger absurdity, but it reads as a
  fantasy premise rather than a forecast; sideways rain keeps the
  broadcast frame intact.
* Adding a second joke (e.g. a named local event) -- would crowd the
  line and dilute the single twist the judge rewards.
* A wilder city name -- a joke name would telegraph the gag before
  the forecast starts; Gloombury stays straight-faced.

The program itself is deliberately deterministic: it writes one fixed
line, validates it against the gate (UTF-8, 1-160 characters, not only
whitespace), and writes it to $MAKEFUN_OUTPUT_DIR/entry.txt (or
/output/entry.txt when the variable is unset), exactly as the rules
require. There is no randomness, no network access, and no dependence
on the working directory.
"""

import os

# The entry: a single deadpan forecast line for the invented city
# of Gloombury. 157 characters, inside the 1-160 gate.
ENTRY = (
    "In Gloombury, expect 23 millimetres of rain falling sideways by noon, "
    "easing to a drizzle of lost umbrellas after six. "
    "High of 9 degrees, low of mild regret."
)

OUTPUT_FILENAME = "entry.txt"


def validate(entry):
    """Check the entry against the competition gate and house style.

    Gate: UTF-8 text, 1 to 160 characters, not only whitespace.
    Style (deadpan broadcast): single line, no leading/trailing
    whitespace, no double spaces, no shouting (no fully-uppercase
    word longer than one character -- a straight-faced forecaster
    never yells), and ends with a full stop, as a read-out line does.
    """
    if not isinstance(entry, str):
        raise TypeError("entry must be a string")
    if not entry.strip():
        raise ValueError("entry must not be only whitespace")
    if entry != entry.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line")
    if "  " in entry:
        raise ValueError("entry must not contain double spaces")
    if not 1 <= len(entry) <= 160:
        raise ValueError(
            "entry must be 1 to 160 characters, got %d" % len(entry)
        )
    entry.encode("utf-8")  # raises if not valid UTF-8 text
    shouted = [
        word for word in entry.split()
        if word.isupper() and len(word.strip(".,;:!?")) > 1
    ]
    if shouted:
        raise ValueError("entry must not shout: %r" % (shouted,))
    if not entry.endswith("."):
        raise ValueError("entry must end with a full stop")
    # The brief demands a concrete image, number or detail that makes
    # the invented place feel real: require at least one digit so the
    # forecast always carries a measured quantity, not just adjectives.
    if not any(char.isdigit() for char in entry):
        raise ValueError("entry must contain a concrete number or detail")
    return entry


def main():
    entry = validate(ENTRY)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, OUTPUT_FILENAME)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(entry)
    return path


if __name__ == "__main__":
    main()
