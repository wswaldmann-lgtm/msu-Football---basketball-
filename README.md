# Spartans Game Tracker

A free, unofficial fan app for Michigan State football and basketball: schedules, countdowns, live scores, rankings, tailgate plans and watch-party invites, all in one place on your phone.

**Open it:** https://wswaldmann-lgtm.github.io/msu-Football---basketball-/

---

## The basics

1. **Put it on your home screen** so it opens like a real app.
   - **iPhone:** open the link in Safari, tap **Share** (the square with the arrow), then **Add to Home Screen**.
   - **Android:** open the link in Chrome, tap **⋮**, then **Add to Home screen** or **Install app**.
2. **Tap in** from the start screen. The fight song plays; the 🔊 button at the top mutes it.
3. **Use the bar at the bottom:**

   | Button | What it does |
   |---|---|
   | 🏈 Football | Football schedule |
   | 🏀 Basketball | Basketball schedule |
   | ⚡ Next Game | Jumps to the next game and opens it |
   | 🍔 Tailgate / 📺 Watch Party | Tailgate planner on the football tab, watch-party invites on the basketball tab |
   | 🔥 Trash Talk | A one-liner for the group chat |

4. **Tap any game** to open its preview and details.
5. Tap **?** at the top of the app any time for the built-in guide.

---

## Everything in more detail

### 📅 Schedule & games
- The countdown at the top always shows the next game.
- Each game card shows the date, time, TV network and where to stream it. Tap it for the preview and prediction.
- Filter with **All Games**, **Home**, **Away** or **Marquee**. The progress bar and record box track the season.

### 🔴 Live scores & rankings
- The **Scoreboard** card loads the latest MSU score. Tap **↻** to refresh; it turns red while a game is live.
- **Rankings & Standings** opens the AP Top 25 or the Big Ten standings, with MSU highlighted.

### 📆 Add games to your calendar
Each sport has an **Add games to your calendar** card. Subscribe once (iPhone/Mac Calendar or Google Calendar) and new kickoff and tip-off times appear on their own as they're announced.

### 🍔 Tailgate planner (football)
1. On the football tab, tap **Tailgate** and pick a home game.
2. **Who's Coming?** Add names and how many each person brings. The headcount adds up at the bottom.
3. **Who's Bringing What?** Starts with the basics (burgers, buns, cooler, grill, chairs, cornhole). Check items off, edit them, add your own, and put a name next to each.
4. **Share Plan** turns the whole thing into one text for the crew.

The tailgate plan is saved on your phone only, so share it to keep everyone in the loop.

### 📺 Watch Party (basketball)
No tailgate for hoops, so throw a watch party at a bar or someone's house.

**Hosting one**
1. On the basketball tab, tap **Watch Party**.
2. Pick the game and fill in **where**, the **address**, the **meet time**, your name and an optional note ("wings half off").
3. Tap **Create & Send Invite** and text the link to your friends.

**What your friends see**
- They tap the link (no app or sign-up needed) and answer 🙌 **Meet you there** (with how many are coming), 🤔 **Maybe**, or 😞 **Can't make it**.
- They can change their answer any time, and there's a map button to the spot.

**Forwarding**
- Anyone can tap **Invite a friend** to pass the invite along.
- People who answer from a forwarded link show up as "Sue *via Dave*," so you can see how word spread.

**Keeping track**
- Your parties are listed at the bottom of the Watch Party screen with live counts ("4 coming · 1 maybe").
- **Who's coming** opens your host view with everyone's answers. You can remove an answer with ×; guests can't.

### 📣 Share Hype & 🔥 Trash Talk
- **Share Hype** writes a countdown message ("6 days until MSU vs…") and opens your phone's share menu.
- **Trash Talk** serves up a one-liner. 🎲 for another, 📋 to copy.

### ⚙️ Buttons at the top
**?** guide · **🔊/🔇** fight-song intro on/off · **🌙/☀️** dark mode · **✕** back to the start screen

### 🔒 Privacy
No accounts or sign-ups. The app counts how many phones open it using a random ID, with no names or personal info. Tailgate lists stay on your phone. Watch-party invites and answers are stored on the invite service so the host and guests can see them.

### 💚 Support
Free, ad-free, made by a Spartan fan. The **Support this app** button at the bottom of the schedule goes to Venmo (@Sparty-Tracker).

*Unofficial fan app. Not affiliated with Michigan State University.*

---

## For the app owner: how it's run

**The app** is one file, `index.html`. Every push to `main` publishes it to GitHub Pages via `.github/workflows/pages.yml`. The old link (`msu-spartans-share.html`) redirects to the new address. One-time setup: repo **Settings → Pages → Build and deployment → Source: GitHub Actions**.

**Calendars:** `msu-football.ics` and `msu-basketball.ics` are the subscription feeds. Keep them at this address; subscribers' calendars point here.

**Spartans Gameday (Netlify project `spartans-gameday`)** runs the parts that need a server. Its code is in [`stats/`](stats/):
- **Visitor stats page:** https://spartans-gameday.netlify.app (opens per day, unique phones, top states)
- **Watch-party invites and answers:** `/p/<party id>`

One-time setup: in Netlify, open **spartans-gameday → Link repository**, choose this repo, and set the base directory to `stats`. After that it redeploys on its own whenever this repo changes.

**Fight-song intro:** synthesized in code (baritones and tubas) from the public-domain melody of "Victory for MSU" (F. I. Lankey, 1915). No audio file.
