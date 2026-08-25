#!/usr/bin/env python3
"""
Rebuilds gallery.html, music.html, music-test.html, music-ep.html and
notes.html from whatever is sitting in the folders. Run automatically by
GitHub every time Fisher pushes. Nothing here needs editing by hand.

  images/          paintings          -> gallery.html
  music/test/      .wav files         -> music-test.html
  music/ep/        .wav files         -> music-ep.html
  notes/           .txt / .md files   -> notes.html

Ordering: files are listed in filename order, so a number at the front
controls position (01 shows first). Notes are dated newest-first.
"""

import html
import os
import re
import subprocess
import urllib.parse
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_EXT = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
AUDIO_EXT = {'.wav', '.mp3', '.m4a', '.flac', '.ogg'}
NOTE_EXT = {'.txt', '.md'}
SKIP_IMAGES = {'bg.png'}


def listdir(rel, exts):
    d = os.path.join(ROOT, rel)
    if not os.path.isdir(d):
        return []
    out = [f for f in os.listdir(d)
           if os.path.splitext(f)[1].lower() in exts
           and f not in SKIP_IMAGES
           and not f.startswith('.')
           and os.path.splitext(f)[0].lower() != 'readme']
    return sorted(out, key=lambda s: s.lower())


def strip_order(name):
    """01-BOHEM.wav -> BOHEM   (the number prefix is positioning, not a title)"""
    stem = os.path.splitext(name)[0]
    return re.sub(r'^\s*\d+\s*[-_.]\s*', '', stem)


def url(path):
    return urllib.parse.quote(path)


def year_added(relpath):
    """Year the file first appeared in the repo. Falls back to this year."""
    try:
        out = subprocess.run(
            ['git', 'log', '--diff-filter=A', '--follow', '--format=%ad',
             '--date=format:%Y', '--', relpath],
            cwd=ROOT, capture_output=True, text=True, timeout=20).stdout.split()
        if out:
            return out[-1]
    except Exception:
        pass
    return str(date.today().year)


# ---------- page shell -------------------------------------------------

def page(title, active, body):
    nav = []
    for label, href in [('home', 'index.html'), ('music', 'music.html'),
                        ('gallery', 'gallery.html'), ('notes', 'notes.html')]:
        cls = ' class="active"' if label == active else ''
        nav.append('      <a href="%s"%s>%s</a>' % (href, cls, label))
    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%s</title>
<link rel="stylesheet" href="style.css">
</head>
<body>

<!-- This page is generated from the folders by build.py. Edits here are
     overwritten on the next push. Add files to the folders instead. -->

<div class="wrap">

  <header>
    <nav>
%s
    </nav>
  </header>

%s

  <div class="newsletter">
    <div class="newsletter-label">subscribe</div>
    <form class="newsletter-row" action="https://formspree.io/f/mjybqnro" method="POST">
      <input type="email" name="email" placeholder="email" required>
      <input type="hidden" name="_subject" value="new subscriber">
      <button type="submit">ok</button>
    </form>
  </div>

  <footer>%s</footer>

</div>

</body>
</html>
''' % (html.escape(title), '\n'.join(nav), body, date.today().year)


# ---------- gallery ----------------------------------------------------

def build_gallery():
    files = listdir('images', IMG_EXT)
    items = '\n\n'.join(
        '      <div class="gallery-item" onclick="openLightbox(this)">\n'
        '        <img src="images/%s" alt="" loading="lazy">\n'
        '      </div>' % url(f) for f in files)
    body = '''  <section class="section">
    <div class="section-label">gallery</div>

    <div class="gallery-grid">

%s

    </div>
  </section>''' % items

    out = page('gallery', 'gallery', body)
    out = out.replace('</body>', '''<div class="lightbox" id="lightbox" onclick="closeLightbox()">
  <div class="lightbox-close">close</div>
  <img id="lightbox-img" src="" alt="">
</div>

<script>
function openLightbox(el) {
  document.getElementById('lightbox-img').src = el.querySelector('img').src;
  document.getElementById('lightbox').classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeLightbox() {
  document.getElementById('lightbox').classList.remove('open');
  document.body.style.overflow = '';
}
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') closeLightbox();
});
</script>

