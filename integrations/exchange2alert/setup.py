
from setuptools import setup, find_packages

setup(
    name="alerta-imap",
    version='1.0.0',
    description="Alerta Imap daemon",
    license="MIT",
    author="Nick Satterly",
    author_email="nick.satterly@theguardian.com",
    url="http://github.com/burakksglu/alerta-contrib",
    py_modules=['imapcheck'],
    install_requires=[
        'alerta',
        'PyYaml'
    ],
    entry_points={
        'console_scripts': [
            'alerta-imap = imapcheck:main'
        ]
    },
    keywords="alerta imap daemon",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: System :: Monitoring',
    ]
)
