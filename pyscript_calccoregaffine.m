fprintf(1,'Executing %s at %s:\n',mfilename(),datestr(now));
ver,
try,
addpath('/i2bm/local/spm12-7487');

        target = '/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/2020-08-28/measFilter_MID294_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID4938_filter_hamming2_freq_0_echo_0.nii';
        moving = '/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/2020-08-28/measFilter_MID295_31P_MT_cATP_FA360_PCr_TPI_P3600_RES12_TR250_TE5_FID4939_filter_hamming2_freq_0_echo_0.nii';
        targetv = spm_vol(target);
        movingv = spm_vol(moving);
        x = spm_coreg(targetv, movingv);
        M = spm_matrix(x);
        save('/neurospin/ciclops/people/Renata/Codes/Pipeline31P/output/pcr_toall3.mat' , 'M' );
        M = inv(M);
        save('/neurospin/ciclops/people/Renata/Codes/Pipeline31P/output/inverse_pcr_toall3.mat','M')
        
,catch ME,
fprintf(2,'MATLAB code threw an exception:\n');
fprintf(2,'%s\n',ME.message);
if length(ME.stack) ~= 0, fprintf(2,'File:%s\nName:%s\nLine:%d\n',ME.stack.file,ME.stack.name,ME.stack.line);, end;
end;