// PostToolUse hook (Edit|Write): format the edited .R file with Air, but only
// when an air.toml or .air.toml exists in its directory or any parent.
// Replaces the kit's jq one-liner (jq is absent here). Never fails the tool
// call: every problem ends in a silent exit 0.
import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { homedir } from "node:os";
import { spawnSync } from "node:child_process";

function hasAirConfig(file) {
  let d = dirname(file);
  for (;;) {
    if (existsSync(join(d, "air.toml")) || existsSync(join(d, ".air.toml"))) return true;
    const up = dirname(d);
    if (up === d) return false;
    d = up;
  }
}

try {
  const payload = JSON.parse(readFileSync(0, "utf8"));
  const file = payload?.tool_input?.file_path;
  if (typeof file === "string" && /\.[Rr]$/.test(file) && existsSync(file) && hasAirConfig(file)) {
    const local = join(homedir(), ".local", "bin", process.platform === "win32" ? "air.exe" : "air");
    const air = existsSync(local) ? local : "air";
    spawnSync(air, ["format", file], { stdio: "ignore", timeout: 25000 });
  }
} catch {
  // Malformed payload or missing air: leave the file as the tool wrote it.
}
process.exit(0);
