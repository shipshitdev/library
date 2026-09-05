import { describe, expect, it } from "bun:test";
import { parseArgs } from "./cli.ts";
import { runLane } from "./run.ts";

const base = ["--parent", "codex", "--provider", "claude", "--effort", "high",
  "--mode", "read-only", "--prompt", "/workspace/prompt.md", "--cwd", "/workspace",
  "--output", "/workspace/output.md", "--receipt", "/workspace/receipt.json"];

describe("harness-owned role selection", () => {
  it("requires the harness to supply a model", () => {
    expect(() => parseArgs(base)).toThrow("model is required");
  });
  it("preserves an explicit supported-provider model without a public default matrix", () => {
    const options = parseArgs([...base, "--model", "operator-selected-model"]);
    expect(options?.model).toBe("operator-selected-model");
    expect(options?.effort).toBe("high");
  });
  it("rejects same-provider external delegation", async () => {
    const args = [...base, "--model", "operator-selected-model"];
    args[3] = "codex";
    const options = parseArgs(args);
    if (options === null) throw new Error("expected options");
    await expect(runLane(options)).rejects.toThrow("native to parent");
  });
});
