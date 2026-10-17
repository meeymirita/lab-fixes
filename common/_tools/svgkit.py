# -*- coding: utf-8 -*-
"""Мини-набор для схем в методичках: прямоугольники, стрелки, подписи на currentColor (светлая и тёмная тема работают сами).
Использование:
    s = Svg(640, 240, 'Описание схемы для скринридера', pid='d1')
    s.box(20, 40, 140, 50, ['Заголовок', 'вторая строка'], fill=.1)
    s.arrow(160, 65, 240, 65, 'подпись')
    html = s.html()          # <div class="diagram"><svg ...>...</svg></div>
Стили .diagram в шаблоне страницы добавляет to_caddy.ensure_css."""
import html as H


def esc(t):
    return H.escape(str(t), quote=False)


class Svg:
    def __init__(self, w, h, label, pid='d'):
        self.w, self.h, self.label, self.pid = w, h, label, pid
        self.p = []

    def text(self, x, y, t, size=12, anchor='middle', weight=None, op=1, italic=False, rot=None):
        extra = (' font-weight="%s"' % weight if weight else '') + (' font-style="italic"' if italic else '')
        if rot is not None:
            extra += ' transform="rotate(%s %s %s)"' % (rot, x, y)
        self.p.append('<text x="%s" y="%s" text-anchor="%s" font-size="%s" fill="currentColor"%s%s>%s</text>' % (
            x, y, anchor, size, ' fill-opacity="%s"' % op if op != 1 else '', extra, esc(t)))

    def box(self, x, y, w, h, lines, fill=.07, bold=False, dash=False, rx=8, size=12, op=1, anchor='middle', pad=10):
        if isinstance(lines, str):
            lines = [lines]
        self.p.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="currentColor" fill-opacity="%s" stroke="currentColor" stroke-width="1.5"%s/>' % (
            x, y, w, h, rx, fill, ' stroke-dasharray="5 4"' if dash else ''))
        n = len(lines)
        lh = size + 5
        y0 = y + h / 2 - (n - 1) * lh / 2 + size / 2 - 1
        tx = x + w / 2 if anchor == 'middle' else x + pad
        for i, t in enumerate(lines):
            self.text(tx, round(y0 + i * lh, 1), t, size=size, anchor=anchor, weight='700' if (bold and i == 0) else None, op=op)

    def line(self, x1, y1, x2, y2, dash=False, op=1, w=1.5):
        self.p.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-width="%s"%s%s/>' % (
            x1, y1, x2, y2, w, ' stroke-dasharray="5 4"' if dash else '', ' stroke-opacity="%s"' % op if op != 1 else ''))

    def arrow(self, x1, y1, x2, y2, label=None, dash=False, both=False, lx=None, ly=None, size=11):
        ms = ' marker-start="url(#%s-s)"' % self.pid if both else ''
        self.p.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-width="1.5"%s marker-end="url(#%s-e)"%s/>' % (
            x1, y1, x2, y2, ' stroke-dasharray="5 4"' if dash else '', self.pid, ms))
        if label:
            mx = lx if lx is not None else (x1 + x2) / 2
            my = ly if ly is not None else (y1 + y2) / 2 - 6
            self.text(mx, my, label, size=size, op=.85)

    def path(self, d, dash=False, arrow=True):
        self.p.append('<path d="%s" fill="none" stroke="currentColor" stroke-width="1.5"%s%s/>' % (
            d, ' stroke-dasharray="5 4"' if dash else '', ' marker-end="url(#%s-e)"' % self.pid if arrow else ''))

    def bar(self, x, y, w, h, label='', fill=.18, dash=False, size=11):
        self.p.append('<rect x="%s" y="%s" width="%s" height="%s" rx="4" fill="currentColor" fill-opacity="%s" stroke="currentColor" stroke-width="1.2"%s/>' % (
            x, y, w, h, fill, ' stroke-dasharray="4 3"' if dash else ''))
        if label:
            self.text(x + w / 2, y + h / 2 + size / 2 - 1, label, size=size)

    def html(self):
        defs = ('<defs><marker id="%(p)s-e" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker>'
                '<marker id="%(p)s-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10,0 L0,5 L10,10 z" fill="currentColor"/></marker></defs>') % {'p': self.pid}
        return ('<div class="diagram"><svg viewBox="0 0 %s %s" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="%s" font-family="inherit">%s%s</svg></div>' % (
            self.w, self.h, esc(self.label).replace('"', '&quot;'), defs, ''.join(self.p)))
