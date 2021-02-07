# crawling-loker-indonesia
Crawling data lowongan pekerjaan dari [Jobstreet](https://www.jobstreet.co.id/) dan [Glints](https://glints.com/id)

## how to use
- Clone project
```
git clone https://github.com/yasirabd/crawling-loker-indonesia.git
```
- Install library
```
pip install -r requirements.txt
```
- Download webdriver untuk Selenium, pastikan sesuai version webdriver dan browser yang digunakan.
- Untuk crawling data lowongan kerja, masuk ke folder <code>lokerid</code>
```
cd lokerid
```
- Crawling data Jobstreet
```
scrapy crawl jobstreet -o jobstreet.csv
```
- Crawling data Glints
```
scrapy crawl glints -o glints.csv
```

Selamat mencoba! :penguin:
