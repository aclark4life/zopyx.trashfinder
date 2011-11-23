import sys
from xmlrpclib import Server

def main():

    prefix = ''
    if len(sys.argv) > 1:
        prefix = sys.argv[1]

    server = Server('http://pypi.python.org/pypi')
    packages = server.list_packages()
    if prefix:
        packages = [p for p in packages if p.startswith(prefix)]

    num_packages = len(packages)

    for i, package in enumerate(packages):
        print 'Processing %r (%d/%d)' % (package, i+1, num_packages)

        versions = server.package_releases(package)
        versions.sort()
        for version in versions:
            print '  ', version
            urls = server.release_urls(package, version)
            metadata = server.release_data(package, version)

            # PyPI hosted packages
            if urls:
                have_eggs = False
                have_sdist = False
                for url in urls:
                    url = url['url']
                    print '    ', url
                    if url.endswith('.bz2') or url.endswith('.zip') or url.endswith('gz'):
                        have_sdist = True
                    if url.endswith('egg'):
                        have_eggs = True

                if have_eggs and not have_sdist:
                    print 'CRAP: %s has only egg release files but no sdist release file' % package

                if have_eggs and have_sdist:
                    print 'CRAP(possible): %s has egg *and* sdist release file' % package

            # externally hosted packages
            else:
                download_url = metadata['download_url']
                if download_url == 'UNKNOWN':
                    print 'CRAP: %s==%s - no release files, no valid download_url' % (package, version)

            if len(metadata['description'] or '') < 40:
                    print 'CRAP: %s==%s - description < 40 chars' % (package, version)
            if len(metadata['summary'] or '') < 10:
                    print 'CRAP: %s==%s - summary < 10 chars' % (package, version)
            if not metadata['author_email'] and not metadata['maintainer_email']:
                    print 'CRAP: %s==%s - no author and no maintainer email given' % (package, version)
            if not metadata['author'] and not metadata['maintainer']:
                    print 'CRAP: %s==%s - no author and no maintainer name given' % (package, version)


if __name__ == '__main__':
    main()
