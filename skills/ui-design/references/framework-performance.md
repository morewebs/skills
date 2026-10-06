# Multi-Stack Framework Performance & Engineering Manuals

Comprehensive rules for building high-performance, accessible user interfaces across modern frontend frameworks.

---

## 1. Next.js 14/15 App Router & React Performance (44 Core Rules)

### 1.1 Async Waterfalls & Data Fetching
1. **Defer Await**: Move `await` statements directly into conditional branches where the data is consumed. Never block non-dependent branches at the top of route handlers.
2. **Promise.all Parallelization**: Execute independent asynchronous operations concurrently (`const [user, posts] = await Promise.all([fetchUser(), fetchPosts()])`).
3. **Partial Dependency Parallelization**: When operations have partial dependencies, start each promise at the earliest possible instant rather than sequentially chaining.
4. **API Route Promise Initiation**: In API handlers, initiate background operations immediately and await later in the function lifecycle.
5. **Granular Suspense Boundaries**: Wrap dynamic async components in `<Suspense fallback={<Skeleton />}>` boundaries so the surrounding layout shell streams instantly.

### 1.2 Bundle Size & Tree Shaking
6. **Direct Asset Imports**: Avoid barrel file imports for icon packages (`import { Check } from 'lucide-react'`). Use direct subpath imports if bundle inspection reveals un-shaken modules.
7. **Dynamic Module Splitting**: Lazy-load heavy components (monaco editors, heavy chart visualizers) via `next/dynamic` with `ssr: false`.
8. **Defer Third-Party Scripts**: Load analytics, tracking, and non-interactive logging scripts after hydration or via Next.js `next/script` with `strategy="afterInteractive"`.
9. **Conditional Module Loading**: Dynamically import heavy computational libraries only when the specific user feature is activated.
10. **Preload on User Intent**: Preload heavy route bundles on hover/focus signals (`onMouseEnter={() => import('./editor')}`) before clicks occur.

### 1.3 Server Components & RSC Boundaries
11. **Server-Side Request Deduplication**: Wrap database or external API queries in `React.cache()` to automatically deduplicate identical calls within a single render cycle.
12. **LRU Cross-Request Caching**: Use an in-memory LRU cache for data shared across sequential requests and user sessions.
13. **Minimize Serialization Overhead**: Only pass scalar values and necessary properties across RSC boundaries into Client Components. Never pass large, un-filtered server database entities.
14. **Parallel Server Fetching**: Structure component trees using composition (`<Header /><Sidebar />`) to allow concurrent RSC rendering.
15. **Non-Blocking Post-Response Work**: Use Next.js `after()` or background queues to execute audit logging, telemetry, and cache warming after the HTTP response has shipped.

### 1.4 Client Hooks & State Management
16. **Automatic Revalidation & SWR**: Use SWR or TanStack Query for client-side data fetching with built-in deduplication, cache sharing, and background revalidation.
17. **Global Event Listener Deduplication**: Share global listeners (e.g. `keydown`, `resize`) through centralized subscriptions rather than registering per-component listeners.
18. **Defer State Reads in Callbacks**: Do not bind components to continuous state if that state is only read when an event fires. Read on-demand in the callback.
19. **Memoize Heavy Computations**: Hoist complex calculations into `useMemo()` or isolate them into dedicated, memoized subcomponents (`React.memo`).
20. **Narrow Primitive Dependencies**: Pass primitive IDs or strings into `useEffect` / `useMemo` dependency arrays rather than wide object references.
21. **Subscribe to Derived Booleans**: When listening to window sizes or scroll offsets, subscribe to derived booleans (`isMobile`) rather than continuous numbers.
22. **Functional State Updates**: Always use the updater syntax `setState(curr => ...)` inside callbacks to avoid stale closures and keep dependency arrays stable.
23. **Lazy State Initialization**: Pass factory functions to `useState(() => computeExpensiveInitialState())` so the initializer only executes on mount.
24. **Concurrent Transitions**: Wrap non-urgent state updates (search filters, tab switching) in `startTransition()` to keep user typing and pointer events responsive.

