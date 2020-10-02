fprintf(1,'Executing %s at %s:\n',mfilename(),datestr(now));
ver,
try,
addpath('/i2bm/local/spm12-7487');

        infile = '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/2020-08-28/fl200200_20200828_001_002_t1_mpr_tra_iso2_0mm.nii';
        outfile = '/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/2020-08-28/fl200200_20200828_001_002_t1_mpr_tra_iso2_0mm.nii'
        transform = load('/neurospin/ciclops/people/Renata/Codes/Pipeline31P/output/inverse_anat1H_anat31P0.mat');

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