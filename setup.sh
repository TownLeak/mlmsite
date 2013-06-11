#! /bin/bash
export APP_ROOT=/Users/molnarzs/Dropbox/Projects/MLM/site/DiamondMLM/mlmsite

export NEO4J_SERVER_DIR=/Users/molnarzs/Dropbox/Projects/MLM/site/neo4j-server
export PATH=${APP_ROOT}/bin:${PATH}
alias NEO4J_SERVER=${NEO4J_SERVER_DIR}/bin/neo4j

# Tests
alias exec_test="NEO4J_SERVER restart; python -Wall manage.py test mlmsite"
