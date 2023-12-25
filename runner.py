from mainpix import crawl
df = crawl(nMonths = 1, phrase = 'income', section = ['Arts', 'World'], Types = ['Article', 'Audio'])
df.run()