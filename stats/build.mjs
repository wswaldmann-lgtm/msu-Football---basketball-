// Netlify build for spartans-gameday.netlify.app (base directory: stats/).
// Puts the Spartans Game Tracker app at the site root, the stats page at /stats,
// and the watch-party invite page at /p/<id> (see netlify.toml).
import { cpSync, mkdirSync, rmSync, readdirSync, existsSync } from "node:fs";
import { execSync } from "node:child_process";
import path from "node:path";

const ROOT = path.resolve("..");          // the repo root, where the app lives
const OUT = path.resolve("dist");

// Refresh the calendar feeds from the schedule in index.html (same step as the GitHub Pages build).
try { execSync("python3 tools/make_ics.py", { cwd: ROOT, stdio: "inherit" }); }
catch { console.warn("Calendar refresh skipped; using the committed .ics files."); }

rmSync(OUT, { recursive: true, force: true });
mkdirSync(path.join(OUT, "stats"), { recursive: true });

for (const f of ["index.html", "msu-spartans-share.html", "manifest.webmanifest", "sw.js", "icons"])
  cpSync(path.join(ROOT, f), path.join(OUT, f), { recursive: true });
for (const f of readdirSync(ROOT).filter(f => /^msu-.*\.ics$/.test(f)))
  cpSync(path.join(ROOT, f), path.join(OUT, f));

cpSync("public/index.html", path.join(OUT, "stats", "index.html"));   // visitor stats
cpSync("public/party.html", path.join(OUT, "party.html"));            // watch-party invites

for (const must of ["index.html", "stats/index.html", "party.html", "icons/icon-192.png"])
  if (!existsSync(path.join(OUT, must))) throw new Error("Build is missing " + must);
console.log("Built app + stats + invites into dist/");
