"""Prepare authorized IC PDFs and real-document previews, preserving originals.

Local input paths are arguments, never recorded in the public provenance.
Run once for each approved source version; this does not edit the catalog.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import pymupdf

ROOT = Path(__file__).resolve().parents[1]

def prepare(source, name, preview_page):
    source = Path(source)
    target = ROOT / 'trabalhos' / (name + '.pdf')
    image = ROOT / 'assets' / (name + '.png')
    with pymupdf.open(source) as doc:
        text = '\n'.join(page.get_text() for page in doc)
        # Stop rather than silently copying apparent personal identifiers.
        assert not re.search(r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b', text), 'Review possible CPF privately'
        assert not re.search(r'[A-Za-z]:[\\/](?:Users|heito)[\\/]', text), 'Review local paths privately'
        assert doc.embfile_count() == 0, 'Review embedded files privately'
        for page in doc:
            assert not list(page.annots() or []), 'Review annotations privately'
            for link in page.get_links():
                assert link['kind'] not in {pymupdf.LINK_LAUNCH, pymupdf.LINK_GOTOR}, 'Review external file actions'
        assert 'Heitor' in text, 'Missing expected authorship'
        assert 1 <= preview_page <= len(doc)
        page = doc[preview_page - 1]
        clip = page.rect
        if name == 'ic-fisica-estatistica' and preview_page == 24:
            figures = sorted(page.get_image_info(), key=lambda row: row['bbox'][1])[-2:]
            assert len(figures) == 2
            clip = pymupdf.Rect(figures[0]['bbox']) | pymupdf.Rect(figures[1]['bbox'])
            clip = pymupdf.Rect(30, clip.y0 - 8, page.rect.width - 30, clip.y1 + 55) & page.rect
        scale = 1200 / clip.width
        page.get_pixmap(matrix=pymupdf.Matrix(scale, scale), clip=clip, alpha=False).save(image)
        pages = len(doc)
    shutil.copyfile(source, target)
    assert hashlib.sha256(source.read_bytes()).digest() == hashlib.sha256(target.read_bytes()).digest()
    return {
        'id': name,
        'document': target.relative_to(ROOT).as_posix(),
        'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
        'pages': pages,
        'preview': image.relative_to(ROOT).as_posix(),
        'previewPage': preview_page,
        'preparation': 'Cópia integral autorizada pelo autor; créditos e referências preservados. Prévia renderizada de uma página real, sem reconstrução dos resultados.'
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--slides', required=True)
    parser.add_argument('--report', required=True)
    parser.add_argument('--report-preview-page', type=int, required=True)
    args = parser.parse_args()
    rows = [prepare(args.slides, 'ic-rotacoes-simetria', 98),
            prepare(args.report, 'ic-fisica-estatistica', args.report_preview_page)]
    (ROOT / 'proveniencia-ics.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(rows, ensure_ascii=True, indent=2))

if __name__ == '__main__':
    main()
