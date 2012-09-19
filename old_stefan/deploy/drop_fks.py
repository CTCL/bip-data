schema_fname  = '/home/gaertner/bip-data/schema/bip_model.sql'
sql = '\n'.join([' '.join(l.strip().split(" ")[:6]).replace('ADD', 'DROP')
    + ';' for l in open(schema_fname).readlines() if "FOREIGN KEY" in l])
print sql
