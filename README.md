# CrunchBase API

A full-featured API library to allow downloading and presenting organization and people data from Crunchbase.

## How to install?

To install it onlline

```bash
pip install git+https://github.com/cskksdfklpz/cbapi.git
```

or you can install it locally

```bash
cd /path/to/cbapi
python setup.py install
```

## How to use?

You can access the following three functions in cbapi, namely

```python
import cbapi
# setup your RAPIDAPI_KEY you've got from ODM endpoints
cbapi.set_rapidapi_key('YOUR_RAPIDAPI_KEY')
# get people information, supporting
'''
name
    STRING
    OPTIONAL
    A full-text query of name only

locations
    STRING
    OPTIONAL
    Filter by location names (comma separated, AND'd together) e.g. locations=California,San Francisco

socials
    STRING
    OPTIONAL
    Filter by social media identity (comma separated, AND'd together) e.g. socials=ronconway

types
    STRING
    OPTIONAL
    Filter by type (currently, either this is empty, or is simply "investor")

updated_since
    NUMBER
    OPTIONAL
    When provided, restricts the result set to Organizations where updated_at >= the passed value

verbose
    BOOL
    OPTIONAL
    Run in the verbose mode

parallel
    BOOL
    OPTIONAL
    Use multiprocessing to speed-up the multi-pages reading
'''
df_ppl = cbapi.get_people(name='Steve',types='investor', parallel=True)
# get organizations information, supporting
'''
updated_since
    NUMBER
    OPTIONAL
    When provided, restricts the result set to Organizations where updated_at >= the passed value

name
    STRING
    OPTIONAL
    Full text search limited to name and aliases

domain_name
    STRING
    OPTIONAL
    Text search of an Organization's domain_name (e.g. www.google.com)

locations
    STRING
    OPTIONAL
    Filter by location names (comma separated, AND'd together) e.g. locations=California,San Francisco

organization_types
    STRING
    OPTIONAL
    Filter by one or more types. Multiple types are separated by commas. Available types are "company", "investor", "school", and "group". Multiple organization_types are logically AND'd.

verbose
    BOOL
    OPTIONAL
    Run in the verbose mode

parallel
    BOOL
    OPTIONAL
    Use multiprocessing to speed-up the multi-pages reading
'''
df_org = cbapi.get_organizations(name='Data', parallel=True)
```

## Speed up using multiprocessing

We can speed up the reading when multiple cores are avaliable.

```python

import cbapi
import psutil

psustill.cpu_count(logical=False)
# output: 2, we use 2 physical cpu here

df_ppl = cbapi.get_people(name='Steve', types='investor', parallel=False)
# Last executed at 2020-08-29 17:45:52 in 41.27s
df_ppl = cbapi.get_people(name='Steve', types='investor', parallel=True)
# Last executed at 2020-08-29 17:45:10 in 20.95s

```

## Unit-test

We can use `pytest` to test our package before launching it.

```bash
> pytest test.py
============================ test session starts =============================
platform darwin -- Python 3.7.3, pytest-6.0.1, py-1.9.0, pluggy-0.13.1
rootdir: /Users/bbb/Desktop/cbapi
collected 1 item

test.py .                                                              [100%]

======================== 1 passed in 66.24s (0:01:06) ========================
```