

INITIALIZATION_B1 = dict()

INITIALIZATION_B1['b1_database_phantom'] = {
    #   'sub-00' : ['/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-01-20/meas_MID112_31P_MT_cATP_FA0_PCr_VA12_FID16768_filter_hamming2_freq_0_echo_0.nii',
 #               '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-01-20/meas_MID110_31P_MT_cATP_FA0_PCr_VA24_FID16766_filter_hamming2_freq_0_echo_0.nii',
 #           '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-01-20/meas_MID103_31P_MT_cATP_FA0_PCr_VA36_FID16759_filter_hamming2_freq_0_echo_0.nii',
 #           '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-01-20/meas_MID108_31P_MT_cATP_FA0_PCr_VA48_FID16764_filter_hamming2_freq_0_echo_0.nii'], 


    'FA_nominal' : [12,24,36,48],
    'T1' : 6.7,
    'TR' : 0.250
    }

INITIALIZATION_B1['b1_database'] = {
#  'sub-000' : [
#     '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/CarteB1/2021-01-27/meas_MID468_31P_MT_cATP_FA0_PCr_VA12_FID17680_filter_hamming2_freq_0_echo_0.nii',
#     '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/CarteB1/2021-01-27/meas_MID467_31P_MT_cATP_FA0_PCr_VA24_FID17679_filter_hamming2_freq_0_echo_0.nii',
#     '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/CarteB1/2021-01-27/meas_MID466_31P_MT_cATP_FA0_PCr_VA36_FID17678_filter_hamming2_freq_0_echo_0.nii',
#     '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/CarteB1/2021-01-27/meas_MID465_31P_MT_cATP_FA0_PCr_VA48_FID17677_filter_hamming2_freq_0_echo_0.nii']
# , 
 'sub-01' : [
'/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/CarteB1/2021-01-29/meas_MID656_31P_MT_cATP_FA0_PCr_VA12_FID17926_filter_hamming2_freq_0_echo_0.nii',
'/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/CarteB1/2021-01-29/meas_MID655_31P_MT_cATP_FA0_PCr_VA24_FID17925_filter_hamming2_freq_0_echo_0.nii',
'/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/CarteB1/2021-01-29/meas_MID654_31P_MT_cATP_FA0_PCr_VA36_FID17924_filter_hamming2_freq_0_echo_0.nii',
'/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/CarteB1/2021-01-29/meas_MID653_31P_MT_cATP_FA0_PCr_VA48_FID17923_filter_hamming2_freq_0_echo_0.nii'] 
,
'sub-02' : [
'/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/CarteB1/2021-02-03/meas_MID282_31P_MT_cATP_FA0_PCr_VA12_FID18235_filter_hamming2_freq_0_echo_0.nii',
'/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/CarteB1/2021-02-03/meas_MID281_31P_MT_cATP_FA0_PCr_VA24_FID18234_filter_hamming2_freq_0_echo_0.nii',
'/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/CarteB1/2021-02-03/meas_MID280_31P_MT_cATP_FA0_PCr_VA36_FID18233_filter_hamming2_freq_0_echo_0.nii',
'/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/CarteB1/2021-02-03/meas_MID279_31P_MT_cATP_FA0_PCr_VA48_FID18232_filter_hamming2_freq_0_echo_0.nii'] 
,
    'FA_nominal' : [12,24,36,48],
    'T1' : 3.37,
    'TR' : 0.250,
}

INITIALIZATION_B1['anat'] = {
#    'sub-000' : 'null',
    'sub-01' : '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/CarteB1/2021-01-29/jl190711_20210129_001_002_t1_mpr_tra_iso2_0mm.nii',
    'sub-02' : '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/CarteB1/2021-02-03/pe210039_20210203_001_002_t1_mpr_tra_iso2_0mm.nii',

} 

INITIALIZATION_B1['template'] = {
    'mni' : '/volatile/softwares/FSL/data/standard/MNI152_T1_2mm.nii',
    'mni_brain' : '/volatile/softwares/FSL/data/standard/MNI152_T1_2mm_brain.nii'
    } 

INITIALIZATION_B1['output_dir'] ={
    'sub-01' : '/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/CarteB1/2021-01-29/',
    'sub-02' : '/neurospin/ciclops/people/Renata/RrocessedData/31P_Volunteer/CarteB1/2021-02-03/',

}  