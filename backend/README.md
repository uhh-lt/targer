Web backend for BiLSTM-CNN-CRF Implementation for Sequence Tagging
based on Python, Flask and Restful API.

dependencies:
- ...

Run behind reverse proxy:
The current code is default set to run at port 6000 behind a reverseproxy like nginx or apache2 on in a subdirectory /arg-mining. You need to add this to your webserver configuration:
nginx:

    location /arg-mining/ {
        proxy_pass http://localhost:6000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Script-Name /arg-mining;
    }

apache2:

    <Location /arg-mining>
        Header add X-Script-Name "/arg-mining"
        RequestHeader set X-Script-Name "/arg-mining"

        ProxyPass http://localhost:6000
        ProxyPassReverse http://localhost:6000
    </Location>


Installation:
You can use a virtualenv for the installation. Download and set up the model from [0]. Add the backend.py into the main directory of the BiLSTM-CNN-CRF Implementation for Sequence Tagging.

Usage:
    python3 backend.py

The webserver will now listen at http://localhost:6000 for incoming request.
The Swagger interface must be accessed at http://localhost:6000/apidocs/ or http://localhost(:80)/arg-ming/apidocs/.


[0] https://github.com/uhh-lt/rnn2argument-web/tree/master/model
