import sys
import asyncio
import os
from stat import S_ISDIR, S_ISREG
from colorama import Fore, Style, Back, init
from typing import Self
import argparse

init(autoreset=True)

class Snapshot:
    name: str
    last_modified: float

    def __init__(self, name: str, last_modified: float):
        self.last_modified = last_modified
        self.name = name

    def dumps(self) -> any:
        pass

class FileSnapshot(Snapshot):
    def __init__(self, name: str, last_modified: float, ext: str):
        super().__init__(name, last_modified)
        self.ext = ext

    def dumps(self) -> any:
        return {
            'last_modified': self.last_modified,
            'ext': self.ext
        }

class DirSnapshot(Snapshot):
    def __init__(self, name: str, last_modified: float, dir: dict[str, Snapshot]):
        super().__init__(name, last_modified)
        self.dir = dir

    def _watch(path: str = '.', ext: list[str] = ['py']) -> Snapshot:
        try:
            stat = os.stat(path)
        except:
            return None
        name = os.path.basename(path)
        if S_ISDIR(stat.st_mode):
            dir = {}
            for file in os.listdir(path):
                snapshot = DirSnapshot._watch(os.path.join(path, file), ext)
                if snapshot is not None:
                    dir[snapshot.name] = snapshot
            return DirSnapshot(name, stat.st_mtime, dir)
        else:
            _, file_extension = os.path.splitext(path)
            if file_extension[1:] in ext:
                return FileSnapshot(name, stat.st_mtime, file_extension)
            return None
        
    def watch(path: str = '.', ext: list[str] = ['py']) -> Self:
        assert(os.path.isdir(path))
        return DirSnapshot._watch(path, ext)
    
    def get_last_modified_files(self) -> float:
        last_modified = 0
        for key, value in self.dir.items():
            if isinstance(value, FileSnapshot):
                last_modified = max(last_modified, value.last_modified)
            elif isinstance(value, DirSnapshot):
                last_modified = max(last_modified, value.get_last_modified_files())
        return last_modified

    def dumps(self) -> any:
        dump = {}
        for key, value in self.dir.items():
            dump[key] = value.dumps()
        return dump

class FilesChangedException(Exception):
    pass

async def watch(path: str, ext: list[str]):
    old_snapshot = None
    while True:
        snapshot = DirSnapshot.watch(path, ext)
        if old_snapshot is not None and snapshot.get_last_modified_files() > old_snapshot.get_last_modified_files():
            raise FilesChangedException()

        old_snapshot = snapshot
        try:
            await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            break

async def main():
    parser = argparse.ArgumentParser(
        prog="pierex",
        description="PieReX is a python script that watches your files and restarts your program when a file changes")
    
    parser.add_argument("file", help="The python file to run")
    parser.add_argument("-e", "--ext", help="The file extensions to watch", default="py")
    parser.add_argument("-d", "--dir", help="The directory to watch", default=".")

    args = parser.parse_args()

    print(f"{Fore.GREEN}PyReX \U0001F996 is watching your files")
    print(f"{Fore.YELLOW}Press \033[4mCTRL + C{Style.RESET_ALL}{Fore.YELLOW} do break from the loop{Style.RESET_ALL}")

    async def create_process():
        return await asyncio.create_subprocess_exec(sys.executable, args.file)

    process = await create_process()
    while True:
        try:
            done, pending = await asyncio.wait([
                asyncio.create_task(process.wait()),
                asyncio.create_task(watch(args.dir, args.ext.split(',')))
            ], return_when=asyncio.FIRST_COMPLETED)
            result = done.pop().result()
            if result == 0:
                print(f"{Fore.GREEN}Program finished with exit code = {done.pop().result()}{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Error detected, waiting for file change{Style.RESET_ALL}")
                await watch()
        except FilesChangedException:
            try:
                process.kill()
            except:
                pass
            print(f"{Fore.YELLOW}Detected file changes, restarting ...{Style.RESET_ALL}")
            process = await create_process()
        except asyncio.CancelledError:
            await process.wait()
            print(f"{Fore.RED}Program stopped by user{Style.RESET_ALL}")
            break
        except Exception as e:
            process.kill()
            print(f"Error: {e}")
            break


if __name__ == '__main__':
    asyncio.run(main())