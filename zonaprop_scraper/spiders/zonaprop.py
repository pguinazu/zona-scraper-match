import scrapy

class ZonapropSpider(scrapy.Spider):
    name = "zonaprop"
    allowed_domains = ["zonaprop.com.ar"]
    # start_urls = ["https://www.zonaprop.com.ar/inmuebles-alquiler.html"]  # no funciona sin user agent
    def start_requests(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }
        
        print("📡 Usando start_requests con User-Agent")
        yield scrapy.Request(
            url="https://www.zonaprop.com.ar/inmuebles-alquiler.html",
            callback=self.parse,
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Cache-Control": "max-age=0",
            }
        )

    def parse(self, response):
        print("Entró a la función parse()")
        # Seleccionamos cada aviso de la página
        for ad in response.css('.postingsList-module__card-container'):
            # title = ad.css('.postingLocations-module__location-address postingLocations-module__location-address-in-listing::text').get()
            price = ad.css('[data-qa="POSTING_CARD_PRICE"]::text').get()
            location = ad.css('[data-qa="POSTING_CARD_LOCATION"]::text').get()
            details = ad.css('h3[data-qa="POSTING_CARD_DESCRIPTION"] a::text').get()
            url = ad.css('h3[data-qa="POSTING_CARD_DESCRIPTION"] a::attr(href)').get()

            if url:
                full_url = response.urljoin(url)

                # Vamos al aviso individual a buscar requisitos
                yield response.follow(
                    full_url,
                    callback=self.parse_aviso,
                    meta={
                        "price": price,
                        "location": location,
                        "details": details,
                        "url": full_url
                    },
                    headers={
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Connection": "keep-alive",
                        "Upgrade-Insecure-Requests": "1",
                        "Sec-Fetch-Dest": "document",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-Site": "none",
                        "Sec-Fetch-User": "?1",
                        "Cache-Control": "max-age=0",
                    }
                )
                
    def parse_aviso(self, response):
        print("🔍 Entró a parse_aviso para:", response.url)

        texto_completo = " ".join(response.css("*::text").getall()).lower()

        if "garantía propietaria" in texto_completo:
            requisito = "Garantía propietaria"
        elif "seguro de caución" in texto_completo:
            requisito = "Seguro de caución"
        elif "recibo de sueldo" in texto_completo:
            requisito = "Recibo de sueldo"
        elif "garante" in texto_completo:
            requisito = "Garante (otro tipo)"
        else:
            requisito = "No especificado"

        yield {
            "price": response.meta["price"],
            "location": response.meta["location"],
            "details": response.meta["details"],
            "url": response.meta["url"],
            "requisitos": requisito
        }
