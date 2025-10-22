code-tools (Python)

Portable CLI providing consistent subcommands for prompts across projects.

Install

- Local dev (editable):
  - cd tools && pip install -e .[web]
- User install:
  - cd tools && pip install .[web]

Usage examples

- List: code-tools list_dir --path . --depth 1
- Search files: code-tools search_file --glob "src/**/*.py"
- Grep: code-tools grep_code --pattern "def main" --paths "src,lib"
- Read: code-tools read_file --path docs/code-assistant.md --start 1 --end 200
- Fetch: code-tools fetch_content --url <https://example.com>
- Replace: code-tools search_replace --file ./.dimitri/design-system.md --replacements @reps.json
- Create: code-tools create_file --file out.txt --content @content.txt --add-last-line-newline
- Edit: code-tools edit_file --file out.txt --patch @new.txt
- Memory: code-tools search_memory --dir ./.dimitri/memory --query "auth flow" --topk 5

JSON responses

- Always prints a single JSON object with ok/tool/version and data or error.

Notes

- `fetch_content` requires optional extra `web` (pip install .[web]).
- `search_web` is a placeholder that returns an error unless you wire a provider.
- Tests
- Run smoke tests with pytest:
-   cd tools && python -m pip install -e .[web] && python -m pip install pytest jsonschema && pytest -q
