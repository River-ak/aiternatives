# Design System: aiternatives

> AI 工具替代方案引擎 — V1 视觉定调
> 风格融合：Vercel 的结构克制 + Stripe 的蓝调阴影 + Apple 的呼吸感间距 + Linear 的精密层级

---

## 1. Visual Theme & Atmosphere

aiternatives 的设计语言定调为 **"数据中的呼吸感"**——一个以结构化对比表为核心、但绝不压抑的浏览体验。整体基调是白底黑字，像 Vercel 一样让内容自己说话，但借用 Stripe 的蓝调阴影注入温度。排版紧凑但不拥挤，间距慷慨但不浪费。这是给做决策的人的页面——清晰、可信、不花哨。

**核心原则：**
- 白色为主画布（`#fafbfc`），近乎纯白但带微妙的蓝灰底色，避免刺眼
- 阴影系统采用 Vercel 的 "shadow-as-border" 技法：`0px 0px 0px 1px` 替代传统边框
- 强调色唯一：**Electric Indigo**（`#5c6cf0`）——只用于联盟链接按钮和核心交互
- 折扣徽章使用暖琥珀色（`#f59e0b`）——独立于主强调色，视觉上形成信息层级
- 排版使用 Inter Variable，开启 `"cv01"` 替代小写 a，更几何化
- 大标题使用负 letter-spacing（-0.96px 到 -1.5px），像 Vercel 一样"压缩"但不失可读性
- 联盟按钮必须是最突出的视觉元素——它是转化漏斗的入口

---

## 2. Color Palette & Roles

### 背景与表面

| Token | Value | Role |
|-------|-------|------|
| `--bg-primary` | `#fafbfc` | 主页面背景 |
| `--bg-card` | `#ffffff` | 卡片/组件表面 |
| `--bg-hover` | `#f3f4f6` | 行悬停背景 |
| `--bg-subtle` | `#f8f9fb` | 极浅背景区分（斑马纹、交替行） |

### 文字层级

| Token | Value | Role |
|-------|-------|------|
| `--text-primary` | `#0f1115` | 主标题、工具名、核心文字 |
| `--text-secondary` | `#4a4f5c` | 次要描述、定价说明 |
| `--text-tertiary` | `#8b919e` | 辅助信息、时间戳、元数据 |
| `--text-disabled` | `#c3c8d1` | 禁用/占位符 |

### 强调色（唯一）

| Token | Value | Role |
|-------|-------|------|
| `--accent` | `#5c6cf0` | 主强调色：联盟按钮背景、链接、聚焦环 |
| `--accent-hover` | `#4a5ae0` | 按钮悬停变深 |
| `--accent-light` | `#eef0ff` | 强调色浅底（标签、高亮行） |
| `--accent-ring` | `rgba(92, 108, 240, 0.35)` | 聚焦环 |

### 折扣徽章

| Token | Value | Role |
|-------|-------|------|
| `--discount-bg` | `#fef3c7` | 折扣徽章背景 |
| `--discount-text` | `#b45309` | 折扣徽章文字 |
| `--discount-border` | `#fcd34d` | 折扣徽章边框 |

### 评分颜色

| Token | Value | Role |
|-------|-------|------|
| `--rating-high` | `#059669` | 4.0+ 评分文字/背景 |
| `--rating-mid` | `#d97706` | 3.0-3.9 评分 |
| `--rating-low` | `#dc2626` | < 3.0 评分 |

### 阴影系统（shadow-as-border）

| Level | Value | Use |
|-------|-------|-----|
| Border-only | `0 0 0 1px rgba(0,0,0,0.07)` | 卡片/表格默认边框（Vercel 技法） |
| Subtle | `0 0 0 1px rgba(0,0,0,0.07), 0 1px 3px rgba(0,0,0,0.04)` | 轻微抬升 |
| Elevated | `0 0 0 1px rgba(0,0,0,0.07), 0 2px 8px rgba(50,50,93,0.08), 0 1px 3px rgba(0,0,0,0.05)` | 卡片浮起（Stripe 蓝调阴影） |
| Sticky Header | `0 0 0 1px rgba(0,0,0,0.06), 0 1px 4px rgba(0,0,0,0.04)` | 粘性表头 |

---

## 3. Typography Rules

### 字体家族

```css
--font-sans: "Inter Variable", "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
--font-mono: "JetBrains Mono", "SF Mono", "Cascadia Code", "Fira Code", ui-monospace, monospace;
```

**OpenType Features**: `"cv01"` 全局开启（替代几何小写 a），`"tnum"` 用于价格列（等宽数字对齐）。

### 层级表

