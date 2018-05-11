import os, sys, re, zipfile, hashlib

def get_hash(profpkg, f, skip_first=False):
    data = profpkg.read(f.filename)
    data = data.split("\n")
    if skip_first:
        data = data[5:]

    return hashlib.md5("".join(data)).hexdigest()
                   
def main():
    path = "."

    pairs = {}

    for path, _, files in os.walk(path):
        for fn in files:
            full_path = os.path.join(path, fn)
            if zipfile.is_zipfile(full_path):
                profpkg = zipfile.ZipFile(full_path)
                
                syms = ""
                vtypes = ""

                for f in profpkg.filelist:
                    if 'symbol.dsymutil' in f.filename.lower():
                        syms = get_hash(profpkg, f, skip_first=True)

                    elif f.filename.endswith(".vtypes"):
                        vtypes = get_hash(profpkg, f)                      
                        
                        
                if syms == "" or vtypes == "":
                    print "BROKE ON %s" % full_path
                    exit()

                key = "%s|%s" % (syms, vtypes)

                if not key in pairs:
                    pairs[key] = []

                pairs[key].append(full_path)


    for paths in pairs.values():
        if len(paths) > 1:
            print paths










if __name__ == "__main__":
    main()
