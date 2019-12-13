import re
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

def highlight_source_code(source, fpath, with_line_number=True):
    return HH.syntax_highlight(source, fpath)
    if not with_line_number:
        return HH.syntax_highlight(source, fpath)
    lines = source.splitlines()
    line_numbers = []
    for i, l in enumerate(lines):
        num = re.findall(r'^\s*[0-9]+\s', l)
        if num:
            line_numbers.append(num[0])
            lines[i] = l[len(num[0]):]
        else:
            line_numbers.append('')
    lines = HH.syntax_highlight('\n'.join(lines), fpath).splitlines()
    return '\n'.join([a + b for a, b in zip(line_numbers, lines)])


class FormatInst():
    def __init__(self, line):
        self.line = line
        self.is_inst = False
        self.header = ''
        self.op = ''
        self.operands = ''
        self.is_inst = self.parse()
        if self.is_inst:
            self.normalize_operands()

    def parse(self):
        # => 0x00007ffff6d7cf4c <+12>:    movabs rax,0xaaaaaaaaaaaaaaaa
        if not re.findall(r'0x[0-9a-f]+.*:', self.line):
            return False
        parts = re.split(r'(>:\s+)', self.line)
        if len(parts) < 3:
            return False
        self.header = parts[0] + parts[1]
        parts = "".join(parts[2:]).split()
        self.op = parts[0]
        if len(parts) > 1:
            self.operands = " ".join(parts[1:])
        return True

    def normalize_operands(self):
        s = self.operands
        # pygment doesn't recognize "QWORD PTR" etc., need to be "qword ptr"
        s = " ".join([x.lower() if x.isupper() else x for x in s.split()])
        # pygment cannot colorify the 0x10 in "rbp-0x10", need to be "rbp - 0x10"
        s = re.sub(r'([^-+*/])(\+|-|\*|/)([^-+*/])', r'\1 \2 \3', s)
        # reduce the spaces before the comment started with #
        s = re.sub(r'\s+(#.*)', r'  \1', s)
        self.operands = s


    def highlighted_str(self):
        if not self.is_inst:
            return self.line
        code = "{:6s} {:s}".format(self.op, self.operands)
        # highlight and replace the color <..>
        # remove the spaces in <..>
        parts = re.split(r'(<.*>)', code)
        for i, p in enumerate(parts):
            if p.startswith('<') and p.endswith('>'):
                parts[i] = "".join(p.split())
        code = "".join(parts)
        highlighted_code = highlight_asm(code)
        # then replace the <> with our format
        raw_parts = code.split()
        parts = highlighted_code.split()
        for i, p in enumerate(raw_parts):
            if p.startswith('<') and p.endswith('>'):
                parts[i] = '\033[35m' + p + '\033[0m'   # pink
        # op need aligned
        parts[0] = '\033[33m' + "{:6s}".format(self.op) + '\033[0m'  # yellow
        code = " ".join(parts)
        # current line
        if re.findall(r'^\s*=>\s', self.header):
            header = '\033[32m' + self.header + '\033[0m'  # green
        else:
            # sub doesn't support \033
            parts = re.split(r'\+(\d+)>:', self.header)
            header = parts[0] + '+\033[35m' + parts[1] + '\033[0m>:' + "".join(parts[2:])
        return header + code


def highlight_gdb_disassemble(code):
    insts = [FormatInst(l) for l in code.splitlines()]
    return '\n'.join([inst.highlighted_str() for inst in insts])