| Role | Size | Weight | Line Height | Letter Spacing | Use |
|------|------|--------|-------------|----------------|-----|
| Display Hero | 48px (3rem) | 600 | 1.1 | -1.2px | 替代方案页主标题 "ChatGPT Alternatives" |
| Section Heading | 28px (1.75rem) | 600 | 1.2 | -0.56px | 区块标题 |
| Card Title | 20px (1.25rem) | 600 | 1.3 | -0.4px | 卡片内标题 |
| Body Large | 18px (1.125rem) | 400 | 1.6 | normal | 介绍段落 |
| Body | 16px (1rem) | 400 | 1.55 | normal | 标准正文 |
| Body Medium | 15px (0.9375rem) | 500 | 1.5 | normal | 工具名（表格内）、导航 |
| Caption | 13px (0.8125rem) | 400 | 1.45 | normal | 元数据、评分来源、标签 |
| Micro | 11px (0.6875rem) | 500 | 1.3 | 0.02em | 折扣徽章、超小标签 |
| Button | 14px (0.875rem) | 500 | 1 | normal | 按钮文字 |
| Price (tabular) | 15px (0.9375rem) | 500 | 1.2 | normal | 价格列 — `font-feature-settings: "tnum"` |

### 排版原则

- **压缩标题**：大标题使用负 letter-spacing，制造"精炼信息"的感觉——这是给做决策的人看的，不是散文。
- **三档字重**：400（阅读）、500（UI/导航）、600（标题/强调）——没有更重的字重，保持轻盈感。
- **等宽数字**：所有价格、百分比使用 `"tnum"`，列对齐时数字不会跳舞。
- **`cv01` 全局**：Inter 的 `"cv01"` 把小写 a 从双层改为单层几何形，更现代、更干净。

---

## 4. Component Stylings

### 按钮

**Primary — 联盟链接按钮（最高视觉权重）**
- Background: `#5c6cf0`
- Text: `#ffffff`
- Padding: 8px 18px（比标准更宽，增加点击面积和视觉重量）
- Radius: 6px
- Font: 14px weight 500
- Hover: `#4a5ae0` + `transform: scale(1.02)`（微缩放反馈，GSAP 驱动）
- Focus: `0 0 0 2px var(--accent-ring)`
- Transition: `all 0.2s cubic-bezier(0.16, 1, 0.3, 1)`（Apple 流体缓动）
- Use: "Visit →" 联盟跳转按钮

**Secondary — 轮廓按钮**
- Background: transparent
- Text: `#4a4f5c`
- Border: `1px solid rgba(0,0,0,0.12)`
- Padding: 7px 17px
- Radius: 6px
- Font: 14px weight 400
- Use: 次要操作

### 标签/徽章

**功能标签（Feature Tag）**
- Background: `#f3f4f6`
- Text: `#4a4f5c`
- Padding: 2px 8px
- Radius: 4px
- Font: 12px weight 400
- Use: "API", "Team Collab", "Custom Models" 等功能标签

**折扣徽章（Discount Badge）**
- Background: `#fef3c7`
- Text: `#b45309`
- Border: `1px solid #fcd34d`
- Padding: 1px 7px
- Radius: 4px
- Font: 11px weight 500
- Use: "30% OFF", "Save $50" 等折扣标记
- 位置：工具名旁边的内联徽章，或价格列上方

**评分徽章（Rating Badge）**
- 高评分 (≥4.0): 文字 `#059669` + 半透明绿底
- 中评分 (3.0-3.9): 文字 `#d97706` + 半透明琥珀底
- 低评分 (<3.0): 文字 `#dc2626` + 半透明白底
- Font: 13px weight 500, `"tnum"` 数字

### 卡片
- Background: `#ffffff`
- Border: shadow-as-border — `0 0 0 1px rgba(0,0,0,0.07)`
- Radius: 8px
- Shadow: 默认 border-only；hover 时加上 `0 2px 8px rgba(50,50,93,0.08)`
- Padding: 24px

### 工具 Logo 插槽
- Size: 32×32px
- Radius: 6px（微圆角）
- Placeholder: `#f3f4f6` 背景 + 工具名首字母（灰色，居中）
- Actual: `<img>` 从 Cloudflare R2 加载，含 `srcset` 响应式

---

## 5. Layout Principles

### 间距系统
- Base unit: 4px（比标准的 8px 更精细，适合数据密集型 UI）
- Scale: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96

### 对比表专用间距
- 单元格内边距: `py-3 px-4`（12px 垂直，16px 水平）——足够的呼吸感而不浪费空间
- 列间距: 第一列（工具名）最小宽度 200px；后续列最小 120px
- 行高: 56px 最小（确保可点击区域足够）
- 表格外容器: `px-4 md:px-8` 内边距；`mx-auto max-w-7xl`

### 容器与网格
- Max content width: `1280px`（`max-w-7xl`）
- 替代方案页布局：`标题区 → 简介 → 对比表 → Related Alternatives`
- 移动端：表格横向滚动（`overflow-x-auto`），第一列 sticky left

### 留白哲学
- **数据呼吸**：表格行的垂直内边距 ≥ 12px，确保 5-15 行数据时不会让用户感到拥挤
- **区块间隔**：标题和表格之间 32px，表格和 Related Alternatives 之间 48px
- **斑马纹**：偶数行使用 `#f8f9fb` 背景，帮助 10+ 行数据时视觉追踪
- **Apple 式间距**：每个主要内容区块之间至少 48px——不吝啬留白

