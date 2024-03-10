import asyncio
import pathlib
import shutil
import subprocess
from datetime import datetime
from urllib.request import urlretrieve

from modal import Image, Period, Stub, Volume, asgi_app

stub = Stub("gov-contracts")
datasette_image = (
    Image.debian_slim()
    .pip_install("datasette~=0.63.2", "sqlite-utils")
    .apt_install("unzip")
)

# ## Persistent dataset storage
volume = Volume.from_name(
    "gov-contracts-2", create_if_missing=True
)

VOLUME_DIR = "/cache-vol"
REPORTS_DIR = pathlib.Path(VOLUME_DIR, "gov-contracts")
DB_PATH = pathlib.Path(VOLUME_DIR, "gov-contracts.db")

def chunks(it, size):
    import itertools

    return iter(lambda: tuple(itertools.islice(it, size)), ())

@stub.function(
    image=datasette_image,
    volumes={VOLUME_DIR: volume},
    timeout=900,
)
def prep_db():
    import sqlite_utils

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite_utils.Database(DB_PATH)

    db.close()

    print("Syncing DB with volume.")
    volume.commit()

# ## Web endpoint
@stub.function(
    image=datasette_image,
    volumes={VOLUME_DIR: volume},
    allow_concurrent_inputs=16,
)
@asgi_app()
def app():
    from datasette.app import Datasette
    
    print(DB_PATH)
    ds = Datasette(files=[DB_PATH], settings={"sql_time_limit_ms": 10000})
    asyncio.run(ds.invoke_startup())
    return ds.app()

# ## Publishing to the web
@stub.local_entrypoint()
def run():
    print("Prepping SQLite DB...")
    prep_db.remote()


#### References
##### 1. https://github.com/modal-labs/modal-examples/blob/main/10_integrations/covid_datasette.py