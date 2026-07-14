# Wireless Quick-Dial Cards

Frequency quick-dial reference cards for pro wireless systems (Sennheiser, Shure, Lectrosonics, Sony, Wisycom & more). Aimed at frequency coordination teams at large events, and their clients.

**Live deck:** https://gothamsound.github.io/quick-dial-cards/

Each card covers one transmitter / portable-receiver pair: how to dial an assigned frequency, RF power settings, safe (RF-off) power-on methods, and watch-outs. Maintained by [Gotham Sound](https://gothamsound.com).

## Suggesting changes

Spot an error, an outdated procedure, or a missing system? Open an issue:

- [**Suggest a change to a card**](../../issues/new?template=suggest-change.yml) — corrections to existing cards
- [**Request a new system card**](../../issues/new?template=new-system.yml) — systems not yet covered

A GitHub account is required (that's the point — every suggestion is attributable). Suggestions are reviewed and verified by Gotham Sound before publishing; please cite a source (manual, firmware note, bench test) so we can verify quickly.

## How the deck is classified

| Badge | Meaning |
|---|---|
| Green | Native 25 kHz tuning spacing — dial any coordinated frequency directly |
| Deep green | Finer than 25 kHz (e.g. Sennheiser 3000/5000 VAR bank, 5 kHz) |
| Amber | Group-gated — a group/bank must be selected before arbitrary MHz entry |
| Red | Setting-gated — a menu setting must be changed first (e.g. Lectrosonics Step Size → 25 kHz) |
| Channel chart only | Fixed channels, no arbitrary tuning (e.g. Comtek 216 MHz) |

## Repository layout

```
index.html                      — fast-lookup app (the published site)
print.html                      — the full print-layout card deck
tools/build_app.py              — generates index.html from print.html
quick-dial-cards.pdf            — print-ready PDF (Letter)
quick-dial-cards-editable.xlsx  — editable workbook, one tab per card
assets/                         — logo and static assets
```

All deliverables are kept in sync — print.html is the canonical source; the app is generated from it verbatim by tools/build_app.py.

**Downloads:** [PDF](quick-dial-cards.pdf) · [Editable XLSX](quick-dial-cards-editable.xlsx)

## License

See [LICENSE](LICENSE).
