from pathlib import Path

ROOT_DIR = Path('amatol')

def extract_metadata(path: Path) -> dict:
    parts = path.parts
    source_type = parts[1]  # e.g., 'books', 'journals', 'newspapers', 'reports', 'web_articles'
    filename = path.stem  # no .txt

    meta = {
        'source_type': source_type.rstrip('s'),  # singular form
        'file_path': str(path)
    }

    if source_type == 'books':
        # amatol/books/amatol_book/p007.txt
        source_id = parts[2]  # amatol_book
        page = filename  # p007, p014-018, etc.
        meta.update({
            'source_id': source_id,
            'source_name': source_id.replace('_', ' ').title(),
            'page': page
        })

    elif source_type == 'journals':
        # amatol/journals/2018-12__sojourn__all-aboard-for-amatol.txt
        date, source_id, title = filename.split('__', 2)
        meta.update({
            'date': date,
            'source_id': source_id,
            'source_name': source_id.replace('-', ' ').title(),
            'title': title.replace('-', ' ')
        })

    elif source_type == 'newspapers':
        # amatol/newspapers/1918/1918-03-07__tuckerton-beacon__p1__new-site-selected.txt
        year = parts[2]
        date, source_id, page, title = filename.split('__', 3)
        meta.update({
            'year': year,
            'date': date,
            'source_id': source_id,
            'source_name': source_id.replace('-', ' ').title(),
            'page': page,
            'title': title.replace('-', ' ')
        })

    elif source_type == 'reports':
        # amatol/reports/1919__war-expenditures-hearings__p490-494__testimony-of-colonel-hawkins.txt
        parts_split = filename.split('__')
        year, source_id, page, title = parts_split[0], parts_split[1], parts_split[2], parts_split[3]
        meta.update({
            'year': year,
            'source_id': source_id,
            'source_name': source_id.replace('-', ' ').title(),
            'page': page,
            'title': title.replace('-', ' ')
        })

    elif source_type == 'web_articles':
        # amatol/web_articles/2013-12-16__press-of-atlantic-city__ghost-town-of-amatol-nj.txt
        date, source_id, title = filename.split('__', 2)
        meta.update({
            'date': date,
            'source_id': source_id,
            'source_name': source_id.replace('-', ' ').title(),
            'title': title.replace('-', ' ')
        })

    return meta


def scan_and_print(root_dir: Path):
    for path in root_dir.rglob('*.txt'):
        meta = extract_metadata(path)
        print(meta)


if __name__ == '__main__':
    scan_and_print(ROOT_DIR)
