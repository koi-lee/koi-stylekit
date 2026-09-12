"""Build a relocatable static gallery. Pillow is a build-only dependency."""
import json
import shutil
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'wireframes'
OUT = ROOT / 'dist'

def build():
    OUT.mkdir(exist_ok=True)
    for name in ('index.html', 'renderer.mjs', 'render-rules.json', 'robots.txt', 'llms.txt'):
        shutil.copy2(SOURCE / name, OUT / name)
    (OUT / '.nojekyll').touch()
    styles = json.loads((SOURCE / 'styles.json').read_text())
    media = OUT / 'media'
    media.mkdir(exist_ok=True)
    original_bytes = 0
    for style in styles:
        source = SOURCE / style['image']
        original_bytes += source.stat().st_size
        with Image.open(source) as img:
            for suffix, size in (('thumb', 480), ('detail', 1200)):
                output = media / f'{style["id"]}-{suffix}.webp'
                if not output.exists() or output.stat().st_mtime < max(source.stat().st_mtime, Path(__file__).stat().st_mtime):
                    preview = ImageOps.exif_transpose(img).convert('RGB')
                    preview.thumbnail((size, size))
                    preview.save(output, 'WEBP', quality=80, method=6)
        # Use the encoded detail size: thumbnail rounding can change its ratio.
        with Image.open(media / f'{style["id"]}-detail.webp') as detail:
            style['image_width'], style['image_height'] = detail.size
        style['thumbnail'] = f'media/{style["id"]}-thumb.webp'
        style['image'] = f'media/{style["id"]}-detail.webp'
        sample = source.with_suffix('.json')
        if sample.exists():
            shutil.copy2(sample, media / f'{style["id"]}.json')
            style['sample_input'] = f'media/{style["id"]}.json'
    # Include the linked application case gallery, compressing its PNGs too.
    cases = SOURCE / 'cases/style-applications'
    target = OUT / 'cases/style-applications'
    target.mkdir(parents=True, exist_ok=True)
    for file in cases.iterdir():
        if file.suffix == '.png':
            with Image.open(file) as img:
                img = img.convert('RGB'); img.thumbnail((1200,1200))
                img.save(target / (file.stem+'.webp'), 'WEBP', quality=80)
        elif file.suffix == '.html':
            (target / file.name).write_text(file.read_text().replace('.png','.webp').replace('<img ', '<img loading="lazy" decoding="async" '))
        elif file.suffix == '.json':
            shutil.copy2(file, target / file.name)
    (OUT / 'styles.json').write_text(json.dumps(styles, ensure_ascii=False, separators=(',',':')))
    size = sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file())
    print(json.dumps({'recipes':len(styles),'original_gallery_bytes':original_bytes,'static_bytes':size,'output':str(OUT)},indent=2))

if __name__ == '__main__':
    build()
