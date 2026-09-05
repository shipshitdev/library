import { describe, expect, it } from "bun:test";
import { join } from "node:path";

const nodeEntryPoints = [
  ["bootstrap", "bootstrap.ts"],
  ["watch-pr", "watch-pr/watch-pr"],
] as const;

describe("Bun runtime guard", () => {
  for (const [name, path] of nodeEntryPoints) {
    it(`rejects Node before ${name} uses Bun-only APIs`, () => {
      const result = Bun.spawnSync(["node", join(import.meta.dir, path)]);

      expect(result.exitCode).toBe(1);
      expect(result.stdout.toString()).toBe("");
      expect(result.stderr.toString()).toBe(
        "Shipshit pstack tooling requires Bun (https://bun.sh). Install Bun, then re-run.\n"
      );
    });
  }
});
