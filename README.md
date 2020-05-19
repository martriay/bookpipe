# bookpipe

HTTP endpoint to send ebooks to kindle

## Usage:
Send a `POST` request with `email` and `url` parameters. If the format is `epub` it will be converted to `mobi`. 
```bash
curl -i -X POST \
   -H "Content-Type:application/x-www-form-urlencoded" \
   -d "email=martriay@kindle.com" \
   -d "url=http://93.174.95.29/main/799000/ab3fe274eb3cb0bd1c5483540b7621cc/Richard%20Rumelt%20-%20Good%20Strategy%20Bad%20Strategy_%20The%20Difference%20and%20Why%20It%20Matters-Crown%20Business%20%282011%29.mobi" \
 'http://127.0.0.1:5000/'
 ```