

INITIALIZATION_B1 = dict()

INITIALIZATION_B1['b1_database_phantom'] = {
#    'sub-000' : ['/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-01-20/meas_MID112_31P_MT_cATP_FA0_PCr_VA12_FID16768_filter_hamming2_freq_0_echo_0.nii',
#             '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-01-20/meas_MID110_31P_MT_cATP_FA0_PCr_VA24_FID16766_filter_hamming2_freq_0_echo_0.nii',
#            '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-01-20/meas_MID103_31P_MT_cATP_FA0_PCr_VA36_FID16759_filter_hamming2_freq_0_echo_0.nii',
#            '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-01-20/meas_MID108_31P_MT_cATP_FA0_PCr_VA48_FID16764_filter_hamming2_freq_0_echo_0.nii'], 
   'sub-001' : ['/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-02-10/rmeas_MID103_31P_MT_cATP_FA0_PCr_VA12_FID19046_filter_hamming2_freq_0_echo_0.nii',
                 '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-02-10/rmeas_MID102_31P_MT_cATP_FA0_PCr_VA24_FID19045_filter_hamming2_freq_0_echo_0.nii',
             '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-02-10/rmeas_MID101_31P_MT_cATP_FA0_PCr_VA36_FID19044_filter_hamming2_freq_0_echo_0.nii',
             '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-02-10/rmeas_MID99_31P_MT_cATP_FA0_PCr_VA48_FID19042_filter_hamming2_freq_0_echo_0.nii'],
  # 'sub-002' : ['/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-02-10/rmeas_MID122_31P_MT_cATP_FA0_PCr_VA12_FID19065_filter_hamming2_freq_0_echo_0.nii',
  #               '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-02-10/rmeas_MID121_31P_MT_cATP_FA0_PCr_VA24_FID19064_filter_hamming2_freq_0_echo_0.nii',
  #           '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-02-10/rmeas_MID120_31P_MT_cATP_FA0_PCr_VA36_FID19063_filter_hamming2_freq_0_echo_0.nii',
  #           '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-02-10/rmeas_MID118_31P_MT_cATP_FA0_PCr_VA48_FID19061_filter_hamming2_freq_0_echo_0.nii'], 
#   'sub-003' : ['/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/2021-02-21/mean_res_12_5mm_deg_12.nii',
#     '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/2021-02-21/mean_res_12_5mm_deg_24.nii',
#     '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/2021-02-21/mean_res_12_5mm_deg_36.nii',
#     '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/2021-02-21/mean_res_12_5mm_deg_48.nii'], 

#   'sub-004' : ['/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/2021-02-21/mean_res_5mm_deg_12.nii',
#                 '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/2021-02-21/mean_res_5mm_deg_24.nii', 
#                 '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/2021-02-21/mean_res_5mm_deg_36.nii',
#                 '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/2021-02-21/mean_res_5mm_deg_48.nii'], 
    
  'sub-005' : ['/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-02-10/reception_profile/meas_MID103_31P_MT_cATP_FA0_PCr_VA12_FID19046_filter_hamming2_freq_0_echo_0_all_channels.nii',
                '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-02-10/reception_profile/meas_MID102_31P_MT_cATP_FA0_PCr_VA24_FID19045_filter_hamming2_freq_0_echo_0_all_channels.nii', 
                '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-02-10/reception_profile/meas_MID101_31P_MT_cATP_FA0_PCr_VA36_FID19044_filter_hamming2_freq_0_echo_0_all_channels.nii',
                '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-02-10/reception_profile/meas_MID99_31P_MT_cATP_FA0_PCr_VA48_FID19042_filter_hamming2_freq_0_echo_0_all_channels.nii'], 
  
 # 'sub-006' : ['/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-02-10/reception_profile/meas_MID122_31P_MT_cATP_FA0_PCr_VA12_FID19065_filter_hamming2_freq_0_echo_0_all_channels.nii',
 #               '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-02-10/reception_profile/meas_MID121_31P_MT_cATP_FA0_PCr_VA24_FID19064_filter_hamming2_freq_0_echo_0_all_channels.nii', 
 #               '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-02-10/reception_profile/meas_MID120_31P_MT_cATP_FA0_PCr_VA36_FID19063_filter_hamming2_freq_0_echo_0_all_channels.nii',
 #               '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-02-10/reception_profile/meas_MID118_31P_MT_cATP_FA0_PCr_VA48_FID19061_filter_hamming2_freq_0_echo_0_all_channels.nii'], 

    'FA_nominal' : [12,24,36,48],
    'T1' : 6.7,
    'TR' : 0.250
    }

