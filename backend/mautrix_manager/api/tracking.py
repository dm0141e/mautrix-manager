# mautrix-manager - A web interface for managing bridges
# Copyright (C) 2020 Tulir Asokan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from aiohttp import web
from yarl import URL

from ..config import Config
from .initable import initializer
from ..mixpanel import is_enabled, track

routes = web.RouteTableDef()


@routes.get("/track")
async def check_track(_: web.Request) -> web.Response:
    return web.json_response({
        "enabled": is_enabled(),
    })


@routes.post("/track")
async def do_track(request: web.Request) -> web.Response:
    data = await request.json()
    try:
        event = data["event"]
        props = data["properties"]
    except KeyError:
        return web.Response(status=400)
    if not isinstance(event, str) or not isinstance(props, dict):
        return web.Response(status=400)
    await track(event=event, user_id=request["token"].user_id,
                user_agent=request.headers["User-Agent"], **props)
    return web.Response(status=204)


@initializer
def init(cfg: Config, app: web.Application) -> None:
    global host, secret, config, client_id
    config = cfg
    secret = cfg["bridges.mx-puppet-slack.secret"]
    if secret:
        host = URL(cfg["bridges.mx-puppet-slack.url"])
        client_id = cfg["bridges.mx-puppet-slack.client_id"]
    app.add_routes(routes)
