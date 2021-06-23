#! /bin/tcsh

foreach i (`grep -vl 'bin/env' *.py`)
    echo "updating " $i
    mv $i $i.old
    gsed -e '1s@^@#! /usr/bin/env python3\n@' $i.old > $i
    chmod +x $i
end
