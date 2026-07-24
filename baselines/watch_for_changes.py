import asyncio
from watchfiles import awatch
from pathlib import Path

path2watch = Path("sample.txt")

# Create a sample file to transfer
with open(path2watch, "w") as fid:
    fid.write("Some changes")


async def main():
    print(f"Watching for changes in `{path2watch}`")
    async for changes in awatch(path2watch):
        print(changes)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped via KeyboardInterrupt")
        path2watch.unlink()
