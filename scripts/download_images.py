import aiohttp
import asyncio

from optparse import OptionParser

image_path = "https://d3304ij6n73kfg.cloudfront.net/prod/thumb/journal_main/{}/500_250"

parallel = 10
parallel_start = 0
parallel_end = parallel_start + parallel


async def downloader(target_url, dist_path):
    """
    Download target url and save it to dist path.
    :param target_url:
    :param dist_path:
    :return:
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(target_url) as response:
            image = await response.read()
            with open(dist_path, "wb") as f:
                f.write(image)


async def worker(thread_hold, position, count, target_path):
    chunk = int(count / parallel)
    start = position + (thread_hold * chunk)
    end = start + chunk
    print("thread_hold: {}, start: {}, end: {}".format(thread_hold, start, end))
    for i in range(start, end):
        await downloader(image_path.format(i), target_path.format(i))


def main():
    """
    $ python scripts/download_images.py --dest-path .temp --position=1 --count=1000
    """
    # command line parameter
    usage = "usage: %prog --dest-path .temp --position=1 --count=1000"
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--dest-path", action="store", type="string",
                      dest="dest_path", help="save destination path")
    parser.add_option("-p", "--position", action="store", type="int",
                      dest="position", help="start download position")
    parser.add_option("-c", "--count", action="store", type="int",
                      dest="count", help="download count")
    option, args = parser.parse_args()
    print("dest path: {}".format(option.dest_path))
    print("position: {}".format(option.position))
    print("count: {}".format(option.count))

    if option.count % parallel == 0:
        print("OK")
    else:
        raise Exception("Invalid count: {}".format(option.count))

    # loop event
    loop = asyncio.get_event_loop()

    # Download
    target_path = option.dest_path + "/sample_{:0=10}.png"
    loop.run_until_complete(asyncio.wait([
        worker(num, option.position, option.count, target_path) for num in range(parallel_start, parallel_end)
    ]))
    loop.close()


if __name__ == "__main__":
    main()
