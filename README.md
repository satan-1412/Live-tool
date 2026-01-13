<div align="center">

<pre style="font-family: 'Courier New', monospace; background-color: #0d1117; color: #3fb950; border: 4px solid #1f2428; border-radius: 12px; padding: 25px; box-shadow: 0 0 25px rgba(63, 185, 80, 0.2); text-align: left; width: fit-content; margin: 0 auto;">
  _______________________________________________________
 |                                                       |
 |   .-----------------------------------------------.   |
 |   |   ___  ____  ____        _   _ ___            |   |
 |   |  / _ \/ ___|| __ )      | | | |_ _|           |   |
 |   | | | | \___ \|  _ \ _____| | | || |            |   |
 |   | | |_| |___) | |_) |_____| |_| || |            |   |
 |   |  \___/|____/|____/       \___/|___|           |   |
 |   |                                               |   |
 |   |   >> MODULE: FRONTEND_PLAYER                  |   |
 |   |   >> ENGINE: CANVAS_DANMAKU_V2                |   |
 |   |   >> RENDER: CSS_GRID_GALLERY                 |   |
 |   '-----------------------------------------------'   |
 |                                                       |
 |      [GRID]   [LIST]   [SRC]   [SET]   [LOG]      |
 |_______________________________________________________|
      /_\                                     /_\
</pre>

<br>

<h1 style="color: #3fb950; font-family: monospace; letter-spacing: 2px;">OSB PLAYER</h1>
<h3 style="color: #8b949e;">Next-Gen HLS Web Player with Smart Navigation</h3>

<p>
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3">
  <img src="https://img.shields.io/badge/JS-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JS">
  <img src="https://img.shields.io/badge/HLS.js-orange?style=for-the-badge&logo=rss&logoColor=white" alt="HLS">
</p>

</div>

---

## 📽️ 项目简介 (INTRODUCTION)

**OSB Player** 是专为 *Open Source Broadcaster* 生态系统打造的现代化 Web 前端。它摒弃了传统的列表式播放器设计，采用**数据驱动 (Data-Driven)** 的架构，直接解析 M3U8 播放列表的元数据，动态渲染出沉浸式的电视盒子风格界面。

> <samp>Design Philosophy: Minimalist, Fast, and Ephemeral.</samp>

### ✨ 核心特性 (KEY FEATURES)

| 功能模块 | 详细描述 |
| :--- | :--- |
| **💠 智能宫格导航** | **Auto-Grid Engine**: 前端自动提取 `group-title` 标签，生成动态分类导航栏与宫格卡片流。 |
| **🚀 即时弹幕系统** | **Stateless Danmaku**: 基于 HTML5 Canvas 的高性能弹幕层。弹幕随画面流过即销毁，**不存储、不联网、零痕迹**。 |
| **🔍 实时过滤引擎** | 顶部常驻搜索栏，支持毫秒级响应的频道关键词过滤，无需刷新页面。 |
| **🎬 沉浸式影院** | 无黑边全屏播放适配，集成 `LIVE` 状态指示灯与微动效反馈。 |
| **📱 响应式布局** | 完美适配 Desktop / Mobile / Tablet，提供类原生 App 的流畅体验。 |

---

## ⚙️ 部署与配置 (SETUP)

本项目设计为**纯静态 (Static)** 页面，无需后端服务器，支持 GitHub Pages 直接部署。

### 1. 绑定数据源
打开 `index.html`，找到配置区域，填入你的后端 M3U8 地址：

```javascript
// --- CONFIGURATION ZONE ---
const SYSTEM_CONFIG = {
    // 指向你的 live 仓库 raw 链接
    sourceUrl: '[https://raw.githubusercontent.com/username/live/main/TV.m3u8](https://raw.githubusercontent.com/username/live/main/TV.m3u8)',
    
    // 默认主题配置
    theme: 'elegant_dark',
    
    // 弹幕生命周期 (毫秒)
    danmakuSpeed: 8000
};

2. 图标适配 (Logo Mapping)
播放器会自动读取 #EXTINF 中的 tvg-logo 属性。
 * 推荐尺寸: 1:1 或 4:3 比例的透明 PNG。
 * 显示逻辑: 若未检测到 Logo，系统将显示默认的 OSB 终端图标。
🕹️ 交互指南 (USER GUIDE)
首页 (Lobby)
 * 点击导航栏: 切换不同的频道分类（如：动画、影视、国际）。
 * 搜索框: 输入关键词（如 "Tom"），宫格将自动折叠非匹配项。
 * 卡片点击: 进入全屏播放模式。
播放页 (Theater)
 * 底部输入栏: 发送即时弹幕（仅当前会话可见）。
 * 侧边滑动: 呼出快速切台列表。
 * ESC / 返回: 退出播放，返回宫格大厅。
<div align="center">


<p style="color: #666; font-size: 12px; font-family: monospace;">
[ SYSTEM READY ]

Designed for privacy and performance.

2026 © OSB Project | Open Source Initiative
</p>
</div>