### 1.5 DOM & CSS Engine Performance
25. **SVG Animation Wrappers**: Wrap SVG elements in `<div>` containers and animate CSS transforms on the container to leverage hardware acceleration.
26. **Content Visibility Optimization**: Apply CSS `content-visibility: auto` with `contain-intrinsic-size` on long lists to defer layout rendering of off-screen nodes.
27. **Hoist Static JSX**: Extract unchanging static JSX elements to module scope to avoid re-allocation during every render cycle.
28. **Flicker-Free Theme Hydration**: Use a minimal inline script in `<head>` to read local storage and inject the `.dark` class before the first HTML paint.
29. **Strict Conditional Ternaries**: Use explicit ternaries (`count > 0 ? <Badge>{count}</Badge> : null`) rather than `&&` to avoid accidentally rendering `0` or `NaN`.
30. **Activity Component Preservation**: Use React `<Activity mode={isOpen ? 'visible' : 'hidden'}>` to preserve expensive DOM and state for frequently toggled drawers and modals.
31. **Batch DOM CSS Mutations**: Apply multiple style changes by toggling classes or updating `cssText` in a single pass to eliminate browser reflow thrashing.
32. **Index Map Lookups**: Construct `Map` or `Set` lookup indices for collections rather than running repeated `.find()` calls in hot paths.
33. **Cache Property Access in Loops**: Cache deep object property paths in local variables before executing iterations.
34. **Memoize Pure Function Results**: Use module-level cache maps for deterministic pure utility transformations.
35. **Cache Web Storage Reads**: Cache `localStorage` reads in memory rather than synchronously reading storage on every render.
36. **Combine Iterations**: Group chained `.filter().map()` operations into a single `for...of` loop when working with large dataset arrays.
37. **Early Length Check**: Compare array lengths first before running deep equality comparisons or sorting checks.
38. **Early Function Return**: Exit immediately when error conditions or boundary cases are determined.
39. **Hoist Regular Expressions**: Declare `RegExp` objects at module scope instead of instantiating new regex instances inside render functions.
40. **Single-Pass Min/Max**: Find minimum and maximum array elements via a single linear loop rather than running full `O(n log n)` array sorts.
41. **Set Membership Checks**: Use `Set.has()` for `O(1)` membership lookups in place of `Array.includes()`.
42. **Immutable Sorting**: Use `Array.prototype.toSorted()` instead of `sort()` to maintain immutability without accidental in-place mutations.
43. **Event Handler Refs**: Store frequently changing callbacks in `useRef` or `useEffectEvent` to avoid re-triggering effect subscriptions.
44. **Latest Value Hook**: Access current state in stable callbacks via `useLatest` hooks without declaring volatile effect dependencies.

---

## 2. shadcn/ui Component System Playbook (20 Rules)

1. **CLI Installation**: Always install components using `npx shadcn@latest add <component>` to ensure dependencies, utilities, and peer tokens are correctly wired.
2. **Proper Project Init**: Run `npx shadcn@latest init` to create `components.json` and initialize baseline styles before copying component code.
3. **Path Aliases**: Enforce `@/components/ui` import aliases in `tsconfig.json` rather than relative traversal (`../../components`).
4. **CSS Variables for Theming**: Define all theme tokens as CSS variables in `globals.css` rather than hardcoding static hex codes in components.
5. **Foreground Color Pairing**: Follow semantic color token conventions where every surface has an explicit foreground companion (`primary` / `primary-foreground`).
6. **Dark Mode Classes**: Ensure `.dark` class selectors exist for all custom CSS variables.
7. **Leverage CVA Variants**: Express component styling variants through `cva()` rather than writing inline ternary chains inside `className`.
8. **Compose with `className`**: Expose `className` on all exported components and merge via `cn()` utility (`clsx` + `tailwind-merge`).
9. **Consistent Sizing**: Standardize size props (`size="sm"`, `size="lg"`, `size="icon"`) across all interactive buttons and inputs.
10. **Compound Component Composition**: Break complex widgets into subcomponents (`Card`, `CardHeader`, `CardTitle`, `CardContent`, `CardFooter`) rather than mega-props.
11. **Semantic Dialog Usage**: Use `Dialog` for modal workflows, forms, and detail inspector views.
12. **Controlled Dialog State**: Use explicit `open` and `onOpenChange` handlers for programmatic modal control.
13. **Required Dialog Hierarchy**: Every `DialogContent` must contain a `DialogTitle` (or `VisuallyHidden(DialogTitle)`) to satisfy WCAG screen reader accessibility.
14. **Sheet Side Panels**: Use `Sheet` for slide-out mobile drawers, contextual filters, and navigation menus.
15. **Explicit Sheet Placement**: Always declare `side="left"` or `side="right"` explicitly on `SheetContent`.
16. **Form Integration**: Integrate form components with `react-hook-form` via the compound `<Form>` wrapper.
17. **FormField Binding**: Wrap every form control in `<FormField>` to guarantee correct label association and error binding.
18. **FormMessage Rendering**: Render `<FormMessage />` directly below controls to supply accessible live-region error announcements.
19. **Schema Validation via Zod**: Define form contracts with Zod schemas and hook into forms via `zodResolver`.
20. **Accessible Selects**: Use the accessible Radix `<Select>` primitive for dropdown options rather than unstyled native `<select>`.

