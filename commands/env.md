# Env - Environment Variable Management

Discover the environment variables the code actually reads, keep
`.env.example` truthful, validate the local `.env` against it, and make sure
no secret file can reach git.

## Usage

```bash
/env              # full pass: discover, scaffold templates, validate (default)
/env validate     # check only — code vs .env.example vs local .env, report gaps
/env scaffold     # regenerate .env.example templates from the code
```

## Workflow

Use the `env-setup` skill, passing the mode through (`setup` default /
`validate` / `scaffold`).

1. **Parse the argument** into a mode. Unknown argument → print Usage, do not
   guess.
2. **Route** to `env-setup` — it scans for env reads, groups templates by
   service, validates without printing secret values, and audits `.gitignore`
   coverage.
3. **Defer** to the skill's gates: it never writes a real `.env`, and confirms
   before overwriting a hand-edited `.env.example`.

## Gates

- `validate` is read-only. `setup`/`scaffold` write only template files and
  `.gitignore` rules — never real secrets, never a real `.env`.
