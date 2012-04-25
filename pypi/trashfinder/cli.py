from xmlrpclib import Server
server = Server('http://pypi.python.org/pypi')


def process_packages(packages):
    results = []
    for i, package in enumerate(packages):
        versions = server.package_releases(package)
        versions.sort()
        if len(versions) > 0:
            version = 
        for version in versions:
            urls = server.release_urls(package, version)
            metadata = server.release_data(package, version)
            if urls:  # PyPI hosted packages
                have_eggs = False
                have_sdist = False
                for url in urls:
                    url = url['url']
                    if url.endswith('.bz2') or url.endswith('.zip') or url.endswith('gz'):
                        have_sdist = True
                    if url.endswith('egg'):
                        have_eggs = True
                if have_eggs and not have_sdist:
                    results.append( '%s has only egg release files but no sdist release file' % package)
            else:  # externally hosted packages
                download_url = metadata['download_url']
                if download_url == 'UNKNOWN':
                    results.append( '%s - No release files, no valid download_url' %
                        version)
            if len(metadata['description'] or '') < 40:
                    results.append( '%s - description < 40 chars' % version)
            if len(metadata['summary'] or '') < 10:
                    results.append( '%s - summary < 10 chars' % version) 
            if not metadata['author_email'] and not metadata['maintainer_email']:
                    results.append( '%s - No author and no maintainer email given' %
                        version)
            if not metadata['author'] and not metadata['maintainer']:
                    results.append( '%s - No author and no maintainer name given' %
                        version)
    if results == list():
        print '%s is OK' % version
    return results
