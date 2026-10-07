# Ignite BA Day Calculator

A one-page tool for Brand Ambassadors. They enter how many £10.99 Ignite starter kits they sold in a store that day. The page then shows what that means for the retailer:

- how much of the agreed replacement bundle the BA's takings cover
- what the store still pays for the bundle (or £0 when it's free)
- the store's profit on return (POR) on the bundle, plus any extra cash left in the till
- the full maths, a kits-sold ladder, and a summary to copy for the store owner

The BA fills it in with the retailer, so the copy talks to the retailer directly ("you pay", "your pocket").

**Did you get the CTU / starter stock free?** When the answer is Yes (the default), the page shows a tick, says what the free stock is worth (Ignite CTU, £78.27 ex VAT) and treats every kit sold as 100% margin. When it is No, the retailer bought their first stock as one of the bundles (Starter, Medium or Pro). The kits then carry that bundle's 55% margin. The total shows the usual bundle margin plus the margin on today's kits on top.

## Bundles

| Preset | Store cost | RRP | Margin with no BA sales |
|---|---|---|---|
| Starter | £41.75 + VAT | £112.35 inc VAT | £51.88 / 55% |
| Medium | £75.70 + VAT | £202.20 inc VAT | £92.80 / 55% |
| Pro | £130.00 + VAT | £347.00 inc VAT | £159.17 / 55% |
| Example | £57.90 | £107.50 | £49.60 / 46% (no VAT) |

The three bundle presets use Vape Local's VAT basis: RRP and kit takings are divided by 1.2, and the bundle cost is ex VAT. You can switch VAT off and edit the prices under **Prices & agreed bundle**.

### Worked example (Example preset)

- No BA day: the store pays £57.90 and sells for £107.50, so POR = 46%
- The BA sells £30: the store pays only £27.90, so POR = 74%
- The BA sells £100: the store pays £0, so POR = 100%, plus £42.10 extra in the till

## Install on an iPad (works offline)

The app is a PWA, served at https://igniteporcal.vercel.app.

1. Open the link in **Safari** on the iPad while it has signal.
2. Tap **Share**, then **Add to Home Screen**, then **Add**.
3. Open **BA Day** from the Home Screen. It runs full screen like an app and works with no signal from then on.

Prices, the chosen bundle and the store name are remembered on the device. When an update is pushed, the app picks it up the next time it is opened with signal.

## Editing

- `src/calculator.html` is the calculator. It is also published as a Claude artifact.
- Run `python3 build.py` after editing. It regenerates `index.html` (with app/iPad tags and local fonts), `manifest.webmanifest` and `sw.js` (the offline cache, versioned from the file contents).
- `fonts/` holds self-hosted Barlow and Barlow Condensed (SIL Open Font License). `icons/` holds the app icons.
- `vercel.json` stops the service worker and page being cached by the CDN, so updates reach installed iPads.
