import recoPreparation, reconstructionAlg, statusAlert, TreeReadFunc, gauss_fit_reco, contour_analyze, IO

from os import chdir, remove, path
from glob import glob
import gc
import numpy as np
from os import makedirs

'''General script to use sub-scripts for muon reconstruction.'''
statusAlert.processStatus("Process started")

"""Where is data located"""
folder = "/media/gpu/Data1/Simulation/bundle_mc_output/"
run = "run2"

"""Paths"""
input_path = folder + run + "/"
output_path = "/media/gpu/Data1/Analysis/muReconstruction/Output/test/"
pickle_path = "/media/gpu/Data1/Simulation/processed_sim/runs/"

"""Array for statistics"""
arrival_array = []
pmt_id_array = []

TreeReadFunc.check_file(input_path, "mu", "TrackLengthInScint", "MuMult")
chdir(input_path)
for file in glob("*-photon.root"):
    statusAlert.processStatus("Reading file: " + str(file))
    file_split = file.split("-")
    muon_file = file_split[0] + "-user-muon.root"

    '''Control, which events are useful for the analysis'''
    # TreeReadFunc.interestChecker(inputpath, "mu", "TrackLengthInScint", "MuMult", "MuMult")
    # TreeReadFunc.interestChecker(inputpath, "mu", "MuMult"
    # TreeReadFunc.muon_file_reader(file)

    new_output_path = recoPreparation.create_output_path(output_path, run, file, "/Extra/",  input_path)
    new_output_path_fit = recoPreparation.create_output_path(output_path, run, file, "/fits/",  input_path)
    new_pickle_path = recoPreparation.create_output_path(pickle_path, run, file, "", input_path)
    '''calculate PMT positions for this file'''
    x_sectors = 1
    y_sectors = 1
    # PmtPositions = recoPreparation.calc_pmt_positions(input_path, x_sectors, y_sectors)
    # IO.pickle_safe(PmtPositions, new_pickle_path, "PMT_positions")

    '''collect entry and exit points of all muons in event'''
    intersec_radius = 17700
    time_resolution = 1*10**-9
    muon_points = recoPreparation.calc_muon_detector_intersec_points(muon_file, intersec_radius, time_resolution)
    IO.pickle_safe(muon_points, new_pickle_path, "muon_truth")

    '''collect information of all photons within certain time snippet and save the separately'''
#     frame_time_cut = 5
#     max_frames = 40
#     photons_in_time_window, photons_of_entire_event, = recoPreparation.hitPMTinTimeSnippetHist2(file,
#                                                                                                 frame_time_cut,
#                                                                                                 max_frames)
#     IO.pickle_safe(photons_in_time_window, new_pickle_path, "framed_photons")
#     IO.pickle_safe(photons_of_entire_event, new_pickle_path, "total_event_photons")

    # photon_data = TreeReadFunc.readPhotonRecoData2(file, 3.0)
    # for photon in photon_data:
    #     arrival_array.append(photon.hit_time)
    #     pmt_id_array.append(photon.pmt_id)
    # # IO.pickle_safe(photon_data, new_pickle_path, "photon_data_array")
    # recoPreparation.hit_time_drawer(arrival_array, new_output_path)
    # recoPreparation.hit_pmt_drawer(pmt_id_array, new_output_path)
    # recoPreparation.hit_time_pmt_scatter(arrival_array, pmt_id_array, new_output_path)

    # TreeReadFunc.muon_file_reader(file)

statusAlert.processStatus("Process finished")