rsync -avz --exclude-from='.rsyncignore' \
-e "ssh -i acao.pem" \
./ ubuntu@44.205.5.63:~/rs