---

## 3. Vue 3 & Nuxt 3 Playbook

- **Composition Setup**: Use `<script setup lang="ts">` exclusively for component declarations.
- **State Reactivity Boundaries**: Use `ref()` for primitive values; use `shallowRef()` or `shallowReactive()` for large nested datasets to bypass deep recursive reactivity proxies.
- **Payload Minimization in SSR**: Use `useFetch()` or `useAsyncData()` with explicit `pick` arrays (`pick: ['id', 'title', 'slug']`) to strip unnecessary fields from client SSR payloads.
- **Nuxt UI Conventions**:
  - Always wrap the application root in `<UApp>` to supply overlay, tooltip, and toast notification contexts.
  - Prefix framework components with `U` (`<UButton>`, `<UModal>`, `<UTable>`).
  - Declare design tokens via `app.config.ts` rather than hardcoding utility overrides.

---

## 4. Svelte 5 & SvelteKit Playbook

- **Runes System (Svelte 5 Standard)**: Modern Svelte 5 applications must use runes exclusively:
  - `$state(initialValue)` for reactive state.
  - `$derived(expression)` for computed values (replacing legacy `$: derived = ...`).
  - `$effect(() => { ... })` for side effects and cleanup lifecycle hooks.
  - `$props()` for component inputs.
- **Legacy Store Interoperability**: The `$store` auto-subscription prefix syntax is strictly retained for consuming external Svelte stores or RxJS observables. For internal application state, use runes.
- **SSR Route Boundaries**:
  - Load data for initial page render in `+page.server.ts` or `+page.ts` via the `load` contract.
  - Perform teardown and subscription cleanup inside `$effect` return callbacks:
    ```svelte
    <script lang="ts">
      let count = $state(0);
      let double = $derived(count * 2);

      $effect(() => {
        const interval = setInterval(() => count++, 1000);
        return () => clearInterval(interval);
      });
    </script>
    ```

---

## 5. Mobile & Cross-Platform (React Native, SwiftUI, Flutter)

### React Native
- **StyleSheet Hoisting**: Always declare styles using `StyleSheet.create()` outside the component function to prevent recreating style objects on every render.
- **FlatList Optimization**: Virtualize large lists with `<FlatList>` using stable `keyExtractor` functions, `getItemLayout` for fixed-height cells, and `maxToRenderPerBatch`.
- **Target Touch Dimensions**: Ensure all interactive wrappers use `<Pressable>` with `hitSlop` configured for tap targets smaller than 44x44 points.

### SwiftUI
- **Primitive Value Types**: Structure layouts around primitive value types (`struct View`) rather than classes to minimize reference counting overhead.
- **Observable Lifecycle**: Isolate view models using `@Observable` (iOS 17+) or `@StateObject` to govern lifecycle ownership.
- **Lazy Stack Loading**: Replace eager `VStack` and `HStack` layouts with `LazyVStack` and `LazyHStack` inside scrollable viewports.

### Flutter
- **Immutable Const Constructors**: Mark immutable widgets with `const` constructors to prevent unnecessary element tree rebuilds.
- **Fine-Grained State Scoping**: Avoid calling `setState()` at root widget boundaries; isolate dynamic zones using fine-grained builders or state providers (`Riverpod`).
- **Semantic Screen Readers**: Provide screen reader descriptions and actions using the `Semantics` widget.
