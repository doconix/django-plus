from ..command import run_command
from ..util import get_dmp_instance, merge_dicts
from .provider_base import BaseProvider

import os
import os.path
import shutil



class CompileProvider(BaseProvider):
    '''
    Compiles static files, such as *.scss or *.less, when an output file 
    timestamp is older than the source file. In production mode, this check
    is done only once (the first time a template is run) per server start.
    
    Special format keywords for use in the options:
        {appdir} - The app directory for the template being rendered (full path).
        {template} - The name of the template being rendered, without its extension.
    '''
    # the command line should be specified as a list (see the subprocess module)
    default_options = merge_dicts(BaseProvider.default_options, {  
        'group': 'styles',
        'weight': 10,  
        'source': '{appdir}/somedir/{template}.source',
        'compiled': '{appdir}/somedir/{template}.output',
        'command': [ 'echo', '{appdir}/somedir/{template}.source', '{appdir}/somedir/{template}.output' ],
    })
    def init(self):
        # doing the check in init() so it only happens one time during production
        fargs = {
            'appdir': self.app_dir, 
            'template': self.template_name,
        }
        source_path = self.options['source'].format(**fargs)
        compiled_path = self.options['compiled'].format(**fargs)
        if os.path.exists(source_path):
            try:
                needs_compile = os.path.getmtime(compiled_path) < os.path.getmtime(source_path)
            except OSError:  # usually means compiled_path doesn't exist
                needs_compile = True  
            if needs_compile:
                run_command(*[ a.format(**fargs) for a in self.options['command'] ])


class CompileScssProvider(CompileProvider):
    '''Specialized CompileProvider that contains settings for *.scss files.'''
    default_options = merge_dicts(CompileProvider.default_options, {  
        'source': '{appdir}/styles/{template}.scss',
        'compiled': '{appdir}/styles/{template}.css',
        'command': [ shutil.which('scss'), '--unix-newlines', '{appdir}/styles/{template}.scss', '{appdir}/styles/{template}.css' ],
    })


class CompileLessProvider(CompileProvider):
    '''Specialized CompileProvider that contains settings for *.less files.'''
    default_options = merge_dicts(CompileProvider.default_options, {  
        'source': '{appdir}/styles/{template}.less',
        'compiled': '{appdir}/styles/{template}.css',
        'command': [ shutil.which('lessc'), '--source-map', '{appdir}/styles/{template}.less', '{appdir}/styles/{template}.css' ],
    })

    