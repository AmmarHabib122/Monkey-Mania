# Forged idea: options-based product refactor (Monkey Mania)

**Problem:** one product per sauce, sauces/toppings hidden in a 75-char note, so stock and bills are inaccurate; many API calls on a weak connection; no images.

## Locked decisions
- **Hierarchy:** ProductCategory > ProductFamily > Product (variant, existing table refactored in place; one table, no old/new split). Category, family, variant and option each have an image column; replacing an image deletes the old file.
- **Variant columns:** `mandatory_parts` (exact total parts; 0 = no mandatory options) and `mandatory_qty_total` (grams for the whole dish; 0 = picks still required, price applies, no stock consumed).
- **Option:** `type` = `mandatory` | `addon`. Price per branch only (`BranchOption`). Allowed options configured per variant (`ProductOption`).
- **Order rules:** mandatory option counts must sum exactly to `mandatory_parts` (UI picks the split, e.g. 4 Nutella or 2+2). Addons: any number. Each order line is its own row; same product can repeat.
- **Stock:** `Recipe` (renamed `BranchProductMaterial`) links a variant OR an option to a Material, global across branches. Mandatory consumption = parts x (qty_total / parts) x recipe qty; addon = count x recipe qty. Frozen at order time in `ProductBillProductOption` (name, parts, qty, price, returned, wasted).
- **MaterialTransaction** (with branch) records every stock change (order, return, waste, purchase, opening); updates atomic; opening stock count after migration because current stock data is corrupted.
- **Returns:** whole line returns all its options; one option can be returned alone (refund only its price; stock returns unless cashier marks it wasted).
- **Money:** whole units; proportional amounts rounded down.
- **Idempotency:** `request_id` on order create, add-items and returns.
- **API:** `GET menu/?branch=` single call (Redis cached, versioned/ETag, image URLs only, no recipes). Order item = `{product_id, quantity, notes, options:[{option_id, count}]}`.
- **Redis** via django-redis plus a redis service in docker-compose. Never cache bills or stock writes.

## Migration (zero data loss for Product, BranchProduct, Bill, ProductBill)
Backup, dry run on a copy; add snapshot columns (name, unit price) to bill lines and backfill first; add columns/tables additively; old flavour rows stay in the same table as retired and linked to their family; the 255 products are fixed manually on production; export recipe rows to CSV before repointing/merging; drop old `layer1/2/3` only in a later release.

## Work items
1. Backup + dry run; `unit_price` and `product_name` snapshot columns on bill lines and returned lines, backfilled, with a read-only report of bills whose lines do not match their stored `total_price`.
2. New schema (category, family, product columns, option, branch option, product option, recipe, material transaction, bill line option).
3. Stock engine: atomic updates, transactions, fix offer quantity compounding (`ProductBillSerializers.py:376`), opening stock count.
4. Order APIs with request_id, option validation, whole/single-option returns, waste.
5. Menu API + Redis caching.
6. Images + production hardening:
   - ImageField on category, family, variant and option; delete the old file on replace; random/hash file names so URLs can be cached long.
   - Fix production: restore `DEBUG = config('DEBUG', default=False, cast=bool)` (the docker branch hardcodes True) and set `DEBUG=False` in the server `.env`.
   - With debug off: bring back WhiteNoise (or let nginx serve `/static/`), run `collectstatic` in `start.sh`, add `LOGGING` so errors reach container logs.
   - Serve `/media/` without the debug helper: first find out whether a reverse proxy (nginx/Caddy) already fronts the container (unknown today). If yes, add a `/media/` location with long cache; if no, add an nginx service to docker-compose sharing the `media` volume; fallback is a Django `serve` route. Include `media/` in backups.
7. Manual production data fix of 255 products; dry run.
8. **Generate an API documentation JSON file (OpenAPI) for all existing and new APIs** (e.g. drf-spectacular schema committed to the repo).
9. Angular refactor (separate repo) to match the new contracts.

## Rejected
Parallel old/new catalog or mapping table; OptionGroup table; rules table (columns instead); table renaming (comments later, except Recipe); offline order queue; per-variant option prices; flavour option type (drinks stay products for now); earlier branches `revamp-products-module-v2` and `refactor-whole-products-model` (outdated, reference only).

## Parked (phase 2, not in current plan)
Discounts and offers: bundle price (specific or generic, e.g. buy 2 waffles get a mango or any drink free), buy-N-get-one-free, manual bill discount; only one mechanism per bill; free items still consume stock.
