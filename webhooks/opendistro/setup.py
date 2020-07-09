from setuptools import setup, find_packages

version = '1.0.0'

setup(
    name="alerta-opendistro",
    version=version,
    description='Alerta Webhook for OpenDistro',
    url='https://github.com/alerta/alerta-contrib',
    license='MIT',
    author='Burak Köseoglu',
    author_email='burakksglu@gmail.com',
    packages=find_packages(),
    py_modules=['alerta_opendistro'],
    install_requires=[],
    include_package_data=True,
    zip_safe=True,
    entry_points={
        'alerta.webhooks': [
            'opendistro = alerta_opendistro:OpenDistroWebhook'
        ]
    }
)
