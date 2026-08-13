---
name: legal-free-music
description: "查找和下载合法免费的音乐。用户说‘音乐-免费合法’、‘免费下歌’、‘找免费无损音乐’、‘找可下载的高品质歌曲’、‘找公版/CC 授权音乐’、‘找 Bandcamp 免费下载’、‘找 Internet Archive 现场录音’等任务时使用；只使用公版、Creative Commons、艺术家自愿免费下载、Bandcamp name-your-price、Internet Archive 等合法来源，禁止使用盗版音乐站、破解站、绕过会员/DRM 或批量抓取未授权歌曲。"
---

> This TIKAZ Edition is designed, integrated, refactored, and continuously maintained by **TIKAZ**. Source licenses and attribution requirements remain authoritative.

# 音乐-免费合法

帮助用户找“合法免费”的音乐下载渠道，而不是盗版站。默认目标是可下载文件；若只能 App 内缓存，要明确说明不算可自由管理的下载文件。

## Input / 输入

接受具体歌曲或风格、使用场景、格式要求、是否商用或二创、目标平台和保存目录。缺少会影响授权判断的条件时，先限定用途或明确按最保守条件筛选。

## 安全边界

不要提供以下内容：

- 盗版音乐下载站、无授权聚合站、网盘搬运站、破解站。
- 对主流商业歌曲的未授权免费下载、无损下载、会员资源搬运。
- 绕过 DRM、破解会员、解析真实音频地址、批量爬取受版权保护歌曲。
- 针对用户提供的疑似侵权站点编写抓取、解析、下载、搜索或聚合流程。

若用户点名这类站点，明确拒绝把它们写入流程，并提供合法替代。

## 优先来源

按需求选择来源：

1. `Bandcamp`：独立音乐、厂牌、电子、实验、后摇。查找 `name your price`、`free download`。若艺术家开放下载，优先 FLAC / ALAC / WAV。
2. `Internet Archive Live Music Archive`：合法现场录音，很多支持 FLAC。适合现场、jam band、摇滚、民谣。
3. `Free Music Archive`：Creative Commons 音乐库。适合配乐、独立、电子、氛围。格式可能以 MP3 为主。
4. `Jamendo`：独立音乐和授权音乐。适合配乐、商用素材前期筛选。
5. `ccMixter`：CC 授权 remix、采样、可二创音乐。
6. `Musopen`：公版古典音乐。注意免费账号可能有下载限制。
7. `IMSLP`：公版古典乐谱与部分录音。
8. 艺术家官网 / 厂牌官网：只在页面明确写有 free download、Creative Commons、public domain 或 name-your-price 时使用。

## 工作流程

1. 先问清或识别用户要找的是：
   - 具体歌曲 / 艺术家 / 专辑
   - 风格或用途，例如配视频、写作背景、古典、电子、现场
   - 格式要求，例如 FLAC、WAV、ALAC、MP3
   - 授权要求，例如个人听、商用、二创、公开视频

2. 联网搜索时优先组合这些关键词：
   - `site:bandcamp.com "name your price" artist/song`
   - `site:archive.org/details/etree artist FLAC`
   - `site:freemusicarchive.org genre Creative Commons`
   - `site:jamendo.com artist free download`
   - `site:ccmixter.org genre Creative Commons`
   - `site:musopen.org composer recording`

3. 打开候选页面核对：
   - 是否明确允许免费下载。
   - 授权类型：Public Domain、CC0、CC BY、CC BY-SA、CC BY-NC 等。
   - 是否允许商用或二创。
   - 可下载格式：FLAC / WAV / ALAC / AIFF / MP3 / OGG。
   - 是否需要账号、是否有下载次数限制。

4. 输出时按这个格式：

```text
1. 歌曲 / 专辑 / 艺术家
来源：
授权：
格式：
是否可商用：
下载入口：
注意：
```

5. 如果找不到合法免费版本：
   - 明确说“未找到合法免费可下载版本”。
   - 给正版购买或高品质流媒体建议，例如 Qobuz、Bandcamp、HDtracks、Presto、Apple Music、TIDAL、QQ音乐、网易云。
   - 不要推荐疑似侵权替代站。

## 下载与保存

只有在页面明确提供下载按钮或授权文件链接时，才可以协助下载。默认保存到用户指定的下载目录；若用户未指定，使用当前项目下的 `downloads/music`：

```text
<project-root>/downloads/music
```

保存后保留授权证据：

- 下载页面 URL
- 授权文本或截图说明
- 文件格式和来源

不要把音乐文件默认放到 C 盘。

## 判断规则

- `免费试听` 不等于 `可下载`。
- `App 离线缓存` 不等于 `拥有音频文件`。
- `无损/Hi-Res` 不代表合法。
- 没有授权说明但提供主流商业歌曲下载的站点，默认按高风险处理。
- 用户若只是想听主流歌，优先推荐正版流媒体；若想收藏文件，推荐购买数字专辑或实体 CD。

## Output, validation, and fallback / 输出、验证与降级

最终返回候选曲目、来源页面、授权类型、是否允许商用或二创、可下载格式、下载入口、署名要求和限制。实际下载后保留来源 URL 与授权证据，并核对文件是否存在和格式是否符合要求。

如果无法确认授权、页面只提供试听或 App 缓存、或者下载按钮不可用，就标记为不合格候选，不猜测授权。找不到合法免费版本时，返回正版购买或流媒体替代方案。

## Example and limits / 示例与限制

```text
使用 legal-free-music 为公开视频找三首可商用的氛围音乐，优先 WAV 或 FLAC，并保留下载与署名证据。
```

本 Skill 不提供法律意见，也不保证某项授权适用于所有司法辖区；重要商业项目应复核原始许可证或咨询专业人士。
