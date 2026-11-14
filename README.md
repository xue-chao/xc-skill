# xc-skill

我的 AI Agent 技能仓库，面向 Qoder / Claude Code / Codex 等支持 Agent Skills 的运行时。架构参考 [JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills)：**每个 skill 自包含、可单独拷走安装，渐进式披露控制上下文成本**。

## Skill 列表

| Skill | 说明 | 来源 |
|-------|------|------|
| [xc-article-illustrator](skills/xc-article-illustrator/SKILL.md) | 文章插图：分析文章结构，按 Type × Style × Palette 三维系统定位并生成插图（23 种风格、4 种色板、29 种预设，默认水彩小清新） | 移植自 baoyu-article-illustrator（MIT） |

> **只装你需要的 skill。** 每个已安装 skill 的 description 都会常驻 agent 上下文，全量安装会带来不必要的开销。

## 安装

### 方式一：安装脚本（推荐）

```bash
./scripts/install.sh --list                  # 查看可用 skill
./scripts/install.sh xc-article-illustrator  # 软链到 ~/.qoder-cn/skills
./scripts/install.sh --all                   # 安装全部
./scripts/install.sh --target ~/.claude/skills xc-article-illustrator  # 装到 Claude Code
./scripts/install.sh --copy xc-article-illustrator  # 复制而非软链
```

默认目标是 `~/.qoder-cn/skills`（Qoder 全局技能目录），可用 `--target` 或环境变量 `XC_SKILLS_TARGET` 覆盖。

### 方式二：手动软链

```bash
ln -s "$(pwd)/skills/xc-article-illustrator" ~/.qoder-cn/skills/xc-article-illustrator
```

### 方式三：项目级安装

把需要的 skill 目录整个拷进项目（例如 `.agents/skills/` 或 `.qoder/skills/`），skill 自包含，不依赖仓库其余部分。

## 配置

偏好与密钥分离，项目级优先于用户级：

| 类型 | 项目级 | 用户级 |
|------|--------|--------|
| 偏好（EXTEND.md） | `.xc-skills/<skill-name>/EXTEND.md` | `~/.xc-skills/<skill-name>/EXTEND.md` |
| 密钥（.env） | `.xc-skills/.env` | `~/.xc-skills/.env` |

- EXTEND.md 由各 skill 首次运行时引导创建（风格、水印、输出目录、图像后端等），schema 见各 skill 的 `references/config/preferences-schema.md`。
- `.env` 已被 `.gitignore` 排除，**不要提交密钥**。

## 目录结构

```
xc-skill/
├── README.md               # 本文件：skill 目录 + 安装说明
├── AGENTS.md               # 仓库约定（给 agent 和贡献者看的宪法）
├── docs/
│   └── creating-skills.md  # 新建/移植 skill 的规范
├── scripts/
│   └── install.sh          # 选择性安装脚本
└── skills/
    └── xc-<name>/          # 每个 skill 自包含
        ├── SKILL.md        #   frontmatter + 主指令（<500 行）
        ├── references/     #   按需加载的细节文档（一层深）
        ├── scripts/        #   可选：Python/shell 脚本
        └── prompts/        #   可选：提示词模板
```

## 贡献 / 新建 skill

见 [AGENTS.md](AGENTS.md) 与 [docs/creating-skills.md](docs/creating-skills.md)。核心规则：

1. 命名统一 `xc-` 前缀
2. skill 目录自包含：SKILL.md 与 references 不得链接目录外文件
3. SKILL.md < 500 行，细节拆进 references/ 按需加载
4. 移植他人 skill 保留出处声明（Credits）

## 致谢

- [JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills)（MIT）— 架构范式与 xc-article-illustrator 的原始实现

## License

[MIT](LICENSE)