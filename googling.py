#! /usr/bin/env python3

import subprocess
from urllib.parse import urlencode
import argparse
import tkinter

SUBPROCESS_TIMEOUT = 1
VERSION = '1.0.0'


def showerror(msg):
    """show message by tkinter popup."""
    root = tkinter.Tk()
    root.title('')
    tkinter.Label(root, text='Error: ' + str(msg), borderwidth=10).pack()
    tkinter.Button(root, text='Ok', command=root.quit, ).pack()
    root.mainloop()


def get_copied_text(encoding='utf-8'):
    """open subprocess and return text by xclip (-o)"""
    with subprocess.Popen(['xclip', '-o', ], stdout=subprocess.PIPE) as proc:
        out, err = proc.communicate(timeout=SUBPROCESS_TIMEOUT)

    if err:
        return {'code': 1, 'msg': 'xclip subprecess error'}
    try:
        string = out.decode(encoding=encoding)
    except:
        return {'code': 1, 'msg': 'decode error'}
    return {'code': 0, 'string': string}


def google_search(browser='firefox', **kargs):
    """Search copied text by google."""
    # check copied text
    copied_text = get_copied_text()
    if copied_text['code'] != 0:
        return copied_text
    string = copied_text.get('string', '')
    if string == '':
        return {'code': 1, 'msg': 'empty buffer'}

    # construct url
    google_search_url = 'http://www.google.ru/search'
    arguments = {'q': string}
    url = google_search_url + '?' + urlencode(arguments, encoding='utf-8')

    # googling
    browsers_commands = {
        'firefox': ['firefox', url, '-new-tab', ]
    }
    command = browsers_commands.get(browser, None)
    if command is None:
        return {'code': 1, 'msg': 'unknown browser'}
    with subprocess.Popen(command, stdout=subprocess.PIPE) as proc:
        out, err = proc.communicate(timeout=SUBPROCESS_TIMEOUT)
    if err:
        return {'code': 1, 'msg': 'googling subprecess error'}
    return {'code': 0}


def google_translate(browser='firefox', from_='en', to='ru', **kargs):
    """Translate copied text by google."""
    # check copied text
    copied_text = get_copied_text()
    if copied_text['code'] != 0:
        return copied_text
    string = copied_text.get('string', '')
    if string == '':
        return {'code': 1, 'msg': 'empty buffer'}

    # construct url
    google_translate_url = 'https://translate.google.com/#%(from)s/%(to)s/%(q)s'
    url = google_translate_url % {
        'from': from_,
        'to': to,
        'q': urlencode({'q':string}, encoding='utf-8')[2:]
    }

    # googling
    browsers_commands = {
        'firefox': ['firefox', url, '-new-tab', ]
    }
    command = browsers_commands.get(browser, None)
    if command is None:
        return {'code': 1, 'msg': 'unknown browser'}
    with subprocess.Popen(command, stdout=subprocess.PIPE) as proc:
        out, err = proc.communicate(timeout=SUBPROCESS_TIMEOUT)
    if err:
        return {'code': 1, 'msg': 'googling subprecess error'}
    return {'code': 0}


# main functions
def search(**kargs):
    result = google_search(**kargs)
    if result['code'] != 0:
        showerror(result.get('msg', 'unknown'))
        exit(1)


def translate(**kargs):
    result = google_translate(**kargs)
    if result['code'] != 0:
        showerror(result.get('msg', 'unknown'))
        exit(1)


def main():
    """init argument parser."""
    parser = argparse.ArgumentParser(
        description='Tools for googling',
        usage='%(prog)s [options]',  # short description
        epilog='',
        prog='googling.py'        # program name
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=VERSION,
        help='show version of full-kitchen-mode'
    )

    subparsers = parser.add_subparsers(
        help='List of commands'
    )

    # search
    search_parser = subparsers.add_parser(
        'search',
        usage='%(prog)s [options]',
        help='search string from buffer'
    )
    search_parser.set_defaults(func=search)

    # translate
    translate_parser = subparsers.add_parser(
        'translate',
        usage='%(prog)s [options]',
        help='translate string from buffer'
    )
    translate_parser.set_defaults(func=translate)


    options = vars(parser.parse_args())
    if options.get('func', None):
        options['func'](**options)

if __name__ == '__main__':
    main()
