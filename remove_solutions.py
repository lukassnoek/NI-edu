from glob import glob
"""
files = sorted(glob('intropy/_build/html/solutions/week_1/*.html'))
for f in files:

    print("Removing solutions from %s ..." % f)
    
    with open(f, 'r') as f_in:
        lines = f_in.readlines()

    new = []
    skip = False
    for line in lines:

        if '### BEGIN SOLUTION' in line or '### BEGIN HIDDEN TESTS' in line:
            skip = True
        
        if not skip:
            new.append(line)

        if '### END SOLUTION' in line or '### END HIDDEN TESTS' in line:
            skip = False
            if '### END SOLUTION' in line:
                new.append('<span class="c1"># YOUR SOLUTION HERE</span>')
            else:
                new.append('<span class="c1"># HIDDEN TESTS HERE</span>')

    with open(f, 'w') as f_out:
        for line in new:
            f_out.write(line)
"""