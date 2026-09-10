# Catalogue expansion

[简体中文](风格扩充.md) | **English**

The catalogue has 300 recipes across nine medium categories: 40 style families and 260 technique or composition variants. A variant inherits its family rules and adds a treatment. This is not a claim of 300 independent art media.

New recipes were written for this project. Upstream images and recipes were not copied. The browsing organization draws on yang0 and the recipe approach on threerocks; existing attribution and licensing records remain applicable.

## Using the catalogue

Filter by category or family, search by number, browse 24 entries per page, compare up to three candidates, select one, and export a prompt for your subject. Documentation is bilingual; the interface and recipe instructions remain Chinese.

## Sample evidence

New samples use the exact exported `prompt_zh` recorded in the adjacent JSON file under `wireframes/assets/catalogue`. The common subject is “a cat holding an umbrella in the rain, full subject, simple background”, with a 1:1 aspect ratio. The built-in image generation tool received no explicit reference image. PNG files preserve the generated originals. Four historical samples retain their earlier subjects and evidence.

Each new image is a single-generation candidate for one subject. Individual visual acceptance, cross-subject repeatability, and cross-model consistency remain unverified. Continuous-line connectivity, flat fills, paper-cut connections, and simple backgrounds can drift. Fixed-palette media may conflict with requested subject colors. Nearby variants may look similar. Successful prompt export does not establish visual quality.

Automated checks cover unique identifiers, family relationships, supported purposes, both color policies, and exact agreement between saved sample prompts and the current renderer. CLI, local HTTP, and browser checks are recorded in the Chinese execution log. Sample completion is represented by the catalogue image field and actual files; publication and CI status are recorded separately.

## Verification on 2026-09-10

All 300 entries have samples: 4 existing images and 296 newly generated candidates. Ten automated tests passed, including 1,264 export combinations, saved prompt provenance, complete PNG chunks and distinct file hashes. All 596 image and input JSON HTTP responses matched local files byte for byte. The browser showed 300 samples and zero pending images; page 13 and entry 300 details were exercised. These are functional checks, not approval of every visual result.
