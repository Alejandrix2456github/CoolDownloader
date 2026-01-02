import argparse
from utils.downloader import download_file

def cli_progress(percent):
    done = int(50 * percent)
    print(f"\r[{'█' * done}{'.' * (50-done)}] {percent*100:.1f}%", end="")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", required=True)
    parser.add_argument("-o", "--output", required=True)
    args = parser.parse_args()

    print(f"--- CoolDownloader CLI ---\nTarget: {args.url}")
    if download_file(args.url, args.output, cli_progress):
        print("\n[SUCCESS] Saved to", args.output)
    else:
        print("\n[ERROR] Download failed.")

if __name__ == "__main__":
    main()