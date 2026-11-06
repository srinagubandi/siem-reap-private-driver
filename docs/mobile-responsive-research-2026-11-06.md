# Mobile responsive research and 22-width test matrix

## Findings

StatCounter's October 2026 mobile data shows Europe concentrated at 414×896 (17.89%), 384×832 (11.06%), 390×844 (8.02%), 393×873 (5.64%), 360×780 (5.38%), and 360×800 (4.70%). Germany's leading widths are 414, 384, 393, 390, and 360 CSS pixels. [1] [2]

StatCounter's September 2026 Asia data shows 360×800 (10.85%), 414×896 (10.43%), 384×832 (4.89%), 393×873 (4.59%), 390×844 (3.85%), and 385×854 (3.23%). India is particularly concentrated at 360×800 (15.71%), followed by 393×873, 384×832, 385×854, and related 360/393 widths. [3] [4]

The site should therefore treat 360–414 CSS-pixel phones as first-class targets, while also covering very narrow 320–359 devices, 428–480 large phones, landscape phone heights, tablets, and desktop widths. The 22 checks below are intentionally a test matrix, not 22 device-specific assumptions.

## Proposed 22 viewport checks

1. 320×568 — narrow compact phone
2. 320×640 — narrow tall phone
3. 344×882 — narrow modern Android portrait
4. 360×640 — compact Android portrait
5. 360×780 — common European/Asian phone
6. 360×800 — leading Asian/India width
7. 375×667 — compact iPhone portrait
8. 375×812 — tall compact iPhone portrait
9. 384×832 — leading European/Asian width
10. 385×854 — common Asian width
11. 390×844 — common European/Asian width
12. 393×852 — modern Android/iPhone-width portrait
13. 393×873 — common European/Asian width
14. 414×736 — large phone short portrait
15. 414×896 — leading European/Asian width
16. 428×926 — large phone portrait
17. 480×800 — large phone / narrow tablet boundary
18. 568×320 — landscape phone
19. 667×375 — landscape phone
20. 768×1024 — tablet portrait
21. 820×1180 — tablet portrait
22. 1024×600 — tablet landscape / small laptop

## Implementation principle

Use mobile-first fluid CSS and add targeted media queries only where content actually needs to change. The booking and calling actions are release-critical: at each portrait width, the first-screen hero must retain a visible booking CTA and a visible call/WhatsApp action without horizontal scrolling. At landscape widths, the header and hero must remain usable without relying on a fixed device model.

web.dev recommends sizing content to the viewport, preventing horizontal scrolling, keeping images fluid with `max-width: 100%`, reserving image space with width/height attributes, and choosing media queries when content needs to change. It also documents minor breakpoints for natural intermediate adjustments. [5]

MDN recommends mobile-first responsive layouts, flexible grids, relative units, and breakpoints chosen where content begins to fail rather than targeting device names. [6] Nielsen Norman Group notes that breakpoints should be based on the site's audience and content, and that most sites usually need only a few major layout ranges; the requested 22 points are therefore used as a QA matrix with fluid interpolation, not 22 separate visual layouts. [7]

## Sources

[1]: https://gs.statcounter.com/screen-resolution-stats/mobile/europe "StatCounter Mobile Screen Resolution Stats in Europe"
[2]: https://gs.statcounter.com/screen-resolution-stats/mobile/germany "StatCounter Mobile Screen Resolution Stats in Germany"
[3]: https://gs.statcounter.com/screen-resolution-stats/mobile/asia "StatCounter Mobile Screen Resolution Stats in Asia"
[4]: https://gs.statcounter.com/screen-resolution-stats/mobile/india "StatCounter Mobile Screen Resolution Stats in India"
[5]: https://web.dev/articles/responsive-web-design-basics "Responsive web design basics"
[6]: https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design "MDN Responsive design"
[7]: https://www.nngroup.com/articles/breakpoints-in-responsive-design/ "Nielsen Norman Group Breakpoints in Responsive Design"
