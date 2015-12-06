# encoding: cinje

# Possible optimization, but not on Python 3!
# : from webext import to_str as _bless, escape_html as _escape

: table = [dict(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9, j=10) for x in range(1000)]

: def bigtable table=table

<table>
    : for row in table
    <tr>
        : for key, value in sorted(row.items())
        <td>${ key }</td><td>#{ value }</td>
        : end
    </tr>
    : end
</table>

:end


: def bigtable_unsafe table=table
: _escape = _bless = str

<table>
    : for row in table
    <tr>
        : for key, value in sorted(row.items())
        <td>${ key }</td><td>#{ value }</td>
        : end
    </tr>
    : end
</table>

:end


: def bigtable_stream table=table, frequency=100

<table>
    : for i, row in enumerate(table)
    <tr>
        : for key, value in sorted(row.items())
        <td>${ key }</td><td>#{ value }</td>
        : end
        : if not (i % frequency)
            : flush
        : end
    </tr>
    : end
</table>

: end


: def bigtable_fancy table=table, frequency=100

<table>
    : for first, last, i, total, row in iterate(table)
    <tr>
        : for key, value in sorted(row.items())
        <td>${ key }</td><td>#{ value }</td>
        : end
        : if not (i % frequency)
            : flush
        : end
    </tr>
    : end
</table>

: end