function ODF = get_ODF_from_CRC_file(CRC_file_path, referenceFrameTransformation, specimenSym, phase)
    
    if isempty(referenceFrameTransformation)
        referenceFrameTransformation = {};
    else
        referenceFrameTransformation = {referenceFrameTransformation};
    end
    
    ebsd = loadEBSD_crc(CRC_file_path, referenceFrameTransformation{:});
    ori = ebsd(phase).orientations;
    ori.SS = specimenSymmetry(specimenSym);
    ODF = calcDensity(ori);
end
