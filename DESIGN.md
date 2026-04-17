```markdown
# Design System Document: The Editorial Expedition

## 1. Overview & Creative North Star
**Creative North Star: "The Curated Sanctuary"**

This design system moves away from the "utility-first" look of standard travel apps. Instead, it adopts a **High-End Editorial** approach, treating the local driver’s service as a premium concierge experience. We are not just building a booking tool; we are designing a digital doorway to the soul of Siem Reap. 

To achieve this, the system breaks the traditional "template" feel through **intentional asymmetry**, **exaggerated white space**, and **tonal layering**. By utilizing high-contrast typography scales and overlapping elements (e.g., a photo breaking the container edge), we create a sense of movement and "soul" that reflects the organic beauty of the Cambodian landscape.

---

## 2. Colors: Earth, Stone, and Jungle
Our palette is a dialogue between the ancient stone of Angkor (`surface_dim`), the rich terracotta of the earth (`secondary`), and the vibrant life of the jungle (`primary`).

### The Palette
- **Primary (`#154212`)**: A deep, lush jungle green. Use this for moments of authority and primary brand actions.
- **Secondary (`#944926`)**: A rich terracotta. This is our "warmth" token, used for highlights and high-engagement CTAs.
- **Surface (`#fcf9f2`)**: An off-white "Stone" background. It is warmer and more premium than pure `#ffffff`, reducing eye strain and feeling more "boutique."

### The "No-Line" Rule
**Explicit Instruction:** Do not use 1px solid borders for sectioning. Boundaries must be defined solely through background color shifts. For example, a card should be defined by its transition from `surface_container_low` to `surface_container_high`, never by a stroke.

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers—like stacked sheets of fine handmade paper. 
- **Base Level:** `surface`
- **Sectioning:** `surface_container_low`
- **Interactive Elements:** `surface_container_highest`

### The "Glass & Gradient" Rule
To avoid a flat, "cheap" feel, use **Glassmorphism** for floating headers or navigation bars. Apply a `surface` color at 80% opacity with a `20px` backdrop blur. For hero sections, use a subtle radial gradient transitioning from `primary` to `primary_container` to add atmospheric depth.

---

## 3. Typography: The Human Voice
We pair the timeless authority of a serif with the modern reliability of a sans-serif.

- **Display & Headlines (`notoSerif`)**: This is our "Character" font. It feels academic yet welcoming. Use `display-lg` (3.5rem) with tight letter-spacing for a bold, editorial look that commands attention.
- **Body & Titles (`manrope`)**: Our "Professional" font. Manrope is a modern sans-serif with excellent legibility. It provides the "Trustworthy" pillar of the system.
- **Hierarchy as Identity:** Use a massive scale contrast. A `display-md` headline should sit closely above `body-md` text to create a high-fashion, editorial layout.

---

## 4. Elevation & Depth: Tonal Layering
We reject heavy, artificial shadows in favor of **Tonal Layering**.

- **The Layering Principle:** Place a `surface_container_lowest` card on a `surface_container_low` background. This creates a "soft lift" that feels architectural rather than digital.
- **Ambient Shadows:** If an element must float (e.g., a "Book Now" FAB), use a shadow tinted with `on_surface` (a deep olive-black) at 5% opacity with a `40px` blur. It should look like a soft glow, not a dark smudge.
- **The "Ghost Border" Fallback:** If a border is required for accessibility, use the `outline_variant` token at **15% opacity**. This creates a "whisper" of a boundary.
- **Glassmorphism:** Use semi-transparent `surface_variant` layers over photography to create "Frosted Stone" overlays for text, ensuring the lush jungle imagery bleeds through the UI.

---

## 5. Components: Organic Primitives

### Buttons
- **Primary**: `primary` background with `on_primary` text. Use `DEFAULT` (0.5rem) roundedness. No borders.
- **Secondary**: `secondary_container` background. This provides the "Warmth" mentioned in the brief.
- **The "Signature" State**: On hover, primary buttons should transition to a subtle gradient of `primary` to `primary_container`.

### Cards & Lists
- **The Divider Ban**: Forbid the use of horizontal divider lines. Separate list items using `1.5rem` of vertical whitespace or by alternating between `surface_container_low` and `surface_container_lowest`.
- **Image Treatment**: Images in cards should always use `md` rounded corners and, where possible, slightly "break" the container (asymmetric margins) to feel less like a grid and more like a scrapbook.

### Input Fields
- **Style**: Use a "filled" style with `surface_container_high` backgrounds. Instead of a bottom border, use a subtle `surface_dim` background shift on focus. Labels should be `label-md` in `on_surface_variant`.

### Signature Component: The "Journey Timeline"
A custom vertical list for tour itineraries. Use a thin `primary_fixed` vertical line with `primary` circular nodes. The background of each itinerary "stop" should be a `surface_container` card with a `backdrop-blur`.

---

## 6. Do's and Don'ts

### Do
- **Do** use large amounts of white space (empty `surface` areas) to convey luxury.
- **Do** overlap images and text blocks to create an editorial, non-linear flow.
- **Do** use `notoSerif` for numbers (e.g., price points) to make them feel prestigious.
- **Do** prioritize high-quality photography of mossy stones and jungle sunbeams.

### Don't
- **Don't** use pure black (`#000000`). Use `on_surface` (`#1c1c18`) for all text.
- **Don't** use standard "Material Blue" or "Success Green." Stick strictly to the earthy tones provided.
- **Don't** use 90-degree sharp corners. Everything must have at least a `sm` (0.25rem) radius to feel "welcoming."
- **Don't** clutter the screen. If a section feels "busy," add more `surface` space.

---

## 7. Interaction Notes
- **Transitions**: All page transitions should be a soft "fade and slide" (200ms, ease-out). 
- **Micro-interactions**: When hovering over an itinerary card, it should subtly scale (1.02x) and shift background from `surface_container_low` to `surface_container_high`—a tactile, physical response.```