## Follow a concrete example

```text
Name tickets.example.invalid
DNS record → selected ALB/CloudFront destination
Certificate → covers the exact intended hostnames
HTTPS service → presents that certificate
Rails → validates allowed hosts/proxy context
```
Use an actual controlled training domain only when you choose to provision. example.invalid is a placeholder, not a working deployment target.