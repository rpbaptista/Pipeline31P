fprintf(1,'Executing %s at %s:\n',mfilename(),datestr(now));
ver,
try,
addpath('/i2bm/local/spm12-7487');

        target = '/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/2020-08-28/imgs/fsl_rfl200200_20200819_001_012_mprage_sag_T1_160sl_iPAT2.nii';
        moving = '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/2020-08-28/fl200200_20200828_001_002_t1_mpr_tra_iso2_0mm.nii';
        targetv = spm_vol(target);
        movingv = spm_vol(moving);
        x = spm_coreg(targetv, movingv);
        M = spm_matrix(x);
        save('/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/2020-08-28/results/anat1H_anat31P0.mat' , 'M' );
        M = inv(M);
        save('/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/2020-08-28/results/inverse_anat1H_anat31P0.mat','M')
        
,catch ME,
fprintf(2,'MATLAB code threw an exception:\n');
fprintf(2,'%s\n',ME.message);
if length(ME.stack) ~= 0, fprintf(2,'File:%s\nName:%s\nLine:%d\n',ME.stack.file,ME.stack.name,ME.stack.line);, end;
end;