# AI Safety & Logging Protocol

## 1. Minimalist Logging (Token-Efficient)
- Before and after every action, append a single-line summary to `ACTION_LOG.md`.
- FORMAT: [Timestamp] | [Action Type] | [Target] | [Result Summary]
- Do NOT record full terminal stdout unless an error occurs. 

## 2. Smart Backup Policy (Original + 2)
- Before the first-ever modification of a file, create `filename.orig`. Never delete or overwrite `.orig`.
- For subsequent edits, maintain exactly two rotating backups: `filename.bak1` and `filename.bak2`.
- Always overwrite the oldest `.bak` file so that you only ever have: [Original], [Previous], and [Current].

## 3. Strict Safety
- Use of `rm` or `shred` is strictly forbidden. 
- To "delete" content, move it to a `.trash/` directory or comment it out.

## 4. Internal Tooling Awareness
- Use your internal `write_file` and `list_dir` tools to verify states before/after actions. 
- When recording logs, prioritize using your internal memory; only write to the markdown log to provide a "hard copy" for the human user.

