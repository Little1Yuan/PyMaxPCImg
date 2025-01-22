import requests
import json

URL = 'https://maxpcimg.cc/api/v1'

def get_headers(token=None):
	ret = {'Accept': 'application/json'}
	if token:
		ret['Authorization'] = 'Bearer %s'%token
	return ret

def get(path, token=None, **kwargs):
	return requests.get(URL + path, headers=get_headers(token), **kwargs)

def post(path, token=None, headers=None, **kwargs):
	return requests.post(URL + path, **kwargs, headers=get_headers(token) if headers is None else headers)

def delete(path, token=None, **kwargs):
	return requests.delete(URL + path, **kwargs, headers=get_headers(token))

def get_token(email:str, pwd:str):
	resp = post('/tokens', data={'email':email,'password':pwd}).json()
	if resp['status']:
		return resp['data']['token']
	print('服务端返回了错误: '%resp)
	return None

def del_token():
	resp = delete('/tokens').json()
	return resp['status']

def get_profile(token):
	resp = get('/profile', token).json()
	# print(resp)
	if resp['status']:
		return resp['data']
	print('服务端返回了错误: '%resp)
	return None

Boundary = '-IamNaHCO3_ThisIsMyCode_ILoveFalsw'
def upload(token, img_path, title='NaHCO3.jpeg', strategy_id=None):
	hs = get_headers(token)
	hs['Content-Type'] = 'multipart/form-data; boundary=' + Boundary
	dt = '--' + Boundary + '\nContent-Disposition: form-data; name="file"; filename="%s"\nContent-Type: image/jpeg\n\n'%title
	dt = dt.encode('utf-8')
	with open(img_path, 'rb') as f:
		dt += f.read() 
	if strategy_id:
		s = '\n--%s\nContent-Disposition: form-data; name="strategy_id"\n\n%d'%(Boundary, strategy_id)
		dt += s.encode('utf-8')
	dt += b'\n--%s--\n'%Boundary.encode('utf-8')
	resp = post('/upload', token, hs, data=dt).json()
	if resp['status']:
		return resp['data']
	print(resp)
	return None

if __name__ == '__main__':
	with open('test.cfg', 'r', encoding='utf-8') as f:
		cfg = json.loads(f.read())
		tk = get_token(cfg['email'], cfg['pwd'])
		rp = upload(tk, '2.jpeg', 'a_new_one.jpeg')
		print(rp)
