#!/usr/bin/python
# -*- coding: utf-8
import unicodedata


class UnilevelTree:
    def _treeToJsonRecursive(self, root):
        children = []

        for node in root.get_children():
            children.append(self.treeToJson(node))

        name = (u'%s (%s)') % (root.owner.username, root.owner.sponsor.username if root.owner.sponsor else "None")
        name = unicodedata.normalize("NFKD", name).encode('ascii', 'ignore')

        return {
            'id': ('%d' % root.id),
            'name': name,
            'data': {},
            'children': children
        }

    def treeToJson(self, root):
        return self._treeToJsonRecursive(root)
