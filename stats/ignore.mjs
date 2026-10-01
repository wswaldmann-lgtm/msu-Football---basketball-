// Netlify "ignore" check: decides whether this site needs a new build for this commit.
// Every production build costs Netlify credits, so a site only rebuilds when files
// that affect IT changed. Netlify runs this before building:
//   exit 0 -> skip the build (no credits used)    exit 1 -> build
import { execSync } from "node:child_process";

const team = (process.env.TEAM || "msu").toLowerCase();
const from = process.env.CACHED_COMMIT_REF, to = process.env.COMMIT_REF || "HEAD";
if (!from || from === to) process.exit(1);             // first build or a manual retry: build

let changed;
try {
  changed = execSync(`git diff --name-only ${from} ${to}`, { cwd: "..", encoding: "utf8" }).split("\n").filter(Boolean);
} catch { process.exit(1); }                           // can't tell what changed: build to be safe

// Server code and pages every site shares (rare changes)
const shared = [/^stats\/(build\.mjs|package\.json)$/, /^stats\/public\//, /^stats\/netlify\/(functions|lib)\//, /^tools\/make_ics\.py$/];
// Each site's own app. Other teams' apps are generated from the MSU app and committed in
// their folders, so an MSU change only rebuilds a team's site if it changed that team's app.
const mine = team === "msu"
  ? [/^index\.html$/, /^sw\.js$/, /^manifest\.webmanifest$/, /^icons\//, /^msu-/]
  : [new RegExp(`^${team}/`), new RegExp(`^teams/${team}\\.json$`)];

const relevant = changed.filter(f => [...shared, ...mine].some(re => re.test(f)));
console.log(relevant.length ? `Building ${team}: ${relevant.join(", ")}` : `Skipping ${team}: nothing it uses changed (${changed.length} files)`);
process.exit(relevant.length ? 1 : 0);
