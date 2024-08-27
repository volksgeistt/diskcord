from colorama import Fore, Style, init

init(autoreset=True)

class Colors:
    @staticmethod
    def banner(txt: str) -> None:
        print(f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}{txt}")

    @staticmethod
    def error(txt: str) -> None:
        print(f"{Fore.RED}[!] {txt}")

    @staticmethod
    def success(txt: str) -> None:
        print(f"{Fore.GREEN}[+] {txt}")

    @staticmethod
    def warning(txt: str) -> None:
        print(f"{Fore.YELLOW}[!] {txt}")
