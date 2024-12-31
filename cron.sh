cd /root/vpn_bot
openssl req -newkey rsa:4096 \
            -x509 \
            -sha256 \
            -days 3650 \
            -nodes \
            -out ssl/fullchain1.pem \
            -keyout ssl/privkey1.pem \
            -subj "/C=SI/ST=Ljubljana/L=Ljubljana/O=Security/OU=IT Department/CN=companyia.site"