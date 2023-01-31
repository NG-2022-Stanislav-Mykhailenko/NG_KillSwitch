# Project: Telegram PC kill switch bot
# Author: Stanislav Mykhailenko
# License: Unlicense

import ctypes, sys
from tg import startBot

def main() -> None:
	if ctypes.windll.shell32.IsUserAnAdmin():
		startBot()
	else:
		ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

if __name__ == '__main__':
	main()
