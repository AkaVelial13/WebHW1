from setuptools import setup, find_packages


setup(
      name='task-manager',
      version='1.0',
      py_modules= ['bot', 'models', 'contact_manager', 'event_manager', 'note_manager', 'file_sorter', 'base_view', 'common'],
      description='It`s a personal helper, witch can be use like the address book, notes manager, event manager and file sorter.',
      url='',
      author='Dreamcode team, Vitaliy Nerg, Omelchenko Anton, Artem Hrytsay, Serhii Nozhenko, Muzychyk Vadym',
      author_email='occultnerg2@gmail.com, omelchenko230783@gmail.com, artem_madrid@hotmail.com, neprokaren41@gmail.com',
      license='MIT',
      install_requires=[
            'tabulate==0.9.0',
            'colorama==0.4.6',
      ],
      entry_points='''
            [console_scripts]
            manager=bot:run
      ''',
      packages=find_packages(where='src'),
      package_dir= {'': 'src'}
)
