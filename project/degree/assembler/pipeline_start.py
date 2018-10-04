#!/usr/bin/env python3

from pipeprocess import *
from surrogate import *
from parameter import *
import os

os.system('mkdir -p log')
os.system('mkdir -p {}'.format(p.report_folder))

Surrogate( PipeProcess() ).start()
