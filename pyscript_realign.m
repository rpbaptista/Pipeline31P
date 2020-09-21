fprintf(1,'Executing %s at %s:\n',mfilename(),datestr(now));
ver,
try,
addpath('/i2bm/local/spm12-7487');

        %% Generated by nipype.interfaces.spm
        if isempty(which('spm')),
             throw(MException('SPMCheck:NotFound', 'SPM not in matlab path'));
        end
        [name, version] = spm('ver');
        fprintf('SPM version: %s Release: %s\n',name, version);
        fprintf('SPM path: %s\n', which('spm'));
        spm('Defaults','fMRI');

        if strcmp(name, 'SPM8') || strcmp(name(1:5), 'SPM12'),
           spm_jobman('initcfg');
           spm_get_defaults('cmdline', 1);
        end

        jobs{1}.spm.spatial.realign.estwrite.data = {...
{...
'/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/2020-08-28/measFilter_MID294_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID4938_filter_hamming2_freq_0_echo_0.nii,1';...
'/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/2020-08-28/measFilter_MID296_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID4940_filter_hamming2_freq_0_echo_0.nii,1';...
'/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/2020-08-28/measFilter_MID297_31P_MT_cATP_FA10_PCr_TPI_P3600_RES12_TR250_TE5_FID4941_filter_hamming2_freq_0_echo_0.nii,1';...
'/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/2020-08-28/measFilter_MID295_31P_MT_cATP_FA360_PCr_TPI_P3600_RES12_TR250_TE5_FID4939_filter_hamming2_freq_0_echo_0.nii,1';...
};
};
jobs{1}.spm.spatial.realign.estwrite.eoptions.rtm = 0;
jobs{1}.spm.spatial.realign.estwrite.roptions.which(1) = 2;
jobs{1}.spm.spatial.realign.estwrite.roptions.which(2) = 1;
jobs{1}.spm.spatial.realign.estwrite.roptions.prefix = 'r';

        spm_jobman('run', jobs);

        
,catch ME,
fprintf(2,'MATLAB code threw an exception:\n');
fprintf(2,'%s\n',ME.message);
if length(ME.stack) ~= 0, fprintf(2,'File:%s\nName:%s\nLine:%d\n',ME.stack.file,ME.stack.name,ME.stack.line);, end;
end;