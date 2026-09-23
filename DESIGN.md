---
version: alpha
colors:
  primary: "#FFC857"
  surface: "#0B0C0E"
  surface-raised: "#17191D"
  border: "#343840"
  on-surface: "#F4F5F7"
  on-surface-muted: "#A7ADB7"
  success: "#61D095"
  error: "#FF6B6B"
typography:
  display:
    fontFamily: "Avenir Next, Avenir, Helvetica Neue, sans-serif"
  body:
    fontFamily: "Avenir Next, Avenir, Helvetica Neue, sans-serif"
  utility:
    fontFamily: "SFMono-Regular, Menlo, Monaco, monospace"
rounded:
  DEFAULT: "14px"
  compact: "10px"
  pill: "999px"
spacing:
  compact: "8px"
  normal: "16px"
  section: "28px"
components:
  panel:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.DEFAULT}"
  action-button:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    rounded: "{rounded.compact}"
  status-waiting:
    backgroundColor: "{colors.border}"
    textColor: "{colors.on-surface-muted}"
    rounded: "{rounded.pill}"
  status-safe:
    backgroundColor: "{colors.success}"
    textColor: "{colors.surface}"
    rounded: "{rounded.pill}"
  status-stopped:
    backgroundColor: "{colors.error}"
    textColor: "{colors.surface}"
    rounded: "{rounded.pill}"
---

## Overview

Cashrail Control Room is a product surface for a nontechnical owner who needs to understand the tournament at a glance. Its North Star is a railway signal board: one path, six stops, one unmistakable current state. It must never resemble a trading terminal, developer console, or dense analytics dashboard.

The signature is the **Cashrail line** connecting six bot stations. Color is restrained: amber means waiting or attention, green means verified, and red means stopped. Every color state also carries a word and symbol.

## Colors

The app is permanently dark because the user explicitly prefers black and gray. Coal is the page, graphite is the raised surface, paper is primary text, and fog is secondary text. Signal, safe, and stop are semantic only. Runtime CSS variables in `cashrail_runtime/control_room/styles.css` are the canonical implementation of these values.

## Typography

Avenir Next provides friendly, highly legible headings and body copy. SF Mono is limited to timestamps and identifiers. Headings use sentence case; technical vocabulary is translated into plain language.

## Layout

The desktop layout is a wide story rail above a two-column explanation area. Below 760px it becomes a single vertical rail. The page uses natural document scrolling and never traps the viewport.

## Elevation & Depth

Graphite panels use borders and very soft shadows. Status—not elevation—creates hierarchy.

## Shapes

Stations are circular because they represent stops on a line. Panels use 14px corners; buttons use 10px. Pills are reserved for short status labels.

## Components

The rail, status banner, explanation cards, and buttons use shared CSS variables. Buttons are real semantic buttons with visible focus. The refresh state reserves button width and uses an accessible live region.

## Do's and Don'ts

- Do show one current truth and one next safe step.
- Do say “waiting,” “working,” “stopped,” or “finished.”
- Do count money only when provider-confirmed.
- Do not expose credentials, hashes, raw provider errors, or Controller mutation controls.
- Do not imply that sample walkthroughs are live activity.
