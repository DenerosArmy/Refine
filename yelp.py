import json
import oauth2
import optparse
import urllib
import urllib2


def locate_food(location="san francisco westfield mall", search_term="vegetarian"):
    consumer_key = "1Q5TbWVfwe5U3krF3eb9yw"
    consumer_secret = "CWCxOOjtX1zKStlu6p_BcY_7abo"
    token = "4gL5o2gxNnEFt5DgKkETDGEVPmocfKOJ"
    token_secret = "mDXZKcKOSNW7toDrsTyUyGUkGO4"

    url_params = {}
    url_params['location'] = location
    url_params['term'] = search_term

    
    
    response = request('api.yelp.com', '/v2/search', url_params, consumer_key, consumer_secret, token, token_secret)
    j = json.dumps(response, sort_keys=True, indent=2)
    a = json.loads(j)
    restaurants_list =[]
    restaurant = {}
    for i in range(1,5):
        restaurant["type"] = "restaurant_info"
        restaurant["name"] = a["businesses"][i][u'name']
        restaurant["address"] = a["businesses"][i][u'location'][u'address']
        restaurant["image"] = a["businesses"][i][u'image_url']
        restaurant["rating"] = a["businesses"][i][u'rating']
        restaurants_list.append(restaurant)                         
    return restaurants_list
  

def request(host, path, url_params, consumer_key, consumer_secret, token, token_secret):
  """Returns response for API request."""
  # Unsigned URL
  encoded_params = ''
  if url_params:
    encoded_params = urllib.urlencode(url_params)
  url = 'http://%s%s?%s' % (host, path, encoded_params)
  

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


