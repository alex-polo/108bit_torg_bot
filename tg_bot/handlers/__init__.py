from typing import Optional

from aiogram import Dispatcher

disp: Dispatcher = Optional[None]


def set_dispatcher(dp: Dispatcher) -> None:
    global disp

    disp = dp
