# Contributing

[简体中文](CONTRIBUTING.md) | **English**

Contributions of style recipes, reproduction evidence, and bug fixes are welcome. Establish the use case before making changes.

Style data lives in `wireframes/styles.json`; `scripts/koi.py` is the shared gallery and CLI renderer. New recipes must include a stable ID, name, source and license, actual complete prompt, sample image, and validation status. Do not import third-party images or entire prompt collections without permission.

Mark generated samples as AI-generated and retain the subject and actual request. Record individual image quality, user approval, cross-subject checks, and cross-model checks separately. One successful sample is not a general guarantee. When changing a recipe, update its version and explain differences from the original sample.

Before submitting code changes, run:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/serve.py
```

Check affected interactions in the browser. For documentation-only changes, verify examples and links as appropriate. Keep Chinese and English user-facing documentation aligned; label links to untranslated material clearly.

Do not commit secrets, private user subjects, caches, or runtime logs. The current server is for local use, not public hosting.
