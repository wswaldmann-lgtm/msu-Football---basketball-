// Netlify build (base directory: stats/). One build serves any team's site:
//   spartans-gameday.netlify.app  -> TEAM unset or "msu" (the MSU app at the repo root)
//   wmu-gameday.netlify.app       -> TEAM=wmu (made from the MSU app + teams/wmu.json)
// Puts the app at the site root, the stats page at /stats, and watch-party
// invites at /p/<id> (see netlify.toml).
import { cpSync, mkdirSync, rmSync, readdirSync, existsSync, readFileSync, writeFileSync } from "node:fs";
import { execSync } from "node:child_process";
import path from "node:path";

const ROOT = path.resolve("..");          // the repo root, where the MSU app lives
const OUT = path.resolve("dist");
const TEAM = (process.env.TEAM || "msu").toLowerCase();
const run = (cmd, what) => {
  try { execSync(cmd, { cwd: ROOT, stdio: "inherit" }); return true; }
  catch { console.warn(`${what} skipped; using the committed files.`); return false; }
};

rmSync(OUT, { recursive: true, force: true });
mkdirSync(path.join(OUT, "stats"), { recursive: true });

let appDir, prefix, team = null;
if (TEAM === "msu") {
  // Refresh the calendar feeds from the schedule in index.html (same step as the GitHub Pages build).
  run("python3 tools/make_ics.py", "Calendar refresh");
  appDir = ROOT; prefix = "msu";
  cpSync(path.join(ROOT, "msu-spartans-share.html"), path.join(OUT, "msu-spartans-share.html"));
} else {
  team = JSON.parse(readFileSync(path.join(ROOT, "teams", `${TEAM}.json`), "utf8"));
  // Rebuild this team's app from the latest MSU app, then its calendar feeds.
  run(`python3 tools/make_team.py ${TEAM}`, `Rebuilding the ${TEAM} app`);
  run(`python3 tools/make_ics.py --dir ${TEAM} --prefix ${TEAM} --team ${team.short} --page ${team.site}/ --app "${team.appName}"`, "Calendar refresh");
  appDir = path.join(ROOT, TEAM); prefix = TEAM;
}

for (const f of ["index.html", "manifest.webmanifest", "sw.js", "icons"])
  cpSync(path.join(appDir, f), path.join(OUT, f), { recursive: true });
for (const f of readdirSync(appDir).filter(f => new RegExp(`^${prefix}-.*\\.ics$`).test(f)))
  cpSync(path.join(appDir, f), path.join(OUT, f));

// Stats and invite pages, recolored and renamed for this team
function themed(src) {
  let s = readFileSync(src, "utf8");
  if (!team) return s;
  const c = team.colors;
  const swaps = [
    ["#18453B", c.primary], ["#0F2B24", c.primaryDark], ["#1E5A4C", c.primaryLight], ["#C5A551", c.accent],
    ["#5BBF97", c.darkText], ["rgba(197,165,81,", `rgba(${hexRgb(c.accent)},`],
    ["MSU Watch Party", `${team.short} Watch Party`], ["Spartans game", `${team.nick} game`],
    ["Spartans Game Tracker", team.appName], ["Spartans Tracker Stats", `${team.nick} Tracker Stats`],
    ["Go Green! 💚", `${team.cheer} ${team.heart}`],
  ];
  for (const [a, b] of swaps) s = s.split(a).join(b);
  return s;
}
function hexRgb(h) { h = h.replace("#", ""); return [0, 2, 4].map(i => parseInt(h.slice(i, i + 2), 16)).join(","); }
writeFileSync(path.join(OUT, "stats", "index.html"), themed("public/index.html"));   // visitor stats
writeFileSync(path.join(OUT, "party.html"), themed("public/party.html"));            // watch-party invites

// Help search engines find the app (the stats page and invites stay out of search results)
const SITE = team ? team.site : "https://spartans-gameday.netlify.app";
writeFileSync(path.join(OUT, "robots.txt"), `User-agent: *\nAllow: /\nDisallow: /stats\nDisallow: /p/\nDisallow: /api/\nSitemap: ${SITE}/sitemap.xml\n`);
writeFileSync(path.join(OUT, "sitemap.xml"), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>${SITE}/</loc><lastmod>${new Date().toISOString().slice(0, 10)}</lastmod><changefreq>daily</changefreq></url>\n</urlset>\n`);

for (const must of ["index.html", "stats/index.html", "party.html", "icons/icon-192.png", `${prefix}-football.ics`])
  if (!existsSync(path.join(OUT, must))) throw new Error("Build is missing " + must);
console.log(`Built the ${TEAM.toUpperCase()} app + stats + invites into dist/`);
