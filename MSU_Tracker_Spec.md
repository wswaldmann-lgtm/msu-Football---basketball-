# MSU Spartans Calendar Tracker: Spec & Roadmap

**Owner:** Michael (wswaldmann@gmail.com)
**Calendar:** Google Calendar, primary
**Current version:** v1 (cruise edition), runs daily as a scheduled task
**Active window:** through **November 17, 2026**, then it shuts itself off

---

## 1. Purpose

Michael is on a cruise and can't keep up with schedule changes. The tracker keeps his calendar accurate for **Michigan State football and men's basketball**. It fills in game times and TV as they're announced, adds betting lines and previews as games get close, and posts final scores afterward. Any change it makes is quiet: no notification emails, no invites.

---

## 2. What v1 does on every run

### Step 0: Stop check
- If today is **after Nov 17, 2026**, it does nothing except report: *"MSU calendar task has ended — you can delete this scheduled task."*

### Step 1: Find the games
- It lists calendar events from **today through 14 days out**.
- **Game events** it recognizes:
  - Football: `MSU Football vs ___` / `MSU Football at ___`
  - Basketball: `🏀 MSU vs/at ___` or `MSU Basketball vs ___`
- **Ignored:** `⏰ Update…` reminder events. These are never edited or deleted.
- **Duplicates:** if two events exist for the same game, both get the same updates.

### Step 2: Confirm time and TV (all games in the 14-day window)
- It searches msuspartans.com, ESPN, Big Ten and schedule sites for the confirmed **kickoff/tip time** and **TV network**.
- If the event time is wrong or still a placeholder ("time TBA" / all-day), it sets the real time:
  - Football events are **3.5 hours** long.
  - Basketball events are **2 hours** long.
  - It uses the game's **local time zone** with the correct UTC offset.
- Once the time is set, it removes "(time TBA)" from the title.
- It adds the TV network to the description.

### Step 3: Game preview (games within 2 days, and always on game day)
It searches sportsbooks, odds and prediction sites, and the Lansing State Journal. Then it rewrites the description in this format:

```
Kickoff 12:00 PM ET · TV: Peacock
RECORDS: MSU 2-4 (0-4 B1G) · Northwestern x-x
THE LINE: MSU -3.5 · ML -165/+140 · O/U 47.5
MODEL: MSU 27, NU 23
LSJ PICK: Michigan State
KEYS: 1) … 2) … 3) …

Spartans Game Tracker: https://spartans-gameday.netlify.app
```

### Step 4: Final score (games that finished yesterday)
- It adds a one-line **FINAL** and a one-sentence recap at the **top** of that game's description.

### Step 5: Summary
- It ends each run with a 2–4 line summary of what changed, or "No changes today."

---

## 3. Rules (guardrails)

| Rule | Why |
|---|---|
| Always `notificationLevel: NONE` on updates | No emails are sent to anyone |
| Never create or delete events | Michael owns the schedule; the tracker only enriches it |
| Never invite anyone | Calendar stays private |
| Never touch non-MSU events | Medication reminders, cruise itinerary, etc. are off-limits |
| Only edit when there is real new info | Avoids pointless churn and keeps the "updated" history clean |
| Don't edit `⏰ Update…` reminders | Those are Michael's own prompts |

---

## 4. Current schedule in the window (as of Oct 12, 2026)

| Date | Game | Time | TV | Status |
|---|---|---|---|---|
| Sat Oct 17 | 🏈 vs Northwestern | 12:00 PM ET | Peacock | Confirmed. Preview due Thu/Fri |
| Tue Oct 20 | 🏀 vs UConn (exh.) | 7:00 PM ET | BTN | Confirmed |
| Sat Oct 24 | 🏈 at UCLA (Rose Bowl) | **TBA** | **TBA** | Placeholder at 12 PM ET; watching for Big Ten announcement |
| Sun Oct 25 | 🏀 at Marquette (exh.) | 12 PM CT / 1 PM ET | YouTube | Confirmed |
| Sat Nov 7 | 🏈 at Michigan | TBA | TBA | `⏰` reminder set for Oct 24 |

