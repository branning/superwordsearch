superwordsearch
===============
Searches a grid of letters for some words.  Reads defined input file, and writes a single line for each word.  If found, the start and end position of each word is writted to standard output.  If not, "NOT FOUND" is written.

    $ cat << EOF | python superwordsearch.py
    > 3 3
    > ABC
    > DEF
    > GHI
    > NO_WRAP
    > 5
    > FED
    > CAB
    > GAD
    > BID
    > HIGH
    > EOF
    (1,2) (1,0)
    NOT FOUND
    NOT FOUND
    NOT FOUND
    NOT FOUND

There is a minor effort made to do POSIX-ish argument parsing.

    $ python superwordsearch.py --help
    Super Word Search!
    usage: python superwordsearch.py <input file>
    options:
    	--test	test some examples
    	--help	print this message

And a few tests.

    $ python superwordsearch.py --test
    example1.txt, 3x3 grid, 5 words ... pass 0.003 s
    example2.txt, 4x3 grid, 5 words ... pass 0.004 s
    bad_input.txt, expected exception, ok
