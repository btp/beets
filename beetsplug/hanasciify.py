from beets.plugins import BeetsPlugin
from beets import config

import os

from unihandecode import Unihandecoder

class HanAsciify(BeetsPlugin):
    def __init__(self):
        super(HanAsciify, self).__init__()
        self.template_funcs['hanasciify'] = _tmpl_hanasciify

def _tmpl_hanasciify(s):
    """Translate non-ASCII characters to their ASCII equivalents using
    language preference priority.

    """
    return hanasciify_path(s, config['path_sep_replace'].as_str())

def hanasciify_path(path, sep_replace):
    """Decodes all unicode characters in a path into ASCII equivalents using
    CJKV language preference priority.

    Substitutions are provided by the hanunidecode module. Path separators in
    the input are preserved.

    Keyword arguments:
    path -- The path to be asciified.
    sep_replace -- the string to be used to replace extraneous path separators.

    """
    if config['hanasciify']['language'].as_str() == "ja":
        d = Unihandecoder(lang='ja')
    if config['hanasciify']['language'].as_str() == "kr":
        d = Unihandecoder(lang='kr')
    if config['hanasciify']['language'].as_str() == "vn":
        d = Unihandecoder(lang='vn')
    if config['hanasciify']['language'].as_str() == "zh":
        d = Unihandecoder(lang='zh')
    else:
        d = Unihandecoder()
    # if this platform has an os.altsep, change it to os.sep.
    if os.altsep:
        path = path.replace(os.altsep, os.sep)
    path_components = path.split(os.sep)
    for index, item in enumerate(path_components):
        path_components[index] = d.decode(item).replace(os.sep, sep_replace)
        if os.altsep:
            path_components[index] = d.decode(item).replace(
                os.altsep,
                sep_replace
            )
    return os.sep.join(path_components)
