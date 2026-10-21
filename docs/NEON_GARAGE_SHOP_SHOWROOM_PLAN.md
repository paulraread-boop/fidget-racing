# Fidget Racing — Neon Garage, Shop & Showroom (design plan)

Status: planning branch only. Preserve approved Build 32 and current working gameplay; no existing game files changed.

## Visual direction
Use the user's approved futuristic neon garage and new Fidget Racing main-menu artwork as visual references. High-contrast, colorful blue/green/purple/gold cards, legible mobile buttons, 2D racing remains unchanged. Original graphics only.

## Navigation
Keep Race, Garage, Championship, Chat Room, Settings. Within Garage provide Cars, Visuals, Performance, Boosters, My Garage, My Showroom and Profile. Back always returns to Fidget Racing main menu.

## Player profile
Player chooses a name; later name changes cost Racing Credits. Car names, racing numbers, team names, flags, logos and emblems are editable for a price. Store owned items and purchases persistently.

## Economy
Earn Racing Credits by racing, finishing position, championships and achievements. Optional credit packs purchased through Google Play Billing only after real integration and purchase verification. Never charge during preview. Confirm prices before deducting credits. All paint/repaint, colors, decals, rims, identity changes and upgrades cost credits. Repainting again costs again. Owned collectibles and achievements persist.

## One-race consumables
Pre-race boosts at +5%, +10%, +15%, +20%, +25%, progressively priced. Proposed 100, 250, 450, 700, 1000 credits respectively, subject to balancing. Activated boosts expire after the single race, then require repurchase. Distinguish these from persistent installed parts. Define race cancellation/disconnect handling before charging.

## Showroom
Personal collection room for colorful futuristic emblems, medals, trophies, purchased collectibles, player achievements, car history, team accomplishments. 2D cars need not display tiny emblems while racing. Future optional visit-other-showrooms feature requires backend and privacy controls.

## Implementation guardrails
No edits to baseline/approved Build 32; implement on separate feature branch. Verify actual current source and builds before merging. Keep all current race modes, tracks, chat, color slider, garage, championship and navigation. Design and economy are not yet implemented by this planning file.