**Last result:** Illinois 38, MSU 37 (OT), Oct 10. MSU is 2–4.

---

## 5. Known issues found in v1 runs

1. **Some sites block direct page reads.** msuspartans.com schedule pages can't be fetched directly during unattended runs. The tracker works around this through news articles, ticket sites and schedule aggregators.
2. **Some sources go stale.** Wikipedia team pages showed blank times and 0–0 records well into the season, so they aren't reliable for live data.
3. **Score order varies between sites.** "37–38" vs "38–37" caused a false "sources disagree" note. The tracker should always confirm the winner from an official recap.
4. **Tracker links are inconsistent.** Basketball events point to the GitHub Pages site; football events point to the Netlify site.
5. **The calendar listing is huge.** Daily medication and cruise events make the 14-day listing very large. Filtering by "MSU" fixes this.
6. **Placeholder times aren't flagged.** The UCLA event sits at 12 PM ET with "Game time TBD" in the description, but the title has no "(time TBA)", so it's easy to mistake for a real time.

---

## 6. Enhancements for future versions

### v1.1: Quick wins
- [ ] **Push notification when a TBA time is announced.** For example: "UCLA kickoff set: 3:30 PM PT on FOX." Silent otherwise.
- [ ] **Show cruise-local time.** Read the "Cruise — [Port]" events and add a line such as *"In Rome that's 6:00 PM local."*
- [ ] **One tracker link on every event.** Pick Netlify or GitHub Pages and use it everywhere.
- [ ] **Flag placeholders clearly.** Add "(time TBA)" to the title of any event still on a placeholder time.
- [ ] **Handle the `⏰ Update` reminders automatically.** When a reminder's date arrives, do what it asks (e.g., check the Michigan kickoff time) instead of waiting for Michael.
- [ ] **Search the calendar by keyword.** Use the "MSU" / "🏀" text filter instead of pulling every event.

### v1.2: Better previews
- [ ] **Injury and availability notes** for key players on both teams.
- [ ] **Weather** for outdoor football games: temperature, wind, rain chance.
- [ ] **Line movement:** opening line → current line.
- [ ] **Head-to-head history:** last meeting and the all-time series.
- [ ] **Where to listen:** Spartan Sports Network radio and the SiriusXM channel.
- [ ] **Multiple prediction sources:** ESPN FPI, SP+ and Vegas, side by side.

### v1.3: Better post-game
- [ ] **Mini box score:** leading passer, rusher and receiver, plus team totals.
- [ ] **Updated record and standings** after each game.
- [ ] **Highlights link** (YouTube or Big Ten).
- [ ] **Bet results:** whether MSU covered the spread and whether the game went over or under.

### v2: Bigger features
- [ ] **Weekly digest email** every Monday: last week's results, this week's games, times and TV.
- [ ] **Season log saved to the Project.** A running doc of every result, line and recap, so the season history lives in one place.
- [ ] **Full basketball season.** Extend past Nov 17 to cover the non-conference and Big Ten slate through March, including tournament seeding.
- [ ] **Postseason mode.** Watch bowl eligibility (6 wins) and add bowl or NCAA Tournament games as they're announced. That would need permission to create events.
- [ ] **Source priority list:** official site → Big Ten → ESPN/CBS → aggregators, with at least two sources required before changing a time.
- [ ] **Other sports:** hockey and women's basketball, if wanted.
- [ ] **Change log in every description:** "Updated Oct 12: time confirmed."

---

## 7. Open questions for Michael

1. Should the tracker keep running after the cruise (past Nov 17), at least for basketball?
2. Push notifications: only for big changes (time announced, final score), or a daily ping on game days?
3. Which tracker link should be the standard, Netlify or GitHub Pages?
4. Would you like betting content (lines, cover results) kept, expanded, or dropped?