INITIALIZATION_B1['b1_database'] = {
#  'sub-000' : [
#     '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-01-27/meas_MID468_31P_MT_cATP_FA0_PCr_VA12_FID17680_filter_hamming2_freq_0_echo_0.nii',
#     '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-01-27/meas_MID467_31P_MT_cATP_FA0_PCr_VA24_FID17679_filter_hamming2_freq_0_echo_0.nii',
#     '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-01-27/meas_MID466_31P_MT_cATP_FA0_PCr_VA36_FID17678_filter_hamming2_freq_0_echo_0.nii',
#     '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-01-27/meas_MID465_31P_MT_cATP_FA0_PCr_VA48_FID17677_filter_hamming2_freq_0_echo_0.nii']
# , 
   'sub-01' : [
  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-01-29/meas_MID656_31P_MT_cATP_FA0_PCr_VA12_FID17926_filter_hamming2_freq_0_echo_0.nii',
  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-01-29/meas_MID655_31P_MT_cATP_FA0_PCr_VA24_FID17925_filter_hamming2_freq_0_echo_0.nii',
  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-01-29/meas_MID654_31P_MT_cATP_FA0_PCr_VA36_FID17924_filter_hamming2_freq_0_echo_0.nii',
  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-01-29/meas_MID653_31P_MT_cATP_FA0_PCr_VA48_FID17923_filter_hamming2_freq_0_echo_0.nii'] 
  ,
  'sub-02' : [
  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-02-03/meas_MID282_31P_MT_cATP_FA0_PCr_VA12_FID18235_filter_hamming2_freq_0_echo_0.nii',
  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-02-03/meas_MID281_31P_MT_cATP_FA0_PCr_VA24_FID18234_filter_hamming2_freq_0_echo_0.nii',
  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-02-03/meas_MID280_31P_MT_cATP_FA0_PCr_VA36_FID18233_filter_hamming2_freq_0_echo_0.nii',
  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-02-03/meas_MID279_31P_MT_cATP_FA0_PCr_VA48_FID18232_filter_hamming2_freq_0_echo_0.nii'] 
  ,
  'sub-03' : [
  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-02-22/meas_MID946_31P_MT_cATP_FA0_PCr_VA12_FID20920_filter_hamming2_freq_0_echo_0.nii',
  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-02-22/meas_MID945_31P_MT_cATP_FA0_PCr_VA24_FID20919_filter_hamming2_freq_0_echo_0.nii',
  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-02-22/meas_MID944_31P_MT_cATP_FA0_PCr_VA36_FID20918_filter_hamming2_freq_0_echo_0.nii',
  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-02-22/meas_MID943_31P_MT_cATP_FA0_PCr_VA48_FID20917_filter_hamming2_freq_0_echo_0.nii'] 
  ,

  'sub-04' : [
  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-03-01/meas_MID46_31P_MT_cATP_FA0_PCr_VA12_FID21674_filter_hamming2_freq_0_echo_0.nii',
  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-03-01/meas_MID45_31P_MT_cATP_FA0_PCr_VA24_FID21673_filter_hamming2_freq_0_echo_0.nii',
  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-03-01/meas_MID44_31P_MT_cATP_FA0_PCr_VA36_FID21672_filter_hamming2_freq_0_echo_0.nii',
  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-03-01/meas_MID43_31P_MT_cATP_FA0_PCr_VA48_FID21671_filter_hamming2_freq_0_echo_0.nii'] 
  ,
 'sub-05' : [
 '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-03-04/meas_MID160_31P_MT_cATP_FA0_PCr_VA12_FID22167_filter_hamming2_freq_0_echo_0.nii',
 '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-03-04/meas_MID159_31P_MT_cATP_FA0_PCr_VA24_FID22166_filter_hamming2_freq_0_echo_0.nii',
 '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-03-04/meas_MID158_31P_MT_cATP_FA0_PCr_VA36_FID22165_filter_hamming2_freq_0_echo_0.nii',
 '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-03-04/meas_MID157_31P_MT_cATP_FA0_PCr_VA48_FID22164_filter_hamming2_freq_0_echo_0.nii'] 
 ,
 'sub-06' : [
 '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-03-10/meas_MID197_31P_MT_cATP_FA0_PCr_VA12_FID23185_filter_hamming2_freq_0_echo_0.nii',
 '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-03-10/meas_MID196_31P_MT_cATP_FA0_PCr_VA24_FID23184_filter_hamming2_freq_0_echo_0.nii',
 '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-03-10/meas_MID195_31P_MT_cATP_FA0_PCr_VA36_FID23183_filter_hamming2_freq_0_echo_0.nii',
 '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-03-10/meas_MID194_31P_MT_cATP_FA0_PCr_VA48_FID23182_filter_hamming2_freq_0_echo_0.nii'] 
 ,


     'FA_nominal' : [12,24,36,48],
    'T1' : 3.37,
    'TR' : 0.250,
}

INITIALIZATION_B1['anat'] = {
#    'sub-000' : 'null',
    'sub-01' : '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-01-29/jl190711_20210129_001_002_t1_mpr_tra_iso2_0mm.nii',
    'sub-02' : '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-02-03/pe210039_20210203_001_002_t1_mpr_tra_iso2_0mm.nii',
    'sub-03' : '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-02-22/ep190340_20210222_001_002_t1_mpr_tra_iso2_0mm.nii',
    'sub-04' : '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-03-01/sl130503_20210301_001_002_t1_mpr_tra_iso2_0mm.nii',
    'sub-05' : '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-03-04/ev070110_20210304_001_004_t1_mpr_tra_iso2_0mm.nii',
    'sub-06' : '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/B1Map/2021-03-10/eb180237_20210310_001_004_t1_mpr_tra_iso2_0mm.nii'
} 
INITIALIZATION_B1['mask'] = {
    'sub-000' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/mask_opened_3_20.tif',
    'sub-001' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/mask_opened_3_20.tif',
    'sub-002' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/mask_opened_3_20.tif',
    'sub-003' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/2021-02-21/mask_res_12_5mm.tif',
    'sub-004' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/2021-02-21/mask_res_5mm.tif',
    'sub-005' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/mask_opened_3_20.tif',

    'sub-01' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Volunteer/2021-01-29/mask_treated.nii',
    'sub-02' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Volunteer/2021-02-03/mask_treated.nii',
    'sub-03' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Volunteer/2021-02-22/mask_treated.nii',
    'sub-04' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Volunteer/2021-03-01/mask_treated.nii',
    'sub-05' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Volunteer/2021-03-04/mask_treated.nii',
    'sub-06' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Volunteer/2021-03-10/mask_treated.nii',

} 

INITIALIZATION_B1['template'] = {
    'mni' : '/volatile/softwares/FSL/data/standard/MNI152_T1_2mm.nii',
    'mni_brain' : '/volatile/softwares/FSL/data/standard/MNI152_T1_2mm_brain.nii',
    'mni_mask' : '/neurospin/ciclops/people/Renata/ProcessedData/Atlases/MNI152_T1_2mm_brain-mask.nii'} 

INITIALIZATION_B1['output_dir'] ={
    'sub-000' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/2021-02-10/phantom_0',
    'sub-001' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/2021-02-10/phantom_1',
    'sub-002' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/2021-02-10/phantom_2',
    'sub-003' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/2021-02-21/res12',
    'sub-004' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/2021-02-21/res5',
    'sub-005' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/2021-02-10/phantom_0_all_chan',
    'volunteer' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Volunteer/',
    'sub-01' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Volunteer/2021-01-29/',
    'sub-02' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Volunteer/2021-02-03/',
    'sub-03' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Volunteer/2021-02-22/',
    'sub-04' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Volunteer/2021-03-01/',
    'sub-05' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Volunteer/2021-03-04/',
    'sub-06' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Volunteer/2021-03-10/',

}  
INITIALIZATION_B1['par_postproce'] ={
    'deg_poly': 8,
    'patch_size': 5,
    'patch_distance' : 6,
    'DENOISE' : False,
    'os_factor' : 2,
}  