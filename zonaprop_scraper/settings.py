BOT_NAME = 'zonaprop_scraper'
SPIDER_MODULES = ['zonaprop_scraper.spiders']
NEWSPIDER_MODULE = 'zonaprop_scraper.spiders'
FEED_EXPORT_ENCODING = 'utf-8'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'

# Proxy settings
HTTPPROXY_ENABLED = True
DOWNLOADER_MIDDLEWARES = {
    'scrapy_cloudflare_middleware.CloudflareMiddleware': 560,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# Retry settings
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [403, 429]

# Rate limiting
DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS = 1