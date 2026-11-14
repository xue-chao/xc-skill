# Usage

```bash
/xc-article-illustrator path/to/article.md                      # auto-select type and style
/xc-article-illustrator path/to/article.md --type flowchart --style notion
/xc-article-illustrator path/to/article.md --density rich
/xc-article-illustrator path/to/article.md --batch-size 4       # up to 4 images in parallel after prompts are saved
/xc-article-illustrator api-design.md --preset tech-explainer
/xc-article-illustrator how-to-deploy.md --preset tutorial --density rich
/xc-article-illustrator article.md --preset tech-explainer --style notion   # preset with override

# Direct content input (paste mode)
/xc-article-illustrator
[paste content]
```

## Options

| Option | Description |
|--------|-------------|
| `--type <name>` | Illustration type (see Three Dimensions in SKILL.md) |
| `--style <name>` | Visual style (see [styles.md](styles.md)) |
| `--preset <name>` | Shorthand for type + style combo (see [style-presets.md](style-presets.md)) |
| `--density <level>` | Image count: minimal / balanced / rich |
| `--batch-size <n>` | Temporary generation batch size for this run. Default: `generation_batch_size` from EXTEND.md, otherwise 4. Clamp to 1-8. |

## Input Modes

| Mode | Trigger | Output Directory |
|------|---------|------------------|
| File path | `path/to/article.md` | Use `default_output_dir` preference, or ask if not set (values: Output Directory in SKILL.md) |
| Paste content | No path argument | `illustrations/{topic-slug}/` |
