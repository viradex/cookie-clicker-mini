import math


def abbreviate_number(number: int) -> str:
    suffixes = [
        "million",
        "billion",
        "trillion",
        "quadrillion",
        "quintillion",
        "sextillion",
        "septillion",
        "octillion",
        "nonillion",
        "decillion",
        "undecillion",
        "duodecillion",
        "tredecillion",
        "quattuordecillion",
        "quindecillion",
        "sexdecillion",
        "septendecillion",
        "octodecillion",
        "novemdecillion",
        "vigintillion",
        "unvigintillion",
        "duovigintillion",
        "trevigintillion",
        "quattuorvigintillion",
        "quinvigintillion",
        "sexvigintillion",
        "septenvigintillion",
        "octovigintillion",
        "novemvigintillion",
        "trigintillion",
        "untrigintillion",
        "duotrigintillion",
        "tretrigintillion",
        "quattuortrigintillion",
        "quintrigintillion",
        "sextrigintillion",
        "septentrigintillion",
        "octotrigintillion",
        "novemtrigintillion",
        "quadragintillion",
        "unquadragintillion",
        "duoquadragintillion",
        "trequadragintillion",
        "quattuorquadragintillion",
        "quinquadragintillion",
        "sexquadragintillion",
        "septenquadragintillion",
        "octoquadragintillion",
        "novemquadragintillion",
        "quinquagintillion",
        "unquadragintillion",
        "duoquadragintillion",
        "trequadragintillion",
        "youJustLostTheGame",
    ]

    number = float(number)
    div = 1_000_000  # Start abbreviating at millions
    i = 0

    if number < div:
        return f"{int(number):,}"

    while i < len(suffixes) - 1 and number >= div * 1000:
        div *= 1000
        i += 1

    short_num = number / div
    short_num_truncated = math.floor(short_num * 100) / 100

    # Remove unnecessary .0
    formatted = (
        str(short_num_truncated).rstrip("0").rstrip(".")
        if "." in str(short_num_truncated)
        else str(short_num_truncated)
    )

    suffix = suffixes[i] if i < len(suffixes) else suffixes[-1]
    return f"{formatted} {suffix}"


if __name__ == "__main__":
    print(abbreviate_number(735807353))
