from optparse import OptionParser

import urllib.error
import urllib.request

image_path = "https://d3304ij6n73kfg.cloudfront.net/prod/thumb/journal_main/{}/500_250"


def downloader(target_url, dist_path):
    """
    Download target url and save it to dist path.
    :param target_url:
    :param dist_path:
    :return:
    """
    try:
        with urllib.request.urlopen(target_url) as r:
            image = r.read()
            with open(dist_path, "wb") as f:
                f.write(image)
    except Exception as e:
        print(e)
    return


def main():
    """
    $ python scripts/download_images.py --dest-path .temp --count=1000
    """
    # command line parameter
    usage = "usage: %prog --dest-path .temp --count=1000"
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--dest-path", action="store", type="string",
                      dest="dest_path", help="save destination path")
    parser.add_option("-s", "--start", action="store", type="int",
                      dest="start", help="start download position")
    parser.add_option("-e", "--end", action="store", type="int",
                      dest="end", help="end download position")
    option, args = parser.parse_args()
    print("dest path: {}".format(option.dest_path))
    print("start: {}".format(option.start))
    print("end: {}".format(option.end))

    # Download
    target_path = option.dest_path + "/sample_{:0=10}.png"
    for i in range(option.start, option.end):
        downloader(image_path.format(i), target_path.format(i))

    # TODO DLを並列で回す(async awaitを使ってやってみるのが良き）


if __name__ == "__main__":
    main()
