from ui.load_ui import Application
from PyQt5.QtWidgets import QApplication
from qasync import QEventLoop
import sys
import asyncio


async def main():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = Application()
    await window.show()
    with loop:
        loop.run_forever()

if __name__ == '__main__':
    asyncio.run(main())
