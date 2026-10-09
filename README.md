# Ignite BA Day Calculator

A one-page app the Brand Ambassador fills in with the retailer. It shows what the day's £10.99 Ignite starter kit sales put in the retailer's pocket, and which replacement bundle those sales pay for.

## How it works

The BA answers two questions:

1. **Did you get the CTU / starter stock free?** If yes, every kit sold is 100% profit (shown with a tick). If no, the BA picks the bundle the stock came from, and the kits carry that bundle's margin.
2. **How many starter kits did we sell?** (or the £ taken)

Everything else follows from those answers and the three Vape Local bundles:

| Bundle | Your price (ex VAT) | RRP (inc VAT) | Margin on its own | Free at |
|---|---|---|---|---|
| Starter | £41.75 | £112.35 | £51.88 / 55% | 5 kits |
| Medium | £75.70 | £202.20 | £92.80 / 55% | 9 kits |
| Pro | £130.00 | £347.00 | £159.17 / 55% | 15 kits |

- **Progress bar:** the day's takings, with a marker where each bundle becomes free.
- **Bundle cards:** for each bundle, free or what's left to pay, kits needed, profit and POR. It shows the best free bundle until the BA taps another.
- **Your bundle:** for the selected bundle, what you pay now, what's left in the till, what the bundle sells for later, and POR.
- **Comparison:** buying the bundle on its own against buying it with today's sales, split into now and later.
- **The maths:** every step, line by line.
- **Kits table:** what each bundle would cost at every number of kits sold.
- **Store name:** the big heading at the top. Tap it to type the store name; it also goes in the summary and the browser tab.
- **Summary:** a copyable message for the store owner.

### Page 2: 12-month forecast

Some of today's kit buyers become regulars and come back for pods and refills. If the retailer gets behind Ignite (on display, kept in stock, recommended by staff), new customers also buy a starter kit every week, and the same share of them become regulars. The regular base snowballs.

Defaults, all editable: retailer engaged, 2 new customers a week, 30% come back, £6.99 a visit (inc VAT, average of pods and refills), every week, 55% margin on reorders, 12 months.

- Regulars from today = kits sold × 30% (rounded)
- Each month (52 ÷ 12 weeks): new customers buy a kit at £10.99, and 30% of them join the regulars (joining steadily through the month)
- Sales a month = regulars × spend per visit × visits a month + new customers' kits
- The first sales sell through the replacement bundle. That profit is already counted on page 1, so the forecast doesn't count it twice.
- After the bundle sells through, every sale makes the reorder margin: reorder profit = (sales ex VAT so far − bundle RRP ex VAT) × 55%
- Total profit = page 1's total profit + reorder profit. The chart splits this into today's deal, reorders from today's regulars, and the extra from new customers.

Example: 10 kits, Medium Bundle, free stock.
- Not engaged: 3 regulars, the bundle sells through in 10 weeks, £591.49 total profit over 12 months.
- Engaged, 2 new customers a week: about 34 regulars by month 12, the bundle sells through in 4 weeks, £3,714.23 total profit (£3,122.74 more).

### Ex VAT / Inc VAT switch

The switch at the top right shows every £ figure either ex VAT (the default, as on Vape Local) or inc VAT. The maths runs in the chosen basis. Ex VAT divides inc-VAT prices (RRP, kit price, till takings) by 1.2. Inc VAT multiplies ex-VAT prices (your bundle price, CTU value) by 1.2. Percentages (POR, margin) are the same in both, and every inc-VAT figure is the ex-VAT figure × 1.2. Example: £184.38 ex VAT = £221.26 inc VAT.

### The maths (ex VAT shown, as on Vape Local)

- Takings ex VAT = kits × £10.99 ÷ 1.2
- You pay now = bundle price − takings (never below £0)
- Left in your till = takings − bundle price (when over £0)
- Bundle sells later for = RRP ÷ 1.2
- POR = (RRP ex VAT − you pay now) ÷ RRP ex VAT
- Total profit = RRP ex VAT − you pay now + left in your till − cost of kits sold (only when the stock wasn't free)

Example: 10 kits, free stock, Medium Bundle. £109.90 taken = £91.58 ex VAT. That covers the £75.70 bundle with £15.88 left in the till. The bundle sells later for £168.50, so POR is 100% and total profit is £184.38, against £92.80 (55%) when buying it on its own.

## Install on an iPad (works offline)

The app is a PWA, served at https://igniteporcal.vercel.app. Vercel deploys every push automatically. Send the team **https://igniteporcal.vercel.app/install.html**, which has a QR code and the steps below.

1. Open the link in **Safari** on the iPad while it has signal.
2. Tap **Share**, then **Add to Home Screen**, then **Add**.
3. Open **BA Day** from the Home Screen. It runs full screen like an app and works with no signal from then on.

Prices, the chosen bundle and the store name are remembered on the device. When an update is pushed, the app picks it up the next time it is opened with signal.

## Editing

- `src/calculator.html` is the calculator. It is also published as a Claude artifact.
- Run `python3 build.py` after editing. It regenerates `index.html` (with app/iPad tags and local fonts), `manifest.webmanifest` and `sw.js` (the offline cache, versioned from the file contents).
- `fonts/` holds self-hosted Barlow and Barlow Condensed (SIL Open Font License). `icons/` holds the app icons.
- `vercel.json` stops the service worker and page being cached by the CDN, so updates reach installed iPads.
