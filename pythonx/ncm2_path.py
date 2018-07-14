# -*- coding: utf-8 -*-

import vim
from ncm2 import Ncm2Source, getLogger
import re
from os import path, listdir

logger = getLogger(__name__)


class Source(Ncm2Source):

    def on_complete_bufpath(self, ctx, path_pattern):
        typed = ctx['typed']
        filepath = ctx['filepath']
        startccol = ctx['startccol']
        base = ctx['base']

        path_keyword = re.search(path_pattern + '$', typed).group(0)

        dr = path.expandvars(path_keyword)
        dr = path.expanduser(dr)
        expanded = False
        if dr != path_keyword:
            expanded = True
        dr = path.dirname(dr)

        logger.debug('dir: %s', dr)

        label = 'buf'
        base_dir = path.dirname(filepath)

        matcher = self.matcher_get(ctx['matcher'])

        matches = []

        joined_dir = path.join(base_dir, dr.strip('/'))
        logger.debug('searching dir: %s', joined_dir)
        try:
            names = listdir(joined_dir)
            names.sort(key=lambda name: name.lower())
            logger.debug('search result: %s', names)
            for name in names:
                p = path.join(joined_dir, name)
                word = path.basename(p)
                menu = '~' + label
                if expanded:
                    menu += '~ ' + p

                m = dict(word=word, menu='~' + label)
                m = self.match_formalize(ctx, m)
                if matcher(base, m):
                    matches.append(m)
        except Exception as ex:
            logger.exception('failed searching dir [%s]', joined_dir)

        refresh = 0

        if len(matches) > 100:
            refresh = 1
            matches = matches[0:100]

        self.complete(ctx, startccol, matches, refresh)

    def on_complete_cwdpath(self, ctx, path_pattern, cwd):
        typed = ctx['typed']
        startccol = ctx['startccol']
        base = ctx['base']

        path_keyword = re.search(path_pattern + '$', typed).group(0)

        dr = path.expandvars(path_keyword)
        dr = path.expanduser(dr)
        expanded = False
        if dr != path_keyword:
            expanded = True
        dr = path.dirname(dr)

        logger.debug('dir: %s', dr)

        label = 'cwd'
        base_dir = cwd

        matcher = self.matcher_get(ctx['matcher'])

        matches = []

        joined_dir = path.join(base_dir, dr.strip('/'))
        logger.debug('searching dir: %s', joined_dir)
        try:
            names = listdir(joined_dir)
            names.sort(key=lambda name: name.lower())
            logger.debug('search result: %s', names)
            for name in names:
                p = path.join(joined_dir, name)
                word = path.basename(p)
                menu = '~' + label
                if expanded:
                    menu += '~ ' + p

                m = dict(word=word, menu='~' + label)
                m = self.match_formalize(ctx, m)
                if matcher(base, m):
                    matches.append(m)
        except Exception as ex:
            logger.exception('failed searching dir [%s]', joined_dir)

        refresh = 0

        if len(matches) > 100:
            refresh = 1
            matches = matches[0:100]

        self.complete(ctx, startccol, matches, refresh)

    def on_complete_rootpath(self, ctx, path_pattern):
        typed = ctx['typed']
        filepath = ctx['filepath']
        startccol = ctx['startccol']
        base = ctx['base']

        path_keyword = re.search(path_pattern + '$', typed).group(0)

        dr = path.expandvars(path_keyword)
        dr = path.expanduser(dr)
        expanded = False
        if dr != path_keyword:
            expanded = True
        dr = path.dirname(dr)

        logger.debug('dir: %s', dr)

        if not dr.startswith('/'):
            return

        menu = '~root'
        if dr != path_keyword:
            menu = dr

        base_dir = '/'

        matcher = self.matcher_get(ctx['matcher'])

        matches = []

        joined_dir = path.join(base_dir, dr)
        logger.debug('searching dir: %s', joined_dir)
        try:
            names = listdir(joined_dir)
            names.sort(key=lambda name: name.lower())
            logger.debug('search result: %s', names)
            for name in names:
                p = path.join(joined_dir, name)
                word = path.basename(p)

                m = dict(word=word, menu=menu)
                m = self.match_formalize(ctx, m)
                if matcher(base, m):
                    matches.append(m)
        except Exception as ex:
            logger.exception('failed searching dir [%s]', joined_dir)

        refresh = 0

        if len(matches) > 100:
            refresh = 1
            matches = matches[0:100]

        self.complete(ctx, startccol, matches, refresh)


source = Source(vim)

on_complete_bufpath = source.on_complete_bufpath
on_complete_cwdpath = source.on_complete_cwdpath
on_complete_rootpath = source.on_complete_rootpath
