# -*- coding: utf-8 -*-

import vim
from ncm2 import Ncm2Source, getLogger
import re
from os import path, listdir

logger = getLogger(__name__)


class Source(Ncm2Source):

    def on_complete(self, ctx, path_pattern):
        typed = ctx['typed']
        filepath = ctx['filepath']
        startccol = ctx['startccol']
        base = ctx['base']

        path_keywrod = re.search(path_pattern + '$', typed).group(0)

        dr = path.expandvars(path_keywrod)
        dr = path.expanduser(dr)
        expanded = False
        if dr != path_keywrod:
            expanded = True
        dr = path.dirname(dr)

        logger.debug('dir: %s', dr)

        base_dirs = []
        if filepath != "":
            curdir = path.dirname(filepath)
            base_dirs.append(('buf', curdir), )

        # full path of current file, current working dir
        cwd = self.nvim.call('getcwd')
        base_dirs.append(('cwd', cwd), )

        if path_keywrod and path_keywrod[0] != ".":
            base_dirs.append(('root', "/"))

        matcher = self.matcher_get(ctx['matcher'])

        seen = set()
        matches = []
        for label, base_dir in base_dirs:
            joined_dir = path.join(base_dir, dr.strip('/'))
            logger.debug('searching dir: %s', joined_dir)
            try:
                names = listdir(joined_dir)
                names.sort(key=lambda name: name.lower())
                logger.debug('search result: %s', names)
                for name in names:
                    p = path.join(joined_dir, name)
                    if p in seen:
                        continue
                    seen.add(p)
                    word = path.basename(p)
                    menu = '~' + label
                    if expanded:
                        menu += '~ ' + p

                    m = dict(word=word, menu='~' + label, dup=1)
                    m = self.match_formalize(ctx, m)
                    if matcher(base, m):
                        matches.append(m)
            except Exception as ex:
                logger.exception( 'failed searching dir [%s]', joined_dir)
                continue

        refresh = 0

        if len(matches) > 1024:
            refresh = 1
            matches = matches[0:1024]

        self.complete(ctx, startccol, matches, refresh)


source = Source(vim)

on_complete = source.on_complete
