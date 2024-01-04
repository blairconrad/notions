import rich.console
import sys

stride = 16


def out_char(b):
    if ord(" ") <= b <= ord("~"):
        return chr(b)
    else:
        return "."


console = rich.console.Console(force_terminal=True)

with open(sys.argv[1], mode="rb") as f:
    text = f.read()

for row_index in range(0, len(text), stride):
    line = "".join(f"{out_char(c)}" for c in text[row_index : row_index + stride])
    line = line.ljust(stride + 3)
    console.out(line, end=None, highlight=False)

    for c in text[row_index : row_index + stride]:
        console.out(f" {c:02x}", end=None, highlight=False, style=f"rgb(255,{15 + 16 * (c//16)},{15 + 16 * (c%16)})")
    console.out()
