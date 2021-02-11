import os.path

dirname = os.getcwd()
print('dirname: ', dirname)

if os.name == 'nt':
    print("on windows")
    ca_path = os.path.join(dirname, 'opt\\mysql\\ssl\\ca.pem')
elif os.name == 'posix':
    print("on mac or linux")
    ca_path = os.path.join(dirname, 'opt/mysql/ssl/ca.pem')

print('ca_path: ', ca_path)

print('read target file:')
with open(ca_path) as f:
    print(f.read())
