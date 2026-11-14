# 视频解析细节

## 目录

- [依赖与安装](#依赖与安装)
- [extract_video.py](#extract_videopy)
- [transcribe.py 与模型选择](#transcribepy-与模型选择)
- [字幕拼贴图读法](#字幕拼贴图读法)
- [核对清单](#核对清单)
- [recipe.md 模板](#recipemd-模板)

## 依赖与安装

```bash
brew install ffmpeg whisper-cpp   # macOS；其他平台用对应包管理器
```

whisper 模型（HuggingFace `ggerganov/whisper.cpp`，仅 HTTPS）：

| 语言 | 模型 | 说明 |
|------|------|------|
| 英文 | `ggml-small.en.bin` (~465MB) | 英文质量高 |
| 中文/多语 | `ggml-large-v3-turbo.bin` (~1.6GB) | 中文数字/术语可靠；small 多语版中文易幻觉 |

下载示例（直连超时走本地代理时加 `--proxy http://127.0.0.1:7890`）：

```bash
curl -L --connect-timeout 20 --retry 2 -o ~/models/ggml-large-v3-turbo.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin
```

## extract_video.py

```bash
python3 {baseDir}/scripts/extract_video.py <video> <outdir> \
  [--frame-interval 2] [--sub-fps 1] [--tile 12] [--sub-crop W:H:X:Y] [--no-subs] [--no-frames]
```

产物：`audio16.wav`（16kHz 单声道）、`frames/f_%03d.jpg`（第 N 张 = (N-1)*interval 秒）、`subs/m_%02d.jpg`（字幕条拼贴）。

字幕条默认裁剪：宽=全宽，高≈画面高×0.12，y≈画面高×0.74（适配竖屏底部字幕）。字幕位置不同时先读 2–3 张整帧目测坐标，用 `--sub-crop` 覆盖。无内嵌字幕时 `--no-subs`，仅靠转写+整帧。

## transcribe.py 与模型选择

```bash
python3 {baseDir}/scripts/transcribe.py <audio16.wav> --out <prefix> --lang zh \
  [--model PATH] [--threads 8] [--download] [--proxy URL]
```

模型解析顺序：`--model` > 环境变量 `WHISPER_MODEL` > `~/models/ggml-large-v3-turbo.bin`（zh）/ `ggml-small.en.bin`（en）。缺失且 `--download` 时按上表 URL 下载（HTTPS、超时、校验内容类型）。输出 `<prefix>.txt` / `<prefix>.srt`。

## 字幕拼贴图读法

- `m_01` 的 12 行 = 秒 0–11；`m_k` 行 r = (k-1)*tile + r 秒。逐张读完，重复行去重。
- 字幕是口播的权威文本；whisper 稿用于解字幕乱码句（如"中和"被识别成"中国家"）。
- 画面事实（数量、生熟、顺序、器具）必须看整帧确认，字幕/语音都不代表画面。

## 核对清单

- [ ] 每个数字（时间/用量）有字幕或语音出处；冲突已仲裁
- [ ] 食材清单与画面一致（含"半斤"这类口播量）
- [ ] 步骤顺序与画面一致（先菜后肉等）
- [ ] 生熟/形态细节记录（肥牛薄卷、变色即捞；番茄丁+块两种刀口）
- [ ] 注意点单独列出，供配图并入步骤
- [ ] 人物/闲聊按用户要求忽略

## 信息完整性核对

转写+字幕读完后，先列"信息行清单"：从字幕全量行中提取所有可操作行，逐条映射到 recipe.md；未映射的行要么补进菜谱，要么明确判定为纯闲聊。

必覆盖类别（缺一即不完整）：
- 用量：半斤/一大勺/一勺/一点/十几只 等
- 时间：烫1分半/咕嘟3分钟/焖1-2分钟 等
- 火候：大火/小火/锅热油热
- 替代料：黄酒或料酒、啥锅都行 等
- 条件规则：虾少加水/虾多不加 等
- 否定规则：不放盐/不用蒜/千万别冷水 等
- 生熟判断：变色就捞/煎至焦香通红/汤汁变浓 等

## recipe.md 模板

```markdown
# {菜名}

## 用料
| 食材 | 用量/处理 |

## 步骤
1. **{小标题}**（{mm:ss}）：…（关键数字加粗）

## 容易翻车的点
- …
```