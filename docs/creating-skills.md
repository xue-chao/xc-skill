# 新建 / 移植 Skill 规范

仓库宪法见 [../AGENTS.md](../AGENTS.md)。本文件是作者侧操作规范与"内联约定母版"——skill 必须自包含，下列母版片段要**逐字复制**进每个 SKILL.md，不得让 SKILL.md 链接本文件。

## 硬性要求

| 要求 | 细节 |
|------|------|
| 前缀 | 一律 `xc-`（逆向 API 类用 `xc-danger-`） |
| name | ≤64 字符，仅小写字母/数字/连字符 |
| description | ≤1024 字符，第三人称，"做什么 + 何时用"，含中英文触发词 |
| SKILL.md 正文 | <500 行，细节进 `references/` |
| references | 从 SKILL.md 一层深链接，避免引用套引用 |
| 自包含 | 不链接 skill 目录外文件；不硬依赖未移植组件 |

## Frontmatter 模板

```yaml
---
name: xc-<name>
description: <第三人称。做什么 + 何时用 + 触发词。>
version: 1.0.0
metadata:
  homepage: https://github.com/xue-chao/xc-skill#xc-<name>
---
```

## 新建步骤

1. 创建 `skills/xc-<name>/SKILL.md`（frontmatter + 主指令）
2. 按需添加 `references/`（细节）、`scripts/`（脚本）、`prompts/`（提示词模板）
3. 需要用户选择 → 内联下方「User Input Tools」母版
4. 生成图像 → 内联下方「Image Generation Tools」母版
5. 需要偏好 → 内联「EXTEND.md 加载」步骤，schema 放 `references/config/preferences-schema.md`，首次引导放 `references/config/first-time-setup.md`
6. 有脚本 → 加「Script Directory」段
7. 更新根 README 的 skill 列表
8. `./scripts/install.sh xc-<name>` 安装并实际跑一遍验证

## 母版一：User Input Tools（需要向用户提问的 skill 必须内联）

放在 SKILL.md 开头简介之后、主流程之前，全文唯一一处：

```markdown
## User Input Tools

When this skill prompts the user, follow this tool-selection rule (priority order):

1. **Prefer built-in user-input tools** exposed by the current agent runtime — e.g., `AskUserQuestion`, `request_user_input`, `clarify`, `ask_user`, or any equivalent.
2. **Fallback**: if no such tool exists, emit a numbered plain-text message and ask the user to reply with the chosen number/answer for each question.
3. **Batching**: if the tool supports multiple questions per call, combine all applicable questions into a single call; if only single-question, ask them one at a time in priority order.

Concrete `AskUserQuestion` references below are examples — substitute the local equivalent in other runtimes.
```

## 母版二：Image Generation Tools（生成图像的 skill 必须内联）

放在「User Input Tools」之后。后端不锁死任何平台：

```markdown
## Image Generation Tools

Resolve the image backend in this order:

1. **User names a backend** in the current message → use it.
2. **`preferred_image_backend`** in `EXTEND.md` names a backend available now → use it. `ask` means ask every run.
3. **Auto-select** (preference `auto`, unset, or the pinned backend is unavailable), first match wins:
   - **Codex `imagegen`** skill is in your available skills → you are in Codex and MUST use it: `Skill` with `skill: "imagegen"`, passing the prompt file's content plus output path and aspect ratio. It outranks non-native skills.
   - **Cursor `GenerateImage`** → use it (outranks non-native skills). It has no aspect-ratio parameter, so state the aspect ratio / dimensions in the `description` prompt; it saves to a tool-managed location, so copy the file to the expected output path. Reference images go in `reference_image_paths`.
   - **Qoder `ImageGen`** → use it (outranks non-native skills). Pass the prompt file's content as `prompt`, pick the `size` preset closest to the target aspect ratio, and copy the returned image to the expected output path. Reference images go in `images`.
   - **Other runtime-native image tool** (e.g., Hermes `image_generate`) → use it the same way.
   - Exactly one non-native image-generation skill or CLI installed → use it.
   - Several non-native backends → ask the user once, batched with other initial questions.
4. **None available** → tell the user and ask how to proceed.

**⛔ Raster only**: never substitute SVG, HTML/CSS, canvas, or other code-based rendering for a raster image, even for diagram-like content. If no raster backend resolves, go to step 4.

**⛔ No bitmap text patching**: never use ImageMagick, Pillow, Canvas, SVG, HTML/CSS, OCR scripts, or any other overlay to cover, rewrite, erase, stroke, or replace text inside an already generated image. Regenerate from a corrected prompt, redraw with less or no on-image text, or ask the user which imperfect candidate to keep.

**Prompt file (hard)**: before invoking any backend, write each image's full, final prompt to its own file under `prompts/` (`NN-{type}-[slug].md`) and pass that file (or its content) to the backend. It is the reproducibility record and lets you switch backends without rewriting prompts.

Tool names above are examples; use the local equivalent in other runtimes.
```

按 skill 需要可微调括号内的产物描述（如 labels/captions），其余保持一致。母版更新后，手动同步到所有已内联的 SKILL.md。

## 母版三：EXTEND.md 加载（需要偏好的 skill 必须内联）

作为流程 Step 1 的阻塞子步骤：

```markdown
**Load Preferences (EXTEND.md) ⛔ BLOCKING** — first match wins:

| Priority | Path | Scope |
|----------|------|-------|
| 1 | `.xc-skills/<skill-name>/EXTEND.md` | Project |
| 2 | `${XDG_CONFIG_HOME:-$HOME/.config}/xc-skills/<skill-name>/EXTEND.md` | XDG |
| 3 | `$HOME/.xc-skills/<skill-name>/EXTEND.md` | User home |

Found → read, parse, display summary. Not found → run first-time setup before anything else.
```

## 母版四：Script Directory（有脚本的 skill 必须内联）

```markdown
## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `{baseDir}`
2. Script path = `{baseDir}/scripts/<script-name>`
3. Python scripts run with `python3`; shell scripts with `bash`
4. Replace all `{baseDir}` in this document with the actual value

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/main.py` | Main entry point |
```

## 移植检查清单

- [ ] 目录与 name 改为 `xc-` 前缀，version 重置 `1.0.0`
- [ ] frontmatter homepage 指向本仓库
- [ ] 配置路径 `.baoyu-skills` 等 → `.xc-skills`（含 XDG 与 `$HOME` 路径、PowerShell 示例）
- [ ] 命令示例 `/旧名` → `/xc-新名`
- [ ] 删除/改写依赖未移植 skill 或 packages 的分支（如 codex-imagegen 包装器）
- [ ] 图像后端规则替换为本仓库母版二
- [ ] SKILL.md 末尾加 `## Credits`：原仓库链接 + 许可证 + 改动说明
- [ ] `grep -ri 原前缀` 仅剩 Credits 中的出处
- [ ] 链接检查：所有 markdown 链接指向 skill 内存在的文件
- [ ] 更新根 README 列表，安装后实际跑一遍