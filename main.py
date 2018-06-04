import recoPreparation, reconstructionAlg, statusAlert, TreeReadFunc, gauss_fit_reco, contour_analyze, IO

from os import chdir, remove, path
from glob import glob
import gc
import numpy as np

'''General script to use sub-scripts for muon reconstruction.'''
statusAlert.processStatus("Process started")

# input_path = "/home/gpu/Simulation/mult/new/"
# input_path = "/home/gpu/Simulation/temp/"
# input_path = "/home/gpu/Simulation/mult/test/"
input_path = "/home/gpu/Simulation/run_scripts/"
# input_path = "/home/gpu/Simulation/test_short/"
# input_path = "/home/gpu/Simulation/single/"

output_path = "/home/gpu/Analysis/muReconstruction/Output/"
# output_path = "/home/gpu/Analysis/muReconstruction/Output/LPMT/"

pickle_path = "/home/gpu/Simulation/processed_sim/lala/"

# input_path = "/home/gpu/Simulation/presentation/y/"
# output_path = "/home/gpu/Analysis/muReconstruction/Output/presentation/y/"

TreeReadFunc.check_file(input_path, "mu", "TrackLengthInScint", "MuMult")
chdir(input_path)
for file in glob("*-photon.root"):

    # TODO start new process for each file. This might solve the memory problem.
    statusAlert.processStatus("Reading file: " + str(file))

    file_split = file.split("-")
    muon_file = file_split[0] + "-user-mu.root"

    '''Control, which events are useful for the analysis'''
    # TreeReadFunc.interestChecker(inputpath, "mu", "TrackLengthInScint", "MuMult", "MuMult")
    # TreeReadFunc.interestChecker(inputpath, "mu", "MuMult"
    # TreeReadFunc.muon_file_reader(file)

    # new_output_path = recoPreparation.create_output_path(output_path, file, "/totalEventHist/",  input_path)
    # new_output_path_fit = recoPreparation.create_output_path(output_path, file, "/fits/",  input_path)
    new_pickle_path = recoPreparation.create_output_path(pickle_path, file, "", input_path)
    '''calculate PMT positions for this file'''
    x_sectors = 20
    y_sectors = 10
    PmtPositions = recoPreparation.calc_pmt_positions(input_path, x_sectors, y_sectors)
    IO.pickle_safe(PmtPositions, new_pickle_path, "PMT_positions")

    '''collect entry and exit points of all muons in event'''
    intersec_radius = 17600
    time_resolution = 1*10**-9
    muon_points = recoPreparation.calc_muon_detector_intersec_points(muon_file, intersec_radius, time_resolution)
    IO.pickle_safe(muon_points, new_pickle_path, "muon_truth")

    '''collect information of all photons within certain time snippet and save the separately'''
    frame_time_cut = 5
    max_frames = 50
    photons_in_time_window, photons_of_entire_event = recoPreparation.hitPMTinTimeSnippetHist2(file,
                                                                                               frame_time_cut,
                                                                                               max_frames)
    IO.pickle_safe(photons_in_time_window, new_pickle_path, "framed_photons")
    IO.pickle_safe(photons_of_entire_event, new_pickle_path, "total_event_photons")

    # TreeReadFunc.muon_file_reader(file)

statusAlert.processStatus("Process finished")