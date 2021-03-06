.. _faq:

FAQ
=================================


General
-----------------------------


Where Is DMP Used?
^^^^^^^^^^^^^^^^^^^^^^^^

This app was developed at MyEducator.com, primarily by `Dr. Conan C. Albrecht <mailto:doconix@gmail.com>`_. Please email me if you find errors with this tutorial or have suggestions/fixes. In addition to several production web sites, I use the framework in my Django classes at BYU. 120+ students use the framework each year, and many have taken it to their companies upon graduation. At this point, the framework is quite mature and robust. It is fast and stable.

I've been told by some that DMP has a lot in common with Rails. When I developed DMP, I had never used RoR, but good ideas are good ideas wherever they are found, right? :)



What's wrong with Django's built-in template language?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Django comes with its own template system, but it's fairly weak (by design). Mako, on the other hand, is a fantastic template system that allows full Python code within HTML pages.

The primary reason Django doesn't allow full Python in its templates is the designers want to encourage you and I to keep template logic simple. I fully agree with this philosophy. I just don't agree with the "forced" part of this philosophy. The Python way is rather to give freedom to the developer but train in the correct way of doing things. Even though I fully like Python in my templates, I still keep them fairly simple. Views are where your logic goes.



Why Mako instead Django or Jinja2?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Python has several mature, excellent templating languages. Both Django and Jinja2 are fairly recent yet mature systems. Both are screaming fast.

Mako itself is very stable, both in terms of "lack of bugs" and in "completed feature set". Today, the Mako API almost never changes because it does exactly what it needs to do and does it well. This make it an excellent candidate for server use.

The short answer is I liked Mako's approach the best. It felt the most Pythonic to me. Jinja2 may feel more like Django's built-in template system, but Mako won out because it looked more like Python--and the point of DMP is to include Python in templates.


Will it bundle?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Yes. DMP's providers automatically create entry files for template-related JS and CSS. See the `Tutorial </tutorial_css_js.html>`_ for how templates relate to their JS and CSS and `Webpack Providers </static_webpack.html>`_ for webpack-specific information.


Using Third-Party Apps
--------------------------------------------------


Does DMP work alonside third-party Django apps?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Yes. DMP plugs in as a regular templating engine per the standard Django API.  You can use both DMP and regular Django simultaneously in the same project.

When you include DMP's ``urls.py`` module in your project, patterns for each DMP-enabled app in your project are linked to our convention-based router.  Other apps won't match these patterns, so other apps route the normal Django way. This means third-party apps work just fine with DMP.


How do I call a tag from a third-party app?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See the `integration docs </install_third_party>`_ for examples.


Can I use both Mako and Django/Jinja2 syntax?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Yes.  Django officially supports having two or more template engines active at the same time.  Third party apps likely use Django's templating system rather than Mako. The two templating systems work fine side by side.

If you temporarily need to switch to Django templating syntax (even within a Mako file), `you can do that too <#using-django-and-jinja2-tags-and-syntax>`_.


Technical Details
---------------------------------

Why am I getting Page Not Found?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check your console logs. Assuming you have DMP logging at DEBUG level (see next question), your terminal should be blowing up with lots of messages that should make the process transparent and debuggable.

Another possibility is that you have the right url, but your view module has syntax or import errors and isn't compiling. In this case, you'll get Django's yellow and white "404 Not Found" page. If a url matches but DMP still can't resolve it, the reason will be listed on this page.

DMP adds a text emoji to help you spot these. In the following example, the sad face ``◉︵◉`` is followed by the reason url reslution failed.

::

    Page not found (404)
    Request Method: 	GET
    Request URL: 	http://localhost:8000/...

    Using the URLconf defined in project.urls, Django tried these URL patterns, in this order:

        ^admin/
        ...
        ^(?P<dmp_page>[_a-zA-Z0-9\-]+)/(?P<dmp_urlparams>.+?)/?$ ◉︵◉ Pattern matched, but discovery failed: module "homepage.views.process_request" could not be imported: cannot import name '...' from '...'

    The current path, ..., didn't match any of these.

    You're seeing this error because you have DEBUG = True in your Django settings file. Change that to False, and Django will display a standard 404 page.



Why is DMP is logging to the browser console?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The automatic inclusion of JS and CSS is a common trouble spot for new users of DMP, so we log debug information to both the Python and browser consoles.

To turn these messages off, adjust the DMP logger in your settings to any level above DEBUG:

.. code-block:: python

    LOGGING = {
        ...
        'loggers': {
            ...
            'django_mako_plus': {
                'handlers': ['console_handler'],
                'level': 'WARNING',     # DMP messages in browser console only show if DEBUG
            },
        },
    }

Is ``dmp-common.min.js`` really necessary?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Normally, yes. It supports DMP's providers (automatic JS/CSS links). The file is only 3K, but yeah, I get it. 3K here, 2K there, and pretty soon we have lots of K.

You CAN move it into your codebase or bundle, though. Just be sure you always match the version of this file with the version of DMP you're using. DMP will display a warning (in the browser console) if the version is mismatched between the server DMP and client DMP file.

To move it into your codebase:

1. Copy the file from DMP's source code to a web-accessible location in your codebase. You can find DMP's local directory with: ``python -c 'import django_mako_plus; print(django_mako_plus.__file__)'``
2. Open ``base.htm`` and adjust ``<script src="/django_mako_plus/dmp-common.min.js"></script>`` for the new location.
3. Be sure this script is loaded before the call to ``django_mako_plus.links()``.

If you don't need the auto-link-creation feature of DMP, you can entirely remove it. Just open ``base.htm`` and remove these lines:

.. code-block:: html

    <script src="/django_mako_plus/dmp-common.min.js"></script>
    ${ django_mako_plus.links(self) }


I updated DMP, but browsers report the old ``dmp-common.min.js``.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is a caching issue, and it can occur with any of your static files (.js, .css, .png, others). Once browsers download the file from your server, they don't check for new versions for a few days (or even weeks). Your server might have a new version of a file, but the browser doesn't know to get it!

A common solution is to add the server start time to all of your links. Since the server start time changes each time you update/bounce the server, the filename changes. Browsers see the new filename in your HTML and think it's an entirely new file being linked. This is called "busting the cache".

One way to implement this is to add the server time to your settings. In ``settings.py``, add the following:

.. code-block:: python

    import time
    SERVER_START = int(time.time() * 1000.0)

Then in your HTML files, add the server start time to your static file links:

.. code-block:: html

    <script src="/django_mako_plus/dmp-common.js?${ settings.SERVER_START }"></script>

The links created by DMP automatically bust the cache in a similar way by adding a CRC32 hash of file contents. That hash code changes whenever you make changes to the files.
