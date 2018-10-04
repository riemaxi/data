#!/usr/bin/env python3

from align_pipeprocess import *
from surrogate import *
import os

os.system('mkdir -p log')
Surrogate( PipeProcess() ).start()
