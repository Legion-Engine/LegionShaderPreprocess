from copy import deepcopy
from typing import Dict, List, Tuple
import re

from rewrite_rules.rewrite_base import RewriteBase
from vprint import vprint1, vprint2


class ExtractDirectives(RewriteBase):
    matcher = re.compile(r"^\s*#\s*state\s(.*)$")

    def rewrite_source(self, source: str, meta_information: Dict[str, str]) -> List[Tuple[str, Dict[str, str]]]:

        reconstruction = ''
        directives = {}
        directives_meta = deepcopy(meta_information)
        directives_meta['location'] = meta_information['location'] + '.directives'
        first_line = True
        for line in source.splitlines(keepends=True):
            if first_line:
                directives[line.strip()] = []
                vprint2(f"[Directives] found variant {line}")
                first_line = False
            match = self.matcher.match(line)
            if match is not None:
                vprint1(f"[Directives] found directive {line}")
                state = match.group(1).split(' ')
                directives[state[0]] = state[1:]
            else:
                reconstruction += line

        directives = '\n'.join([' '.join([k] + v) for k, v in directives.items()]) + '\n'

        return [(reconstruction, meta_information), (directives, directives_meta)]
