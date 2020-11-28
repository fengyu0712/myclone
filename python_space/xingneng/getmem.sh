
    #!/bin/bash
while true
`    do
        free|awk '/Mem/{print  '"\"$(date +%Y-%m-%d" "%T)\""'","$2/$3}'
        sleep 5
    done
    