from flask import Flask
import serial
import re
from collections import OrderedDict

app = Flask(__name__)


def count_s(s, string):
    regexp = r'(?=(' + string + '))'
    return len(re.findall(regexp, s))


def gen(s, k):
    i = 0
    ret = OrderedDict()
    for c in s:
        fi = i + k
        #print i, fi
        if fi <= (len(s) - k):
            if(count_s(s, s[i:fi]) >= 2):
                ret[s[i:fi]] = count_s(s, s[i:fi])
            i = i + 1
    return ret


def kmer(s):
    ret = gen(s, 5)
    if(len(ret) or len(ret) > 0):
        return 'green'
    else:
        return 'false'


@app.route('/<x>')
def hello(x):
    ser = serial.Serial('/dev/ttyACM0', 9600)
    var = kmer(x)

    if(var == 'green'):
        ret = ser.write('7')
    else:
        ret = ser.write('8')

    if(ret):
        return 'Exito %s' % x
    return 'NOO %s' % x

if __name__ == "__main__":
    app.run(host='0.0.0.0')
