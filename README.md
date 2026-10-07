# Ignite BA Day Calculator

A one-page tool for Brand Ambassadors. They enter how many £10.99 Ignite starter kits they sold in a store that day. The page then shows what that means for the retailer:

- how much of the agreed replacement bundle the BA's takings cover
- what the store still pays for the bundle (or £0 when it's free)
- the store's profit on return (POR) on the bundle, plus any extra cash left in the till
- the full maths, a kits-sold ladder, and a summary to copy for the store owner

The starter kits were supplied free, so every kit sold is 100% margin and goes towards the bundle.

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

## Use

Open `index.html` in a browser on a phone or tablet. Edit `src/calculator.html`, then run `./build.sh` to regenerate `index.html`.
