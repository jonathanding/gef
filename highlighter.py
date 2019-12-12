from functools import lru_cache
import color.syntax_highlight as HH

@lru_cache(maxsize=256)
def highlight_file(filename):
    # Notice that the code is cached
    with open(filename, encoding='utf-8') as f:
        source = f.read()

    raw_lines = source.splitlines()
    source = HH.syntax_highlight(source, filename)

    source_lines = source.splitlines()
    return [line.rstrip() for line in source_lines], [line.rstrip() for line in raw_lines]

def highlight_asm(code):
    return HH.syntax_highlight(code, filename=".asm")




