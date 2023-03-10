
import subprocess as sp
import os
import shutil
from remove_duplicates import remove_all_duplicates
# from extract_contract_ids import extract_ids

REPORT_NAMES = ['type1-report', 'type2-report', 'type2c-report', 'type3-1-report', 'type3-2-report', 'type3-2c-report']
folder_names = ['corpus_contracts-clones', 'corpus_contracts-blind-clones', 'corpus_contracts-consistent-clones']
file_names = []
file_names_with_source = []

for n in folder_names:
    file_names.append(n+'/'+n+'-0.00-classes.xml')
    file_names_with_source.append(n+'/'+n+'-0.00-classes-withsource.xml')
    file_names.append(n+'/'+n+'-0.30-classes.xml')
    file_names_with_source.append(n+'/'+n+'-0.30-classes-withsource.xml')
clone_types = ['type-1', 'type-3-1', 'type-2', 'type-3-2', 'type-2c', 'type-3-2c']

def run_nicad(config_name):
    for i, name in enumerate(REPORT_NAMES):
        nicad_cmd = './nicad6 contracts sol systems/corpus {}-{}'.format(name, config_name)
        sp.run(nicad_cmd.split(' '))
        print('{} done'.format(name))
    os.makedirs('systems/{}'.format(config_name), exist_ok=True)

    for i,(n_with_source, n, ctype) in enumerate(zip(file_names_with_source, file_names, clone_types)):
        os.makedirs('systems/{}/withoutsource'.format(config_name), exist_ok=True)
        os.makedirs('systems/{}/withsource'.format(config_name), exist_ok=True)
        shutil.move('systems/{}'.format(n), 'systems/{}/withoutsource/{}'.format(config_name, ctype+'.xml'))
        shutil.move('systems/{}'.format(n_with_source), 'systems/{}/withsource/{}'.format(config_name, ctype+'.xml'))


def take_diff(from_path, to_path):
    for type in clone_types:
        print('taking diff of {}'.format(type))
        cmd = 'diff {}/{} {}/{}'.format(from_path, type+'.xml', to_path, type+'.xml')

        sp.run(cmd.split(' '))   
 

if __name__=='__main__':
    config = 'macro'
    run_nicad(config)
    # create a data folder if it does not exists
    os.makedirs(f'python_scripts/data', exist_ok=True)

    # delete the config folder if it exists
    shutil.rmtree(f'python_scripts/data/{config}', ignore_errors=True)
    shutil.move(f'systems/{config}', f'python_scripts/data/{config}')
    
    # now we are in the manipulation domain
    os.chdir('python_scripts')
    print("REMOVING DUPLICATES")
    
    shutil.rmtree('duplicates', ignore_errors=True)
    remove_all_duplicates(config)

    print("EXTRACTING contract IDS")
    # extract_ids(config)
    # get_top_function_ids('duplicates')
    # take_diff('systems/baseline', 'systems/min5')
    print('done')





