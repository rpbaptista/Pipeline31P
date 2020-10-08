fprintf(1,'Executing %s at %s:\n',mfilename(),datestr(now));
ver,
try,
addpath('/i2bm/local/spm12-7487');

        infile = '/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/2020-09-24/imgs/rmeas_MID314_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID7298_filter_hamming2_freq_-300_echo_0.nii';
        outfile = '/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/2020-09-24/imgs/r2meas_MID314_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID7298_filter_hamming2_freq_-300_echo_0.nii'
        transform = load('/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/2020-09-24/results/inverse_anat1H_anat31P0.mat');

        V = spm_vol(infile);
        X = spm_read_vols(V);
        [p n e v] = spm_fileparts(V.fname);
        V.mat = transform.M * V.mat;
        V.fname = fullfile(outfile);
        spm_write_vol(V,X);

        
,catch ME,
fprintf(2,'MATLAB code threw an exception:\n');
fprintf(2,'%s\n',ME.message);
if length(ME.stack) ~= 0, fprintf(2,'File:%s\nName:%s\nLine:%d\n',ME.stack.file,ME.stack.name,ME.stack.line);, end;
end;