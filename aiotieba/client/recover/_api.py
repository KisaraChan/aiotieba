import sys

import yarl

from .._core import HttpCore
from .._helper import log_success, pack_web_form_request, parse_json, send_request
from ..const import WEB_BASE_HOST
from ..exception import TiebaServerError


def parse_body(body: bytes) -> None:
    res_json = parse_json(body)
    if code := res_json['no']:
        raise TiebaServerError(code, res_json['error'])


async def request(http_core: HttpCore, fname: str, fid: int, tid: int, pid: int, is_hide: bool) -> bool:
    data = [
        ('tbs', http_core.core._tbs),
        ('fn', fname),
        ('fid', fid),
        ('tid_list[]', tid),
        ('pid_list[]', pid),
        ('type_list[]', '1' if pid else '0'),
        ('is_frs_mask_list[]', int(is_hide)),
    ]

    request = pack_web_form_request(
        http_core,
        yarl.URL.build(scheme="https", host=WEB_BASE_HOST, path="/mo/q/bawurecoverthread"),
        data,
    )

    __log__ = f"fname={fname} tid={tid} pid={pid}"

    body = await send_request(request, http_core.connector, read_bufsize=1024)
    parse_body(body)

    log_success(sys._getframe(1), __log__)
    return True
