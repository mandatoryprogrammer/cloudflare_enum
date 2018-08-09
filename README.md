# Cloudflare Enumeration Tool v1.2

A simple tool to allow easy querying of Cloudflare's DNS data written in Python.

```
./cloudflare_enum.py -e test@gmail.com -p testing -d test.com -o /tmp/cf.csv
```

If you want to run using Docker,

```
docker run -it abhartiya/tools_cfenum -e test@gmail.com -p testing -d test.com -o /tmp/cf.csv
docker ps -a
docker cp <cont-id>:/tmp/cf.csv .
```

## Requirements if running without Docker

* pip install requests
* pip install bs4

## Notes

Make sure you don't have a `&` in the password of your Cloudflare account.
