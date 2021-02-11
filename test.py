import os.path

print('[dirname]')
dirname = os.getcwd()
ca_path = os.path.join(dirname, 'opt\\mysql\\ssl\\ca.pem')

print('ca_path: ', ca_path)

print('read target file:')
with open(ca_path) as f:
    print(f.read())
