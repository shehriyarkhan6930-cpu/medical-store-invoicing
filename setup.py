from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='medical-store-invoicing',
    version='1.0.0',
    description='Medical Store Invoicing System - Offline desktop application',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Medical Store Solutions',
    author_email='info@medicalstore.com',
    url='https://github.com/shehriyarkhan6930-cpu/medical-store-invoicing',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        'Flask==2.3.2',
        'Flask-SQLAlchemy==3.0.5',
        'Flask-Login==0.6.2',
        'Flask-WTF==1.1.1',
        'Werkzeug==2.3.6',
        'SQLAlchemy==2.0.19',
        'bcrypt==4.0.1',
        'python-dotenv==1.0.0',
        'reportlab==4.0.4',
        'PyPDF2==3.0.1',
        'pillow==10.0.0',
        'openpyxl==3.1.2',
        'pandas==2.0.3',
        'PyInstaller==6.1.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Healthcare Industry',
        'Topic :: Office/Business :: News/Diary',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    entry_points={
        'console_scripts': [
            'medical-store=app.main:main',
        ],
    },
)
