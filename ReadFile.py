from hyperlink import URL
from furl import furl


class Traverse:
    pass


def package_list(package_name: object = None) -> object:
    default_url_text = 'http://127.0.0.1:5000/api/package-list?package-name=tcpd'

    file_name = open("status", "r", encoding="utf8")
    main_dict = {}
    for item in file_name.read().split('\n\n'):
        key, value = '', ''
        commands = {}
        x = 0
        dict_key = ''
        for row in item.split('\n'):
            if not row == '':
                if x == 0:
                    dict_key = row.split(':', 1)[1].strip()
                    x += 1
                    commands['Depends'] = ''
                if not row.startswith(' '):
                    key = row.split(':', 1)[0].strip()

                    if key == 'Depends':
                        value = row.split(':', 1)[1].split(',')
                        commands[key] = []
                        for dependency in value:
                            commands[key].append(dependency.split('(')[0].strip())
                    elif key == 'Package':
                        value = row.split(':', 1)[1].strip()
                        commands[key] = value
                    elif key == 'Description':
                        value = row.split(':', 1)[1].strip()
                        commands[key] = value
                else:
                    if key == 'Depends':
                        commands[key] += row
                    elif key == 'Description':
                        commands[key] += row
        main_dict[dict_key] = commands
    file_name.close()

    if package_name is not None:
        # for inverse dependencies scan through all dependencies of all packages
        url = ''
        url_dict = {}
        for package in main_dict:
            for depends in main_dict[package]['Depends']:
                if depends.strip() == package_name:
                    url = furl(default_url_text)
                    url.set({"package_name": package})
                    url.url
                    url_dict[package] = url
        main_dict[package_name]['InverseDependency'] = url_dict

    for package in main_dict:
        url_dict = {}
        for depends in main_dict[package]['Depends']:
            dependency_this = depends.split('(')[0]
            key_url, url = '', ''
            for each_package in main_dict:
                # print(each_package)
                key_url = each_package
                if dependency_this.strip() == each_package.strip():
                    url = furl(default_url_text)
                    url.set({"package_name": key_url})
                    url.url
                    url_dict[key_url] = url
        main_dict[package]['Depends'] = url_dict
    if package_name is not None:
        main_dict = {package_name: main_dict[package_name]}
    return main_dict


# main_dict = Traverse.package_list('libws-commons-util-java')
# print(Traverse.package_list('libws-commons-util-java'))
# tel={'jack': 4098, 'sape': 4139, 'guido': 4127}
# print(tel['jack'])

# for di in main_dict:
#      print(di, main_dict[di])
url_text = 'http://127.0.0.1:5000/api/package-list?package-name=tcpd'
urls = ''
url = furl(url_text)
url.set({"package_name": "tcpd"})
url.url
url_text = 'http://127.0.0.1:5000/api/package-list?package-name=tcpd'
url2 = furl(url_text)
url2.set({"package_name": "tcpd"})
url2.url

print(url)
# print(url.replace(path=u'http://github.com/python-hyper/'))
