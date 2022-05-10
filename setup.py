from setuptools import setup, find_packages

with open('LICENSE') as f:
    license = f.read()

setup(
    name='NftRarity',
    version='0.1.0',
    description='Nft metadata fetch and rarity analysis',
    long_description="Nft metadata fetch and rarity analysis",
    author='JJ',
    author_email='',
    url='https://github.com/jj-btc/NftRarity',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
