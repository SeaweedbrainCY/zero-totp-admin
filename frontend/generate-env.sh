#! /bin/bash
echo "export const environment = {production: true,imageHash : \"$1\"};" > src/environments/environment.prod.ts