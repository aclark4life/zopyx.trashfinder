from xmlrpclib import Server
server = Server('http://pypi.python.org/pypi')


def process_package(package):
    results = []
    versions = server.package_releases(package)
    versions.sort()
    if len(versions) > 0:
        version = versions[-1]
        urls = server.release_urls(package, version)
        metadata = server.release_data(package, version)
        if urls:  # PyPI hosted packages
            have_eggs = False
            have_sdist = False
            for url in urls:
                url = url['url']
                if (url.endswith('.bz2') or url.endswith('.zip') or
                    url.endswith('gz')):
                    have_sdist = True
                if url.endswith('egg'):
                    have_eggs = True
            if have_eggs and not have_sdist:
                msg = '%s has only egg release files but no sdist'
                msg += 'release file'
                results.append(msg % package)
        else:  # externally hosted packages
            download_url = metadata['download_url']
            if download_url == 'UNKNOWN':
                msg = 'No release files, no valid download_url'
                results.append(msg)
        if len(metadata['description'] or '') < 40:
            msg = 'description < 40 chars'
            results.append(msg)
        if len(metadata['summary'] or '') < 10:
            results.append('summary < 10 chars')
        if not metadata['author_email'] and not metadata['maintainer_email']:
            results.append('No author and no maintainer email given')
        if not metadata['author'] and not metadata['maintainer']:
            results.append('No author and no maintainer name given')
    return results
