
from functools import cached_property
import json
from pathlib import Path
from string import Template
from typing import Dict

from pydantic import BaseModel, BaseConfig

from .config import webhook_dir, webhook_builtin_dir


class WebhookType(BaseModel):
    builtin: bool = True
    body: dict = {}
    help: str = ""

    @cached_property
    def template(self):
        return Template(json.dumps(self.body, ensure_ascii=False))

    def dumps_indent(self):
        return json.dumps(self.body, indent=4, ensure_ascii=False)
    
    def format(self, d: dict):
        return self.template.safe_substitute(d)

    class Config(BaseConfig):
        keep_untouched = BaseConfig.keep_untouched + (cached_property, )


_webhook_types: Dict[str, WebhookType] = {}


def init():
    _webhook_types.clear()

    def load_from(dir: Path, builtin: bool):
        for path in dir.glob("*.json"):
            _try_add_from_file(path, builtin)
    load_from(webhook_builtin_dir, True)
    load_from(webhook_dir, False)


def format(type: str, title: str, sub: str, torrent: str):
    return _webhook_types.get(type).format(dict(
        title=title,
        subscribe=sub,
        torrent=_get_magnet_hash(torrent)
    )).encode()

from urllib import parse

def _get_magnet_hash(url : str):
    _url = parse.urlparse(url)
    parad = parse.parse_qs(_url.query)
    return str(parad["hash"][0])
 

def get(type: str):
    return _webhook_types.get(type)


def _try_add_from_file(file: Path, builtin: bool):
    if file.exists():
        wt = _webhook_types[file.name.removesuffix(".json")] = WebhookType.parse_file(file)
        wt.builtin = builtin


def add(type: str, webhook: WebhookType):
    with (webhook_dir / f"{type}.json").open('w', encoding='utf-8') as w:
        json.dump(webhook.dict(), w, ensure_ascii=False, indent=4)
    _webhook_types[type] = webhook


def list():
    return _webhook_types.keys()


def remove(type: str):
    (webhook_dir / f"{type}.json").unlink(True)
    del _webhook_types[type]
    _try_add_from_file(webhook_builtin_dir / f"{type}.json", True)

init()