# EXTEND.md Schema

```yaml
---
version: 1
preferred_style: watercolor-journal   # watercolor-journal | comic-unified | impasto-warm | null(每次问)
preferred_image_backend: auto         # auto | ask | imagegen | ImageGen | GenerateImage | ...
generation_batch_size: 4
output_root: recipe-post              # 输出根目录，相对 cwd；最终 {output_root}/{slug}/
archive_root: ~/Desktop/漫画菜谱      # 桌面归档根目录；最终 {archive_root}/{YYYY-MM-DD}{菜名}/
language: zh                          # 转写与文案语言
whisper_model: null                   # 显式模型路径；null 时按语言自动定位
proxy: null                           # 模型下载代理，如 http://127.0.0.1:7890；null 直连
---
```

密钥（如 REDFOX_API_KEY）不放 EXTEND.md，放 `.xc-skills/.env` / `~/.xc-skills/.env`（gitignore）。