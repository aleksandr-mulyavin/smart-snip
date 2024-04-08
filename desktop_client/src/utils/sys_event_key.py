from typing import Callable, Optional

from PyQt5.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher

from pyqtkeybind import keybinder as kb


class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, key_binder):
        self.key_binder = key_binder
        super().__init__()

    def nativeEventFilter(self, event_type, message):
        ret = self.key_binder.handler(event_type, message)
        return ret, 0


class EventDispatcher:
    def __init__(self, key_binder) -> None:
        self.win_event_filter = WinEventFilter(key_binder)
        self.event_dispatcher: QAbstractEventDispatcher = (
            QAbstractEventDispatcher.instance())
        self.event_dispatcher.installNativeEventFilter(self.win_event_filter)


class QtKeyBinder:
    def __init__(self, win_id: Optional[int]) -> None:
        self.key_binder = kb
        self.key_binder.init()
        self.win_id = win_id

        self.event_dispatcher = EventDispatcher(key_binder=self.key_binder)

    def register_hotkey(self, hotkey: str, callback: Callable) -> None:
        self.key_binder.register_hotkey(self.win_id, hotkey, callback)

    def unregister_hotkey(self, hotkey: str) -> None:
        self.key_binder.unregister_hotkey(self.win_id, hotkey)
