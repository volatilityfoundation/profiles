import os, sys, re, zipfile

def exec_vtypes(filename):
    env = {}
    exec(filename, dict(__builtins__ = None), env)
    return env["mac_types"]

def parse_dsymutil(data, wanted_symbol):
    """Parse the symbol file."""
    
    ret = 0

    # get the system map
    for line in data.splitlines():
        ents = line.split()

        match = re.search("\[.*?\(([^\)]+)\)\s+[0-9A-Fa-z]+\s+\d+\s+([0-9A-Fa-f]+)\s'(\w+)'", line)

        if match:
            (sym_type, addr, name) = match.groups()
            sym_type = sym_type.strip()
    
            addr = int(addr, 16)

            if addr == 0 or name == "":
                continue

            if name == wanted_symbol:
                ret = addr
                break

    return ret

def main():
    path = sys.argv[1]

    lenargs = len(sys.argv)

    if lenargs == 3:
        sym = sys.argv[2]
    else:
        structname = sys.argv[2]
        member     = sys.argv[3]

    for path, _, files in os.walk(path):
        for fn in files:
            full_path = os.path.join(path, fn)
            if zipfile.is_zipfile(full_path):
                #print "checking %s" % full_path

                profpkg = zipfile.ZipFile(full_path)
                
                for f in profpkg.filelist:
                    if lenargs == 3 and 'symbol.dsymutil' in f.filename.lower():
                        ret = parse_dsymutil(profpkg.read(f.filename), sym)
               
                        if ret == 0:
                            print "NOT FOUND: %s" % full_path

                        #print "%s -> %x" % (sym, ret)

                        break

                    elif lenargs == 4 and f.filename.endswith(".vtypes"):
                        v = exec_vtypes(profpkg.read(f.filename))                       
                        
                        if structname in v:
                            member_info = v[structname][1]

                            if member in member_info:
                                info = member_info[member]
                                print "found: %s | %s" % (full_path, info)
                            else:
                                print "member %s not found!" % full_path
                        else:
                            print "struct %s not found in %s!" % (structname, full_path)
            
                        break

if __name__ == "__main__":
    main()
