import json
import oauth2
import optparse
import urllib
import urllib2


def yelp():
    consumer_key = "1Q5TbWVfwe5U3krF3eb9yw"
    consumer_secret = "CWCxOOjtX1zKStlu6p_BcY_7abo"
    token = "4gL5o2gxNnEFt5DgKkETDGEVPmocfKOJ"
    token_secret = "mDXZKcKOSNW7toDrsTyUyGUkGO4"

    url_params = {}
    url_params['location'] = "san francisco"

    response = request('api.yelp.com', '/v2/search', url_params, consumer_key, consumer_secret, token, token_secret)
    print json.dumps(response, sort_keys=True, indent=2)

    

def request(host, path, url_params, consumer_key, consumer_secret, token, token_secret):
  """Returns response for API request."""
  # Unsigned URL
  encoded_params = ''
  if url_params:
    encoded_params = urllib.urlencode(url_params)
  url = 'http://%s%s?%s' % (host, path, encoded_params)
  print 'URL: %s' % (url,)

  # Sign the URL
  consumer = oauth2.Consumer(consumer_key, consumer_secret)
  oauth_request = oauth2.Request('GET', url, {})
  oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                        'oauth_timestamp': oauth2.generate_timestamp(),
                        'oauth_token': token,
                        'oauth_consumer_key': consumer_key})

  token = oauth2.Token(token, token_secret)
  oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
  signed_url = oauth_request.to_url()
  print 'Signed URL: %s\n' % (signed_url,)

  # Connect
  try:
    conn = urllib2.urlopen(signed_url, None)
    try:
      response = json.loads(conn.read())
    finally:
      conn.close()
  except urllib2.HTTPError, error:
    response = json.loads(error.read())

  return response


