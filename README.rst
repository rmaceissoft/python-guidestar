================
python-guidestar
================

Overview
========

Python client library for `Guidestart API`_.

Installation
===================

* direct from repository::

    pip install git+git://github.com/rmaceissoft/python-guidestar.git


Usage
=====

Search organizations by ein code::

    from guidestar.api import Api

    client = Api(username="foobar@gmail.com", password="123")
    organizations = client.search(ein="54-1774039")


Get Details for a given organization::

    from guidestart.api import Api
    client = Api(username="foobar@gmail.com", password="123")
    organization = client.get_details(7831216)
    print organization.organization_name
    print organization.ein


Issues
======

Please use the `Github issue tracker`_ for any bug reports or feature
requests.

.. _`Guidestart API`: https://data.guidestar.org
.. _`Github issue tracker`: https://github.com/rmaceissoft/python-guidestar/issues