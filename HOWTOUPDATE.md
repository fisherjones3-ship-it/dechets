# How to update your site

You don't edit any code. You put files in folders and the site rebuilds
itself. That's the whole system.

**Your site:** https://dechets.us
**Where it lives:** https://github.com/fisherjones3-ship-it/dechets

---

## The one thing to install

**GitHub Desktop** — free, from https://desktop.github.com

Install it, sign in with your GitHub account, and choose
**Clone a repository** → `fisherjones3-ship-it/dechets`.

That puts a folder on your computer that mirrors your website. From then on
every update is the same three steps:

1. **Put a file in the right folder**
2. Open GitHub Desktop, type a few words in the box at the bottom left,
   click **Commit to main**
3. Click **Push origin** at the top

Wait about two minutes. The site rebuilds itself and the change is live.

You never open an HTML file. You never type a command.

---

## The folders

```
images/          your paintings
music/test/      songs on the "test" page
music/ep/        songs on the "ep" page
notes/           your writing
```

---

## Adding a painting

Drop the image into **`images/`**. That's it — commit and push.

The gallery page rebuilds itself with the new painting in it, and the
lightbox works automatically.

**Order:** paintings appear in filename order. To control where one sits,
put a number at the front:

```
01-cow.jpg
02-sailor.jpg
```

Files without a number sort alphabetically. Mixing is fine.

**Size:** resize to about 1500–2000 pixels on the long edge before adding.
Anything under 1MB keeps the site fast.

---

## Adding a song

Drop the `.wav` into **`music/test/`** or **`music/ep/`**. Commit and push.

**The filename becomes the song title.** Put a number in front for order —
`01` shows at the top.

```
01-BOHEM.wav        shows as     BOHEM
02-Lander pt3.wav   shows as     Lander pt3
```

Spaces and capitals are fine. The number and the `.wav` are stripped off,
everything else is used exactly as you typed it.

The year is filled in automatically from when you added the file.

**Songs must go through GitHub Desktop**, not the website — github.com's
upload button rejects anything over 25MB and your songs are bigger than
that. GitHub Desktop handles up to 100MB per file.

---

## Adding a note

Make a text file in **`notes/`**. Name it with the date first:

```
2026-09-14-on-the-cardboard-pieces.txt
```

Inside, the **first line is the title**. Everything after is the body.
Leave a blank line between paragraphs:

```
On the cardboard pieces

I started these in the winter.

The boxes came from the shop on the corner.
```

Newest date appears at the top automatically. Write it in Notepad — save as
`.txt`, that's all it needs.

---

## Removing something

Delete the file from the folder, commit, push. The page rebuilds without it.

---

## Small edits without GitHub Desktop

For text-only changes you can work straight on github.com in your browser:
open the file, click the **pencil icon**, edit, click **Commit changes**.
Fine for notes and for deleting things. Not for songs.

---

## Changing the background drawing

The drawing behind every page is `images/bg.png`. It is white lines on a
transparent background — that's what keeps it from showing as a grey box.

- **To swap it:** replace `bg.png` with a new file of the same name. It must
  also be white line art on transparent, or you'll get a grey rectangle.
- **Stronger or fainter:** open `style.css`, find `--bg-opacity: 0.16;` near
  the top, change the number. `0.05` is barely there, `0.35` is loud. There's
  a second, lower value in the mobile section at the bottom.

---

## Your newsletter

Sign-ups go to Formspree and land at **fisher.jones@dechets.us**.
Manage them at https://formspree.io — the form is `mjybqnro`.
Free tier is 50 submissions a month.

---

## Things to avoid

- **Don't rename or delete `.nojekyll`, `CNAME`, `build.py`, or the
  `.github` folder.** They look pointless. They are what make the site work.
- **Don't edit `gallery.html`, `music.html`, `music-test.html`,
  `music-ep.html` or `notes.html`.** They are rewritten from the folders on
  every push, so your changes would be wiped. Change the folders instead.
- **You can edit `index.html` and `style.css`** — those are yours, nothing
  overwrites them.
- **Keep songs under 100MB each.** That's a hard GitHub limit.

---

## If something breaks

GitHub keeps every version. Go to the repository, click the clock icon
(**History**), find the last version that worked, and revert to it.
Nothing is ever permanently lost.

If a push seems to do nothing, check the **Actions** tab on GitHub — a red X
means the rebuild failed and the message there will say why.

---

## What costs money

Nothing. GitHub Pages hosting is free, the rebuild robot is free for public
repositories, and Formspree's free tier covers 50 sign-ups a month.

The only bill is your domain, `dechets.us`, which renews **28 March 2027**.
