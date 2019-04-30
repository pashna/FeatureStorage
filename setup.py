from setuptools import setup, find_packages

with open('requirements.txt') as fp:
    install_requires = fp.read()
print(find_packages())
setup(name='feature_storage',
      version='0.0.1',
      description='Feature Storage',
      author='Pavel Kochetkov',
      author_email='pavel.kochetkov@careem.com',
      packages=find_packages(),
      install_requires=install_requires,
      zip_safe=False)
