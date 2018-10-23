
import os
import sys
import numpy as np
from pdb import set_trace as tr
import time

outdir = '/home/jbq/repositories/notebooks/development/BASISPowderDiffraction/searchWaterBragg/searchBragg'

def applyPowder(ipts_list):
    from mantid.simpleapi import BASISPowderDiffraction, SaveAscii, DeleteWorkspace
    minimal_size = int(10e6)  # 10MB
    for ipt in ipts_list:
        print('ipts =', ipt)
        for root, dirs, files in os.walk('/SNS/BSS/IPTS-{}/0'.format(ipt)):
            print('nfiles =', len(files))
            time.sleep(3)
            for file in files:
                if file.endswith('event.nxs'):
                    full_path = os.path.join(root, file)
                    if os.stat(full_path).st_size > minimal_size:
                        print(full_path)
                        run_number = full_path.split('BSS_')[1].split('_event')[0]
                        print(run_number)
                        out_name = 'ipts_{}_run_{}'.format(ipt, run_number)
                        out_name = os.path.join(outdir, out_name)
                        title = 'IPTS {} RUN {}'.format(ipt, run_number)
                        print(out_name)
                        print(title)
                        try:
                            BASISPowderDiffraction(RunNumbers=run_number,
                                                   MomentumTransferBins=[0.1,0.0025,3.0],
                                                   OutputWorkspace='w',
                                                   MonitorNormalization=0)
                            SaveAscii(InputWorkspace='w_angle', Filename=out_name + '_angle.dat', WriteSpectrumID=False, Separator='Space', ColumnHeader=False)
                            DeleteWorkspace(Workspace='w_angle')
                        except:
                            pass
                        finally:
                            print('\n\n\n**********************************')
                            print('\n   {}   '.format(title))
                            print('\n**********************************\n\n')
                            time.sleep(2)

def all_ratios(min_intensity=0.0, discard_IPTS=None, outfile='searchBragg_r.dat'):
    """
    Calculate for each pattern the max to average ratio.
    Save to file run numeber, ratio, and location of the maximum 
    """
    if discard_IPTS is None:
        discard_IPTS = list()
    all = list()
    wrong_files = list()
    for f in os.listdir(outdir):
        ipts = f.split('ipts_')[1].split('_run')[0]
        if ipts in discard_IPTS:
            continue
        run = f.split('run_')[1].split('_angle')[0]
        y = np.loadtxt(os.path.join(outdir,f), usecols=(0,1))
        if np.mean(y[::,1]) == 0:
            wrong_files.append(f)
        else:
            r = np.max(y[::,1]) / np.mean(y[::,1])
            a = y[np.argmax(y[::,1])][0]  # angle where the maximum is located
            intensity = np.sum(y[::,1])
            if intensity > min_intensity:
                all.append('{} {} {} {} {}'.format(ipts, run, r, a, intensity))
        header = '# IPTS  RUN   ratio  angle_at_max intensity\n'
    open(outfile, 'w').write(header + '\n'.join(all) + '\n')
    open('wrong_files.txt', 'w').write('\n'.join(wrong_files) + '\n')

if __name__ == '__main__':

    #ipts = '21266 20776 20668 20354 19386 18958 18915 18634 18156 17894 17806 17726 17699 17379 17137 16550 16287 15975 15729 15370 15336 14995 14599 14550 14414 14179 14130 14061 13867 13637 13435 13326 13068 13003 12973 12929 12828 12505'.split()
    #applyPowder(ipts)
    #all_ratios()
    #all_ratios(min_intensity=1.0e5, discard_IPTS=['18915',], outfile='searchBragg_intensity_filtered.dat')

    # IPTS involving water and data not yet in long-term storage
    #ipts = '20354 19386 19355 18634 18019 17806 16529 16525 16427 15382 15173 14414 14179 13506 13376 13326 12929 12716 11846 11844 11816 11650 11097 10999 10952 10774 10764'.split()
    #applyPowder(ipts)
    #all_ratios()
    all_ratios(min_intensity=1.0e5, outfile='searchBragg_intensity_filtered.dat')
