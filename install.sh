#!/usr/bin/env bash
cd jena-arq && xargs -n 1 curl -O < libs.txt && cd ..
