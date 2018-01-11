from typing import Callable

WsgiApp = Callable[[dict, Callable[[str, list], None]], str]
