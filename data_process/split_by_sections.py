smallfile = None
with open('sample1_sections/science_parse_output.txt') as bigfile:
    for lineno, line in enumerate(bigfile):
        if re.search(r'\d+\.\d+', line) != None:
            if smallfile:
                smallfile.close()
            small_filename = 'sample1/small_file_{}.txt'.format(lineno + lines_per_file)
            smallfile = open(small_filename, "w")
        smallfile.write(line)
    if smallfile:
        smallfile.close()