### Border Radius Scale
- Micro (4px): 功能标签、徽章
- Standard (6px): 按钮、Logo 占位符
- Comfortable (8px): 卡片、对比表容器
- Large (12px): 特色面板

---

## 6. Depth & Elevation

| Level | Treatment | Use |
|-------|-----------|-----|
| Flat | No shadow | 页面背景 |
| Border-only | `0 0 0 1px rgba(0,0,0,0.07)` | 卡片/表格/输入框默认态 |
| Sticky Header | `0 0 0 1px rgba(0,0,0,0.06), 0 1px 4px rgba(0,0,0,0.04)` | 表头粘性态 |
| Focus Ring | `0 0 0 2px rgba(92,108,240,0.35)` | 键盘聚焦 |

**阴影哲学**：借用 Vercel 的核心技法——"阴影即边框"。传统 `border` 会改变盒模型、影响圆角裁切、过渡不够柔顺。`0px 0px 0px 1px` 的 box-shadow 解决了所有这些问题。在需要"浮起"效果时叠加 Stripe 式的蓝调第二层阴影。

---

## 7. Do's and Don'ts

### Do
- 使用 Inter Variable + `"cv01"` 作为全局字体——干净、现代、可读
- 用 `0 0 0 1px rgba(0,0,0,0.07)` 替代传统 CSS border
- 联盟按钮必须是最突出的视觉元素（主强调色 + 较大内边距 + 微缩放 hover）
- 价格列使用 `"tnum"` 确保数字对齐
- 斑马纹帮助 10+ 行数据追踪（但不要太明显——`#f8f9fb` vs `#ffffff`）
- 移动端表头 sticky left + 横向滚动——这是对比表的正确姿势
- 折扣徽章用暖色调独立于主强调色——形成清晰的信息层级

### Don't
- 不要使用第二个强调色——`#5c6cf0` 是唯一
- 不要使用 `backdrop-filter`（毛玻璃）——高消耗，在对比表场景中毫无必要
- 不要在移动端隐藏列——用户需要完整对比信息；横向滚动即可
- 不要使用纯黑（`#000`）——最深的文字用 `#0f1115`
- 不要给表格行加边框——用斑马纹 + hover 高亮区分行即可
- 不要使用 weight 700+ —— 600 是标题最大字重
- 不要在表格内使用大于 14px 的按钮——视觉比例失衡

---

## 8. Responsive Behavior

### 断点
| Name | Width | Key Changes |
|------|-------|-------------|
| Mobile | <640px | 单列，表格横向滚动，第一列 sticky left |
| Tablet | 640-1024px | 表格自然宽度，3-4 列可见 |
| Desktop | 1024-1280px | 全宽表格，所有列可见 |
| Large | >1280px | 居中最大宽度 1280px |

### 对比表响应策略
- **移动端**（<640px）：表格 `overflow-x-auto`，工具名列 sticky left（`position: sticky; left: 0`），背景带轻微阴影表示滚动暗示
- **平板**（640-1024px）：表格自然展开，可能仍有横向滚动，但更多列可见
- **桌面**（>1024px）：全部列可见，表格不再需要横向滚动
- 功能标签在移动端可能折叠——显示前 3 个 + "+N more" 指示

---

## 9. Agent Prompt Guide

### 快速色彩参考
- 页面背景: `#fafbfc`
- 卡片/表行: `#ffffff`
- 主文字: `#0f1115`
- 次要文字: `#4a4f5c`
- 辅助文字: `#8b919e`
- 主强调色（按钮）: `#5c6cf0`
- 强调色悬停: `#4a5ae0`
- 折扣徽章背景: `#fef3c7`
- 折扣徽章文字: `#b45309`
- 高评分: `#059669`
- 卡片边框（shadow）: `0 0 0 1px rgba(0,0,0,0.07)`
- 斑马纹行: `#f8f9fb`
- 行悬停: `#f3f4f6`
- 聚焦环: `0 0 0 2px rgba(92,108,240,0.35)`

### 示例 Prompt
- "Create a comparison table row: white background, 56px min-height, tool logo 32x32px with 6px radius, tool name at 15px weight 500 in #0f1115, features as 12px tags in #f3f4f6 bg, rating badge, affiliate 'Visit' button in #5c6cf0 with 8px 18px padding and 6px radius."
- "Style the discount badge: #fef3c7 background, #b45309 text, 1px solid #fcd34d border, 4px radius, 11px weight 500, positioned inline next to tool name."
- "Design the sticky table header: #ffffff background with shadow-as-border 0 0 0 1px rgba(0,0,0,0.07), column labels at 13px weight 500 in #8b919e, uppercase tracking 0.05em."

---

> **Design System Version**: V1.0
> **Last Updated**: 2026-07-06
> **Inspiration**: Vercel (structure + shadow-as-border), Stripe (blue-tinted shadows), Apple (breathing room), Linear (precision hierarchy)
