---
name: uniface
description: Use when building, styling, reviewing, or documenting User Interface. Provides hard baseline constraints (accessibility, animation, layout), Radix/Tailwind component patterns, stack-specific performance rules (Next.js, Vue, Svelte, SwiftUI, React Native, Flutter), visual QA checklists, and a searchable style/palette/chart reference via bundled Python scripts.
---

# UI/UX Engineering & Design System

## §0 Architecture & Operational Routing

This system governs the end-to-end lifecycle of digital interfaces: strategic workflow gating, aesthetic direction, hard baseline constraints, component-level implementation, stack-specific performance, and visual verification.

### Subsystem Directory

| Domain | Section | Primary Purpose | Reference File |
|---|---|---|---|
| Workflow Gating | **§1** | Risk classification, validation gates, execution readiness | Inline |
| Baseline Constraints | **§2** | Non-negotiable constraint floor against low-quality UI/code | Inline |
| Aesthetic Direction | **§3** | Contextual styling, typography scale, editorial voice, anti-slop | Inline |
| Spatial & Motion | **§4** | Depth, glassmorphism, 3D transforms, scroll-driven motion | Inline |
| Micro-interactions | **§5** | High-performance interactive details, feedback, delight | Inline |
| Component Primitives | **§6** | Headless accessible components & Tailwind architecture | [`references/components.md`](file:///c:/Users/W/Documents/morewebs/skills/skills/ui-design/references/components.md) |
| Visual QA & Testing | **§7** | Visual regression, edge-case audits, accessibility verification | Inline |
| Framework Manuals | **§8** | Deep rules for Next.js, React, Vue, Svelte 5, Mobile | [`references/framework-performance.md`](file:///c:/Users/W/Documents/morewebs/skills/skills/ui-design/references/framework-performance.md) |
| Search Engine Scripts | **§9** | BM25 retrieval across styles, palettes, blueprints, charts | [`scripts/core.py`](file:///c:/Users/W/Documents/morewebs/skills/skills/ui-design/scripts/core.py) |
| Master Datasets | **§10** | Exhaustive datasets (styles, palettes, blueprints, patterns) | `data/*.csv` |

### Precedence & Conflict Resolution

1. **Explicit Project Brief**: Concrete constraints stated directly by the brief override general suggestions.
2. **Baseline UI Floor (§2)**: Hard constraints (e.g., WCAG AA contrast, keyboard accessibility, mobile safe-areas, compositor-only feedback) cannot be bypassed unless explicitly instructed for specific technical exceptions.
3. **Workflow Escalation (§1)**: High-risk architectural or destructive state changes require structured review prior to code implementation. Skip Understanding Lock for single-component styling tweaks and minor fixes.
4. **Aesthetic Direction & Spatial Motion (§3, §4)**: Contextual styling, typography discipline, and depth treatments. Ambient motion and domain-specific accents (e.g., Cyberpunk neon, Aurora blends) are permitted when aligned with brand identity.
5. **Reference Catalogs (§10 / `data/*.csv`)**: Informational and inspirational catalogs at lowest precedence; they provide domain-specific starting points but must yield to §2 baseline floor constraints (e.g., ensure CTA contrast meets WCAG AA 4.5:1 even if a catalog row suggests a vibrant color).

---

## §1 Workflow Orchestration & Validation Gate

Ensures concepts progress systematically from definition to critique, approval, and implementation.

```
[Problem Definition] ──> [Understanding Lock] ──> [Design Drafting]
                                                          │
                                                          ▼
[Implementation] <── [Readiness Sign-Off] <── [Risk Assessment & Review]
```

### 1. Requirements Lock
Before drafting UI architectures or writing component code for new features:
- Establish the **Understanding Lock**: Target audience, technical constraints, operational context, core user jobs.
- Initialize a **Decision Log**: Record key structural, accessibility, and architectural assumptions.
- *Velocity Fast-Lane*: Skip the Understanding Lock for single-component styling changes, localized copy edits, or trivial fixes.

### 2. Risk Classification
- **Low Risk**: Standard component iteration, localized copy/style adjustments, non-destructive workflow updates.  
  *Action*: Proceed to implementation planning.
- **Moderate Risk**: New user flows, cross-cutting theme/layout changes, third-party component integrations.  
  *Action*: Perform structured heuristic evaluation across accessibility, responsive behavior, and performance.
- **High Risk**: Core architectural migration, irreversible data actions, destructive state mutations, checkout/auth flows.  
  *Action*: Require independent verification and comprehensive failure-mode analysis.

### 3. Implementation Gate
Do not begin coding until:
- [ ] Visual architecture and state behaviors are specified.
- [ ] Error, loading, empty, and edge states are accounted for.
- [ ] Accessibility requirements (WCAG 2.1 AA) are established.
- [ ] Known performance risks (bundle impact, reflow risks) are acknowledged.

---

## §2 Baseline UI Constraints (Hard Floor)

Enforces strict standards to prevent common layout, interaction, and styling bugs.

### Tech Stack Standards
- **CSS Architecture**: Use Tailwind CSS default tokens unless custom design tokens are explicitly declared.
- **Tailwind Version Awareness**:
  - **Tailwind v4**: Uses CSS-first `@theme` blocks, native `backdrop-blur-xs`, and `tw-animate-css` / native keyframes.
  - **Tailwind v3**: Uses `tailwind.config.js`, HSL triple tokens in `globals.css`, and `tailwindcss-animate`. Do not use `backdrop-blur-xs` in v3 without custom utility configuration.
- **Dynamic JavaScript Animations**: Use `motion/react` (formerly `framer-motion`) when JS runtime physics/coordination are required.
- **Class Logic**: Merge classes exclusively through the `cn` utility (`clsx` + `tailwind-merge`).

### Component & Accessibility Standards
- **Accessible Primitives**: Use tested unstyled primitives (`Base UI`, `React Aria`, `Radix UI`) for components with keyboard navigation, focus trapping, or ARIA state needs.
- **Zero Primitive Mixing**: Never mix multiple primitive component foundations inside the same interaction surface.
- **Icon Buttons**: Icon-only buttons must have an unambiguous `aria-label`.
- **Keyboard Navigation**: Never rebuild native focus or keyboard behaviors manually when accessible primitives exist.
- **Visible Focus States**: Every interactive element must display a visible `:focus-visible` focus ring (2px–4px). Never apply `outline-none` without providing a distinct focus ring alternative.

### Interaction & Layout Standards
- **Destructive Confirmations**: Destructive or irreversible state mutations must require an `AlertDialog` confirmation.
- **Loading Feedback**: Use structured skeleton layouts matching content shape for content containers; route-level or indeterminate initial page loads may use minimal centered loading indicators when content geometry is unknown.
- **Mobile Viewports**: Never use `h-screen`; use `h-dvh` to account for dynamic mobile browser chrome.
- **Safe Area Insets**: Account for `env(safe-area-inset-*)` on fixed/floating elements.
- **Contextual Error Display**: Render validation errors adjacent to the specific input triggering the failure.
- **Input Paste**: Never block paste events on `input` or `textarea` elements.
- **Root-Cause Overflow Fix**: Identify and eliminate the root cause of horizontal overflow (unconstrained fixed widths, large images, negative margins). Do not merely mask layout bugs with `overflow-x-hidden` on parent wrappers.

### Animation Standards
- **Interaction Duration**: User feedback animations must complete within `≤200ms`.
- **Entrance & Modal Motion**: Entrance, exit, and modal reveals may run `300ms–600ms`.
- **Ambient Decorative Motion**: Ambient loops (e.g. Aurora mesh) may run `8s–12s`, hardware-accelerated.
- **Compositor Props Only**: Animate only `transform` and `opacity` during high-frequency transitions. Never animate `width`, `height`, `top`, `left`, `margin`, or `padding`.
- **Dynamic Depth Transitions**: Do not continuously transition `box-shadow` on hover; transition opacity on a pseudo-element (`::after`) with pre-rendered shadow to maintain 60fps.
- **Off-Screen Animations**: Automatically pause or unmount continuous animations when elements leave the viewport.
- **Reduced Motion**: Enforce `@media (prefers-reduced-motion: reduce)` across all animated properties.

### Typography Standards
- **Headline Balance**: Apply `text-balance` to headings.
- **Body Flow**: Apply `text-pretty` to body paragraphs.
- **Numerical Data**: Apply `tabular-nums` to financial, statistical, and tabular figures.
- **Text Overflow**: Apply `truncate` or `line-clamp-*` to prevent overflow in constrained layouts.

### Visual Restraint Standards
- **Gradients & Accents**: Avoid non-semantic multi-color gradients. Thematic genres (Aurora UI, Cyberpunk, HUD/Sci-Fi, Web3, Retro-Futurism) justify neon accents, dark canvas, or mesh gradients when explicitly aligned with domain identity.
- **Affordance Clarity**: Never use glow effects or drop shadows as the sole indicator of interactivity.

---

## §3 Aesthetic & Creative Direction

Directs distinctive, professional interfaces tailored to the target domain, eliminating generic styling clichés.

### Domain-Grounded Identity
Visual treatments must stem from the domain itself:
- **Developer Tools**: High density, monospaced data alignment, muted slate surfaces, and immediate keyboard affordances.
- **Enterprise Banking**: High-contrast typography, explicit numerical alignments, subtle borders, and verifiable trust markers.
- **Consumer Lifestyle**: Spacious typography, rich media staging, warm palettes, and tactile feedback.

### Anti-Cliché Rules
Avoid generic design defaults that indicate template-driven production:
1. **The Generic Card Kit**: Slicing all content into uniform rounded cards with identical radii and faint drop shadows.
2. **Typographic Monotony**: Using tracked-out all-caps labels above every heading, or inserting middle dots (`·`) and directional arrows (`→`) decoratively.
3. **Arbitrary Accents**: Randomly highlighting single words in headlines with bolding, italics, or mismatched colors.
4. **Unjustified Neons**: Applying arbitrary dark backgrounds with radioactive neon accents without thematic justification (cybersecurity/gaming domains are excepted).

---

## §4 Antigravity & Spatial Motion Design

For interfaces requiring 3D perspective, weightlessness, layered glassmorphism, and scroll-linked depth.

### Core Principles
- **Diffused Depth**: Layer drop shadows using soft, multi-tier spreads rather than harsh single offsets:
  ```css
  box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.05), 0 20px 40px -10px rgba(0, 0, 0, 0.03);
  ```
- **Z-Axis Hierarchy**: Establish spatial layers where background planes recede and interactive surfaces advance using CSS `perspective: 1000px;` and `transform: translateZ(...)`.
- **Glass Surfaces**: Pair translucent fills with subtle background blurring and delicate borders:
  ```css
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  ```
- **Hardware Layering**: Toggle `will-change: transform` only during active scroll/interaction loops; revert upon completion.

---

## §5 Micro-Interactions & Tactile Feedback

- **Isolate High-Value Targets**: Focus on high-frequency interaction points: form submit triggers, mode toggles, status pills, navigation links.
- **Physics-Based Feedback**: Replace mechanical linear transitions with calibrated easing curves:
  - Spring/Overshoot: `cubic-bezier(0.34, 1.56, 0.64, 1)`
  - Smooth Exit: `cubic-bezier(0.25, 1, 0.5, 1)`
- **Zero Layout Shifts**: Never alter container geometry during hover/focus to prevent Cumulative Layout Shift (CLS).

---

## §6 Component Primitives & Design Systems

For complete TypeScript code examples of headless Radix UI components (Dropdown Menu, Accessible Dialog) and Tailwind v3 vs v4 configuration templates, refer to:
👉 [`references/components.md`](file:///c:/Users/W/Documents/morewebs/skills/skills/ui-design/references/components.md)

---

## §7 Visual Validation Checklist

Pre-delivery verification gatekeeper:
```markdown
- [ ] No raw emojis used as icons (SVG icons from Lucide/Heroicons only).
- [ ] `cursor-pointer` applied to all clickable elements.
- [ ] Interactive elements have visible `:focus-visible` focus rings (2px–4px).
- [ ] Contrast ratio meets WCAG 2.1 AA (4.5:1 text, 3:1 graphical elements).
- [ ] Responsive layouts tested at 375px, 768px, 1024px, and 1440px.
- [ ] Zero horizontal scroll on mobile viewports (root cause resolved; not masked).
- [ ] All inputs have explicit `<label>` tags or `aria-label` bindings.
- [ ] Skeletons/loading indicators prevent Layout Shifts (CLS).
- [ ] Interactive state transitions complete within <=200ms.
- [ ] `@media (prefers-reduced-motion: reduce)` disables non-essential animations.
```

---

## §8 Multi-Stack Framework Engineering

For deep performance checklists and implementation patterns across Next.js (44 rules), shadcn/ui (20 rules), Vue 3/Nuxt, Svelte 5 (runes vs stores), and Mobile, refer to:
👉 [`references/framework-performance.md`](file:///c:/Users/W/Documents/morewebs/skills/skills/ui-design/references/framework-performance.md)

---

## §9 Search Engine Tooling (`scripts/core.py`)

The skill includes a standalone Okapi BM25 search CLI for instant retrieval across all design reference datasets.

### When to Invoke
When the user asks for:
- Visual styles, aesthetics, or design prompts: search `--domain style`
- Color palettes and hex schemes: search `--domain color`
- Complete product UI specifications: search `--domain blueprint`
- Landing page sections, CTA placement, or funnel patterns: search `--domain pattern`
- Data visualization and chart choices: search `--domain chart`
- Lucide icon recommendations: search `--domain icon`
- UX usability and layout rules: search `--domain ux`
- Web accessibility standards: search `--domain web`

### CLI Command Syntax
```bash
python scripts/core.py "<query>" --domain <domain> [--max <results>]
```

### Usage Examples
```bash
# Style recommendation and copy-paste AI prompts
python scripts/core.py "minimalist dashboard" --domain style

# Authored hex color palettes by product category
python scripts/core.py "coffee shop" --domain color

# Full product category blueprint (style + landing pattern + dashboard + palette)
python scripts/core.py "fintech" --domain blueprint

# Landing page section order and conversion strategies
python scripts/core.py "pricing comparison" --domain pattern

# Chart selection by data structure
python scripts/core.py "time-series trends" --domain chart

# Lucide icon primitives with import syntax
python scripts/core.py "trash delete" --domain icon

# UX usability guidelines
python scripts/core.py "z-index modal stacking" --domain ux

# Web interface & accessibility standards
python scripts/core.py "focus ring" --domain web
```

---

## §10 Quick Reference Catalogs

Full datasets are stored in `data/*.csv` and queried via `scripts/core.py`. Below is the high-level canonical index.

### 23 Canonical Styles Quick-Index (`data/styles.csv`)
| Id | Style Category | Archetype | Best For |
|---|---|---|---|
| 1 | **Minimalism & Swiss Style** | Clean Modern | SaaS tools, Documentation, Editorial, Corporate |
| 2 | **Neumorphism** | Tactile Depth | Smart home, Audio dials, Calculator apps |
| 3 | **Glassmorphism** | Spatial Layered | Modern dashboards, Web3 wallets, Overlays |
| 4 | **Brutalism** | Raw High-Contrast | Art galleries, Fashion, Underground music, Indie dev |
| 5 | **3D & Hyperrealism** | Spatial Immersion | Automotive configurators, Gaming, Hardware |
| 6 | **Vibrant & Block-based** | Bold Expressive | EdTech, Consumer apps, Marketing landing pages |
| 7 | **Dark Mode (OLED)** | Technical Contrast | Developer tools, Crypto dashboards, Night apps |
| 8 | **Accessible & Ethical** | Universal Standard | Government, Healthcare, Public utilities, Civic |
| 9 | **Claymorphism** | Playful 3D | Kids apps, Social communities, Gamified learning |
| 10 | **Aurora UI** | Atmospheric Gradient | AI landing pages, Creative portfolios, Music |
| 11 | **Retro-Futurism** | Nostalgic Cyber | Tech blogs, Indie gaming, Synth hardware |
| 12 | **Flat Design** | Utilitarian 2D | Productivity dashboards, Enterprise utilities, Docs |
| 13 | **Skeuomorphism** | Realistic Texture | Audio plugins, Luxury timepieces, Craft brands |
| 14 | **Liquid Glass** | Dynamic Refraction | Spatial computing showcases, Conceptual tech |
| 15 | **Motion-Driven** | Kinetic Interactive | Storytelling landing pages, Product reveals |
| 16 | **Micro-interactions** | Precision Feedback | Fintech mobile apps, Productivity tools |
| 17 | **Inclusive Design** | Universal Access | Public services, Healthcare, Education |
| 18 | **Zero Interface** | Conversational Ambient | AI chat agents, Voice assistants, Ambient IoT |
| 19 | **Soft UI Evolution** | Refined Contemporary | SaaS platforms, Modern dashboards, Web apps |
| 20 | **Bento Grids** | Structured Modular | Product feature showcases, Personal homepages |
| 21 | **Neubrutalism** | Pop Stark | Fintech challengers, Creative dev tools, Gen-Z |
| 22 | **HUD / Sci-Fi FUI** | Futuristic Telemetry | Cybersecurity consoles, Drone telemetry, Defense |
| 23 | **Pixel Art** | 8-Bit Arcade | Gaming platforms, Web3 retro games, Nostalgia |

### Product Blueprints Index (`data/blueprints.csv`)
Contains 96 complete product categories mapped strictly to the 23-style canon, 30 landing patterns, and normalized dashboard archetypes (Real-Time Telemetry, Drill-Down Analytics, Executive Overview, Financial Matrix, Operations Dispatch).