</body>''')
    write('gallery.html', out)
    return len(files)


# ---------- music ------------------------------------------------------

def read_order(folder):
    """Optional music/<folder>/order.txt  ->  filename = Display Title
       Line order sets page order. Missing files fall back to filename."""
    for cand in ('music/%s/order.txt' % folder, 'music/order.txt' if folder == 'test' else None):
        if not cand:
            continue
        fp = os.path.join(ROOT, cand)
        if os.path.isfile(fp):
            pairs = []
            for line in open(fp, encoding='utf-8'):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                name, _, title = line.partition('=')
                pairs.append((name.strip(), title.strip()))
            return pairs
    return []


def build_music_set(folder, slug, label):
    # files in music/<folder>/ ; plus, for test, any loose files in music/
    files = [('music/%s/%s' % (folder, f)) for f in listdir('music/' + folder, AUDIO_EXT)]
    if slug == 'test':
        files += [('music/%s' % f) for f in listdir('music', AUDIO_EXT)]
    files = sorted(set(files), key=lambda s: os.path.basename(s).lower())

    titles = {}
    ordered = []
    for name, title in read_order(folder):
        match = [r for r in files if os.path.basename(r) == name]
        if match:
            ordered.append(match[0])
            if title:
                titles[match[0]] = title
    files = ordered + [r for r in files if r not in ordered]

    blocks = []
    for rel in files:
        f = os.path.basename(rel)
        blocks.append(
            '    <div class="track">\n'
            '      <div class="track-title">%s</div>\n'
            '      <div class="track-info">%s</div>\n'
            '      <audio controls preload="none">\n'
            '        <source src="%s" type="audio/%s">\n'
            '      </audio>\n'
            '      <a href="%s" download class="track-download">download</a>\n'
            '    </div>' % (
                html.escape(titles.get(rel, strip_order(f))), year_added(rel), url(rel),
                'wav' if f.lower().endswith('.wav') else 'mpeg', url(rel)))
    body = '''  <section class="section">
    <div class="section-label">music / %s</div>

%s

  </section>''' % (label, '\n\n'.join(blocks))
    write('music-%s.html' % slug, page(label, 'music', body))
    return len(files)


def build_music_index(n_test, n_ep):
    body = '''  <section class="section">
    <div class="section-label">music</div>
    <div class="index-list">
      <a href="music-test.html" class="index-row"><span>test</span><span class="index-count">%d</span></a>
      <a href="music-ep.html" class="index-row"><span>ep</span><span class="index-count">%d</span></a>
    </div>
  </section>''' % (n_test, n_ep)
    write('music.html', page('music', 'music', body))


# ---------- notes ------------------------------------------------------

DATE_RE = re.compile(r'^(\d{4})[-.](\d{2})[-.](\d{2})[-_. ]*(.*)$')


def build_notes():
    files = listdir('notes', NOTE_EXT)
    files.sort(key=lambda s: s.lower(), reverse=True)   # newest date first
    posts = []
    for f in files:
        raw = open(os.path.join(ROOT, 'notes', f), encoding='utf-8').read()
        lines = raw.replace('\r\n', '\n').strip('\n').split('\n')
        if not lines:
            continue
        title = lines[0].strip()
        rest = '\n'.join(lines[1:]).strip('\n')
        paras = [p.strip() for p in re.split(r'\n\s*\n', rest) if p.strip()]

        stem = os.path.splitext(f)[0]
        m = DATE_RE.match(stem)
        datestr = '%s.%s.%s' % (m.group(1), m.group(2), m.group(3)) if m else ''

        body_html = '\n'.join(
            '        <p>%s</p>' % html.escape(p).replace('\n', '<br>')
            for p in paras)
        posts.append(
            '    <article class="post">\n'
            '      <div class="post-date">%s</div>\n'
            '      <div class="post-title">%s</div>\n'
            '      <div class="post-body">\n%s\n      </div>\n'
            '    </article>' % (datestr, html.escape(title), body_html))

    body = '''  <section class="section">
    <div class="section-label">notes</div>

%s

  </section>''' % '\n\n'.join(posts)
    write('notes.html', page('notes', 'notes', body))
    return len(files)


# ---------- go ---------------------------------------------------------

def write(name, content):
    p = os.path.join(ROOT, name)
    old = open(p, encoding='utf-8').read() if os.path.exists(p) else None
    if old != content:
        open(p, 'w', encoding='utf-8', newline='\n').write(content)
        print('  updated %s' % name)
    else:
        print('  unchanged %s' % name)


if __name__ == '__main__':
    print('building dechets.us')
    g = build_gallery()
    t = build_music_set('test', 'test', 'test')
    e = build_music_set('ep', 'ep', 'ep')
    build_music_index(t, e)
    n = build_notes()
    print('  %d paintings, %d test tracks, %d ep tracks, %d notes' % (g, t, e, n))
