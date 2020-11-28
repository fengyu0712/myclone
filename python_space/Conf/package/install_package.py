import os
path=os.path.split(os.path.realpath(__file__))[0]
package_path=path+'/package.txt'

shell= 'pip install -r %s'%package_path
os.system(shell)
print('finish')