#!/usr/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir="/home/mark/OneDrive/Uni/7.Sem/Bach/Simulation/gr-nr_sync/python"
export GR_CONF_CONTROLPORT_ON=False
export PATH="/home/mark/OneDrive/Uni/7.Sem/Bach/Simulation/gr-nr_sync/build/python":"$PATH"
export LD_LIBRARY_PATH="":$LD_LIBRARY_PATH
export PYTHONPATH=/home/mark/OneDrive/Uni/7.Sem/Bach/Simulation/gr-nr_sync/build/swig:$PYTHONPATH
/usr/bin/python3 /home/mark/OneDrive/Uni/7.Sem/Bach/Simulation/gr-nr_sync/python/qa_generate_rgrid_c.py 
