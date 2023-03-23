import logging
import requests
import json
import os
import inspect
import docker

CA_CERT = './ca.pem'

CLIENT_CERT = './cert.pem'
CLIENT_KEY = './key.pem'

URL = 'https://demeterdev:2376/v1.24/containers/2b6465a1d424/top'

#tls_config = docker.tls.TLSConfig(ca_cert='./ca.pem', client_cert=('./cert.pem', './key.pem'))
#client = docker.DockerClient(base_url='https://demeterdev:2376', tls=tls_config)

tls_config = docker.tls.TLSConfig(
  client_cert=(CLIENT_CERT, CLIENT_KEY),
  verify= CA_CERT
)
#client = docker.Client(base_url='<https_url>', tls=tls_config)

class ResourceManagement:
  def __init__(self):
    pass