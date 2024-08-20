import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/home/recupe18/public_html/classificador.recuperasimples.com.br/Projeto/templates/NCM")

from app import app as application
