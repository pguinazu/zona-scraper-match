import subprocess

if __name__ == "__main__":
    subprocess.run(["scrapy", "crawl", "zonaprop", "-o", "/home/data/output.json"])