function ODF = get_ODF_from_CTF_file(CTF_file_path, referenceFrameTransformation, specimenSym, phase)
    
    if isempty(referenceFrameTransformation)
        referenceFrameTransformation = {};
    else
        referenceFrameTransformation = {referenceFrameTransformation};
    end

    ebsd = loadEBSD_ctf(CTF_file_path, referenceFrameTransformation{:});
    ori = ebsd(phase).orientations;
    ori.SS = specimenSymmetry(specimenSym);
    ODF = calcDensity(ori);
end
